#!/usr/bin/env python3
from ..longest_palindromic_substring import Solution


def test_example1():
    assert Solution().longest_palindrome('babad') == 'aba'


def test_example2():
    assert Solution().longest_palindrome('cbbd') == 'bb'
