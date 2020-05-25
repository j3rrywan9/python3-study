# LC 1


class Solution(object):
    def two_sum(self, nums, target):
        map = {}

        for index, num in enumerate(nums):
            complement = target - num

            if complement in map:
                return [map[complement], index]
            else:
                map[num] = index

        raise RuntimeError("No two sum solution")


if __name__ == '__main__':
    print(Solution().two_sum([2, 7, 11, 15], 9))
