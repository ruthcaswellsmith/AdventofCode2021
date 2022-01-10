from enum import Enum, auto
from typing import List, Dict
import numpy as np
import random

DIGITS = 14

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

    def find_valid_number(self, number: str, valid_numbers: List):

        if len(number) == DIGITS:
            return number

        digit = len(number) - 1
        if digit in [2, 3, 6, 8, 10, 11, 12]:
            alu = ALU(self.instructions, self.parameters)
            for i, c in enumerate(number):
                input = [int(c)]
                input.extend([parameter for parameter in alu.parameters[i]])
                alu.process_program(input=input)
            next_digit = alu.variables['z'] % 26 + alu.parameters[digit+1][1]
            if next_digit in range(1, 10):
                valid_number = self.find_valid_number(number=number + str(next_digit), valid_numbers=valid_numbers)
                if valid_number:
                    valid_numbers.append(valid_number)
        else:
            for next_digit in range(9, 0, -1):
                valid_number = self.find_valid_number(number=number + str(next_digit), valid_numbers=valid_numbers)
                if valid_number:
                    valid_numbers.append(valid_number)

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

    alu = ALU(instructions=monad, parameters=parameters)
    valid_numbers = []
    alu.find_valid_number(number='', valid_numbers=valid_numbers)

    print(f'The answer to part one is {valid_numbers[1]}.')
    print(f'The answer to part two is {valid_numbers[-1]}.')