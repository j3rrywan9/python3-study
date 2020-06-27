#!/usr/bin/env python3
from ..knight_dialer import Solution


def test_example1():
    assert Solution().knight_dialer(1) == 10


def test_example2():
    assert Solution().knight_dialer(2) == 20


def test_example3():
    assert Solution().knight_dialer(3) == 46
