# LC 973


class Solution:
    def k_closest(self, points, k):
        points.sort(key=lambda p: p[0] ** 2 + p[1] ** 2)
        return points[:k]
