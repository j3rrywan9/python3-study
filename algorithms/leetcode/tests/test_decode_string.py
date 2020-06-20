#!/usr/bin/env python3
from algorithms.leetcode.decode_string import Solution


def test_example1():
    assert Solution().decode_string('3[a]2[bc]') == 'aaabcbc'


def test_example2():
    assert Solution().decode_string('3[a2[c]]') == 'accaccacc'


def test_example3():
    assert Solution().decode_string('2[abc]3[cd]ef') == 'abcabccdcdcdef'


def test_example4():
    assert Solution().decode_string('abc3[cd]xyz') == 'abccdcdcdxyz'
