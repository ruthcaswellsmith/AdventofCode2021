import string
from enum import Enum, auto
import numpy as np
from typing import List

class Part(str, Enum):
    PART_ONE = auto()
    PART_TWO = auto()

class Grid():

    def __init__(self, grid: np.ndarray):

        self.grid = grid
        self.x_max = grid.shape[0] - 1
        self.y_max = grid.shape[1] - 1
        self.min_points = 9 * self.x_max + 9 * self.y_max
        self.min_paths = []

    def travel(self, x, y, path, points):

        points += self.grid[x, y]
        path.append([x, y])
        if x == self.x_max and y == self.y_max:
            if points < self.min_points:
                print(f'New minimum with {points} points.')
                self.min_points = points
                self.min_paths.append(path)
            return

        if points > self.min_points:
            return

        if x != self.x_max:
            self.travel(x + 1, y, path, points)

        if y != self.y_max:
            self.travel(x, y + 1, path, points)


def process_file(filename):

    with open(filename, 'r') as f:
        data = f.read().rstrip('\n').split('\n')

    grid = []
    for row in data:
        grid.append([int(c) for c in row])
    grid = np.array(grid)

    return grid

if __name__ == "__main__":

    filename = "input/Day15.txt"
    grid = Grid(process_file(filename))

    grid.travel(0, 0, [], -grid.grid[0,0])
    print(f'The answer is {grid.min_points}.')
