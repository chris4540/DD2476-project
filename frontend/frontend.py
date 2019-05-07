from datetime import datetime
from elasticsearch import Elasticsearch
from flask import Flask, render_template, request
from math import sqrt
from time import time
import json
from usr_profile_lib.usr_profile_log import UserProfileLogger

app = Flask(__name__)
UserProfileLogger.USER_PROFILE_DB = "/var/usr_prf/user_profile.db"

es = Elasticsearch("elastic.haochen.lu", port="9200", timeout = 100)
#es = Elasticsearch("localhost:9200", port="9200", timeout = 100)

INDEX = 'enwiki'
DOC_TYPE = 'page'

# A test user that likes Adolf Hitler, Albert Speer and Java
# programming.
TEST_USER = {
    'hitler' : 10,
    'albert' : 5, 'speer' : 3,
    'java' : 2, 'programming' : 2
}

def cos_sim(v1, v2):
    '''Computes the cosine similarity between two vectors stored as Python
    dictionaries.'''

    # Euclidean norm
    l1 = sqrt(sum(e*e for e in v1.values()))
    l2 = sqrt(sum(e*e for e in v2.values()))

    # Normalize vectors
    v1 = {w : e / l1 for w, e in v1.items()}
    v2 = {w : e / l2 for w, e in v2.items()}
    parts = [v1.get(w, 0)*v2.get(w, 0) for w in v1]
    return sum(parts)

def score_doc(doc_vec, u, q):
    '''For ease of typing:
        u: user vector
        q: query vector
        ti: document title vector
        tx: document text vector
        ct: document category vector
        s_X_Y: similarity between X and Y
    '''
    id, ti, tx, ct = doc_vec
    s_u_ti = cos_sim(u, ti)
    s_u_tx = cos_sim(u, tx)
    s_u_ct = cos_sim(u, ct)
    s_q_ti = cos_sim(q, ti)
    s_q_tx = cos_sim(q, tx)
    s_q_ct = cos_sim(q, ct)

    # Weigh the scores together
    score = 0.3 * (0.5 * s_u_ti + 0.2 * s_u_tx + 0.3 * s_u_ct) \
        + 0.7 * (0.5 * s_q_ti + 0.2 * s_q_tx + 0.3 * s_q_ct)

    fmt = '%-40s %.2f %.2f %.2f %.2f %.2f %.2f | %.3f'
    title_str = ' '.join(ti.keys())
    pretty_text = fmt % (title_str,
                         s_u_ti, s_u_tx, s_u_ct,
                         s_q_ti, s_q_tx, s_q_ct, score)
    return score, id, pretty_text

def score_docs(doc_vecs, u, q):
    scores = [score_doc(d, u, q) for d in doc_vecs]
    for score, id, pretty_text in sorted(scores):
        print(pretty_text)

def get_doc_vecs(doc):
    '''Get the document vectors for the document.'''
    id = doc['_id']
    vecs = doc['term_vectors']

    # Make a tf vector of the title field
    terms = vecs['title']['terms']
    title_vec = {w : d['term_freq'] for w, d in terms.items()}

    # Same for the text
    terms = vecs['text']['terms']
    text_vec = {w : d['term_freq'] for w, d in terms.items()}

    # And for categories
    terms = vecs['category']['terms']
    cat_vec = {w : d['term_freq'] for w, d in terms.items()}
    return id, title_vec, text_vec, cat_vec

def fetch_docs_vecs(es, el_res):
    '''Fetches the documents' vectors for the result set.'''
    ids = [pe["_id"] for pe in el_res["hits"]["hits"]]
    body = {
        'ids' : ids,
        'parameters' : {
            'term_statistics' : True
        }
    }
    res = es.mtermvectors(index = INDEX, doc_type = DOC_TYPE,
                          body = body)
    return [get_doc_vecs(d) for d in res['docs']]

def fetch_query_vec(es, query):
    '''Fetches a term frequency vector from the query.'''
    res = es.termvectors(index = INDEX, doc_type = DOC_TYPE,
                         body = {'doc' : {'text' : query}})
    vecs = res['term_vectors']
    terms = vecs['text']['terms']
    query_vec = {w : d['term_freq'] for w, d in terms.items()}
    return query_vec

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/log/click", methods=["POST"])
def log():
    data = request.get_json()
    # log into db
    timestamp = datetime.now()
    return "Ok"

@app.route("/search", methods=["POST"])
def search():
    data = request.get_json()
    query = data["query"]
    results_size = data["results_size"]
    results_from = data["results_from"]
    email = data["email"]

    # log the user query
    with UserProfileLogger(email) as profile_logger:
        profile_logger.log_search(
            query=query, query_type="Unknown", ranking_type=None)

    q = {
        "query": {
            "multi_match" : {
                "query" : query,
                "fields" : [ "title", "text"]
            }
        },
        "from": results_from,
        "size": results_size
    }

    el_res = es.search(body=q)

    # Proof of concept code for fetching tf vectors:
    print('Fetching query vectors...')
    t0 = time()
    query_vec = fetch_query_vec(es, query)
    doc_vecs = fetch_docs_vecs(es, el_res)
    print('... took %.2f seconds.' % (time() - t0))
    score_docs(doc_vecs, TEST_USER, query_vec)

    res = {"results": []}
    res["n_results"] = el_res["hits"]["total"]
    for pe in el_res["hits"]["hits"]:
        obj = {}
        obj["id"] = pe["_id"]
        obj["string"] = pe["_source"]["title"]
        obj["url"] = "http://en.wikipedia.org/wiki/" \
            + pe["_source"]["title"]
        obj["synopsys"] = pe["_source"]["text"][:400]
        res["results"].append(obj)

    return json.dumps(res)


if __name__ == "__main__":
    app.run(host="0.0.0.0")
