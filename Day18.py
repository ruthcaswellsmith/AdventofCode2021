from enum import Enum, auto
import regex as re
import math

class Part(str, Enum):

    PART_ONE = auto()
    PART_TWO = auto()

class SnailfishNum():

    def __init__(self, string):

        self.string = string
        self.pos = None

    def reduce(self):

        done = False
        while not done:

            while self.need_to_explode():

                self.explode(self.pos)

            done = True

            if self.need_to_split():

                self.split(self.pos)
                done = False


    def add(self, string):

        self.string = f'[{self.string},{string}]'

    def need_to_explode(self):

        positions = [m.start() for m in re.finditer('\[\d+,\d+\]', self.string)]
        for pos in positions:
            left = self.string[0:pos+1]
            depth = left.count('[') - left.count(']')
            if depth > 4:
                self.pos = pos
                return True
        return False

    def need_to_split(self):

        x = re.search('\d{2}', self.string)
        if x:
            self.pos = x.start()
            return True
        else:
            return False

    def split(self, pos):

        num = int(self.string[pos: pos + 2])
        left = math.floor(num / 2)
        right = math.ceil(num / 2)
        self.string = self.string[:pos] + f'[{str(left)},{str(right)}]' + self.string[pos+2:]

    def explode(self, pos):

        right = self.string[pos:]
        exploding_pair = right[:right.index(']')+1]
        comma_ind = exploding_pair.index(',')
        left, right = exploding_pair[1: comma_ind], exploding_pair[comma_ind+1: len(exploding_pair)-1]
        left_str, right_str = self.string[0:pos], self.string[pos + len(exploding_pair):]

        num_to_left = self.__find_left(left_str)
        if num_to_left:
            replacement = str(int(num_to_left) + int(left))
            ind = left_str.rfind(num_to_left)
            self.string = self.string[0:ind] + replacement + self.string[ind + len(num_to_left):]
            if len(num_to_left) == 1 and len(replacement) == 2:
                pos += 1

        num_to_right = self.__find_right(right_str)
        if num_to_right:
            replacement = str(int(num_to_right) + int(right))
            ind = pos + len(exploding_pair) + right_str.find(num_to_right)
            self.string = self.string[0:ind] + replacement + self.string[ind + len(num_to_right):]

        self.string = self.string[0: pos] + '0' + self.string[pos + len(exploding_pair):]

    def __find_left(self, left_str):

        num = next(iter(reversed(re.findall("\d+", left_str))), None)
        return num

    def __find_right(self, right_str):

        nums = re.findall("\d+", right_str)
        return nums[0] if nums else None

    def get_magnitude(self, string):

        if string.isnumeric():
            return int(string)

        # Split string
        pos = self.__split_string(string)

        return 3 * self.get_magnitude(string[1:pos]) + 2 * self.get_magnitude(string[pos+1:len(string)-1])

    @staticmethod
    def __split_string(string):

        positions = [m.start() for m in re.finditer(',', string)]

        for pos in positions:
            substr = string[:pos]
            if substr.count('[') - substr.count(']') == 1:
                return pos

def get_greatest_magnitude(data):

    num = len(data)
    snailfishnums = []
    for i in range(num):
        snailfishnums.append(SnailfishNum(data[0]))

    magnitudes = []
    for i in range(num):
        for j in range(num):
            if i != j:
                magnitudes.append(snailfishnums[i].add(snailfishnums[j]))

def process_file(filename):

    with open(filename, 'r') as f:
        data = f.read().rstrip('\n').split('\n')

    return data

if __name__ == "__main__":

    filename = 'input/Day18.txt'
    data = process_file(filename)
    snailfishnum = SnailfishNum(data[0])
    for line in data[1:]:
        snailfishnum.add(line)
        snailfishnum.reduce()
    snailfishnum.magnitude = snailfishnum.get_magnitude(snailfishnum.string)
    print(f'The answer to part one is {snailfishnum.magnitude}')



