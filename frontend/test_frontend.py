# File for writing tests
from frontend import cos_sim

def test_cos_sim():
    v1 = {'hitler' : 10}
    v2 = {'hitler' : 3}
    assert cos_sim(v1, v2) == 1.0

    v1 = {'hitler' : 1, 'nazi' : 1}
    v2 = {'banana' : 1, 'nazi' : 1}
    assert round(cos_sim(v1, v2), 2) == 0.5

    v1 = {}
    v2 = {'foo' : 30}
    assert cos_sim(v1, v2) == 0.0

if __name__ == '__main__':
    test_cos_sim()
