# LC 917


class Solution:
    def reverse_only_letters(self, S):
        ans = []
        j = len(S) - 1

        for x in S:
            if x.isalpha():
                while not S[j].isalpha():
                    j -= 1

                ans.append(S[j])
                j -= 1
            else:
                ans.append(x)

        return ''.join(ans)
