import numpy as np
from enum import Enum, auto
from typing import List

class PART(str, Enum):

    PART_ONE = auto()
    PART_TWO = auto()

NUMBERS = {
    0: {'a', 'b', 'c', 'e', 'f', 'g'},
    1: {'c', 'f'},
    2: {'a', 'c', 'd', 'e', 'g'},
    3: {'a', 'c', 'd', 'f', 'g'},
    4: {'b', 'c', 'd', 'f'},
    5: {'a', 'b', 'd', 'f', 'g'},
    6: {'a', 'b', 'd', 'e', 'f', 'g'},
    7: {'a', 'c', 'f'},
    8: {'a', 'b', 'c', 'd', 'e', 'f', 'g'},
    9: {'a', 'b', 'c', 'd', 'f', 'g'}
}

LETTERS = {'a', 'b', 'c', 'd', 'e', 'f', 'g'}

UNIQUE_NUMBERS = [1, 4, 7, 8]
UNIQUE_LENGTHS = [len(NUMBERS[number]) for number in UNIQUE_NUMBERS]

class Note():

    def __init__(self, signal_patterns: List[str], output_values: List[str]):

        self.signal_patterns = [set(signal_pattern) for signal_pattern in signal_patterns]
        self.output_values = [set(output_value) for output_value in output_values]
        self.mapping = {}

    def count_unique_segments(self):

        lengths = np.array(list(map(len, self.output_values)))
        counts = [np.count_nonzero(lengths == num) for num in range(8)]
        return np.array(counts)[UNIQUE_LENGTHS].sum()

    def get_mapping(self):

        # Now find out which two are c and f
        c_and_f = self.__get_signal_patterns_of_length(2)[0]

        # Find out which one is a.  It is the one that is in a 3-length but not in c_and_f
        key = next(iter(self.__get_signal_patterns_of_length(3)[0] - c_and_f))
        self.mapping[key] = 'a'

        # Find out which is c.  It is one that is in every 6-length
        self.__map_based_on_length_six(c_and_f, 'c', 'f')

        # Find b_and_d.  They are number of length 4 but not number of length 2
        b_and_d = self.__get_signal_patterns_of_length(4)[0] - c_and_f
        self.__map_based_on_length_six(b_and_d, 'd', 'b')

        # Now find g.  It is the only letter in every length 6 that is not already mapped
        signals_6 = self.__get_signal_patterns_of_length(6)
        possible_gs = signals_6[0]
        for signal in signals_6:
            possible_gs.intersection_update(signal)

        key = next(iter(possible_gs - set(self.mapping.keys())))
        self.mapping[key] = 'g'

        # And e is the last one left
        key = next(iter(LETTERS - set(self.mapping.keys())))
        self.mapping[key] = 'e'

    def __map_based_on_length_six(self, letters, letter1, letter2):

        signals_6 = self.__get_signal_patterns_of_length(6)
        for letter in letters:

            if sum([letter in item for item in signals_6]) == len(signals_6):
                self.mapping[letter] = letter2
                self.mapping[next(iter(letters - set(letter)))] = letter1


    def __get_signal_patterns_of_length(self, length):

        return [signal_pattern for signal_pattern in self.signal_patterns if len(signal_pattern) == length]

    def decode_output_values(self):

        digits = []
        for output_value in self.output_values:

            decoded_output_value = set()
            for elem in output_value:
                decoded_output_value.add(self.mapping[elem])

            for key, val in NUMBERS.items():
                temp = (val==decoded_output_value)
                if val == decoded_output_value:
                    digits.append(key)

        return int(''.join(map(str, digits)))


def process_file(filename):

    with open(filename, 'r') as f:
        data = f.read().rstrip('\n').split('\n')

    notes = []
    for line in data:
        split_line = line.split('|')
        notes.append(Note(split_line[0].strip().split(), split_line[1].strip().split()))

    return notes

if __name__ == "__main__":

    filename = "input/Day8.txt"
    notes = process_file(filename)
    for note in notes:
        note.get_mapping()

    answer = 0
    for note in notes:
        answer += note.count_unique_segments()
    print(f'The answer to part one is {answer}.')

    answer = 0
    for note in notes:
        answer += note.decode_output_values()
    print(f'The answer to part two is {answer}.')

