import numpy as np
from typing import List
import time


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

    def identify_basins(self, type='recursive'):

        basin_numbers = []
        for point in self.low_points:

            basin = np.zeros((self.max_x + 1, self.max_y + 1), dtype=bool)

            if type == 'recursive':
                self.__travel_grid(point.x, point.y, basin)
            else:
                self.__travel_grid_iteratively(point.x, point.y, basin)

            basin_numbers.append(basin[basin].sum())

        basin_numbers.sort()
        return basin_numbers

    def __travel_grid_iteratively(self, x, y, basin):

        # We save our starting position and start our stacks
        x_start, y_start = x, y
        locations = [[x_start, y_start]]
        directions = [np.zeros(4, dtype=bool)]

        while (locations[-1][0] != x_start) or (locations[-1][1] != y_start) or (directions[-1].sum() < 4):

            x, y = locations[-1][0], locations[-1][1]

            # Add the current point to the basin
            basin[x, y] = True
            current_val = self.grid[x, y]

            if directions[-1].sum() == 0:
                directions[-1][0] = True
                if x < self.max_x:
                    next_x, next_y = x + 1, y
                    if self.__move_on(next_x, next_y, current_val):
                        locations.append([next_x, next_y])
                        directions.append(np.zeros(4, dtype=bool))

            elif directions[-1].sum() == 1:
                directions[-1][1] = True
                if x > 0:
                    next_x, next_y = x - 1, y
                    if self.__move_on(next_x, next_y, current_val):
                        locations.append([next_x, next_y])
                        directions.append(np.zeros(4, dtype=bool))

            elif directions[-1].sum() == 2:
                directions[-1][2] = True
                if y < self.max_y:
                    next_x, next_y = x, y + 1
                    if self.__move_on(next_x, next_y, current_val):
                        locations.append([next_x, next_y])
                        directions.append(np.zeros(4, dtype=bool))

            elif directions[-1].sum() == 3:
                directions[-1][3] = True
                if y > 0:
                    next_x, next_y = x, y - 1
                    if self.__move_on(next_x, next_y, current_val):
                        locations.append([next_x, next_y])
                        directions.append(np.zeros(4, dtype=bool))

            else:

                # we're done with this point, get rid of it.
                directions.pop()
                locations.pop()

    def __travel_grid(self, x, y, basin):

        # We're here so we're in the basin
        basin[x, y] = True
        current_val = self.grid[x, y]

        if x < self.max_x:
            next_x, next_y = x + 1, y
            if self.__move_on(next_x, next_y, current_val):
                self.__travel_grid(next_x, next_y, basin)

        if x > 0:
            next_x, next_y = x - 1, y
            if self.__move_on(next_x, next_y, current_val):
                self.__travel_grid(next_x, next_y, basin)

        if y < self.max_y:
            next_x, next_y = x, y + 1
            if self.__move_on(next_x, next_y, current_val):
                self.__travel_grid(next_x, next_y, basin)

        if y > 0:
            next_x, next_y = x, y - 1
            if self.__move_on(next_x, next_y, current_val):
                self.__travel_grid(next_x, next_y, basin)


    def __move_on(self, x, y, val):

        return (self.grid[x, y] != 9) and (self.grid[x, y] > val)


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

    # The answer is the sum of 1 + height all low points
    answer = sum([1 + point.val for point in heightmap.low_points])
    print(f'The answer to part one is {answer}.')

    # type = iterative/recursive
    start = time.time()
    basin_numbers = heightmap.identify_basins(type='iterative')
    end = time.time()
    print(end - start)

    # The answer is the product of the number of points in the three largest basins
    answer = np.array(basin_numbers[-3:]).prod()
    print(f'The answer to part two is {answer}.')

