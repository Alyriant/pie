
# The number of tasks is in the range [1, 10000].
# The integer n is in the range [0, 100].

from typing import List
from collections import Counter

class Solution:
    
    def leastInterval(self, tasks: List[str], n: int) -> int:
        counter = Counter(tasks)
        counts = []
        for task in counter:
            counts.append(counter[task])
        counts.sort(reverse=True)
        num_most_frequent = counts[0]
        num_distinct = 1
        i = 1
        while i < len(counts):
            if counts[i] == counts[0]:
                num_distinct += 1
                i += 1
            else:
                break
        min_with_idles = (num_most_frequent-1)*(n+1)+num_distinct
        min_total = max(min_with_idles, len(tasks))
        
        #return min_total
        
        s = "print(n, len(tasks), num_most_frequent, num_distinct, min_with_idles, min_total)"
        print(s)
        exec(s)
        
if __name__ == '__main__':
#tasks = ["A","A","A","A","A","A","B","C","D","E","F","G"]
    tasks = ["A","A","A","B","B","B"]
    s = Solution()
    s.leastInterval(tasks, 2)