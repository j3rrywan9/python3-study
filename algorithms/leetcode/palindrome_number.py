# LC 9


class Solution:
    def is_palindrome(self, x):
        if x < 0 or (x != 0 and x % 10 == 0):
            return False

        reverted_number = 0

        while x > reverted_number:
            reverted_number = reverted_number * 10 + x % 10
            x //= 10

        return x == reverted_number or x == reverted_number // 10
