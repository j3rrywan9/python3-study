# LC 11


class Solution:
    def max_area(self, height):
        i, j, max_area = 0, len(height) - 1, 0

        while i < j:
            if height[i] < height[j]:
                min_height = height[i]
                i += 1
            else:
                min_height = height[j]
                j -= 1

            area = (j - i + 1) * min_height
            max_area = max(max_area, area)

        return max_area
