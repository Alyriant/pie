from collections import Counter

class Solution:
    def longestPalindrome(self, s: str) -> int:
        c = Counter(s)
        hasOdd = False
        total = 0
        for elem, count in c.items():
            if count % 2 == 1:
                hasOdd = True
            total += count - count % 2
        if hasOdd:
            total += 1
        return total
    