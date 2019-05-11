"""
File to place all routines closely related to elasticsearch and its response
json structure.
"""
import numpy as np
from elasticsearch import Elasticsearch
from algorithm import get_tfidf_weight

def term_vector_to_weight(term_vecs, weight_scheme):
    """
    Tranlate a term vector with the information like tf and idf to a weight
    Args:
        term_vecs: a dictionary with terms as keys
        E.g.
            {
                'field_statistics': {
                    'sum_doc_freq': 3217420,
                    'doc_count': 1169019,
                    'sum_ttf': 3228465
                },
                'terms': {
                    'actor': {
                        'doc_freq': 45598,
                        'ttf': 110098,
                        'term_freq': 1
                    },
                    ...
                }
            }
    Return:
        E.g.
        {
            "actor": 123.11,
            "kth": 12.34,
            ...
        }
    """
    if weight_scheme == "tf":
        weight_fun = lambda term_vec: term_vec['term_freq']
    elif weight_scheme == "tfidf":
        doc_count = term_vecs['field_statistics']['doc_count']
        weight_fun = lambda term_vec: get_tfidf_weight(term_vec, doc_count)
    else:
        raise ValueError("Unknown weighting scheme")

    # loop over terms
    ret = dict()
    for t in term_vecs['terms']:
        ret[t] = weight_fun(term_vecs['terms'][t])
    return ret

def fetch_term_vecs(es, ids, index, doc_type="page", weight_scheme="tfidf"):
    """
    Fetch term vectors for multiple documents

    Args:
        es (elastic search instance): the connector of the elastic search
        ids (list): list of document indices
        index (str): the name of the index in the engine, e.g. "enwiki" or "svwiki"
        doc_type (Optional [str]): the type of the docuement
    Return:
        a dictionary return:
        {
            "ids": <list of ids>,
            "title": <list of term vectors for title field only>,
            "text": <list of term vectors for text field only>,
            "category": <list of term vectors for category field only>
        }
    """
    request_body = {
        'ids' : ids,
        'parameters' : {
            'term_statistics' : True
        }
    }
    resp = es.mtermvectors(index=index, doc_type=doc_type,body=request_body)

    # build up the return
    ret = dict()
    for k in ["ids", "title", "text", "category"]:
        ret[k] = list()

    for d in resp['docs']:
        if "term_vectors" in d:
            ret['ids'].append(d['_id'])
            for k in ["title", "text", "category"]:
                ret[k].append(
                    term_vector_to_weight(d["term_vectors"][k], weight_scheme)
                )
    return ret

if __name__ == "__main__":
    es = Elasticsearch("elastic.haochen.lu", port="9200", timeout=1000)
    term_vecs = fetch_term_vecs(es, ["25609", "15545269"], "enwiki")
