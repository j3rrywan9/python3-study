# LC 70


class Solution:
    def climb_stairs(self, n):
        if n <= 2:
            return n

        first, second, third = 1, 2, 3

        for i in range(3, n+1):
            third = first + second
            first, second = second, third

        return third
