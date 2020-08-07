#!/usr/bin/env python3
from algorithms.leetcode.heap.kth_smallest_element_in_a_sorted_matrix import Solution


def test_example1():
    assert Solution().kth_smallest([[1,  5,  9], [10, 11, 13], [12, 13, 15]], 8) == 13
