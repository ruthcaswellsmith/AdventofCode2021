from enum import Enum, auto


class AmphipodType(str, Enum):
    A = "A"
    B = "B"
    C = "C"
    D = "D"

class SpaceType(str, Enum):
    LOWER_ROOM = auto()
    UPPER_ROOM = auto()
    HALL = auto()

ENERGY = {AmphipodType.A: 1,
          AmphipodType.B: 10,
          AmphipodType.C: 100,
          AmphipodType.D: 1000}

ROOMS = 4

class Burrow:

    def __init__(self, data):
        self.hallway = [Space(occupant=None, type=SpaceType.HALL) for _ in range(11)]
        self.rooms = []
        for i, (name, member) in enumerate(AmphipodType.__members__.items()):
            lower = Space(occupant=data[3][3 + 2*i], type=SpaceType.LOWER_ROOM)
            upper = Space(occupant=data[2][3 + 2*i], type=SpaceType.UPPER_ROOM)
            self.rooms.append(Room(name=name, number=i, lower=lower, upper=upper))
        self.amphipods = []
        for i, room in enumerate(self.rooms):
            self.amphipods.append(Amphipod(type=room.lower.occupant, space=room.lower))
            self.amphipods.append(Amphipod(type=room.upper.occupant, space=room.upper))

    def path_clear(self, source, destination):

        if source.type == SpaceType.LOWER_ROOM:
            # Check if upper room is free
            if

    def is_sorted(self):

        for room in self.rooms:
            if not room.is_sorted():
                return False
        return True

    def sort(self):

        pass

    def __move_amphipod(self, space1, space2):

        pass


class Space:

    def __init__(self, occupant: AmphipodType, type: SpaceType):
        self.type = type
        self.occupant = occupant

class Amphipod:

    def __init__(self, type: AmphipodType, space: Space):
        self.type = type
        self.space = space
        self.energy = 0

    def can_move(self, destination):

        pass

    def move(self, source, destination):

        self.space = space2
        source.occupant = None
        destination.occupant = self.type
        self.energy =



class Room:

    def __init__(self, name: AmphipodType, number: int, lower: Space, upper: Space):
        self.name = name
        self.number = number
        self.hallway = 2 + 2 * number
        self.lower = lower
        self.upper = upper

    def is_empty(self):
        return False if self.lower.occupant or self.upper.occupant else True

    def upper_is_empty(self):
        return False if self.upper.occupant else True

    def lower_is_sorted(self):
        return True if self.name == self.lower.occupant else False

    def upper_is_sorted(self):
        return True if self.name == self.upper.occupant else False

    def is_sorted(self):
        return True if self.lower_is_sorted() and self.upper_is_sorted() else False


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