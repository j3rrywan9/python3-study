# LC 862
import collections


class Solution:
    def shortest_subarray(self, A, K):
        N = len(A)
        P = [0]

        for x in A:
            P.append(P[-1] + x)

        ans = N + 1
        mono_queue = collections.deque()

        for y, Py in enumerate(P):
            while mono_queue and Py <= P[mono_queue[-1]]:
                mono_queue.pop()
            while mono_queue and Py - P[mono_queue[0]] >= K:
                ans = min(ans, y-mono_queue.popleft())

            mono_queue.append(y)

        return ans if ans < N+1 else -1


if __name__ == '__main__':
    print(Solution().shortest_subarray([1], 1))
    print(Solution().shortest_subarray([1, 2], 4))
    print(Solution().shortest_subarray([2, -1, 2], 3))
