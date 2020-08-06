#!/usr/bin/env python3
from ..interval_list_intersections import Solution


def test_example1():
    assert Solution().interval_intersection(
        [[0, 2], [5, 10], [13, 23], [24, 25]], [[1, 5], [8, 12], [15, 24], [25, 26]]) == \
           [[1, 2], [5, 5], [8, 10], [15, 23], [24, 24], [25, 25]]
