from ..backtracking.combination_sum import Solution


def test_example1():
    assert Solution().combination_sum([2, 3, 6, 7], 7) == [[2, 2, 3], [7]]


def test_example2():
    assert Solution().combination_sum([2, 3, 5], 8) == [[2, 2, 2, 2], [2, 3, 3], [3, 5]]
