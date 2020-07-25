#!/usr/bin/env python3
from ..reverse_only_letters import Solution


def test_example1():
    assert Solution().reverse_only_letters("ab-cd") == "dc-ba"


def test_example2():
    assert Solution().reverse_only_letters("a-bC-dEf-ghIj") == "j-Ih-gfE-dCba"


def test_example3():
    assert Solution().reverse_only_letters("Test1ng-Leet=code-Q!") == "Qedo1ct-eeLg=ntse-T!"
