from flask import Flask, render_template
from elasticsearch import Elasticsearch
import json
app = Flask(__name__)

es = Elasticsearch("elastic.haochen.lu", port="9200")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/search/<query>")
def search(query):
    el_res = es.search(body={"query": {"match": {"title": query}}})
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
    app.run()
