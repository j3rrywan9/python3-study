#!/usr/bin/env python 3
from ..valid_palindrome import Solution


def test_example1():
    assert Solution().is_palindrome("A man, a plan, a canal: Panama") is True


def test_example2():
    assert Solution().is_palindrome("race a car") is False
