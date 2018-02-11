from itertools import islice

import pytest

from pipeline.processor.synthesis.draw import Gradient


def test_iterate():
    n = 5
    g = Gradient([(0, 0, 0), (1, 1, 1)], n)
    five = list(islice(iter(g), n))
    assert list(range(n)) == [int(i * n) for i in range(n)]
