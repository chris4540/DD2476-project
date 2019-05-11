"""
Run:
    1. python -m unittest tests/test_algo.py
    2. nosetests -v tests/test_algo.py
"""
import unittest
from algorithm import cosine_similarity
from algorithm import aggregate_time_term_vecs
import time

class TestAlgorithmModule(unittest.TestCase):

    def test_cos_sim(self):
        # case 1
        v1 = {'hitler' : 10}
        v2 = {'hitler' : 3}
        self.assertEqual(cosine_similarity(v1, v2), 1.0)

        # case 2
        v1 = {'hitler' : 1, 'nazi' : 1}
        v2 = {'banana' : 1, 'nazi' : 1}
        # assert round(cosine_similarity(v1, v2), 2) == 0.5
        self.assertAlmostEqual(cosine_similarity(v1, v2), 0.5, places=2)

        v1 = {}
        v2 = {'foo' : 30}
        self.assertEqual(cosine_similarity(v1, v2), 0.0)

    def test_aggregate_time_term_vecs(self):
        time_diff = 12 * 3600  # 12 hours
        time_now = int(time.time())
        v_now = {
            'sweden': 1.0,
            'meetball': 1.0,
        }

        v_old = {
            'sweden': {
                'score': 1.0,
                'posix_time': (time_now - time_diff)
            }
        }
        vec = aggregate_time_term_vecs(v_now, v_old, half_life=time_diff)

        # The term sweden should be decayed by half.
        self.assertEqual(vec['sweden'], 1.5)
        self.assertEqual(vec['meetball'], 1.0)


