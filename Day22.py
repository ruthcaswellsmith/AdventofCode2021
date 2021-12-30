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
        self.start = int(range[range.index('=') + 1: range.index("..")]) + offset
        self.end = int(range[range.index('..') + 2:]) + offset

class Prism:

    def __init__(self, ranges):
        self.x, self.y, self.z = [range for range in ranges]

class Instruction:

    def __init__(self, instruction: str, part: Part):
        offset = OFFSET if part == part.PART_ONE else 0
        self.action, ranges = instruction.split(' ')
        prism_ranges = [Range(range, offset) for range in ranges.split(',')]
        self.prism = Prism(prism_ranges)

    def is_initialization(self, part: Part):

        if part == Part.PART_ONE:
            for range in [self.prism.x, self.prism.y, self.prism.z]:
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
        self.prisms = []
        self.on = 0

    def update_grid(self, step):

        fn = np.ones if step.action == Action.ON else np.zeros
        prism_shape = (step.prism.x.end - step.prism.x.start + 1,
                       step.prism.y.end - step.prism.y.start + 1,
                       step.prism.z.end - step.prism.z.start + 1)
        self.grid[step.prism.x.start:step.prism.x.end + 1,
                step.prism.y.start:step.prism.z.end + 1,
                step.prism.z.start:step.prism.z.end + 1] = fn(prism_shape)
        self.on = np.sum(self.grid)

    def process_instructions(self, part: Part):

        if part == Part.PART_ONE:
            for step in self.instructions:
                if step.is_initialization(part):
                    self.update_grid(step)
        else:
            for i, step  in enumerate(self.instructions):
                self.__process_step(step)

    def __process_step(self, step):

        intersections = []
        for prism in self.prisms:
            intersections.append(self.__get_intersection(step.prism, prism))
        # if len(intersections)>1:
        #     print('oops')
        for intersection in intersections:
            if step.action == Action.ON:
                new_prisms = self.__remove_intersection(step.prism, intersection)
            # else:
            #     new_prisms = self.__remove_intersection(prism, intersection)
        self.prisms.extend(new_prisms)

    @staticmethod
    def __remove_intersection(prism, intersection):

        new_prisms = []
        if intersection.y.start > prism.y.start:
            ranges = [f'{prism.x.start}..{prism.x.end}', f'{prism.y.start}..{intersection.y.start}', f'{prism.z.start}..{prism.z.end}']
            new_prisms.append(Prism(ranges))
        if prism.y.end > intersection.y.end:
            ranges = [f'{prism.x.start}..{prism.x.end}', f'{intersection.y.end}..{prism.y.end}', f'{prism.z.start}..{prism.z.end}']
            new_prisms.append(Prism(ranges))
        if intersection.z.start > prism.z.start:
            ranges = [f'{prism.x.start}..{prism.x.end}', f'{intersection.y.start}..{intersection.y.end}', f'{prism.z.start}..{intersection.z.start}']
            new_prisms.append(Prism(ranges))
        if prism.z.end > intersection.z.end:
            ranges = [f'{prism.x.start}..{prism.x.end}', f'{intersection.y.start}..{intersection.y.end}', f'{intersection.z.end}..{prism.z.end}']
            new_prisms.append(Prism(ranges))
        if intersection.x.start > prism.x.start:
            ranges = [f'{prism.x.start}..{intersection.x.start}', f'{intersection.y.start}..{intersection.y.end}', f'{intersection.z.start}..{intersection.z.end}']
            new_prisms.append(Prism(ranges))
        if prism.x.end > intersection.x.end:
            ranges = [f'{intersection.x.end}..{prism.x.end}', f'{intersection.y.start}..{intersection.y.end}', f'{intersection.z.start}..{intersection.z.end}']
            new_prisms.append(Prism(ranges))
        return new_prisms

    def __get_intersection(self, prism1, prism2):

        x_start, x_end = self.__get_intersection_point(prism1.x.start, prism1.x.end, prism2.x.start, prism2.x.end)
        if x_start and x_end:
            y_start, y_end = self.__get_intersection_point(prism1.y.start, prism1.y.end, prism2.y.start, prism2.y.end)
            z_start, z_end = self.__get_intersection_point(prism1.z.start, prism1.z.end, prism2.z.start, prism2.z.end)
            ranges = [f'{x_start}..{x_end}', f'{y_start}..{y_end}', f'{z_start}..{z_end}']
            return Prism(ranges)

    @staticmethod
    def __get_intersection_point(p1_start, p1_end, p2_start, p2_end):

        if p1_start in range(p2_start, p2_end + 1):
            start = p1_start
        elif p2_start in range(p1_start, p1_end + 1):
            start = p2_start
        else:
            return None

        if p1_end in range(p2_start, p2_end + 1):
            end = p1_end
        elif p2_end in range(p1_start, p1_end + 1):
            end = p2_end
        else:
            end = None

        return start, end

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

    filename = 'input/test22-1.txt'
    instructions = process_file(filename)
    core = Core(instructions, part=Part.PART_ONE)
    core.process_instructions(part=Part.PART_ONE)
    print(f'The answer to part one is {core.on}.')

    core = Core(instructions, part=Part.PART_TWO)
    core.process_instructions(part=Part.PART_TWO)
    # print(f'The answer to part two is {core.on}.')
