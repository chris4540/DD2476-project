"""
A module for all NLP or IR related algorithms or subroutines
"""

import numpy as np
from math import sqrt
from math import exp
from math import log
import time

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

    # Euclidean norm (L2-norm)
    vec1_norm = np.linalg.norm(list(vec1.values()), ord=2)
    vec2_norm = np.linalg.norm(list(vec2.values()), ord=2)

    # Normalize vectors
    n_vec1 = {w : e / vec1_norm for w, e in vec1.items()}
    n_vec2 = {w : e / vec2_norm for w, e in vec2.items()}

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
    tf = term_vec['term_freq']
    idf = np.log(doc_count / term_vec['doc_freq'])  # natual log
    return tf*idf

def aggregate_term_vecs(term_vecs, weigths):
    """
    Args:
        term_vecs from fetcher.fetch_term_vecs
    """
    ret = dict()

    for cat in weigths.keys():
        w = weigths[cat]
        t_vecs = term_vecs[cat]
        for t_vec in t_vecs:
            for term in t_vec.keys():
                if term not in ret:
                    ret[term] = 0
                ret[term] += w*t_vec[term]
    print(len(ret))
    return ret

def aggregate_time_term_vecs(term_vec_now, term_vec_t, half_life=86400):
    """
    Aggregate term vector at centain time t to current term vec

    Args:
        half_life (float): the half life in exponential decay.
            Default is one day
    """
    # calculate the decay rate lambda
    decay_rate = log(2) / half_life

    t_now = int(time.time())
    ret = term_vec_now.copy()

    for term in term_vec_t:
        t_past = term_vec_t[term]['posix_time']
        time_decay_factor = exp(-decay_rate*(t_now-t_past))
        print(time_decay_factor)
        val = ret.get(term, 0) + time_decay_factor*term_vec_t[term]['score']
        ret[term] = val

    return ret
