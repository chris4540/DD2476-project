"""
File to place all routines closely related to elasticsearch and its response
json structure.
"""
import numpy as np
from elasticsearch import Elasticsearch
from algorithm import get_tfidf_weight
from config import Config
from time import time

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
        # this is the doc count per shard
        doc_count = term_vecs['field_statistics']['doc_count']
        weight_fun = lambda term_vec: get_tfidf_weight(term_vec, doc_count)
    else:
        raise ValueError("Unknown weighting scheme")

    # loop over terms
    ret = dict()
    for t in term_vecs['terms']:
        ret[t] = weight_fun(term_vecs['terms'][t])
    return ret

def fetch_term_vecs(es, doc_id, index, doc_type="page"):
    """
    Fetch term vectors for one documents

    Args:
        es (elastic search instance): the connector of the elastic search
        id (str): the document index
        index (str): the name of the index in the engine, e.g. "enwiki" or "svwiki"
        doc_type (Optional [str]): the type of the docuement
    Return:
        a dictionary return:
        {
            "title": <term vectors for title field only>,
            "text": <term vectors for text field only>,
            "category": <term vectors for category field only>
        }
    """
    resp = es.termvectors(index=index, id=doc_id, doc_type=doc_type, term_statistics=True)

    # build up the return
    ret = dict()

    if "term_vectors" in resp:
        for k in ["title", "text", "category"]:
            ret[k] = term_vector_to_weight(resp["term_vectors"][k], Config.weight_scheme)
    return ret

def fetch_mulitple_term_vecs(es, ids, index, fields, doc_type="page"):
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
            <id1>:{
                "title": term_vec_for_title,
                "text": term_vec_for_text,
                "category": term_vec_for_cat,
            },
            <id2>:{
                ...
            }
        }
    """
    body = {
        "ids": ids,
        "parameters": {
            "fields" : fields,
            "offsets" : False,
            "payloads" : False,
            "positions" : False,
            "term_statistics" : True,
            "field_statistics" : True,
        }
    }
    ts = time()
    resp = es.mtermvectors(index=index, doc_type=doc_type, body=body)
    print("[Reordering] Time for fetch documents term vecs = ", time() - ts)
    # build up the return
    ret = dict()

    for d in resp['docs']:
        if "term_vectors" in d:
            doc_id = d['_id']
            ret[doc_id] = dict()
            for k in fields:
                term_vec = term_vector_to_weight(d["term_vectors"][k], Config.weight_scheme)
                ret[doc_id][k] = term_vec
    return ret

def fetch_query_term_vec(es, query, index, doc_type="page"):
    """
    TODO: documentation
    """
    field = "title"
    body = {
        "fields" : [field],
        "doc": {
            field: query
        },
        "positions": False,
        "offsets" : False,
        "payloads" : False,
        "term_statistics" : True
    }
    resp = es.termvectors(index=index, doc_type=doc_type, body=body)

    if 'term_vectors' in resp:
        ret = term_vector_to_weight(resp['term_vectors'][field], Config.weight_scheme)
    else:
        ret = dict()
    return ret

if __name__ == "__main__":
    es = Elasticsearch("elastic.haochen.lu", port="9200", timeout=1000)
    term_vecs = fetch_term_vecs(es, "25609", "enwiki")
    query_term_vec = fetch_query_term_vec(es, "Stockholm University", "enwiki")
    print(query_term_vec)
