# LC 22


class Solution:
    def generate_parentheses(self, n):
        def generate(ans, cur, left, right):
            if len(cur) == 2 * n:
                ans.append(cur)
                return

            if left < n:
                generate(ans, cur + '(', left + 1, right)

            if right < left:
                generate(ans, cur + ')', left, right + 1)

        ans = []
        generate(ans, "", 0, 0)

        return ans
