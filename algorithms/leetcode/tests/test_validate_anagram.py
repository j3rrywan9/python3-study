#!/usr/bin/env python3
from ..validate_anagram import Solution


def test_example1():
    assert Solution().is_anagram('anagram', 'nagaram') is True


def test_example2():
    assert Solution().is_anagram('rat', 'car') is False
