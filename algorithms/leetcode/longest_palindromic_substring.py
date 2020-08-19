# LC 5


class Solution(object):
    def longest_palindrome(self, s):
        """
        :param s: input string
        :type s: str
        :return: the longest palindromic substring in input string
        :rtype: str
        """
        res = ""

        for i in range(len(s)):
            res = max(self.helper(s, i, i), self.helper(s, i, i + 1), res, key=len)

        return res

    def helper(self, s, left, right):
        while left >= 0 and right < len(s) and s[left] == s[right]:
            left -= 1
            right += 1

        return s[left+1:right]
