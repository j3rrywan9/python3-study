# LC 378
import heapq


class Solution:
    def kth_smallest(self, matrix, k):
        n = len(matrix)
        min_heap = []

        for row in range(min(k, n)):
            # add a triplet of information for first element on each row
            min_heap.append((matrix[row][0], row, 0))

        heapq.heapify(min_heap)

        # until we find k elements
        while k:
            # get the smallest element from the heap
            element, row, column = heapq.heappop(min_heap)

            # add new items in the current row if there is any
            if column < n - 1:
                heapq.heappush(min_heap, (matrix[row][column+1], row, column+1))

            k -= 1

        return element
