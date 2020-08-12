# LC 152


class Solution:
    def max_product(self, nums):
        if len(nums) == 0:
            return 0

        max_product_so_far = nums[0]
        min_product_so_far = nums[0]
        result = max_product_so_far

        for i in range(1, len(nums)):
            current = nums[i]
            temp_max_product = max(current, max_product_so_far * current, min_product_so_far * current)
            min_product_so_far = min(current, max_product_so_far * current, min_product_so_far * current)

            max_product_so_far = temp_max_product

            result = max(max_product_so_far, result)

        return result
