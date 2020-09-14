class Solution:
    def findPermutation(self, s: str) -> List[int]:
        n = len(s)
        num = 1
        i = 0
        series = []

        def countDAt(i):
            j = i
            count = 0
            while j < n and s[j] == 'D':
                count += 1
                j += 1
            return count
        
        if i == 0 and s[i] == 'I':
            series.append(num)
            num += 1
        while i < n:
            if s[i] == 'D':
                numD = countDAt(i)
                for j in range(numD+num, num-1, -1):
                    series.append(j)
                i += numD
                num += numD + 1
            elif i < n-1 and s[i+1] == 'D':
                numD = countDAt(i+1)
                for j in range(numD+num, num-1, -1):
                    series.append(j)
                i += numD + 1
                num += numD + 1
            else:
                series.append(num)
                i += 1
                num += 1
        
        return series
