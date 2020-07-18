#!/usr/bin/env python3
from ..partition_equal_subset_sum import Solution


def test_example1():
    assert Solution().can_partition([1, 5, 11, 5]) is True


def test_example2():
    assert Solution().can_partition([1, 5]) is False
