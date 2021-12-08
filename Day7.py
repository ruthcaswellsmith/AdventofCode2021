import numpy as np
from enum import Enum, auto
from typing import List

class PART(str, Enum):

    PART_ONE = auto()
    PART_TWO = auto()

# These are number of segments used by numbers 0-9
SEGMENTS = [6, 2, 5, 5, 4, 5, 6, 3, 7, 6]

UNIQUE_SEGMENTS = [2, 3, 4, 7]

class Display():

    def __init__(self):

        self.numbers = {
            0: {'a', 'b', 'c', 'e', 'f', 'g'},
            1: {'c', 'f'},
            2: {'a', 'c', 'd', 'e', 'g'},
            3: {'a', 'c', 'd', 'f', 'g'},
            4: {'b', 'c', 'd', 'f'},
            5: {'a', 'b', 'd', 'f', 'g'},
            6: {'b', 'c', 'd', 'e', 'f'},
            7: {'a', 'c', 'f'},
            8: {'b', 'b', 'c', 'd', 'e', 'f', 'g'},
            9: {'a', 'b', 'c', 'd', 'f', 'g'},
}


class Note():

    def __init__(self, signal_patterns: List[str], output_values: List[str]):

        self.signal_patterns = signal_patterns
        self.output_values = output_values

    def count_segments(self):

        lengths = np.array(list(map(len, self.output_values)))
        counts = [np.count_nonzero(lengths == num) for num in range(8)]
        return np.array(counts)

class Notes():

    def __init__(self, notes: List[Note]):

        self.notes = notes

    def get_answer(self, part: PART):

        if part == PART.PART_ONE:

            answer = 0
            for note in self.notes:

                answer += note.count_segments()[UNIQUE_SEGMENTS].sum()

        return answer

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
    notes = Notes(process_file(filename))

    answer = notes.get_answer(PART.PART_ONE)
    print(f'The answer to part one is {answer}.')
