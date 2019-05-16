import os.path
import json
from time import time
from collections import OrderedDict
from elasticsearch import Elasticsearch
from flask import Flask, render_template, request, jsonify
from usr_profile_lib.usr_profile_log import UserProfileLogger
from algorithm import cosine_similarity as cos_sim
from algorithm import aggregate_term_vecs
from algorithm import filter_term_vec
from algorithm import calcuate_term_vec_now
from algorithm import get_sorted_term_vec
from algorithm import get_sorted_dict
from algorithm import normalize_term_vec
from algorithm import weight_mean_term_vecs
from fetcher import fetch_term_vecs
from fetcher import fetch_query_term_vec
from fetcher import fetch_mulitple_term_vecs
from config import Config

# the folder containing this script
from word_cloud import plot_usr_word_cloud_bytes

script_dir = os.path.dirname(__file__)

es = Elasticsearch(Config.elastic_host, port=Config.elastic_port, timeout=Config.timeout)
#es = Elasticsearch("localhost:9200", port="9200", timeout = 100)

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
            # normalize the term vector
            vec = normalize_term_vec(vec)
            # log it to the database
            profile_logger.log_term_vec_to_profile(vec, field=k)
    # ==========================================================================
    return "Ok"

@app.route("/search", methods=["POST"])
def search():
    time_start = time()
    # Extracting information of post body
    data = request.get_json()
    query = data["query"]
    results_size = data["results_size"]
    results_from = data["results_from"]
    email = data["email"]

    if not query:
        return json.dumps({
            "status": "failed",
            "reason": "Empty query",
            "n_results": 0,
            'results': [],
        })

   # log the user query
    with UserProfileLogger(email) as profile_logger:
        profile_logger.log_search(
            query=query, query_type="Unknown", ranking_type=None)

    query_body = {
        "query": {
            "bool": {
                # "must": {
                # },
                "should": [
                    {
                        "match": {
                            "title": {
                                "query": query,
                                "boost": Config.boost['title'],
                            }
                        }
                    },
                    {
                        "match": {
                            "text": {
                                "query": query,
                                "boost": Config.boost['text'],
                            }
                        }
                    },
                ]
            }
        },
        "from": results_from,
        "size": results_size
    }
    # ======================================================
    # query expansion
    # get the query term vector
    query_term_vec = fetch_query_term_vec(es, query, Config.index)

    # calculate the dynamic profile vector
    term_vecs_t = dict()
    with UserProfileLogger(email) as profile_logger:
        for f in Config.weights.keys():
            vec_t = profile_logger.get_user_dynamic_profile_vec(field=f)
            term_vecs_t[f] = vec_t

    # calculate term vector now
    term_vecs_now = dict()
    for f in term_vecs_t.keys():
        tvec_now = calcuate_term_vec_now(
            term_vecs_t[f], half_life=Config.half_life[f])
        # normalization
        tvec_now = normalize_term_vec(tvec_now)
        # save it
        term_vecs_now[f] = tvec_now

    # weighted average
    term_vec = aggregate_term_vecs(term_vecs_now, Config.weights)
    # removing unwanted terms
    term_vec = filter_term_vec(term_vec)

    dyn_profile_vec = get_sorted_term_vec(term_vec, limit=Config.expansion_size)
    dyn_profile_vec = normalize_term_vec(dyn_profile_vec)
    # End calculate the dynamic profiling

    # calculate the static profile
    with UserProfileLogger(email) as profile_logger:
        st_profile_vec = profile_logger.get_user_static_profile_vec()

    st_profile_vec = normalize_term_vec(st_profile_vec)
    profile_vec = weight_mean_term_vecs(
        st_profile_vec, dyn_profile_vec,
        Config.profile_weights["static"], Config.profile_weights["dynamic"])

    # remove the impact if the query already in the epansion
    expansion = dict()
    for k in profile_vec:
        if k not in query_term_vec:
           expansion[k] = profile_vec[k]

    # normalize the expansion again
    expansion = normalize_term_vec(expansion)
    for field in ["text"]:
        for k, v in expansion.items():  # the expansion is still a term vector
            term_boost_dict = {
                "term":{
                    field: {
                        "value": k,
                        "boost": v*Config.feedback_weight*Config.boost[field],
                    }
                }
            }
            query_body["query"]["bool"]["should"].append(term_boost_dict)
    # ======================================================
    # search with the query body
    el_res = es.search(index=Config.index, body=query_body)

    # log the query to profile if success
    if el_res["hits"]["total"] > 0:
        with UserProfileLogger(email) as profile_logger:
            profile_logger.log_term_vec_to_profile(query_term_vec, field="query")
    # ==========================================================================
    # Perpare the well formated results
    docid_to_score = OrderedDict()  #  doc_id -> score
    docid_to_desc = dict()  # doc_id -> simple description of doc
    for s_rslt in el_res["hits"]["hits"]:
        id_ = s_rslt["_id"]
        match_score = s_rslt["_score"]
        docid_to_score[id_] = match_score
        docid_to_desc[id_] = {
            "synopsys": s_rslt["_source"]["text"][:400],
            "title": s_rslt["_source"]["title"]
        }
    # ==========================================================================
    # Reordering
    # get the similarity score of the docs and our profile
    if Config.is_reorder_search_results and len(profile_vec) > 0:
        # fetch doc term vectors
        docs_term_vecs = fetch_mulitple_term_vecs(
            es, list(docid_to_score.keys()), Config.index, fields=["text", "category", "text"])

        # for each document, aggregate one document term vector and calcuate
        # the similary score and the adjusted score
        adj_scores = dict()
        for doc_id in docs_term_vecs:
            doc_tvec = aggregate_term_vecs(docs_term_vecs[doc_id], Config.weights)
            profile_dot_doc_tvec = cos_sim(doc_tvec, profile_vec)
            adj_scores[doc_id] = (
                Config.rerank_alpha*docid_to_score[doc_id]
            + (1-Config.rerank_alpha)*profile_dot_doc_tvec)

        docid_to_adjscore = get_sorted_dict(adj_scores)
    else:
        # no sorting
        docid_to_adjscore = docid_to_score

    # =========================================================================
    # build up the response
    res = {
        "results": [],
        "n_results": el_res["hits"]["total"]
    }
    for i, docid in enumerate(docid_to_adjscore.keys()):
        result = {
            "id": docid,
            "pos": i + results_from + 1,
            "score": docid_to_score[docid],
            "modified_score": docid_to_adjscore[docid],
            "string": docid_to_desc[docid]["title"],
            "synopsys": docid_to_desc[docid]["synopsys"],
            "url": Config.wiki_url_fmt.format(title=docid_to_desc[docid]["title"]),
        }
        res["results"].append(result)

    time_end = time() - time_start
    print("Search used: ", time_end)
    return json.dumps(res)


