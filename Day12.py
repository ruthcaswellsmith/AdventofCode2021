from enum import Enum, auto
import numpy as np
from typing import List

START = 'start'
END = 'end'

class Caves():

    def __init__(self, connections: List):

        self.connections = connections
        self.lookup = {}

        for connection in self.connections:

            self.__add_connection(connection[0], connection[1])
            self.__add_connection(connection[1], connection[0])

        self.small_caves = [cave for cave in self.lookup.keys() if cave.islower() and cave not in ['start','end']]
        self.paths = []

        print(self.__ok_to_visit('A,B,c,b', 'c'))

    def __add_connection(self, a, b):

        if a in self.lookup:
            self.lookup[a].append(b)
        else:
            self.lookup[a] = [b]

    def get_paths_part_one(self, path):

        most_recent_cave = path[path.rfind(',') + 1:]
        for next_cave in self.lookup[most_recent_cave]:

            if (next_cave.islower() and next_cave in path) or (next_cave == START):
                pass
            elif next_cave == END:
                self.paths.append(f'{path},{END}')
            else:
                self.get_paths_part_one(f'{path},{next_cave}')

        return


    def get_paths_part_two(self, path):

        most_recent_cave = path[path.rfind(',') + 1:]

        caves_to_traverse = self.lookup[most_recent_cave]
        for next_cave in caves_to_traverse:

            if next_cave == START:
                pass
            elif next_cave == END:
                self.paths.append(f'{path},{END}')
            elif not self.__ok_to_visit(path, next_cave):
                pass
            else:
                self.get_paths_part_two(f'{path},{next_cave}')

        return

    def __ok_to_visit(self, path, cave):

        visits = np.array([path.count(small_cave) for small_cave in self.small_caves])

        if max(visits) < 2:
            # We haven't visited any small cave more than once
            return True

        elif self.small_caves[int(np.where(visits > 1)[0])] == cave:
            # The cave we've visited more than once is this cave
            return True

        else:
            return False


def process_file(filename):

    with open(filename, 'r') as f:
        data = f.read().rstrip('\n').split('\n')

    connections = []
    for i in range(len(data)):
        connections.append(data[i].split('-'))

    return connections

if __name__ == "__main__":

    filename = "input/test.txt"
    connections = process_file(filename)
    caves = Caves(connections)

    caves.get_paths_part_one('start')
    print(f'The answer to part one is {len(caves.paths)}.')

    caves.get_paths_part_two('start')
    print(f'The answer to part one is {len(caves.paths)}.')

