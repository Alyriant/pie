from dataclasses import dataclass, field
import heapq
import math
import random
import typing

NUM_STATS = 6
POPULATION_SIZE = 1_000_000
NUM_TO_FIND = 10

class CharacterClass:
    def __init__(self, name, weight_multipliers):
        self.name = name
        self.weight_multipliers = weight_multipliers
        self.priority_queue = []
        
classes = [
    CharacterClass("Cleric",	    [ 3,  3,  9,  3,  3,  3]),
    CharacterClass("Druid",	        [ 3,  3, 12,  3,  3, 15]),
    CharacterClass("Fighter",	    [ 9,  3,  3,  3,  7,  3]),
    CharacterClass("Paladin",	    [12,  9, 13,  3,  9, 17]),
    CharacterClass("Ranger",	    [13, 13, 14,  3, 14,  3]),
    CharacterClass("Magic-User",	[ 3,  9,  3,  3,  3,  3]),
    CharacterClass("Illusionist",	[ 3, 15,  3, 16,  3,  3]),
    CharacterClass("Thief",	        [ 3,  3,  3,  9,  3,  3]),
    CharacterClass("Assassin",	    [12, 11,  3, 12,  3,  3]),
    CharacterClass("Monk",	        [15,  3, 15, 15, 11,  3]),
    CharacterClass("Bard",	        [15, 12, 15, 15, 10, 15]),
]
    
class Character:
    def __init__(self):
        self.stats = []
        self.roll()
        
    def roll(self):
        for i in range(NUM_STATS):
            s = random.randrange(1,7) + random.randrange(1,7) + random.randrange(1,7)
            self.stats.append(s)
    
    def print_stats(self):
        s = self.stats
        print(f"Str {s[0]:2} Int {s[1]:2} Wis {s[2]:2} Dex {s[3]:2} Con {s[4]:2} Chr {s[5]:2} ")


@dataclass(order=True)
class WeightedCharacter:
    priority: int
    character: Character=field(compare=False)
    
    def __init__(self, priority, character):
        self.priority = priority
        self.character = character

   
def find_top_characters(num_total, num_to_find):
    if num_total < num_to_find:
        num_to_find = num_total
    
    for i in range(num_total+1):
        c = Character()
        for char_class in classes:
            pq = char_class.priority_queue
            wm = char_class.weight_multipliers
            weight = 0
            for j in range(NUM_STATS):
                if c.stats[j] < wm[j]:
                    break
                weight += c.stats[j] * wm[j]
                if j == NUM_STATS-1:
                    if len(pq) < num_to_find:
                        heapq.heappush(pq, (WeightedCharacter(weight, c)))
                    elif weight > pq[0].priority:
                        heapq.heapreplace(pq, WeightedCharacter(weight, c))
    
    for char_class in classes:
        pq = char_class.priority_queue
        pq.sort()
    
        print("\n", char_class.name, char_class.weight_multipliers)
        for item in pq:
            item.character.print_stats()
        
if __name__ == "__main__":
    find_top_characters(num_total=POPULATION_SIZE,num_to_find=NUM_TO_FIND)
    
    