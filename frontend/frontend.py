from flask import Flask, render_template, request
from elasticsearch import Elasticsearch
from datetime import datetime
import json
from usr_profile_lib.usr_profile_log import UserProfileLogger

app = Flask(__name__)
UserProfileLogger.USER_PROFILE_DB = "/var/usr_prf/user_profile.db"

es = Elasticsearch("elastic.haochen.lu", port="9200")
#es = Elasticsearch("localhost:9200", port="9200")

INDEX = 'data'
DOC_TYPE = 'page'

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
    return id, title_vec, text_vec

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
    return [get_doc_vectors(d) for d in res['docs']]

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
    #print(fetch_docs_vecs(es, el_res))
    #print(fetch_query_vec(es, query))

    res = {"results": []}
    res["n_results"] = el_res["hits"]["total"]
    for pe in el_res["hits"]["hits"]:
        obj = {}
        obj["id"] = pe["_id"]
        obj["string"] = pe["_source"]["title"]
        obj["url"] = "http://en.wikipedia.org/wiki/" + pe["_source"]["title"]
        obj["synopsys"] = pe["_source"]["text"][:400]
        res["results"].append(obj)

    return json.dumps(res)


if __name__ == "__main__":
    app.run(host="0.0.0.0")
