#!/usr/bin/env python3
from ..squares_of_a_sorted_array import Solution


def test_example1():
    assert Solution().sorted_squares([-4, -1, 0, 3, 10]) == [0, 1, 9, 16, 100]


def test_example2():
    assert Solution().sorted_squares([-7, -3, 2, 3, 11]) == [4, 9, 9, 49, 121]
