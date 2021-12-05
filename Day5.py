import numpy as np
from enum import Enum, auto

SIZE = 1000

class Orientation(str, Enum):

    HORIZONTAL = auto()
    VERTICAL = auto()
    DIAGONAL = auto()

class Part(str, Enum):

    PART_ONE = auto()
    PART_TWO = auto()

class Point():

    def __init__(self, point):
        self.x = int(point[0])
        self.y = int(point[1])

class Line():

    def __init__(self, p1, p2):

        self.p1 = p1
        self.p2 = p2
        self.__get_orientation()

    def __get_orientation(self):

        if self.p1.x == self.p2.x:
            self.orientation = Orientation.VERTICAL

        elif self.p1.y == self.p2.y:
            self.orientation = Orientation.HORIZONTAL

        else:
            self.orientation = Orientation.DIAGONAL

class Diagram():

    def __init__(self):
        self.points = np.zeros((SIZE, SIZE), dtype=int)

    def populate(self, lines, part):

        if part == Part.PART_ONE:

            for line in lines:
                if line.orientation in [Orientation.VERTICAL, Orientation.HORIZONTAL]:
                    self.__process_line(line)

        else:
            for line in lines:
                self.__process_line(line)


    def __process_line(self, line):

        x, y = line.p1.x, line.p1.y

        while (x != line.p2.x) or (y != line.p2.y):
            self.points[x, y] += 1
            if x != line.p2.x:
                x += 1 if x < line.p2.x else -1
            if y != line.p2.y:
                y += 1 if y < line.p2.y else -1

        self.points[x, y] += 1

    def get_overlap(self):

        return len(self.points[np.where(self.points > 1)])

def process_file(filename):

    with open(filename, 'r') as f:
        data = f.read().rstrip('\n').split('\n')
    f.close()

    lines = []
    while data:

        points = data[0].split('->')
        p1, p2 = Point(points[0].strip(' ').split(',')), Point(points[1].strip(' ').split(','))
        lines.append(Line(p1, p2))

        data = data[1:]

    return lines


if __name__ == "__main__":

    filename = "input/Day5.txt"
    lines = process_file(filename)

    diagram = Diagram()
    diagram.populate(lines, Part.PART_ONE)
    print(f'The number of overlapping points for Part One is {diagram.get_overlap()}')

    diagram = Diagram()
    diagram.populate(lines, Part.PART_TWO)
    print(f'The number of overlapping points for Part Two is {diagram.get_overlap()}')
