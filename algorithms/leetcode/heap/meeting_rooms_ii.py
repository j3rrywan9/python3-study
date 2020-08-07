# LC 253
import heapq


class Solution:
    def min_meeting_rooms(self, intervals):
        if not intervals:
            return 0

        rooms = []

        # Sort the intervals by start time
        intervals.sort(key=lambda i: i[0])

        # Add first meeting's end time
        heapq.heappush(rooms, intervals[0][1])

        # Iterate over remaining intervals
        for interval in intervals[1:]:
            # If the room due to free up the earliest is free, assign that room to this meeting.
            if interval[0] >= rooms[0]:
                heapq.heappop(rooms)

            # If a new room is to be assigned, then also we add to the heap,
            # If an old room is allocated, then also we have to add to the heap with updated end time.
            heapq.heappush(rooms, interval[1])

        # The size of the heap tells us the minimum rooms required for all the meetings.
        return len(rooms)
