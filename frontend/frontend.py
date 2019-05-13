import os.path
import json
from time import time
from elasticsearch import Elasticsearch
from flask import Flask, render_template, request
from usr_profile_lib.usr_profile_log import UserProfileLogger
from algorithm import cosine_similarity as cos_sim
from algorithm import aggregate_term_vecs
from algorithm import filter_term_vec
from algorithm import calcuate_term_vec_now
from algorithm import get_sorted_term_vec
from algorithm import normalize_term_vec
from algorithm import weight_mean_term_vecs
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
    # time_start = time()
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
                "must": {
                    "match": {
                        "title": {
                            "query": query,
                            "boost": Config.boost['title'],
                        }
                    }
                },
                "should": [
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
    # TODO: add switch to off query expansion
    # TODO: add using static profile

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
        term_vecs_now[f] = tvec_now
    term_vec = aggregate_term_vecs(term_vecs_now, Config.weights)
    term_vec = filter_term_vec(term_vec)
    dyn_profile_vec = get_sorted_term_vec(term_vec, limit=Config.expansion_size)
    dyn_profile_vec = normalize_term_vec(dyn_profile_vec)
    # End calculate the dynamic profiling

    # calculate the static profile
    with UserProfileLogger(email) as profile_logger:
        st_profile_vec = profile_logger.get_user_static_profile_vec()

    st_profile_vec = normalize_term_vec(st_profile_vec)
    expansion = weight_mean_term_vecs(
        st_profile_vec, dyn_profile_vec,
        Config.profile_weights["static"], Config.profile_weights["dynamic"])
    # normalize the expansion again
    expansion = normalize_term_vec(expansion)
    # TODO: consider expand title field
    for k, v in expansion.items():  # the expansion is still a term vector
        term_boost_dict = {
            "term":{
                "text": {
                    "value": k,
                    "boost": v*Config.feedback_weight,
                }
            }
        }
        query_body["query"]["bool"]["should"].append(term_boost_dict)
    # ======================================================
    # search with the query body
    el_res = es.search(index=Config.index, body=query_body)

    # log the query to profile if success
    if el_res["hits"]["total"] > 0:
         # get the query as term vector
        query_term_vec = fetch_query_term_vec(es, query, Config.index)
        with UserProfileLogger(email) as profile_logger:
            profile_logger.log_term_vec_to_profile(query_term_vec, field="query")

    # build up the response
    res = {"results": []}
    res["n_results"] = el_res["hits"]["total"]
    for pe in el_res["hits"]["hits"]:
        obj = {}
        obj["id"] = pe["_id"]
        obj["string"] = pe["_source"]["title"]
        obj["url"] = Config.wiki_url_fmt.format(title=pe["_source"]["title"])
        obj["synopsys"] = pe["_source"]["text"][:400]
        res["results"].append(obj)
    # time_end = time() - time_start
    # print("Search used: ", time_end)
    return json.dumps(res)


if __name__ == "__main__":
    app.run(host="0.0.0.0")
