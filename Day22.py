from enum import Enum, auto

import numpy as np

SIZE = 199
OFFSET = 51
MIN_INIT = -50
MAX_INIT = 50

class Part(str, Enum):
    PART_ONE = auto()
    PART_TWO = auto()

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

    def is_initialization(self, part: Part):

        if part == Part.PART_ONE:
            for range in [self.x, self.y, self.z]:
                if range.start < MIN_INIT + OFFSET or range.end > MAX_INIT + OFFSET:
                    return False
        return True

class Core:

    def __init__(self, instructions, part: Part):
        if part == Part.PART_ONE:
            self.grid = np.zeros((SIZE, SIZE, SIZE), dtype = bool)
        self.instructions = instructions
        self.count = 0

    def process_instructions(self, part: Part):

        if part == Part.PART_ONE:
           for step in self.instructions:
                if step.is_initialization(part):
                    self.update_grid(step)
        else:
            for i, step  in enumerate(instructions):
                self.__get_net_effect(step, instructions[:i-1])

    def __get_net_effect(self, current, previous):

        current_size = self.__get_number_of_cubes(step)
        current_action = current.action
        for step in previous:
            previous_size = self.__get_number_of_cubes(previous)
            previous_action = previous.action
            self.__get_intersection(current, step)
            if current_action == Action.ON and previous_action == Action.ON:
                net_effect = current_size - previous_size

    def __get_intersection(self, current, step):

        intersection = 0
        for x in range(current.x.start, current.x.end):
            for y in range(current.y.start, current.y.end):
                for z in range(current.z.start, current.z.end):
                    if self.__cube_in_step(x, y, z, step):
                        intersection += 1

    @staticmethod
    def __get_number_of_cubes(self, step):
        return (step.x.end - step.x.start + 1) * (step.y.end - step.y.start + 1) * (step.z.end - step.z.start + 1)

    @staticmethod
    def __cube_in_step(x, y, z, step):
        return True if x in range(step.x.start, step.x.end) and\
                y in range(step.y.start, step.y.end) and\
                z in range(step.z.start, step.z.end) \
            else False


    def update_count(self, step):


    def update_grid(self, step):

        fn = np.ones if step.action == Action.ON else np.zeros
        prism_shape = (step.x.end - step.x.start + 1, step.y.end - step.y.start + 1, step.z.end - step.z.start + 1)
        self.grid[step.x.start: step.x.end + 1, step.y.start: step.y.end + 1, step.z.start: step.z.end + 1] = \
            fn(prism_shape)
        self.count = np.sum(self.grid)

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
    core = Core(instructions, part=Part.PART_ONE)
    core.process_instructions(part=Part.PART_ONE)
    print(f'The answer to part one is {core.count}.')

    core = Core(instructions, part=Part.PART_TWO)
    core.process_instructions(part=Part.PART_TWO)
    print(f'The answer to part one is {core.count}.')
