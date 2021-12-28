from enum import Enum, auto


class Amphipod(str, Enum):
    A = "A"
    B = "B"
    C = "C"
    D = "D"


ENERGY = {Amphipod.A: 1,
          Amphipod.B: 10,
          Amphipod.C: 100,
          Amphipod.D: 1000}

ROOMS = 4

class Burrow():

    def __init__(self, data):
        self.hallway = [Space() for i in range(11)]
        self.rooms = []
        for i in range(ROOMS):
            self.rooms.append(Room(i, data[3][3+ 2*i], data[2][3 + 2*i]))

    def is_sorted(self):

        for room in self.rooms:
            if not (room.lower_is_sorted and room.upper_is_sorted()):
                return False
        return True

    def sort(self):

        while not self.is_sorted():


class Space():

    def __init__(self):
        self.occupant = None

class Room():

    def __init__(self, number, lower, upper):
        self.number = number
        self.hallway = 2 + 2 * number
        self.lower = lower
        self.upper = upper

    def is_empty(self):
        return False if self.lower or self.upper else True

    def lower_is_sorted(self):
        if self.number == 0 and self.lower == Amphipod.A:
            return True
        if self.number == 1 and self.lower == Amphipod.B:
            return True
        if self.number == 2 and self.lower == Amphipod.C:
            return True
        if self.number == 3 and self.lower == Amphipod.D:
            return True
        return False

    def upper_is_sorted(self):
        if self.number == 0 and self.upper == Amphipod.A:
            return True
        if self.number == 1 and self.upper == Amphipod.B:
            return True
        if self.number == 2 and self.upper == Amphipod.C:
            return True
        if self.number == 3 and self.upper == Amphipod.D:
            return True
        return False


def process_file(filename):

    with open(filename, 'r') as f:
        data = f.read().rstrip('\n').split('\n')

    return data

if __name__ == "__main__":

    filename = 'input/test2.txt'
    burrow = Burrow(process_file(filename))
    burrow.sort()
    print(burrow.is_sorted())
    print('hi')