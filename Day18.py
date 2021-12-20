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

                self.explode()

            done = True

            if self.need_to_split():

                self.split()
                done = False


    def add(self, snailfishnum):

        self.string = f'[{self.string},{snailfishnum.string}]'

    def need_to_explode(self):

        positions = [m.start() for m in re.finditer('\[\d+,\d+\]', self.string)]
        for pos in positions:
            left = self.string[0:pos+1]
            depth = left.count('[') - left.count(']')
            if depth > 4:
                self.exp_pos = pos
                right = self.string[pos:]
                self.exp_pair = right[:right.index(']')+1]
                return True
        return False

    def need_to_split(self):

        x = re.search('\d{2}', self.string)
        if x:
            self.split_pos = x.start()
            self.split_num = int(self.string[x.start():x.end()])
            return True
        else:
            return False

    def split(self):

        left = math.floor(self.split_num / 2)
        right = math.ceil(self.split_num / 2)
        self.string = f'{self.string[:self.split_pos]}[{str(left)},{str(right)}]{self.string[self.split_pos+2:]}'

    def explode(self):

        comma_ind = self.exp_pair.index(',')
        left_num, right_num = int(self.exp_pair[1: comma_ind]), int(self.exp_pair[comma_ind+1: len(self.exp_pair)-1])
        left_str, right_str = self.string[0:self.exp_pos], self.string[self.exp_pos + len(self.exp_pair):]

        num_to_left, num_to_right = self.__find_num(left_str, 'L'), self.__find_num(right_str, 'R')

        if num_to_left:
            left_rep = str(int(num_to_left) + left_num)
            left_ind = left_str.rfind(num_to_left)
            left_str = f'{left_str[:left_ind]}{left_rep}{left_str[left_ind + len(num_to_left):]}'

        if num_to_right:
            right_rep = str(int(num_to_right) + right_num)
            right_ind = right_str.find(num_to_right)
            right_str = f'{right_str[:right_ind]}{right_rep}{right_str[right_ind + len(num_to_right):]}'

        self.string = f'{left_str}0{right_str}'

    def __find_num(self, string, type):

        if type == 'L':
            return next(iter(reversed(re.findall("\d+", string))), None)
        else:
            return next(iter(re.findall("\d+", string)), None)

    def get_magnitude(self, string):

        if string.isnumeric():
            return int(string)

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
    magnitudes = []
    for i in range(num):
        for j in range(num):
            if i != j:
                print(f'adding {i} and {j}')
                snailfishnum = SnailfishNum(data[i])
                snailfishnum.add(SnailfishNum(data[j]))
                snailfishnum.reduce()
                snailfishnum.magnitude = snailfishnum.get_magnitude(snailfishnum.string)
                magnitudes.append(snailfishnum.magnitude)
    return max(magnitudes)

def process_file(filename):

    with open(filename, 'r') as f:
        data = f.read().rstrip('\n').split('\n')

    return data

if __name__ == "__main__":

    filename = 'input/Day18.txt'
    data = process_file(filename)
    snailfishnum = SnailfishNum(data[0])
    for line in data[1:]:
        snailfishnum.add(SnailfishNum(line))
        snailfishnum.reduce()
    snailfishnum.magnitude = snailfishnum.get_magnitude(snailfishnum.string)
    print(f'The answer to part one is {snailfishnum.magnitude}')

    print(f'The answer to part two is {get_greatest_magnitude(data)}')