# LC 15


class Solution:
    def three_sum(self, nums, target=0):
        res = []
        found = set()

        for i, val1 in enumerate(nums):
            seen = set()

            for j, val2 in enumerate(nums[i+1:]):
                complement = target - val1 - val2

                if complement in seen:
                    min_val = min(val1, val2, complement)
                    max_val = max(val1, val2, complement)

                    if (min_val, max_val) not in found:
                        found.add((min_val, max_val))
                        res.append([val1, complement, val2])

                seen.add(val2)

        return res
