# LC 104


class Solution:
    def max_depth(self, root):
        if root is None:
            return 0
        else:
            left_height = self.max_depth(root.left)
            right_height = self.max_depth(root.right)
            return max(left_height, right_height) + 1
