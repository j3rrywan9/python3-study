# LC 61


class Solution:
    def rotate_right(self, head, k):
        if head is None or head.next is None or k == 0:
            return head

        old_tail = head
        n = 1

        while old_tail.next:
            old_tail = old_tail.next
            n += 1

        old_tail.next = head

        new_tail = head

        for i in range(n - k % n - 1):
            new_tail = new_tail.next

        new_head = new_tail.next

        new_tail.next = None

        return new_head
