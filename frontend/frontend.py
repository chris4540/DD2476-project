from flask import Flask, render_template
from elasticsearch import Elasticsearch
from datetime import datetime
import json
from usr_profile_lib.usr_profile_log import UserProfileLogger

app = Flask(__name__)
UserProfileLogger.USER_PROFILE_DB = "/var/usr_prf/user_profile.db"

es = Elasticsearch("elastic.haochen.lu", port="9200")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/log/click/<element_id>")
def log(element_id):
    # log into db
    timestamp = datetime.now()

@app.route("/search/<email>/<query>/<results_size>_<results_from>")
def search(email, query, results_size, results_from):

    # log the user query
    with UserProfileLogger(email) as profile_logger:
        profile_logger.log_search(
            query=query, query_type="Unknown", ranking_type=None)

    q = {
        "query": {
            "match": {
                "title": query
            }
        },
        "from": results_from,
        "size": results_size
    }
    el_res = es.search(body=q)
    res = {"results": []}
    res["n_results"] = el_res["hits"]["total"]
    for pe in el_res["hits"]["hits"]:
        obj = {}
        obj["id"] = pe["_id"]
        obj["string"] = pe["_source"]["title"]
        obj["url"] = "http://en.wikipedia.org/wiki/" + pe["_source"]["title"]
        res["results"].append(obj)

    return json.dumps(res)


if __name__ == "__main__":
    app.run(host="0.0.0.0")
