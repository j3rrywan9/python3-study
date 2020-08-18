# LC 242


class Solution:
    def is_anagram(self, s, t):
        if len(s) == 0 and len(t) == 0:
            return True

        if len(s) == 0 or len(t) == 0:
            return False

        if len(s) != len(t):
            return False

        table = [0] * 26

        for i in range(len(s)):
            table[ord(s[i])-ord('a')] += 1

        for i in range(len(t)):
            table[ord(t[i])-ord('a')] -= 1

        for i in range(26):
            if table[i] != 0:
                return False

        return True
