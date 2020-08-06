# LC 986


class Solution:
    def interval_intersection(self, A, B):
        ans = []
        i = j = 0

        while i < len(A) and j < len(B):
            lo = max(A[i][0], B[j][0])
            hi = min(A[i][1], B[j][1])

            if lo <= hi:
                ans.append([lo, hi])

            # remove the interval with the smallest end point
            if A[i][1] < B[j][1]:
                i += 1
            else:
                j += 1

        return ans
