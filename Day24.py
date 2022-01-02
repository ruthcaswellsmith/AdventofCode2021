from enum import Enum, auto
from typing import List, Dict
import numpy as np
import random

DIGITS = 14
ZLIMIT = {}
ZLIMIT[0] = 26**1
ZLIMIT[1] = 26**2
ZLIMIT[2] = 26**3
ZLIMIT[3] = 26**3
ZLIMIT[4] = 26**2
ZLIMIT[5] = 26**3
ZLIMIT[6] = 26**4
ZLIMIT[7] = 26**4
ZLIMIT[8] = 26**4
ZLIMIT[9] = 26**3
ZLIMIT[10] = 26**3
ZLIMIT[11] = 26**2
ZLIMIT[12] = 26**1
ZLIMIT[13] = 26**0

class Action(str, Enum):
    INPUT = 'inp'
    ADD = 'add'
    MULTIPLY = 'mul'
    DIVIDE = 'div'
    MODULO = 'mod'
    EQUAL = 'eql'

class Instruction:

    def __init__(self, action: Action, operands: List[str]):
        self.action = action
        self.operands = operands


class ALU:

    def __init__(self, instructions: List[Instruction], parameters: Dict):
        self.variables={}
        for var in ['v', 'w', 'x', 'y', 'z']:
            self.variables[var] = 0
        self.instructions = instructions
        self.parameters = parameters
        self.valid_numbers = []

    def process_program(self, input: List[int]):

        for step in self.instructions:
            if step.action == Action.INPUT:
                var = step.operands[0]
                self.variables[var] = input.pop(0)
            else:
                var = step.operands[0]
                val1 = self.variables[var]
                op2 = step.operands[1]
                val2 = self.variables[op2] if op2.isalpha() else int(op2)
                if step.action == Action.ADD:
                    self.variables[var] = val1 + val2
                elif step.action == Action.MULTIPLY:
                    self.variables[var] = val1 * val2
                elif step.action == Action.DIVIDE:
                    self.variables[var] = int(val1 / val2)
                elif step.action == Action.MODULO:
                    self.variables[var] = val1 % val2
                elif step.action == Action.EQUAL:
                    self.variables[var] = 1 if val1 == val2 else 0

    def __is_valid(self, number):

        digit = len(number) - 1
        # Run instructions for current number
        alu = ALU(self.instructions, self.parameters)
        for i, c in enumerate(number):
            input = [int(c)]
            input.extend([parameter for parameter in alu.parameters[i]])
            alu.process_program(input=input)
        # Now compare the value of z
        return True if alu.variables['z'] < ZLIMIT[digit] else False

    def find_valid_number(self, number: str):

#        if number and int(number)%11_111 == 0:
        print(number)

        if len(number) == DIGITS:
            print('got a 14-digit number')
            print(number)
            exit(100)

        digit = len(number) - 1
        if digit in [2, 3, 6, 8, 10, 11, 12]:
            alu = ALU(self.instructions, self.parameters)
            for i, c in enumerate(number):
                input = [int(c)]
                input.extend([parameter for parameter in alu.parameters[i]])
                alu.process_program(input=input)
            next_digit = alu.variables['z']%26 + alu.parameters[digit+1][1]
            if next_digit in range(0,10):
                self.find_valid_number(number + str(next_digit))
        else:
            for next_digit in range(9, 0, -1):
               self.find_valid_number(number + str(next_digit))

    def find_valid_zs(self):

        digit_13 = self.__get_possibilities_x_equal_w(13, [['', 0]])
        print(len(digit_13))
        digit_12 = self.__get_possibilities_x_equal_w(12, digit_13)
        print(len(digit_12))
        digit_11 = self.__get_possibilities_x_equal_w(11, digit_12) + \
                   self.__get_possibilities_x_not_equal_w(11, digit_12)
        print(len(digit_11))
        digit_10 = self.__get_possibilities_x_not_equal_w(10, digit_11)
        print(len(digit_10))
        digit_9 = self.__get_possibilities_x_equal_w(9, digit_10) + \
                   self.__get_possibilities_x_not_equal_w(9, digit_10)
        print(len(digit_9))
        digit_8 = self.__get_possibilities_x_equal_w(8, digit_9)
        print(len(digit_8))

    def __get_possibilities_x_equal_w(self, digit, next_digit):

        this_digit = []
        for num, z in next_digit:
            for w in range(1, 10):
                this_digit.append([str(w) + num, w - self.parameters[digit][1] + 26*z])
        return this_digit

    def __get_possibilities_x_not_equal_w(self, digit, next_digit):

        this_digit = []
        for num, z in next_digit:
            for w in range(1, 10):
                z = (z - self.parameters[digit][2] - w) / self.parameters[digit][0]
                if int(z) == z:
                    this_digit.append([str(w) + num, z])

        return this_digit


def read_instructions(filename):

    with open(filename, 'r') as f:
        data = f.read().rstrip('\n').split('\n')

    instructions = []
    while data:
        txt = data[0].split(' ')
        instructions.append(Instruction(txt.pop(0), txt))
        data = data[1:]
    return instructions

def read_parameters(filename):

    with open(filename, 'r') as f:
        data = f.read().rstrip('\n').split('\n')

    parameters = {}
    digit = 0
    while digit < 14:
        parameters[digit] = []
        for step in [4, 5, 15]:
            parameters[digit].append(int(data[step + digit*18].split(' ')[-1]))
        digit += 1

    return parameters


if __name__ == "__main__":

    filename = 'input/Day24-parameterized.txt'
    monad = read_instructions(filename)

    filename = 'input/Day24.txt'
    parameters = read_parameters(filename)

    # alu = ALU(instructions=monad, parameters=parameters)
    # alu.find_valid_number(number='')
    # print(alu.valid_numbers)

#    Test the number we found
    number = '39924989499969'
    alu = ALU(instructions=monad, parameters=parameters)
    for i, c in enumerate(number):
        input = [int(c)]
        input.extend([parameter for parameter in alu.parameters[i]])
        print(input)
        alu.process_program(input=input)
        print(alu.variables)

