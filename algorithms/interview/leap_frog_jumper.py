#!/usr/bin/env python3
import re
from collections import deque


class Solution:
    def get_char_at_index(self, s, index):
        pattern = re.compile(r'([a-zA-Z]+)(\d+)')
        match = pattern.findall(s)

        if match:
            queue = deque([(t[0], int(t[1])) for t in match])
            seq = ""

            while queue:
                t = queue.popleft()
                seq = (seq + t[0]) * t[1]

            if len(seq) > index:
                return seq[index]

        return ""
