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
        self.variables={}
        for var in ['w','x','y','z']:
            self.variables[var] = 0

    def process_program(self, instructions: List[Instruction], input: List[int]):

        for step in instructions:
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
                    self.variables[var] = val1 - int(val1 / val2) * val2
                elif step.action == Action.EQUAL:
                    self.variables[var] = 1 if val1 == val2 else 0
            print(step.action, step.operands, self.variables)


    def validate_model_number(self, instructions, model_number):

        self.process_program(instructions=instructions, input=[int(c) for c in model_number])
        return self.variables['z'] == 0

def process_file(filename):

    with open(filename, 'r') as f:
        data = f.read().rstrip('\n').split('\n')

    instructions = []
    while data:
        txt = data[0].split(' ')
        instructions.append(Instruction(txt.pop(0), txt))
        data = data[1:]
    return instructions

def decrement(model_number):

    int_model_number = int(model_number)
    contains_zero = True
    while contains_zero:
        int_model_number = int_model_number - 1
        if '0' not in str(int_model_number):
            contains_zero = False
    return str(int_model_number)

if __name__ == "__main__":

    filename = 'input/Day24.txt'
    monad = process_file(filename)

    alu = ALU()
    model_number = '19999999999999'
    alu.validate_model_number(instructions=monad, model_number=model_number)
    # valid = False
    # while not valid:
    #     model_number = decrement(model_number)
    #     print(model_number)
    #     alu = ALU()
    #     if alu.validate_model_number(instructions=monad, model_number=model_number):
    #         valid = True
