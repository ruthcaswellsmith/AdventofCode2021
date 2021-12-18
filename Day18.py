from enum import Enum, auto

class Part(str, Enum):

    PART_ONE = auto()
    PART_TWO = auto()

class Pair():

    def __init__(self, string):

        self.string = string

    def process_string(self):

        char = self.string[0]
        if char == "[":
            self.left = Pair(self.string[1:])
        elif char == "]":
            pass
            # close a pair
        elif char == ",":
            # process rest of the string
            self.right = Pair(self.string[1:])
        elif char.isnumeric():
            return int(char)


def process_file(filename):

    with open(filename, 'r') as f:
        data = f.read().rstrip('\n').split('\n')

    data = data[0]
    x_min = int(data[data.index("=") + 1: data.index("..")])
    x_max = int(data[data.index("..") + 2: data.index(",")])
    data = data[data.index(","):]
    y_min = int(data[data.index("=") + 1: data.index("..")])
    y_max = int(data[data.index("..") + 2:])

    return x_min, x_max, y_min, y_max

if __name__ == "__main__":

    string = '[1,2]'
    pair = Pair(string)
    pair.process_string()
    # filename = "input/Day17.txt"
    # target = Target(process_file(filename))
    # projectile = Projectile(target)
    # projectile.iterate(0, 200, -200, 200)
    # print(f'The highest point reached while still hitting the target was {projectile.get_answer(part=Part.PART_ONE)}')
    # print(f'The number of velocity values that result in hits is {projectile.get_answer(part=Part.PART_TWO)}')
