#!/usr/bin/env python 3
from ..palindrome_number import Solution


def test_example1():
    assert Solution().is_palindrome(121) is True


def test_example2():
    assert Solution().is_palindrome(-121) is False
