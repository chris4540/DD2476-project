"""
Run:
    1. python -m unittest tests/test_algo.py
    2. nosetests -v tests/test_algo.py
"""
import unittest
from algorithm import cosine_similarity

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

