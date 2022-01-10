from enum import Enum, auto
from typing import List

MAX = 50

class Part(str, Enum):
    PART_ONE = auto()
    PART_TWO = auto()

class Action(str, Enum):
    ON = "on"
    OFF = "off"


class Range:

    def __init__(self, start, end):
        self.start = start
        self.end = end

    def count_lights(self):
        return self.end - self.start + 1


class Prism:

    def __init__(self, xrange: Range, yrange: Range, zrange: Range):
        self.x = xrange
        self.y = yrange
        self.z = zrange

    def count_lights(self):
        return self.x.count_lights() * self.y.count_lights() * self.z.count_lights()


class Instruction:

    def __init__(self, action: Action, xrange: Range, yrange: Range, zrange: Range):
        self.action = action
        self.prism = Prism(xrange, yrange, zrange)

    def is_initialization(self, part: Part):

        if part == Part.PART_ONE:
            for xyz in [self.prism.x, self.prism.y, self.prism.z]:
                if xyz.start < -MAX or xyz.end > MAX:
                    return False
        return True

class Core:

    def __init__(self, instructions: List[Instruction]):
        self.instructions = instructions
        self.prisms = []
        self.lights = 0

    def process_instructions(self, part: Part):

        for ind, step in enumerate(self.instructions):
            if step.is_initialization(part) and step.action == Action.ON:
                remaining = [] if ind == len(self.instructions) else self.instructions[ind+1:]
                self.prisms.extend(self.__process_step(step, remaining))

    def __process_step(self, step, remaining):

        outersections = [step.prism]
        while remaining:
            ind = 0
            while ind < len(outersections):
                new = self.__get_outersection(outersections[ind], remaining[0].prism)
                outersections = outersections[:ind] + new + outersections[ind+1:]
                ind = ind + len(new)
            remaining = remaining[1:]

        return outersections

    def print_prisms(self):
        for prism in self.prisms:
            print(prism.x.start, prism.x.end, prism.y.start, prism.y.end, prism.z.start, prism.z.end)

    def count_lights(self):

        for prism in self.prisms:
            self.lights += prism.count_lights()

    @staticmethod
    def __get_outersection(prism1, prism2):

        # We can have as many as six prisms
        prisms = []

        # If we have no overlap between x, y, or z, then return all of prism1
        if (max(prism1.x.start, prism2.x.start) > min(prism1.x.end, prism2.x.end)) or \
                (max(prism1.y.start, prism2.y.start) > min(prism1.y.end, prism2.y.end)) or \
                (max(prism1.z.start, prism2.z.start) > min(prism1.z.end, prism2.z.end)):
            return [prism1]

        # First do all x
        rx = Range(prism1.x.start, prism1.x.end)

        # Combine with all y, outersections of z
        ry = Range(prism1.y.start, prism1.y.end)
        if prism1.z.start < prism2.z.start:
            rza = Range(prism1.z.start, prism2.z.start - 1)
            prisms.append(Prism(rx, ry, rza))
        if prism2.z.end < prism1.z.end:
            rzb = Range(prism2.z.end + 1, prism1.z.end)
            prisms.append(Prism(rx, ry, rzb))

        # get intersection of z
        rz = Range(max(prism1.z.start, prism2.z.start), min(prism1.z.end, prism2.z.end))

        # Combine it with all x and outersection of y
        if prism1.y.start < prism2.y.start:
            rya = Range(prism1.y.start, prism2.y.start - 1)
            prisms.append(Prism(rx, rya, rz))
        if prism2.y.end < prism1.y.end:
            ryb = Range(prism2.y.end + 1, prism1.y.end)
            prisms.append(Prism(rx, ryb, rz))

        # Combine with intersection of y and outersection of x
        ry = Range(max(prism1.y.start, prism2.y.start), min(prism1.y.end, prism2.y.end))
        if prism1.x.start < prism2.x.start <= prism1.x.end:
            rxa = Range(prism1.x.start, prism2.x.start - 1)
            prisms.append(Prism(rxa, ry, rz))
        if prism1.x.start <= prism2.x.end < prism1.x.end:
            rxb = Range(prism2.x.end + 1, prism1.x.end)
            prisms.append(Prism(rxb, ry, rz))

        return prisms


def process_file(filename):

    with open(filename, 'r') as f:
        data = f.read().rstrip('\n').split('\n')

    instructions = []
    while data:
        starts, ends = [], []
        action, ranges = data[0].split(' ')
        for xyz in ranges.split(','):
            starts.append(int(xyz[xyz.index('=') + 1: xyz.index("..")]))
            ends.append(int(xyz[xyz.index('..') + 2:]))
        instructions.append(Instruction(action, Range(starts[0], ends[0]), Range(starts[1], ends[1]), Range(starts[2], ends[2])))
        data = data[1:]

    return instructions

if __name__ == "__main__":

    filename = 'input/Day22.txt'
    instructions = process_file(filename)
    core = Core(instructions)
    core.process_instructions(part=Part.PART_ONE)
    core.count_lights()
    print(f'The answer to part one is {core.lights}.')

    core = Core(instructions)
    core.process_instructions(part=Part.PART_TWO)
    core.count_lights()
    print(f'The answer to part two is {core.lights}.')
