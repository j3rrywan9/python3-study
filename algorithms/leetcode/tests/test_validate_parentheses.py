#!/usr/bin/env python3
from ..validate_parentheses import Solution


def test_example1():
    assert Solution().is_valid('()[]{}') is True


def test_example2():
    assert Solution().is_valid('(]') is False


def test_example3():
    assert Solution().is_valid('([)]') is False


def test_example4():
    assert Solution().is_valid('{[]}') is True
