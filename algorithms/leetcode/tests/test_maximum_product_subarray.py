#!/usr/bin/env python3
from ..dp.maximum_product_subarray import Solution


def test_example1():
    assert Solution().max_product([2, 3, -2, 4]) == 6


def test_example2():
    assert Solution().max_product([-2, 0, -1]) == 0
