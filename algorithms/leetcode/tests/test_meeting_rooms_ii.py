#!/usr/bin/env python3
from ..meeting_rooms_ii import Solution


def test_example1():
    assert Solution().min_meeting_rooms([[0, 30], [5, 10], [15, 20]]) == 2


def test_example2():
    assert Solution().min_meeting_rooms([[7, 10], [2, 4]]) == 1
