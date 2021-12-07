import numpy as np
from enum import Enum, auto

class PART(str, Enum):

    PART_ONE = auto()
    PART_TWO = auto()

class Crabs():

    def __init__(self, positions: np.ndarray):

        self.positions = positions
        self.num_crabs = len(self.positions)

    def get_best_position(self, part: PART):

        fuels = []
        for i in range(len(self.positions) + 1):
            fuels.append(self.__calculate_fuel(i, part))

        return min(fuels)

    def __calculate_fuel(self, target: int, part: PART):

        diffs = abs(self.positions - target * np.ones(self.num_crabs, dtype=int))
        return sum(np.vectorize(self.__fuel_cost)(diffs, part))

    @staticmethod
    def __fuel_cost(n, part: PART):

        if part == PART.PART_ONE:
            return n
        else:
            return int(n * (n+1) / 2)

def process_file(filename):

    positions = np.loadtxt(filename, dtype=int, delimiter=',')

    return positions

if __name__ == "__main__":

    filename = "input/Day7.txt"
    positions = process_file(filename)

    crabs = Crabs(positions)

    fuel = crabs.get_best_position(PART.PART_ONE)
    print(f'P1: They must spend {fuel} fuel to get to the best position.')

    fuel = crabs.get_best_position(PART.PART_TWO)
    print(f'P2: They must spend {fuel} fuel to get to the best position.')