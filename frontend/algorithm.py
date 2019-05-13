"""
A module for all NLP or IR related algorithms or subroutines
"""

import numpy as np
from math import sqrt
from math import exp
from math import log
import time
import re
from collections import OrderedDict

def normalize_term_vec(term_vec, ord_=2):
    elements = list(term_vec.values())
    norm = np.linalg.norm(elements, ord=ord_)

    ret = dict()
    for t in term_vec.keys():
        ret[t] = term_vec[t] / norm

    return ret

def cosine_similarity(vec1, vec2):
    """
    Computes the cosine similarity between two vectors stored as Python
    dictionaries.

    Args:
        vec1 (dict): The term vector 1
        vec2 (dict): The term vector 2

    Return:
        a floating point number representing the cosine similarity
    """

    # Normalize vectors with L2-norm
    n_vec1 = normalize_term_vec(vec1, ord_=2)
    n_vec2 = normalize_term_vec(vec2, ord_=2)

    # sum the similarity
    ret = 0.0
    for w in n_vec1.keys(): # w: an iterator for word
        ret += n_vec1.get(w, 0) * n_vec2.get(w, 0)

    return ret

def get_tfidf_weight(term_vec, doc_count):
    """
    Tranditional tf-idf algorithm
    Args:
        term_vec (dict):
            E.g.
            {
                "doc_freq": 1012,
                "term_freq": 2
            }
        doc_count (int): the total number of documents
    Return:
        tf-idf value
    """
    tf = term_vec.get('term_freq', 0)
    doc_freq = term_vec.get('doc_freq', 0)
    idf = np.log(doc_count/(1+doc_freq))
    return tf*idf

def aggregate_term_vecs(term_vecs, weigths):
    """
    Args:
        term_vecs:
        {
            "title": {
                'sweden': 1.0,
                ...
            }
            "text": {
                'sweden': 1.0,
                ...
            }
            ...,
        }
    """
    ret = dict()

    weight_sum = 0
    for cat in weigths.keys():
        weight_sum += weigths[cat]

    for cat in weigths.keys():
        w = weigths[cat] / weight_sum
        t_vec = term_vecs[cat]
        n_t_vec = normalize_term_vec(t_vec)
        for term in n_t_vec.keys():
            if term not in ret:
                ret[term] = 0
            ret[term] += w*t_vec[term]

    return ret

def weight_mean_term_vecs(vec1, vec2, weight1, weight2):
    alpha = weight1 / (weight1 + weight2)
    beta = (1 - alpha)

    terms = set(vec1.keys()).union(set(vec2.keys()))

    ret = dict()
    for t in terms:
        ret[t] = alpha*vec1.get(t, 0) + beta*vec2.get(t, 0)
    return ret

# def aggregate_time_term_vecs(term_vec_now, term_vec_t, half_life=86400):
def aggregate_time_term_vecs(term_vec_now, term_vec_t, half_life):
    """
    Aggregate term vector at centain time t to current term vec

    Args:
        half_life (float): the half life in exponential decay.
    """
    # calculate the decay rate lambda
    decay_rate = log(2) / half_life

    t_now = int(time.time())
    ret = term_vec_now.copy()

    for term in term_vec_t:
        t_past = term_vec_t[term]['posix_time']
        time_decay_factor = exp(-decay_rate*(t_now-t_past))
        val = ret.get(term, 0) + time_decay_factor*term_vec_t[term]['score']
        ret[term] = val
    return ret

def calcuate_term_vec_now(term_vec_t, half_life):
    # calculate the decay rate lambda
    decay_rate = log(2) / half_life
    t_now = int(time.time())

    ret = dict()
    for term in term_vec_t.keys():
        time_past = term_vec_t[term]['posix_time']
        time_decay_factor = exp(-decay_rate*(t_now-time_past))
        ret[term] = time_decay_factor*term_vec_t[term]['score']
    return ret

def filter_term_vec(term_vec):
    """
    Filter a term vector

    TODO: get filtering rule from config
    """
    ret = dict()
    pattern = re.compile(r"^\d+[,.]?\d*$")  # match if number
    for t in term_vec.keys():
        if not pattern.fullmatch(t):
            ret[t] = term_vec[t]
    return ret

def get_sorted_term_vec(term_vec, limit=None):
    # if limit is not None and limit > 0:
    #     pass

    sorted_items = sorted(term_vec.items(), key=lambda kv: kv[1], reverse=True)
    if isinstance(limit, int) and limit > 0:
        # make it have a limit
        sorted_items = sorted_items[:limit]

    sorted_vec = OrderedDict(sorted_items)
    return sorted_vec

