# LC 98


class Solution:
    def is_valid_BST(self, root):
        stack, inorder = [], float('-inf')

        while stack or root:
            while root:
                stack.append(root)
                root = root.left

            root = stack.pop()

            if root.val <= inorder:
                return False

            inorder = root.val
            root = root.right

        return True
