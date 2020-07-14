#!/usr/bin/env python3
from ..longest_substring_without_repeating_characters import Solution


def test_example1():
    assert(Solution().length_of_longest_substring("abcabcbb") == 3)


def test_example2():
    assert(Solution().length_of_longest_substring("bbbbb") == 1)


def test_example3():
    assert(Solution().length_of_longest_substring("pwwkew") == 3)
