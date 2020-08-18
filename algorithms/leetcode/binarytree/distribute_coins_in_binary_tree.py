# LC 979


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def distribute_coins(self, root):
        self.ans = 0

        def balance(node):
            if node is None:
                return 0
            left_subtree_balance = balance(node.left)
            right_subtree_balance = balance(node.right)
            self.ans += abs(left_subtree_balance) + abs(right_subtree_balance)
            # root balance
            return node.val - 1 + left_subtree_balance + right_subtree_balance

        balance(root)
        return self.ans
