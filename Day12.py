from enum import Enum, auto
import numpy as np
from typing import List

class Caves():

    def __init__(self, connections: List):

        self.connections = connections
        self.lookup = {}

        for connection in self.connections:

            self.__add_connection(connection[0], connection[1])
            self.__add_connection(connection[1], connection[0])

        self.paths = []

    def __add_connection(self, a, b):

        if a in self.lookup:
            self.lookup[a].append(b)
        else:
            self.lookup[a] = [b]

    def get_paths(self, path):

        most_recent_cave = path[path.rfind(',') + 1:]

        root_path = path
        for next_cave in self.lookup[most_recent_cave]:

            path = root_path
            if (next_cave.islower() and next_cave in path) or (next_cave == 'start'):
                return 'bad_path'
            if next_cave == 'end':
                return f'{path},end'
            else:
                while not ('end' in path or path == 'bad_path'):
                    path = self.get_paths(f'{path},{next_cave}')
                if 'end' in path:
                    self.paths.append(path)


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

    caves.get_paths('start')
    print('hi')

    # initial_energy_levels = process_file(filename)
    #
    # octopi = Octopi(initial_energy_levels)
    # octopi.take_n_steps(n=100)
    # print(f'The answer to part one is {octopi.num_flashes}.')
    #
    # octopi = Octopi(initial_energy_levels)
    # octopi.get_all_flashing_step()
    # print(f'The answer to part two is {octopi.step}.')
