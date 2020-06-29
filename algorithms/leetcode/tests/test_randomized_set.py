#!/usr/bin/env python3
from ..randomized_set import RandomizedSet


def test_example():
    randomized_set = RandomizedSet()
    assert randomized_set.insert(1) is True
    assert randomized_set.remove(2) is False
    assert randomized_set.insert(2) is True
    assert randomized_set.get_random() == 1 or 2
    assert randomized_set.remove(1) is True
    assert randomized_set.insert(2) is False
    assert randomized_set.get_random() == 2
