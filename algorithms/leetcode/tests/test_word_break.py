#!/usr/bin/env python3
from ..word_break import Solution


def test_example1():
    assert Solution().word_break('leetcode', ['leet', 'code']) is True


def test_example2():
    assert Solution().word_break('applepenapple', ['apple', 'pen']) is True


def test_example3():
    assert Solution().word_break('catsandog', ['cats', 'dog', 'sand', 'and', 'cat']) is False
