import os.path
import json
from time import time
from elasticsearch import Elasticsearch
from flask import Flask, render_template, request
from usr_profile_lib.usr_profile_log import UserProfileLogger
from algorithm import cosine_similarity as cos_sim
from algorithm import aggregate_term_vecs
from algorithm import filter_term_vec
from fetcher import fetch_term_vecs
from fetcher import fetch_query_term_vec
from config import Config

# the folder containing this script
script_dir = os.path.dirname(__file__)
app = Flask(__name__)
# ===========================================================
# check the path of the user profile db
default_db_file = "/var/www/frontend/user_profile.db"
if os.path.exists(default_db_file):
    UserProfileLogger.USER_PROFILE_DB = default_db_file
else:
    db_file = os.path.join(script_dir, "../usr_profile_db/user_profile.db")
    print("[DEV MODE] Using the profile db: ", db_file)
    UserProfileLogger.USER_PROFILE_DB = db_file
# ===========================================================
es = Elasticsearch(Config.elastic_host, port="9200", timeout = 100)

# DOC_TYPE = 'page'

# A test user that likes Adolf Hitler, Albert Speer and Java programming.
# TEST_USER = {
#     'hitler' : 10,
#     'albert' : 5,
#     'speer' : 3,
#     'java' : 2,
#     'programming' : 2
# }

# def score_doc(doc_vec, u, q):
#     '''For ease of typing:
#         u: user vector
#         q: query vector
#         ti: document title vector
#         tx: document text vector
#         ct: document category vector
#         s_X_Y: similarity between X and Y
#     '''
#     id, ti, tx, ct = doc_vec
#     s_u_ti = cos_sim(u, ti)
#     s_u_tx = cos_sim(u, tx)
#     s_u_ct = cos_sim(u, ct)
#     s_q_ti = cos_sim(q, ti)
#     s_q_tx = cos_sim(q, tx)
#     s_q_ct = cos_sim(q, ct)

#     # Weigh the scores together
#     score = 0.3 * (0.5 * s_u_ti + 0.2 * s_u_tx + 0.3 * s_u_ct) \
#         + 0.7 * (0.5 * s_q_ti + 0.2 * s_q_tx + 0.3 * s_q_ct)

#     fmt = '%-40s %.2f %.2f %.2f %.2f %.2f %.2f | %.3f'
#     title_str = ' '.join(ti.keys())
#     pretty_text = fmt % (title_str,
#                          s_u_ti, s_u_tx, s_u_ct,
#                          s_q_ti, s_q_tx, s_q_ct, score)
#     return score, id, pretty_text

# def score_docs(doc_vecs, u, q):
#     scores = [score_doc(d, u, q) for d in doc_vecs]
#     for score, id, pretty_text in sorted(scores):
#         print(pretty_text)

# def get_doc_vecs(doc):
#     '''Get the document vectors for the document.'''
#     id = doc['_id']
#     vecs = doc['term_vectors']

#     # Make a tf vector of the title field
#     terms = vecs['title']['terms']
#     title_vec = {w : d['term_freq'] for w, d in terms.items()}

#     # Same for the text
#     terms = vecs['text']['terms']
#     text_vec = {w : d['term_freq'] for w, d in terms.items()}

#     # And for categories
#     terms = vecs['category']['terms']
#     cat_vec = {w : d['term_freq'] for w, d in terms.items()}
#     return id, title_vec, text_vec, cat_vec

# def fetch_docs_vecs(es, el_res):
#     '''Fetches the documents' vectors for the result set.'''
#     ids = [pe["_id"] for pe in el_res["hits"]["hits"]]
#     body = {
#         'ids' : ids,
#         'parameters' : {
#             'term_statistics' : True
#         }
#     }
#     res = es.mtermvectors(index=INDEX, doc_type=DOC_TYPE,
#                           body=body)
#     return [get_doc_vecs(d) for d in res['docs']]

# def fetch_query_vec(es, query):
#     """
#     Fetches a term frequency vector from the query.

#     Args:

#     Returns:

#     """
#     res = es.termvectors(index=INDEX, doc_type=DOC_TYPE,
#                          body={'doc' : {'text' : query}})
#     vecs = res['term_vectors']
#     terms = vecs['text']['terms']
#     query_vec = {w : d['term_freq'] for w, d in terms.items()}
#     return query_vec
# ==============================================================================
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/log/click", methods=["POST"])
def log():
    data = request.get_json()
    # log the retrieved record into db
    email = data['email']
    retrieved_doc_id = data['doc_id']
    with UserProfileLogger(email) as profile_logger:
        profile_logger.log_retrieved(doc_id=retrieved_doc_id, index=Config.index)

    # ==========================================================================
    # fetch the term vector
    term_vectors = fetch_term_vecs(
        es, retrieved_doc_id, Config.index, doc_type=Config.doc_type)
    # save them to db
    with UserProfileLogger(email) as profile_logger:
        # since we only fetch one doc
        for k in term_vectors.keys():
            vec = term_vectors[k]
            # filter the term vector
            vec = filter_term_vec(vec)
            profile_logger.log_term_vec_to_profile(vec, field=k)
    # ==========================================================================
    return "Ok"

@app.route("/search", methods=["POST"])
def search():
    # Extracting information of post body
    data = request.get_json()
    query = data["query"]
    results_size = data["results_size"]
    results_from = data["results_from"]
    email = data["email"]

    # get the query as term vector
    query_term_vec = fetch_query_term_vec(es, query, Config.index)

    # log the user query
    with UserProfileLogger(email) as profile_logger:
        profile_logger.log_search(
            query=query, query_type="Unknown", ranking_type=None)
        profile_logger.log_term_vec_to_profile(query_term_vec, field="query")

    query_body = {
        "query": {
            "multi_match" : {
                "query" : query,
                "fields" : [ "title", "text"]
            }
        },
        "from": results_from,
        "size": results_size
    }

    # search with the query body
    el_res = es.search(index=Config.index, body=query_body)

    res = {"results": []}
    res["n_results"] = el_res["hits"]["total"]
    for pe in el_res["hits"]["hits"]:
        obj = {}
        obj["id"] = pe["_id"]
        obj["string"] = pe["_source"]["title"]
        obj["url"] = Config.wiki_url_fmt.format(title=pe["_source"]["title"])
        obj["synopsys"] = pe["_source"]["text"][:400]
        res["results"].append(obj)

    return json.dumps(res)


if __name__ == "__main__":
    app.run(host="0.0.0.0")
