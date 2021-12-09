import numpy as np
from enum import Enum, auto
from typing import List

class Part(str, Enum):

    PART_ONE = auto()
    PART_TWO = auto()

class Directions(str, Enum):

    EAST = auto()
    WEST = auto()
    SOUTH = auto()
    NORTH = auto()

class Point():

    def __init__(self, val, x, y):

        self.val = val
        self.x = x
        self.y = y
        self.diffs = []

class Heightmap():

    def __init__(self, grid: np.ndarray, points: List[Point]):

        self.grid = grid
        self.max_x = self.grid.shape[0] - 1
        self.max_y = self.grid.shape[1] - 1
        self.points = points
        self.low_points = []

    def calc_diffs(self):

        for point in self.points:

            if point.x != 0:
                point.diffs.append(self.grid[point.x - 1, point.y] - point.val)

            if point.x != self.max_x:
                point.diffs.append(self.grid[point.x + 1, point.y] - point.val)

            if point.y != 0:
                point.diffs.append(self.grid[point.x, point.y - 1] - point.val)

            if point.y != self.max_y:
                point.diffs.append(self.grid[point.x, point.y + 1] - point.val)

    def identify_low_points(self):

        for point in self.points:
            diffs = np.array(point.diffs)
            if len(diffs) == len(diffs[np.where(diffs > 0)]):
                self.low_points.append(point)

    def get_answer(self, part: Part):

        if part == part.PART_ONE:

            answer = 0
            for point in self.low_points:

                answer += 1 + point.val

            return answer

    def identify_basins(self):

        basin_numbers = []
        for point in self.low_points:

            basin = np.zeros((self.max_x + 1, self.max_y + 1), dtype=bool)

            self.__travel_grid(point.x, point.y, basin)

            basin_numbers.append(basin[basin].sum())

        basin_numbers.sort()
        return basin_numbers


    def __travel_grid(self, x, y, basin):

        # We're here so we're in the basin
        basin[x, y] = True
        current_val = self.grid[x, y]

        # Check to the east
        if (x < self.max_x):
            next_x, next_y = x + 1, y
            if (self.grid[next_x, next_y] != 9) and (self.grid[next_x, next_y] > current_val):
                self.__travel_grid(next_x, next_y, basin)

        # Check to the west
        if (x > 0):
            next_x, next_y = x - 1, y
            if (self.grid[next_x, next_y] != 9) and (self.grid[next_x, next_y] > current_val):
                self.__travel_grid(next_x, next_y, basin)

        # Check to the north
        if (y < self.max_y):
            next_x, next_y = x, y + 1
            if (self.grid[next_x, next_y] != 9) and (self.grid[next_x, next_y] > current_val):
                self.__travel_grid(next_x, next_y, basin)

        # Check to the south
        if (y > 0):
            next_x, next_y = x, y - 1
            if (self.grid[next_x, next_y] != 9) and (self.grid[next_x, next_y] > current_val):
                self.__travel_grid(next_x, next_y, basin)

def process_file(filename):

    with open(filename, 'r') as f:
        data = f.read().rstrip('\n').split('\n')

    max_x = len(data)
    max_y = len(data[0])

    points = []
    grid = np.zeros((max_x, max_y))
    for x, line in enumerate(data):
        for y, c in enumerate(line):
            val = int(c)
            points.append(Point(val, x, y))
            grid[x, y] = val

    return Heightmap(grid, points)

if __name__ == "__main__":

    filename = "input/Day9.txt"
    heightmap = process_file(filename)

    heightmap.calc_diffs()
    heightmap.identify_low_points()

    answer = heightmap.get_answer(part=Part.PART_ONE)
    print(f'The answer to part one is {answer}.')

    basin_numbers = heightmap.identify_basins()
    answer = np.array(basin_numbers[-3:]).prod()
    print(f'The answer to part two is {answer}.')

