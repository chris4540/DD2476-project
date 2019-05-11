"""
A module for all NLP or IR related algorithms or subroutines
"""

import numpy as np
from math import sqrt

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

if __name__ == "__main__":
    v1 = {'hitler' : 10}
    v2 = {'hitler' : 3}
    assert cosine_similarity(v1, v2) == 1.0

    v1 = {'hitler' : 1, 'nazi' : 1}
    v2 = {'banana' : 1, 'nazi' : 1}
    assert round(cosine_similarity(v1, v2), 2) == 0.5

    v1 = {}
    v2 = {'foo' : 30}
    assert cosine_similarity(v1, v2) == 0.0
