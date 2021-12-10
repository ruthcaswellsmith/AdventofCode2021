from enum import Enum, auto

LEFT_CHARACTERS = [
    '(',
    '[',
    '{',
    '<'
]

PAIRS = {
    '(': ')',
    '[': ']',
    '{': '}',
    '<': '>'
}

PART1_POINTS = {
    ')': 3,
    ']': 57,
    '}': 1197,
    '>': 25137
}

PART2_POINTS = {
    ')': 1,
    ']': 2,
    '}': 3,
    '>': 4
}


class Part(str, Enum):

    PART_ONE = auto()
    PART_TWO = auto()

class Line():

    def __init__(self, text):

        self.text = text
        self.stack = []
        self.corrupt = False
        self.completion = []
        self.points1 = 0
        self.points2 = 0

    def process(self):

        remaining_characters = self.text

        while (not self.corrupt) and (len(remaining_characters) > 0):

            new_char = remaining_characters[0]
            remaining_characters = remaining_characters[1:]

            if new_char in LEFT_CHARACTERS:
                self.stack.append(new_char)
            else:
                if new_char == PAIRS[self.stack[-1]]:
                    # we have a match pop the stack
                    self.stack.pop()
                else:
                    self.corrupt = True
                    self.points1 = PART1_POINTS[new_char]

        # If the line it not corrupt, it may be incomplete, so complete it
        if not self.corrupt:
            while self.stack:

                matching_char = PAIRS[self.stack[-1]]
                self.completion.append(matching_char)
                self.stack.pop()
                self.points2 = 5 * self.points2 + PART2_POINTS[matching_char]

class Report():

    def __init__(self, lines):

        self.lines = lines

    def process_lines(self):

        for line in self.lines:
            line.process()

    def get_answer(self, part=Part.PART_ONE):

        if part == Part.PART_ONE:

            return sum([line.points1 for line in self.lines])

        else:

            # We sort the scores and take the middle score
            scores = [line.points2 for line in self.lines]
            scores.sort()
            return scores[round(len(scores)/2)]

    def remove_corrupted_lines(self):

        self.lines = [line for line in self.lines if not line.corrupt]

def process_file(filename):

    with open(filename, 'r') as f:
        data = f.read().rstrip('\n').split('\n')

    lines = []
    for i, line in enumerate(data):
        lines.append(Line(data[i]))

    return lines

if __name__ == "__main__":

    filename = "input/Day10.txt"
    report = Report(process_file(filename))

    report.process_lines()

    answer = report.get_answer(part=Part.PART_ONE)
    print(f'The answer to part one is {answer}.')

    report.remove_corrupted_lines()
    answer = report.get_answer(part=Part.PART_TWO)
    print(f'The answer to part two is {answer}.')
