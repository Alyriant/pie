class Solution:
    def titleToNumber(self, s: str) -> int:
        value = 0
        for c in s:
            value *= 26
            value += ord(c) - ord('A') + 1
        return value