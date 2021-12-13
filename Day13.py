from enum import Enum, auto
import numpy as np
from typing import List

class FoldType(str, Enum):

    HORIZONTAL = auto()
    VERTICAL = auto()

class Fold():

    def __init__(self, fold_type: FoldType, position: int):

        self.type = fold_type
        self.position = position

class Paper():

    def __init__(self, points: List[List], folds: List[Fold]):

        self.folds = folds

        max_x, max_y = 0, 0
        for point in points:
            max_x = max(max_x, point[0])
            max_y = max(max_y, point[1])

        self.grid = np.zeros((max_x + 1, max_y + 1), dtype=bool)
        for point in points:
            self.grid[point[0], point[1]] = True

    def execute_folds(self, n=1):

        for i in range(n):
            self.__fold_paper(self.folds[i])

    def rotate_grid(self):

        # This rotates our grid so we can read it
        self.grid = np.flipud(self.grid)
        for i in range(3):
            self.grid = np.rot90(self.grid)

    def __fold_paper(self, fold: Fold):

        if fold.type == FoldType.HORIZONTAL:
            self.grid1 = self.grid[0:fold.position, :]
            self.grid2 = np.flipud(self.grid[fold.position + 1:, :])
        else:
            self.grid1 = self.grid[:, 0:fold.position]
            self.grid2 = np.fliplr(self.grid[:, fold.position + 1:])

        self.grid = np.logical_or(self.grid1, self.grid2)

def process_file(filename):

    with open(filename, 'r') as f:
        data = f.read().rstrip('\n').split('\n')

    points = []
    i=0
    while data[i]:
        points.append([
            int(data[i].split(",")[0]),
            int(data[i].split(",")[1])])
        i += 1

    data = data[i+1:]
    folds = []
    for i in range(len(data)):
        fold = data[i].split('=')
        fold_type = FoldType.HORIZONTAL if fold[0][-1] == 'x' else FoldType.VERTICAL
        position = int(fold[1])
        folds.append(Fold(fold_type, position))

    return points, folds

if __name__ == "__main__":

    filename = "input/Day13.txt"
    points, folds = process_file(filename)

    paper = Paper(points, folds)
    paper.execute_folds(n=1)

    print(f'The answer to part one is {np.sum(paper.grid)}.')

    paper = Paper(points, folds)
    paper.execute_folds(n=len(paper.folds))
    paper.rotate_grid()
    # Put a breakpoint here so we can read the code!
    print(paper.grid)

