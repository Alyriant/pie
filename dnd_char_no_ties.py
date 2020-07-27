from dataclasses import dataclass, field
import heapq
import math
import random
import typing

NUM_STATS = 6
POPULATION_SIZE = 10_000
NUM_TO_FIND = 10


class Character:
    def __init__(self):
        self.stats = []
        self.simple_weight = 0
        self.rms_weight = 0
        self.roll()
        
    def roll(self):

        for i in range(NUM_STATS):
            s = random.randrange(1,7) + random.randrange(1,7) + random.randrange(1,7)
            self.stats.append(s)
            self.simple_weight += s
            self.rms_weight += s**2
        self.rms_weight = math.sqrt(self.rms_weight / 6)
    
    def print_stats(self):
        s = self.stats
        print(f"Str {s[0]:2} Int {s[1]:2} Wis {s[2]:2} Dex {s[3]:2} Con {s[4]:2} Chr {s[5]:2} "
            f"Weight: {self.simple_weight/6:.1f} RMS: {self.rms_weight:.1f}")

@dataclass(order=True)
class SimpleWeightedCharacter:
    priority: int
    character: Character=field(compare=False)
    
    def __init__(self, character):
        self.character = character
        self.priority = character.simple_weight

@dataclass(order=True)
class RMSWeightedCharacter:
    priority: float
    character: Character=field(compare=False)
    
    def __init__(self, character):
        self.character = character
        self.priority = character.rms_weight

   
def find_top_characters(num_total, num_to_find):
    if num_total < num_to_find:
        num_to_find = num_total
    
    pq = []
    rpq = []
    for i in range(num_to_find+1):
        c = Character()
        pq.append(SimpleWeightedCharacter(c))
        rpq.append(RMSWeightedCharacter(c))
    heapq.heapify(pq)
    heapq.heapify(rpq)
    
    for i in range(num_total - num_to_find):
        c = Character()
        if c.simple_weight > pq[0].priority:
            heapq.heapreplace(pq, SimpleWeightedCharacter(c))
        if c.rms_weight > rpq[0].priority:
            heapq.heapreplace(rpq, RMSWeightedCharacter(c))
    
    pq.sort()
    rpq.sort()
    
    print("Top characters by simple weight:")
    for item in pq:
        item.character.print_stats()
    print("Top RMS characters:")
    for item in rpq:
        item.character.print_stats()
        
if __name__ == "__main__":
    find_top_characters(num_total=POPULATION_SIZE,num_to_find=NUM_TO_FIND)
    
    