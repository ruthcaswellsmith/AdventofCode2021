from enum import Enum, auto
from typing import List, Dict
import numpy as np
import pandas as pd
import random


class Cuke(int, Enum):
    EAST_MOVING = 1
    SOUTH_MOVING = 2


class Direction(str, Enum):
    NORTH = auto()
    SOUTH= auto()
    EAST = auto()
    WEST = auto()

class Herd:

    def __init__(self, array: np.ndarray):

        self.array = array
        self.steps = 0
        self.moving = 1000

    def move_until_done(self):

        while self.moving > 0:
            self.moving = self.__take_step()
            self.steps += 1

    def __take_step(self):

        moving_counts = {}
        for type in [Cuke.EAST_MOVING, Cuke.SOUTH_MOVING]:

            moving_counts[type] = self.__move(type=type)

        return sum(list(moving_counts.values()))

    def __move(self, type: Cuke):

        if type == Cuke.EAST_MOVING:
            shifted = self.__shift_array(self.array, Direction.WEST)
        else:
            shifted = self.__shift_array(self.array, Direction.NORTH)

        moving = (self.array == type) & (shifted == 0)

        if type == Cuke.EAST_MOVING:
            moving_shifted = self.__shift_array(moving, Direction.EAST)
        else:
            moving_shifted = self.__shift_array(moving, Direction.SOUTH)

        self.array[moving] = 0
        self.array[moving_shifted] = Cuke.EAST_MOVING.value if type == Cuke.EAST_MOVING else Cuke.SOUTH_MOVING.value

        return np.sum(moving)

    @staticmethod
    def __shift_array(array, direction=Direction):

        if direction == Direction.WEST:
            shifted = np.concatenate((array[:, 1:array.shape[1]], array[:, 0][:, None]), axis=1)
        elif direction == Direction.EAST:
            shifted = np.concatenate((array[:, array.shape[1]-1][:, None], array[:, 0:array.shape[1]-1]), axis=1)
        elif direction == Direction.NORTH:
            shifted = np.concatenate((array[1:array.shape[0], :], array[0, :][None, :]), axis=0)
        else:
            shifted = np.concatenate((array[array.shape[0]-1,:][None, :], array[:array.shape[0] - 1, :]), axis=0)

        return shifted


def read_file(filename):

    with open(filename, 'r') as f:
        data = f.read().rstrip('\n').split('\n')

    rows = []
    while data:

        rows.append([0 if c == '.' else 1 if c == '>' else 2 for c in data[0]])
        data = data[1:]

    array = np.array(rows)
    return array

if __name__ == "__main__":

    filename = 'input/test25.txt'

    herd = Herd(read_file(filename))
    herd.move_until_done()
    print(f'The answer to part one is {herd.steps}')
