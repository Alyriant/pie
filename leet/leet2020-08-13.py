class CombinationIterator:

    def __init__(self, characters: str, combinationLength: int):
        n = len(characters)
        r = combinationLength
        self.combos = []
        self.nextCombo = 0
        combo = ""
        self.generateCombos(0, r, n, characters, combo)
        #print(self.combos)
        
    def generateCombos(self, start, r, n, characters, combo):
        for i in range(start, n - r + 1):
            c = combo + characters[i]
            if r == 1:
                self.combos.append(c)
                #print(c)
            else:
                self.generateCombos(i+1, r-1, n, characters, c)         

    def next(self) -> str:
        #print("next()")
        n = self.combos[self.nextCombo]
        self.nextCombo += 1
        return n

    def hasNext(self) -> bool:
        #print("hasNext()")
        return self.nextCombo < len(self.combos)

# Your CombinationIterator object will be instantiated and called as such:
# obj = CombinationIterator(characters, combinationLength)
# param_1 = obj.next()
# param_2 = obj.hasNext()

if __name__ == "__main__":
    c = CombinationIterator("abcdefg", 3)
    while c.hasNext():
        print(c.next())
        