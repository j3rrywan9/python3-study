# LC 238


class Solution(object):
    def product_except_self(self, nums):
        """
        :param nums: an array of integers
        :type nums: list of int
        :return:
        :rtype: list of int
        """
        length = len(nums)
        answer = [0] * length

        answer[0] = 1

        for i in range(1, length):
            answer[i] = nums[i-1] * answer[i-1]

        R = 1

        for i in reversed(range(length)):
            answer[i] = answer[i] * R
            R *= nums[i]

        return answer


if __name__ == '__main__':
    print(Solution().product_except_self([1, 2, 3, 4]))
