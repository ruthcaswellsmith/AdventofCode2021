from enum import Enum, auto
import numpy as np

MAX_ENERGY = 10

class Octopi():

    def __init__(self, energy_levels: np.ndarray):

        self.energy_levels = energy_levels
        self.new_energy_levels = energy_levels
        self.size = len(energy_levels)
        self.num_octopi = self.size ** 2
        self.num_flashes = 0
        self.step = 0

    def get_all_flashing_step(self):

        self.new_energy_levels = self.energy_levels
        while (self.new_energy_levels == 0).sum() < self.num_octopi:
            octopi.__one_step()
            octopi.energy_levels = octopi.new_energy_levels.copy()
            self.step += 1

    def take_n_steps(self, n=0):

        for i in range(n):
            octopi.__one_step()
            octopi.energy_levels = octopi.new_energy_levels.copy()

    def __one_step(self):

        self.new_energy_levels = self.energy_levels + 1
        self.flashed = np.zeros((self.size, self.size), dtype=bool)

        while (self.new_energy_levels == self.energy_levels).sum() < self.num_octopi:

            self.energy_levels = self.new_energy_levels.copy()
            self.__process_flashes()
            self.flashed = (self.energy_levels >= MAX_ENERGY)

        self.num_flashes += self.flashed.sum()
        self.new_energy_levels = np.where(self.new_energy_levels >= MAX_ENERGY, 0, self.new_energy_levels)

    def __process_flashes(self):

        self.deltas = np.zeros((self.size, self.size), dtype=int)
        for i in range(self.size):
            for j in range(self.size):
                if self.new_energy_levels[i, j] < MAX_ENERGY:
                    self.deltas[i, j] = self.__count_neighboring_flashes(i, j)
        self.new_energy_levels += self.deltas

    def __count_neighboring_flashes(self, row, col):

        num = 0
        for i in range(max(row - 1, 0), min(row + 1, self.size - 1) + 1):
            for j in range(max(col - 1, 0), min(col + 1, self.size - 1) + 1):
                num += 1 if (self.new_energy_levels[i, j] >= MAX_ENERGY) and not self.flashed[i, j] else 0

        return num

def process_file(filename):

    with open(filename, 'r') as f:
        data = f.read().rstrip('\n').split('\n')

    array = []
    num_rows = len(data)
    for i in range(num_rows):
        array.append([int(c) for c in data[i]])

    return np.array(array)

if __name__ == "__main__":

    filename = "input/Day11.txt"
    initial_energy_levels = process_file(filename)

    octopi = Octopi(initial_energy_levels)
    octopi.take_n_steps(n=100)
    print(f'The answer to part one is {octopi.num_flashes}.')

    octopi = Octopi(initial_energy_levels)
    octopi.get_all_flashing_step()
    print(f'The answer to part two is {octopi.step}.')
