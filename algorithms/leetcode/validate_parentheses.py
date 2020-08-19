# LC 20


class Solution:
    def is_valid(self, s):
        if len(s) == 0:
            return True

        stack = []

        for c in s:
            if c == '[' or c == '(' or c == '{':
                stack.append(c)
            elif c == ']' and len(stack) > 0 and stack[-1] == '[' or \
                    c == ')' and len(stack) > 0 and stack[-1] == '(' or \
                    c == '}' and len(stack) > 0 and stack[-1] == '{':
                stack = stack[:-1]
            else:
                return False

        return len(stack) == 0
