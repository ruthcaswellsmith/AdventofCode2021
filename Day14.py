import string
from enum import Enum, auto
import numpy as np
from typing import List

class Part(str, Enum):
    PART_ONE = auto()
    PART_TWO = auto()

class Polymer():

    def __init__(self, template: str, rules: List[List[str]]):

        self.polymer = template
        self.rules = {}
        for rule in rules:
            self.rules[rule[0]] = rule[1]
        self.pair_counts = {}
        for pair in self.rules.keys():
            self.pair_counts[pair] = self.polymer.count(pair)
        self.letters = list(string.ascii_uppercase)
        self.letter_counts = []

    def find_terminating_rule(self):

        for pair, letter in self.rules.items():
            if pair.count(pair[0]) == 2:
                letter1 = pair[0]
                letter2 = letter
                if (self.rules[letter1 + letter2] in [letter1, letter2]) \
                    and (self.rules[letter2 + letter1] in [letter1, letter2]):
                    print(pair, letter)

    def n_steps(self, n: int, part: Part):

        for i in range(n):
            self.__step(part, i)
            print(self.polymer)
        self.__get_letter_counts()

    def __step(self, part: Part, step: int):

        if part == Part.PART_ONE:
            insertions = []
            for i in range(len(self.polymer) - 1):
                insertions.append(self.rules[self.polymer[i:i + 2]])

            for i in range(len(insertions)):
                divide = 2 * (i + 1)
                left = self.polymer[:divide]
                right = self.polymer[divide:]
                self.polymer = left[:-1] + insertions[i] + left[-1] + right

        else:
            pass
            # insertions = []
            # for i in range(len(self.polymer) - 1):
            #     if self.polymer[i].isnum():
            #
            #     insertions.append(self.rules[self.polymer[i:i + 2]])


    def __get_letter_counts(self):

        self.letter_counts = []
        for letter in self.letters:
            self.letter_counts.append(self.polymer.count(letter))

        self.letter_counts = [count for count in self.letter_counts if count > 0]

def process_file(filename):

    with open(filename, 'r') as f:
        data = f.read().rstrip('\n').split('\n')

    template = data[0]

    data = data[2:]
    rules = []
    for i in range(len(data)):
        rule = data[i].split('->')
        rules.append([rule[0].strip(), rule[1].strip()])

    return template, rules

if __name__ == "__main__":

    filename = "input/Day14.txt"
    template, rules = process_file(filename)

    polymer = Polymer(template, rules)
    polymer.n_steps(10, Part.PART_ONE)
    print(f'The answer to part one is {max(polymer.letter_counts) - min(polymer.letter_counts)}.')

    polymer = Polymer(template, rules)
    polymer.find_terminating_rule()
#    polymer.predict_n_steps(n=3)
