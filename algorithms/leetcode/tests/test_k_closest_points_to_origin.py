#!/usr/bin/env python3
from ..k_closest_points_to_origin import Solution


def test_example1():
    assert Solution().k_closest([[1, 3], [-2, 2]], 1) == [[-2, 2]]


def test_example2():
    assert Solution().k_closest([[3, 3], [5,- 1], [-2, 4]], 2) == [[3, 3], [-2, 4]]