@app.route("/user_profile", methods=["GET", "POST"])
def user_profile():
    email = request.args['email']
    if request.method == 'GET':
        if len(email) == 0:
            return jsonify({
                "email": "",
                "age": 0,
                "city": "",
                "country": "",
                "lang": "",
                "gender": ""
            })
        UserProfileLogger.create_user_if_not_exists(email)
        with UserProfileLogger(email) as profile_logger:
            profile = profile_logger.get_user_profile()
            return jsonify(profile)
    elif request.method == 'POST':
        if len(email) == 0:
            return "Ok"
        data = request.get_json()
        with UserProfileLogger(email) as profile_logger:
            profile_logger.modify_user_profile(data)
        return "Ok"


@app.route("/static_profile", methods=["GET", "POST"])
def static_profile():
    email = request.args['email']
    if request.method == 'GET':
        UserProfileLogger.create_user_if_not_exists(email)
        with UserProfileLogger(email) as profile_logger:
            st_profile_vec = profile_logger.get_user_key_terms()
            return jsonify(st_profile_vec)
    elif request.method == 'POST':
        data = request.get_json()
        terms = data['terms']
        vec = {a: b for (a, b) in zip(terms, [1.0]*len(terms))}
        with UserProfileLogger(email) as profile_logger:
            profile_logger.modify_user_static_profile_vec(vec)
        return "Ok"

@app.route("/wordcloud/<email>")
def generate_wordcloud(email):
    return plot_usr_word_cloud_bytes(email)



if __name__ == "__main__":
    app.run(host="0.0.0.0")
