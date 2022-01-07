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

if __name__ == "__main__":

    filename = "input/Day15.txt"
    grid = Grid(process_file(filename))
    grid.get_shortest_path()
    print(f'The answer to Part One is {grid.distances[grid.x_max, grid.y_max]}.')
