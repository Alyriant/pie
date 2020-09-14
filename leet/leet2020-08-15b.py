class Solution:
    def eraseOverlapIntervals(self, intervals: List[List[int]]) -> int:
        erase_count = 0
        # sort by interval ending soonest
        intervals = sorted(intervals, key = lambda x: x[1])
        prev_end = float("-inf")
        for start, end in intervals:
            if start < prev_end:
                erase_count += 1
            else:
                prev_end = end
        return erase_count