#!/usr/bin/env python3
from pathlib import Path
import heapq


class Solution:
    def get_top_k_largest_integers(self, k, path='./root'):
        files = [p for p in list(Path(path).glob('**/*')) if p.is_file()]
        heap = []

        for file in files:
            with open(str(file.resolve())) as fp:
                lines = fp.readlines()
                for line in lines:
                    heapq.heappush(heap, int(line))

        return heapq.nlargest(k, heap)


if __name__ == '__main__':
    print(Solution().get_top_k_largest_integers(k=5))
