# LC 70


class Solution:
    def climb_stairs(self, n):
        dp1, dp2 = 1, 1

        for i in range(2, n + 1):
            dp2, dp1 = dp1 + dp2, dp2

        return dp2
