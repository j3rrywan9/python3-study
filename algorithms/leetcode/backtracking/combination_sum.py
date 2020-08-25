# LC 39


class Solution:
    def combination_sum(self, candidates, target):
        res = []

        candidates.sort()
        self.__backtrack(res, [], candidates, target, 0)

        return res

    def __backtrack(self, res, curr, candidates, remain, start):
        if remain < 0:
            return
        elif remain == 0:
            res.append(list(curr))
        else:
            for i in range(start, len(candidates)):
                if candidates[i] > remain:
                    break
                curr.append(candidates[i])
                self.__backtrack(res, curr, candidates, remain - candidates[i], i)
                curr.pop(len(curr) - 1)
