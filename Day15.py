from enum import Enum, auto
import numpy as np

class Part(str, Enum):
    PART_ONE = auto()
    PART_TWO = auto()

LARGE = 1_000_000

class Grid():

    def __init__(self, grid: np.ndarray):

        self.grid = grid
        self.x_min, self.y_min = 0, 0
        self.x_max, self.y_max = grid.shape[0] - 1, grid.shape[1] - 1
        self.visited = np.zeros(grid.shape, dtype=bool)
        self.distances = LARGE * np.ones(grid.shape, dtype=int)
        self.distances[0, 0] = 0
        self.current = (0, 0)
        self.unvisited_neighbors = []

    def get_shortest_path(self):

        done = False
        while not done:

            self.__get_unvisited_neighbors()
            self.__update_neighbors_distance()
            self.visited[self.current[0], self.current[1]] = True
            if not self.visited[self.x_max, self.y_max]:
               self.__update_current()
            else:
                done = True

    def __get_unvisited_neighbors(self):

        self.unvisited_neighbors = []
        x, y = self.current[0], self.current[1]
        if x > self.x_min and not self.visited[x - 1, y]:
            self.unvisited_neighbors.append((x - 1, y))
        if x < self.x_max and not self.visited[x + 1, y]:
            self.unvisited_neighbors.append((x + 1, y))
        if y > self.y_min and not self.visited[x, y - 1]:
            self.unvisited_neighbors.append((x, y - 1))
        if y < self.y_max and not self.visited[x, y + 1]:
            self.unvisited_neighbors.append((x, y + 1))

    def __update_neighbors_distance(self):

        for neighbor in self.unvisited_neighbors:
            x, y = neighbor[0], neighbor[1]
            self.distances[x, y] = min(self.distances[x, y], self.distances[self.current[0], self.current[1]] + self.grid[x, y])

    def __update_current(self):

        min_distance = np.min(self.distances[~self.visited])
        min_locations = np.logical_and(self.distances == min_distance, ~self.visited)
        self.current = (np.where(min_locations)[0][0], np.where(min_locations)[1][0])

def process_file(filename):

    with open(filename, 'r') as f:
        data = f.read().rstrip('\n').split('\n')

    grid = []
    for row in data:
        grid.append([int(c) for c in row])
    grid = np.array(grid)

    return grid

def add_num(element, i):
    return element + i if element + i < 10 else (element + i) % 9

add_one_vectorized = np.vectorize(add_num)

def create_grid_p2(grid_p1):

    rows, cols = grid_p1.shape
    grid_p2 = np.zeros((5*rows, 5*cols), dtype=int)
    for i in range(5):
        starting_grid = add_one_vectorized(grid_p1, i * 1)
        for j in range(5):
            grid_p2[i*rows: (i+1)*rows, j*cols: (j+1)*cols] = add_one_vectorized(starting_grid, j * 1)
    return grid_p2


if __name__ == "__main__":

    filename = "input/Day15.txt"
    grid_p1 = process_file(filename)
    grid1 = Grid(grid_p1)
    grid1.get_shortest_path()
    print(f'The answer to Part One is {grid1.distances[grid1.x_max, grid1.y_max]}.')

    grid_p2 = create_grid_p2(grid_p1)
    grid2 = Grid(grid_p2)
    grid2.get_shortest_path()
    print(f'The answer to Part Two is {grid2.distances[grid2.x_max, grid2.y_max]}.')
