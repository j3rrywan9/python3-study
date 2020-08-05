# LC 112


class Solution:
    def has_path_sum(self, root, sum):
        if not root:
            return False

        if root.val == sum and not root.left and not root.right:
            return True

        return self.has_path_sum(root.left, sum - root.val) or self.has_path_sum(root.right, sum - root.val)
