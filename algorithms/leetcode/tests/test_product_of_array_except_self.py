#!/usr/bin/env python3
from algorithms.leetcode.product_of_array_except_self import Solution


def test_example():
    assert Solution().product_except_self([1, 2, 3, 4]) == [24, 12, 8, 6]
