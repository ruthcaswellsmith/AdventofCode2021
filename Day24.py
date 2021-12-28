from enum import Enum, auto
from typing import List
import numpy as np

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

    def __init__(self):
        self.w, self.x, self.y, self.z = 0, 0, 0, 0

    def process_program(self, instructions: List[Instruction], input: List[int]):

        for step in instructions:
            if step.action == Action.INPUT:
                var = step.operands[0]
                self.__assign_value(var, input.pop(0))
            else:
                var = step.operands[0]
                val1 = self.__get_value(var)
                op2 = step.operands[1]
                val2 = self.__get_value(op2) if op2.isalpha() else int(op2)
                if step.action == Action.ADD:
                    self.__assign_value(var, val1 + val2)
                elif step.action == Action.MULTIPLY:
                    self.__assign_value(var, val1 * val2)
                elif step.action == Action.DIVIDE:
                    self.__assign_value(var, int(val1 / val2))
                elif step.action == Action.MODULO:
                    self.__assign_value(var, val1 - int(val1 / val2) * val2)
                elif step.action == Action.EQUAL:
                    self.__assign_value(var, 1 if val1 == val2 else 0)

    def __assign_value(self, var, value):
        if var == 'w':
            self.w = int(value)
        elif var == 'x':
            self.x  = int(value)
        elif var == 'y':
            self.y = int(value)
        else:
            self.z = int(value)

    def __get_value(self, var):
        if var == 'w':
            return self.w
        elif var == 'x':
            return self.x
        elif var == 'y':
            return self.y
        else:
            return self.z

    def validate_model_number(self, instructions, model_number):

        self.process_program(instructions=instructions, input=[int(c) for c in model_number])
        return self.z == 0

def process_file(filename):

    with open(filename, 'r') as f:
        data = f.read().rstrip('\n').split('\n')

    instructions = []
    while data:
        txt = data[0].split(' ')
        instructions.append(Instruction(txt.pop(0), txt))
        data = data[1:]
    return instructions

if __name__ == "__main__":

    filename = 'input/Day24.txt'
    monad = process_file(filename)

    alu = ALU()
    model_number = 99999999999999
    valid = False
    while not valid:
        alu.validate_model_number(instructions=monad, str(model_number))
        model_number -= 1

