# LC 42


class Solution:
    def trap(self, height):
        if len(height) == 0:
            return 0

        n = len(height)
        left, right = 0, n - 1
        max_left, max_right = height[left], height[right]
        ans = 0

        while left < right:
            if max_left < max_right:
                ans += max_left - height[left]
                left += 1
                max_left = max(max_left, height[left])
            else:
                ans += max_right - height[right]
                right -= 1
                max_right = max(max_right, height[right])

        return ans
