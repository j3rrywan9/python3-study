# LC 102
from collections import deque


class Solution:
    def level_order(self, root):
        result = []

        if root is None:
            return result

        queue = deque()

        queue.append(root)

        while queue:
            level_size = len(queue)
            current_level = []

            for _ in range(level_size):
                current_node = queue.popleft()

                current_level.append(current_node.val)

                if current_node.left:
                    queue.append(current_node.left)
                if current_node.right:
                    queue.append(current_node.right)

            result.append(current_level)

        return result
