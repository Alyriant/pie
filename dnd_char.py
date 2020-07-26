import heapq
import math
import random
import typing

NUM_STATS = 6
POPULATION_SIZE = 10_000_000
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
        self.rms_weight = math.sqrt(self.rms_weight / NUM_STATS)
    
    def print_stats(self, char_num):
        s = self.stats
        print(f"({char_num:3}) "
            f"Str {s[0]:2} Int {s[1]:2} Wis {s[2]:2} Dex {s[3]:2} Con {s[4]:2} Chr {s[5]:2} "
            f"Weight: {self.simple_weight/NUM_STATS:.1f} RMS: {self.rms_weight:.1f}")
   
def find_top_characters(num_total, num_to_find):
    if num_total < num_to_find:
        num_to_find = num_total
    
    # priority queues of found character weights
    pq = []
    rpq = []
    # dict of priority -> characters at that priority
    found_pq = {}
    found_rpq = {}
    
    def add_character(char, weight, found_chars, pq):
        
        if len(pq) == num_to_find and weight < pq[0]:
            return  #optimization
        else:
            char_set = found_chars.get(weight)
            if char_set:
                char_set.add(char)
            else:
                char_set = {char,}
                found_chars[weight] = char_set
                if len(pq) < num_to_find:
                    heapq.heappush(pq, weight)
                elif pq[0] < weight:
                    removed = heapq.heapreplace(pq, weight)
                    found_chars.pop(removed)
    
    def create_characters():
        for i in range(num_total+1):
            c = Character()        
            add_character(c, c.simple_weight, found_pq, pq)
            add_character(c, c.rms_weight, found_rpq, rpq)
    
    def print_characters(pq, found_chars, label):
        pq.sort()
        pq.reverse()
        num_printed = 0
        
        print(label)
        for weight in pq:
            for char in found_chars[weight]:
                num_printed += 1
                char.print_stats(num_printed)
            if num_printed >= num_to_find:
                break
                    
    create_characters()
    print_characters(pq, found_pq, "Top characters by simple weight:")
    print_characters(rpq, found_rpq, "Top RMS characters:")

        
if __name__ == "__main__":
    find_top_characters(num_total=POPULATION_SIZE, num_to_find=NUM_TO_FIND)
    
    