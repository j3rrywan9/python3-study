#!/usr/bin/env python3
from ..n_queens import Solution


def test_example():
    assert Solution().solve_n_queens(4) == [['.Q..', '...Q', 'Q...', '..Q.'], ['..Q.', 'Q...', '...Q', '.Q..']]
