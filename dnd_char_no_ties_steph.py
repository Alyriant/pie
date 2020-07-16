from functools import reduce
from heapq import heapify, heappop, heappush, nsmallest
from math import sqrt, trunc
from random import randrange

MAX_NUMBER = float("inf")
NUM_PLAYERS = 100000
TOP_N = 10

STAT_NAMES = [ "Str", "Int", "Wis", "Dex", "Con", "Chr" ]
NUM_STATS = len(STAT_NAMES)

WEIGHTING = {
    "sum": sum,
    "RMS": lambda scores : sqrt(reduce(lambda a,b : a + b*b))/scores.length
}
NUM_WEIGHTS = len(keys(WEIGHTING))


class Character:
    def __init__(self, id):
        self.id = id
        self.stats = []
        self.weights = {}
        self.__create_stats()

    @staticmethod
    def roll():
        return randrange(1, 7)

    def __create_stats(self):
        for i in range(NUM_STATS):
            s = self.roll() + self.roll() + self.roll()
            self.stats.append(s)
        self.weights = { key: func(self.stats) for key, func in WEIGHTING }

    def __str__(self):
        s = f"{id}:"
        for i in range(NUM_STATS):
            s = f"{s}{STAT_NAMES[i]}: {self.stats[i]}  "
        for i in range(NUM_WEIGHTS):
            s = f"{s} {WEIGHTING[i]} weight: {self.weights[WEIGHTING[i]]:.1f}  "
        return s


class ContainerHeap:
    def __init__(self, weight_name, heap_limit=MAX_NUMBER):
        self.weight_name = weight_name
        self.heap_limit = heap_limit
        self.min = MAX_NUMBER
        self.min_container = None
        self.size = 0
        self.heap = heapify([])
        self.containers = {}

    @dataclass(order=True)
    class CharacterContainer():
        priority: int
        def __init__(self, character):
            self.players = {character.id: character}
            self.priority = trunc(character.weight[self.weight_name])
            self.size = 1

        def add(self, character):
            self.players[character.id](character)
            self.size += 1

        def __str__(self):
            return "\n".join([str(player) for player in self.players])

    def push_container(self, container):
        heappush(self.heap, container)
        self.containers[container.priority] = container
        self.size += container.size

    def pop_container(self):
        container = heappop(self.heap)
        self.containers.pop(container.priority)
        self.size -= container.size
        self.min_container = nsmallest(1,self.heap)[0]
        self.min = self.min_container.size

    def push(self, character):
        priority = character.weights[self.weight_name]
        if priority < self.min:
            if self.size < self.heap_limit:
                container = self.CharacterContainer(character)
                self.push_container(container)
                self.min = container.priority
                self.min_container = container
        else:
            container = self.containers.get(priority, None)
            if container is None:
                container = self.CharacterContainer(character)
                self.push_container(container)
            else:
                container.add(character)
                self.size += 1

            if container is not self.min_container and (self.size - self.min_container.size) > self.heap_limit:
                self.pop_container()

    def __str__(self):
        s = "/n".join([str(container) for container in self.heap])
        return f"Top {self.heap_limit} (with ties) sorted by {self.weight_name}:\n{s}\n"


# begin execution
def find_top_characters(num_total, num_to_find):

    # create and populate dict of priority queue for each type of weighting
    pqs = {}
    for weight_name in WEIGHTING.keys():
        pqs[weight_name] = ContainerHeap(num_to_find)

    # now create characters and plop into limited-size priority queues of character containers
    for id in range(num_total):
        character = Character(id)
        for weight_name in WEIGHTING.keys():
            pqs[weight_name].push(character)

    # then print the container contents
    for weight_name in WEIGHTING.keys():
        print(pqs[weight_name])

if __name__ == "__main__":
    find_top_characters(NUM_PLAYERS, TOP_N)
