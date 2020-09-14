class Solution:
        
    def orangesRotting(self, grid):
        print("Grid:", grid)
        minutes = 0
        rows = len(grid)
        cols = len(grid[0])
        unvisited = [(x,y) for x in range(rows) for y in range(cols) if grid[x][y] == 2]
        new_unvisited = []
        
        def rot(x,y):
            print("rotting", x, y)
            if grid[x][y] == 1:
                grid[x][y] = 2
                new_unvisited.append((x,y))
                
        def rot_neighbors(x, y):
            print("rot neighbors of ", x, y)
            if x > 0: rot(x-1, y)
            if x < rows-1: rot(x+1, y)
            if y > 0: rot(x, y-1)
            if y < cols-1: rot(x,y+1)
        
        def has_fresh():
            for x in range(rows):
                for y in range(cols):
                    if grid[x][y] == 1:
                        return True
                        
        while unvisited:
            while unvisited:
                x,y = unvisited.pop()
                rot_neighbors(x, y)
            if new_unvisited:
                minutes += 1
                unvisited = new_unvisited
                new_unvisited = []
            
        if has_fresh():
            return -1
        else:
            return minutes

if __name__ ==  "__main__":
    s = Solution()
    print(s.orangesRotting([[2,1,1],[1,1,0],[0,1,1]]), "expect 4")
    print(s.orangesRotting([[2,1,1],[0,1,1],[1,0,1]]), "expect -1")
    print(s.orangesRotting([[0,2]]), "expect 0")
    print(s.orangesRotting([[1,2]]), "expect 1")
