# LC 138


class Node:
    def __init__(self, x, next: None, random: None):
        self.val = int(x)
        self.next = next
        self.random = random


class Solution:

    def __init__(self):
        self.visited = {}

    def get_cloned_node(self, node):
        if node:
            if node in self.visited:
                return self.visited[node]
            else:
                self.visited[node] = Node(node.val, None, None)
                return self.visited[node]

        return None

    def copy_random_list(self, head):
        if not head:
            return head

        old_node = head
        new_node = Node(old_node.val, None, None)
        self.visited[old_node] = new_node

        while old_node is not None:
            new_node.random = self.get_cloned_node(old_node.random)
            new_node.next = self.get_cloned_node(old_node.next)

            old_node = old_node.next
            new_node = new_node.next

        return self.visited[head]
