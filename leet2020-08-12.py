class Solution:
    def getRow(self, rowIndex: int) -> List[int]:
        k = 0
        p = [1]
        if rowIndex == 0:
            return p
        elif rowIndex == 1:
            p.append(1)
            return p
        else:
            for k in range(rowIndex + 1):
                q = [1]
                for j in range(k-1):
                    q.append(p[j] + p[j+1])
                q.append(1)
                p = q
            return p
    