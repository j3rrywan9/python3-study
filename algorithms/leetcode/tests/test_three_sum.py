#!/usr/bin/env python3
from algorithms.leetcode.three_sum import Solution


def test_example():
    assert Solution().three_sum([-1, 0, 1, 2, -1, -4]) == [[-1, 0, 1], [-1, 2, -1]]
