# LC 3


class Solution(object):
    def length_of_longest_substring(self, s):
        """
        :param s: input string
        :type s: str
        :return: the length of the longest substring without repeating characters
        :rtype: int
        """
        start = max_length = 0
        used_char = {}

        for index, char in enumerate(s):
            if char in used_char and start <= used_char[char]:
                start = used_char[char] + 1
            else:
                max_length = max(max_length, index - start + 1)

            used_char[char] = index

        return max_length
