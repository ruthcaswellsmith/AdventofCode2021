import string
from enum import Enum, auto
import numpy as np
from typing import List

class Part(str, Enum):
    PART_ONE = auto()
    PART_TWO = auto()

def get_bits(char):
    return bin(int(char, 16))[2:].zfill(4)

class Message():

    def __init__(self, message):

        self.message = message
        self.packets = []

    def decode(self):

        while self.message:

            version, type, bits = self.__decode_header(self.message[0:2])
            self.message = self.message[2:]

            if type == 4:

                literal = Literal(version, type, bits, self.message)
                self.packets.append(literal)
                literal.decode()
                print('hi')

            else:

                operator = Operator(version, type, bits, self.message)
                self.packets.append(operator)
                operator.decode()

    def __decode_header(self, first_two_chars):

        bits = ''
        for i in range(2):
            bits += get_bits(first_two_chars[i])

        version = int(bits[0:3], 2)
        type = int(bits[3:6], 2)

        return version, type, bits[6:8]

class Literal():

    def __init__(self, version, type, bits, message):

        self.version = version
        self.type = type
        self.bits = bits
        self.message = message

    def decode(self, bits):

        num = ''
        done = False
        while not done:
            while len(self.bits) < 5:
                self.bits += get_bits(self.message[0])
                self.message = self.message[1:]
            if self.bits[0] == '0':
                done = True
            num += self.bits[1:5]
            self.bits = self.bits[5:]

        self.num = int(num, 2)


class Operator():

    def __init__(self, version, type, bits, message):

        self.version = version
        self.bits = bits
        self.type = type
        self.message = message

    def decode(self):

        self.length_type_id = self.bits[0]
        self.bits = self.bits[1:]
        self.__process_length_type_id()



    def __process_length_type_id(self, bits):

        num_bits = 15 if self.length_type_id == '0' else 11
        while len(self.bits) < num_bits:
            self.bits += get_bits(self.message[0])
            self.message = self.message[1:]

        self.packet_info = int(bits[0:num_bits], 2)
        self.bits = self.bits[num_bits:]

def process_file(filename):

    with open(filename, 'r') as f:
        data = f.read().rstrip('\n').split('\n')

    return data[0]

if __name__ == "__main__":

    filename = "input/test.txt"
    message = Message(process_file(filename))
    message.decode()
    print('hi')

#    print(f'The answer is {grid.min_points}.')
