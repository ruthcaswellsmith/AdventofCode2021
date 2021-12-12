from enum import Enum, auto
import numpy as np
from typing import List

START = 'start'
END = 'end'

class Part(str, Enum):
    PART_ONE = auto()
    PART_TWO = auto()

class Caves():

    def __init__(self, connections: List):

        self.connections = connections
        self.lookup = {}

        for connection in self.connections:

            self.__add_connection(connection[0], connection[1])
            self.__add_connection(connection[1], connection[0])

        self.small_caves = [cave for cave in self.lookup.keys() if cave.islower() and cave not in [START, END]]
        self.paths = []

    def __add_connection(self, a: str, b: str):

        if a in self.lookup:
            self.lookup[a].append(b)
        else:
            self.lookup[a] = [b]

    def get_paths(self, path: str, part: Part):

        most_recent_cave = path[path.rfind(',') + 1:]
        for next_cave in self.lookup[most_recent_cave]:

            if next_cave == START or not self.__ok_to_visit(path=path, cave=next_cave, part=part):
                pass
            elif next_cave == END:
                self.paths.append(f'{path},{END}')
            else:
                self.get_paths(path=f'{path},{next_cave}', part=part)

    def __ok_to_visit(self, path: str, cave: str, part: Part):

        if cave.isupper():
            return True

        if part == part.PART_ONE:

            return False if cave in path else True

        else:

            if cave not in path:
                return True
            else:
                visits = np.array([path.count(small_cave) for small_cave in self.small_caves])
                return True if max(visits) == 1 else False


def process_file(filename):

    with open(filename, 'r') as f:
        data = f.read().rstrip('\n').split('\n')

    connections = []
    for i in range(len(data)):
        connections.append(data[i].split('-'))

    return connections

if __name__ == "__main__":

    filename = "input/Day12.txt"
    connections = process_file(filename)

    caves = Caves(connections)
    caves.get_paths('start', Part.PART_ONE)
    print(f'The answer to part one is {len(caves.paths)}.')

    caves = Caves(connections)
    caves.get_paths('start', Part.PART_TWO)
    print(f'The answer to part two is {len(caves.paths)}.')

