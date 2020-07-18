# LC 416


class Solution:
    def can_partition(self, nums):
        n, sum_of_nums = len(nums), sum(nums)

        # if sum_of_nums is an odd number, we can't have two subsets with same total
        if sum_of_nums % 2 != 0:
            return False

        sum_of_nums //= 2

        # whether we can sum to s using first i numbers
        dp = [[False] * (sum_of_nums + 1) for _ in range(n)]

        # populate the s=0 column with True, as we can always have '0' sum without including any element
        for i in range(n):
            dp[i][0] = True

        # with only one number, we can form a subset only when the required sum is equal to its value
        for s in range(1, sum_of_nums + 1):
            dp[0][s] = nums[0] == s

        # process all subsets for all sums
        for i in range(1, n):
            for s in range(1, sum_of_nums + 1):
                # if we can get the sum 's' without the number at index 'i'
                if dp[i - 1][s]:
                    dp[i][s] = dp[i - 1][s]
                # else if we can find a subset to get the remaining sum
                elif s >= nums[i]:
                    dp[i][s] = dp[i - 1][s - nums[i]]

        return dp[n-1][sum_of_nums]
