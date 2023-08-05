# -*- coding: utf-8 -*-

import pytest
from trackimo.skeleton import fib

__author__ = "Troy Kelly"
__copyright__ = "Troy Kelly"
__license__ = "mit"


def test_fib():
    assert fib(1) == 1
    assert fib(2) == 1
    assert fib(7) == 13
    with pytest.raises(AssertionError):
        fib(-10)
