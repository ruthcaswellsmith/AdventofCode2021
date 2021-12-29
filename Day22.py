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

    def __init__(self, range: str, offset):
        self.start = int(range[range.index('=')+1: range.index("..")]) + offset
        self.end = int(range[range.index('..') + 2:]) + offset


class Instruction:

    def __init__(self, instruction: str, part: Part):
        offset = OFFSET if part == part.PART_ONE else 0

        self.action, ranges = instruction.split(' ')
        for i, range in enumerate(ranges.split(',')):
            if i == 0:
                self.x = Range(range, offset)
            elif i == 1:
                self.y = Range(range, offset)
            else:
                self.z = Range(range, offset)

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

        self.instructions = []
        while instructions:
            self.instructions.append(Instruction(instructions[0], part=part))
            instructions = instructions[1:]
        self.on = 0

    def update_grid(self, step):

        fn = np.ones if step.action == Action.ON else np.zeros
        prism_shape = (step.x.end - step.x.start + 1, step.y.end - step.y.start + 1, step.z.end - step.z.start + 1)
        self.grid[step.x.start: step.x.end + 1, step.y.start: step.y.end + 1, step.z.start: step.z.end + 1] = \
            fn(prism_shape)
        self.on = np.sum(self.grid)

    def process_instructions(self, part: Part):

        if part == Part.PART_ONE:
           for step in self.instructions:
                if step.is_initialization(part):
                    self.update_grid(step)
        else:
            for i, step  in enumerate(self.instructions):
                self.__process_step(step, self.instructions[:i])

    def __process_step(self, current, previous):

        print('processing step', current.action, current.x, current.y, current.z)
        net_effect = 0
        for x in range(current.x.start, current.x.end + 1):
            for y in range(current.y.start, current.y.end + 1):
                for z in range(current.z.start, current.z.end + 1):
                    net_effect += self.__get_net_effect(x, y, z, current.action, previous)
 #                   print(x, y, x, net_effect)
        self.on += net_effect

    def __get_net_effect(self, x, y, z, current_action, previous):

        for step in reversed(previous):
            if self.__cube_in_step(x, y, z, step):
                if step.action == Action.ON:
                    return 0 if current_action == Action.ON else -1
                if step.action == Action.OFF:
                    return 1 if current_action == Action.ON else 0
        return 1 if current_action == Action.ON else 0

    @staticmethod
    def __cube_in_step(x, y, z, step):
        return True if x in range(step.x.start, step.x.end + 1) and\
                y in range(step.y.start, step.y.end + 1) and\
                z in range(step.z.start, step.z.end + 1) else False

def process_file(filename):

    with open(filename, 'r') as f:
        data = f.read().rstrip('\n').split('\n')

    return data

if __name__ == "__main__":

    filename = 'input/test22-3.txt'
    instructions = process_file(filename)
    core = Core(instructions, part=Part.PART_ONE)
    core.process_instructions(part=Part.PART_ONE)
    print(f'The answer to part one is {core.on}.')

    core = Core(instructions, part=Part.PART_TWO)
    core.process_instructions(part=Part.PART_TWO)
    print(f'The answer to part two is {core.on}.')
