class Solution:
    def hIndex(self, citations: List[int]) -> int:
        lenc = len(citations)
        if lenc == 0:
            return 0
        citations.sort(reverse=True)
        for hm in range(lenc):
            if citations[hm] >= hm+1:
                if hm+1 < len(citations):
                    if citations[hm+1] <= hm+1:
                        return hm+1
        return min(citations[lenc-1], lenc)
