import string
from enum import Enum, auto
import numpy as np
from typing import List

class Packet():

    def __init__(self, bits, message):

        self.bits = bits
        self.message = message
        self.packets = []

    def value(self):

        if self.type == 4:
            return self.num
        elif self.type == 0:
            return np.sum(np.array([packet.value() for packet in self.packets]))
        elif self.type == 1:
            return np.prod(np.array([packet.value() for packet in self.packets]))
        elif self.type == 2:
            return np.min(np.array([packet.value() for packet in self.packets]))
        elif self.type == 3:
            return np.max(np.array([packet.value() for packet in self.packets]))
        elif self.type == 5:
            return 1 if self.packets[0].value() > self.packets[1].value() else 0
        elif self.type == 6:
            return 1 if self.packets[0].value() < self.packets[1].value() else 0
        elif self.type == 7:
            return 1 if self.packets[0].value() == self.packets[1].value() else 0

    def sum_versions(self):

        sub_packet_versions = 0
        for packet in self.packets:
            sub_packet_versions += packet.sum_versions()
        return self.version + sub_packet_versions

    def decode(self):

        self.__decode_header()

        if self.type == 4:
            self.__decode_literal()
        else:
            self.__decode_operator()

    @staticmethod
    def __get_bits(char):
        return bin(int(char, 16))[2:].zfill(4)

    def __decode_header(self):

        while len(self.bits) < 6:
            self.bits += self.__get_bits(self.message[0])
            self.message = self.message[1:]

        self.version = int(self.bits[0:3], 2)
        self.type = int(self.bits[3:6], 2)
        self.bits = self.bits[6:]


    def __decode_literal(self):

        self.tot_bits = 6 + len(self.bits)
        num = ''
        done = False
        while not done:
            while len(self.bits) < 5:
                self.bits += self.__get_bits(self.message[0])
                self.tot_bits += 4
                self.message = self.message[1:]
            if self.bits[0] == '0':
                done = True
            num += self.bits[1:5]
            self.bits = self.bits[5:]
        self.num = int(num, 2)
        self.tot_bits -= len(self.bits)

    def __decode_operator(self):

        if not self.bits:
            self.bits += self.__get_bits(self.message[0])
            self.message = self.message[1:]

        self.length_type_id = self.bits[0]
        self.tot_bits = 22 if self.length_type_id == '0' else 18
        self.bits = self.bits[1:]

        num_bits = 15 if self.length_type_id == '0' else 11
        while len(self.bits) < num_bits:
            self.bits += self.__get_bits(self.message[0])
            self.message = self.message[1:]

        self.length = int(self.bits[0:num_bits], 2)
        self.bits = self.bits[15:] if self.length_type_id == '0' else self.bits[11:]

        if self.length_type_id == '1':
            for i in range(self.length):
                packet = Packet(self.bits, self.message)
                packet.decode()
                self.bits, self.message = packet.bits, packet.message
                self.packets.append(packet)
                self.tot_bits += packet.tot_bits

        else:

            literal_bits = sum([packet.tot_bits for packet in self.packets])
            while literal_bits < self.length:
                packet = Packet(self.bits, self.message)
                packet.decode()
                self.bits, self.message = packet.bits, packet.message
                self.packets.append(packet)
                literal_bits += packet.tot_bits
                self.tot_bits += packet.tot_bits

def process_file(filename):

    with open(filename, 'r') as f:
        data = f.read().rstrip('\n').split('\n')

    return data[0]

if __name__ == "__main__":

    filename = "input/Day16.txt"
    packet = Packet("", process_file(filename))
    packet.decode()
    print(f'The answer to part one is {packet.sum_versions()}')
    print('The answer to part two is {packet.value()}')
