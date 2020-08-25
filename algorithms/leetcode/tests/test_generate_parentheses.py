from ..backtracking.generate_parentheses import Solution


def test_example1():
    assert Solution().generate_parentheses(3) == [
      "((()))",
      "(()())",
      "(())()",
      "()(())",
      "()()()"
    ]
