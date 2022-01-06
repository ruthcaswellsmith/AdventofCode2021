from enum import Enum, auto
from typing import List, Dict
import numpy as np
import pandas as pd
import random


class Cuke(str, Enum):
    EAST_MOVING = ">"
    SOUTH_MOVING = "v"


class Direction(str, Enum):
    NORTH = auto()
    SOUTH= auto()
    EAST = auto()
    WEST = auto()

class Herd:

    def __init__(self, df: pd.DataFrame):

        self.df = df
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
            shifted = self.__shift_df(self.df, Direction.WEST)
            shifted.columns = self.df.columns
        else:
            shifted = self.__shift_df(self.df, Direction.NORTH)
            shifted.reset_index(inplace=True, drop=True)
        moving = (self.df == type) & (shifted == '.')

        if type == Cuke.EAST_MOVING:
            moving_shifted = self.__shift_df(moving, Direction.EAST)
            moving_shifted.columns = shifted.columns
        else:
            moving_shifted = self.__shift_df(moving, Direction.SOUTH)
            moving_shifted.reset_index(inplace=True, drop=True)

        self.df[moving] = '.'
        self.df[moving_shifted] = Cuke.EAST_MOVING.value if type == Cuke.EAST_MOVING else Cuke.SOUTH_MOVING.value

        return moving.sum().sum()

    @staticmethod
    def __shift_df(df, direction=Direction):

        if direction == Direction.WEST:
            shifted = pd.concat([pd.DataFrame(df.iloc[:, 1:df.shape[1]]), df.iloc[:, 0]], axis=1)
        elif direction == Direction.EAST:
            shifted = pd.concat([pd.DataFrame(df.iloc[:, df.shape[1] - 1]), df.iloc[:, 0:df.shape[1] - 1]], axis=1)
        elif direction == Direction.NORTH:
            shifted = pd.concat([df.iloc[1:df.shape[0], :], pd.DataFrame(df.iloc[0, :]).T], axis=0)
        else:
            shifted = pd.concat([pd.DataFrame(df.iloc[df.shape[0] - 1, :]).T, df.iloc[0:df.shape[0] - 1, :], ], axis=0)

        return shifted


def read_file(filename):

    with open(filename, 'r') as f:
        data = f.read().rstrip('\n').split('\n')

    rows = []
    while data:

        rows.append(list(data[0]))
        data = data[1:]

    df = pd.DataFrame(rows)
    df.columns = ['Col' + str(i) for i in range(len(df.columns))]
    return df


if __name__ == "__main__":

    filename = 'input/test25.txt'

    herd = Herd(read_file(filename))
    herd.move_until_done()
    print(f'The answer to part one is {herd.steps}')
