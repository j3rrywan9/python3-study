# LC 692
from collections import Counter
import heapq


class Solution:
    def top_k_frequent(self, words, k):
        count = Counter(words)
        heap = [(-frequency, word) for word, frequency in count.items()]
        heapq.heapify(heap)

        return [heapq.heappop(heap)[1] for _ in range(k)]
