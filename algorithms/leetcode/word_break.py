# LC 139


class Solution:
    def __init__(self):
        self.memo = dict()

    def word_break(self, s, word_dict):
        return self.word_break_topdown(s, set(word_dict))

    def word_break_topdown(self, s, word_dict):
        # In memo, directly return
        if s in self.memo:
            return self.memo[s]

        # The whole string is a word, memoize and return
        if s in word_dict:
            self.memo[s] = True
            return True

        # Try every break point
        for i in range(len(s)):
            left = s[0:i]
            right = s[i:]

            # Find the solution for s
            if self.word_break_topdown(left, word_dict) and right in word_dict:
                self.memo[s] = True
                return True

        # No solution for s, memoize and return
        self.memo[s] = False
        return False
