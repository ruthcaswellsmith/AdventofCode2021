from enum import Enum, auto

import numpy as np

SIZE = 200
OFFSET = 51
MIN_INIT = -50
MAX_INIT = 50

class Action(str, Enum):
    ON = "on"
    OFF = "off"


class Range:

    def __init__(self, range: str):
        self.start = int(range[range.index('=')+1: range.index("..")]) + OFFSET
        self.end = int(range[range.index('..') + 2:]) + OFFSET


class Instruction:

    def __init__(self, action: Action, ranges: str):
        self.action = action
        for i, range in enumerate(ranges.split(',')):
            if i == 0:
                self.x = Range(range)
            elif i == 1:
                self.y = Range(range)
            else:
                self.z = Range(range)

    def is_initialization(self):

        for range in [self.x, self.y, self.z]:
            if range.start < MIN_INIT + OFFSET or range.end > MAX_INIT + OFFSET:
                return False
        return True

class Core:

    def __init__(self, instructions):
        self.grid = np.zeros((SIZE, SIZE, SIZE), dtype = bool)
        self.instructions = instructions

    def process_instructions(self):

        for step in self.instructions:
            if step.is_initialization():
                self.update_grid(step)

    def update_grid(self, step):

        fn = np.ones if step.action == Action.ON else np.zeros
        prism_shape = (step.x.end - step.x.start + 1, step.y.end - step.y.start + 1, step.z.end - step.z.start + 1)
        try:
            self.grid[step.x.start: step.x.end + 1, step.y.start: step.y.end + 1, step.z.start: step.z.end + 1] = \
                fn(prism_shape)
        except:
            print('hi')

def process_file(filename):

    with open(filename, 'r') as f:
        data = f.read().rstrip('\n').split('\n')

    instructions = []
    while data:
        action, ranges = data[0].split(' ')
        instructions.append(Instruction(action, ranges))
        data = data[1:]

    return instructions

if __name__ == "__main__":

    filename = 'input/Day22.txt'
    instructions = process_file(filename)
    core = Core(instructions)
    core.process_instructions()
    print(np.sum(core.grid))
    print('hi')
