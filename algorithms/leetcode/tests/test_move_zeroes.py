#!/usr/bin/env python3
from ..move_zeroes import Solution


def test_example1():
    nums = [0, 1, 0, 3, 12]

    Solution().move_zeroes(nums)
    assert nums == [1, 3, 12, 0, 0]
