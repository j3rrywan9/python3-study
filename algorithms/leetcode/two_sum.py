# LC 1


class Solution(object):
    def two_sum(self, nums, target):
        d = {}

        for index, num in enumerate(nums):
            complement = target - num

            if complement in d:
                return [d[complement], index]
            else:
                d[num] = index

        raise RuntimeError("No two sum solution")
