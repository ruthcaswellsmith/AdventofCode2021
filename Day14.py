import string
from enum import Enum, auto
import numpy as np
from typing import List

class Part(str, Enum):
    PART_ONE = auto()
    PART_TWO = auto()

class Polymer():

    def __init__(self, template: str, rules: List[List[str]]):

        self.template = template
        self.pair_counts = {}

        self.rules = {}
        for rule in rules:
            self.rules[rule[0]] = rule[1]

        for pair in self.rules.keys():
            self.pair_counts[pair] = 0
        for i in range(len(self.template) - 1):
            self.pair_counts[self.template[i:i+2]] += 1

        self.letter_counts = {}
        for letter in list(string.ascii_uppercase):
            self.letter_counts[letter] = 0

    def n_steps(self, n: int):

        for i in range(n):
            self.__step()

    def __step(self):

        self.new_pair_counts = {}
        for pair in self.rules.keys():
            self.new_pair_counts[pair] = 0

        for pair, count in self.pair_counts.items():

            if count > 0:
                left_letter = pair[0]
                right_letter = pair[1]
                insert_letter = self.rules[pair]
                self.new_pair_counts[left_letter + insert_letter] += count
                self.new_pair_counts[insert_letter + right_letter] += count

        self.pair_counts = self.new_pair_counts.copy()

    def count_letters(self):

        for pair, count in self.pair_counts.items():

            right_letter = pair[1]
            self.letter_counts[right_letter] += count

        # Finally count the left-most letter of our template
        self.letter_counts[self.template[0]] += 1

    def get_answer(self):

        self.letter_counts = [count for count in self.letter_counts.values() if count > 0]
        return max(self.letter_counts) - min(self.letter_counts)

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
    polymer.n_steps(40)
    polymer.count_letters()
    answer = polymer.get_answer()
    print(f'The answer is {answer}.')

