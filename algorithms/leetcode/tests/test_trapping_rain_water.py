#!/usr/bin/env python3
from ..trapping_rain_water import Solution


def test_example1():
    assert Solution().trap([0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1]) == 6
