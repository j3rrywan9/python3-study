# LC 283


class Solution:
    def move_zeroes(self, nums):
        anchor = 0

        for explorer in range(len(nums)):
            if nums[explorer]:
                nums[anchor], nums[explorer] = nums[explorer], nums[anchor]
                anchor += 1
