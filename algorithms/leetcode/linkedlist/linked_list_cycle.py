# LC 141


class Solution:
    def has_cycle(self, head):
        if head is None or head.next is None:
            return False

        slow = head
        fast = head.next

        while slow != fast:
            if fast is None or fast.next is None:
                return False

            slow = slow.next
            fast = fast.next.next

        return True
