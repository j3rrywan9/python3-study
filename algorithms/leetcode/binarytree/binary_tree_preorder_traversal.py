# LC 144


class Solution:
    def preorder_traversal(self, root):
        if root is None:
            return []

        result, stack = [], [root, ]

        while stack:
            root = stack.pop()

            if root is not None:
                result.append(root.val)

                if root.right is not None:
                    stack.append(root.right)
                if root.left is not None:
                    stack.append(root.left)

        return result
