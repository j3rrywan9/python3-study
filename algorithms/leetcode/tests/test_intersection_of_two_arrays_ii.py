#!/usr/bin/env python3
from ..intersection_of_two_arrays_ii import Solution


def test_example1():
    assert Solution().intersect([1, 2, 2, 1], [2, 2]) == [2, 2]


def test_example2():
    assert Solution().intersect([4, 9, 5], [9, 4, 9, 8, 4]) == [4, 9]
