from enum import Enum, auto
from typing import List
import math
import numpy as np

PAD = 2

class Image():

    def __init__(self, enhancement: str, image: List[List[str]]):

        self.enhancement = np.array([1 if c == '#' else 0 for c in enhancement])
        self.length = len(image)
        self.width = len(image[0])
        self.image = np.zeros((self.length, self.width), dtype=int)
        for ind, row in enumerate(image):
            self.image[ind, :] = np.array([1 if c == '#' else 0 for c in row])

    def enhance(self, times: int):

        for time in range(times):
            self.__pad(time)
            self.new_image = np.zeros((self.length + 2*PAD, self.width + 2*PAD), dtype=int)

            for row in range(1, self.length + 3):
                for col in range(1, self.width + 3):
                    self.new_image[row, col] = self.__enhance_pixel(row, col)

            self.image = self.new_image[1: self.length + 3, 1: self.width + 3]
            self.length += 2
            self.width += 2

    def __enhance_pixel(self, row, col):

        string = ''.join([str(self.image[i, j]) for i in range(row - 1, row + 2) for j in range(col - 1, col + 2)])
        return self.enhancement[int(string, 2)]

    def get_answer(self):

        return np.sum(self.new_image)

    def __pad(self, time):

        # If the first bit of enhancement is 1 then if time is even we pad with 0's else with 1's
        if self.enhancement[0] == 1:
            value = 0 if time % 2 == 0 else 1
        else:
            value = 0

        self.image = np.pad(self.image, ((PAD, PAD), (PAD, PAD)), 'constant', constant_values=((value, value), (value, value)))

def process_file(filename):

    with open(filename, 'r') as f:
        data = f.read().rstrip('\n').split('\n')

    enhancement = data[0]
    data = data[2:]

    image = []
    while data:

        image.append(data[0])
        data = data[1:]

    return enhancement, image

if __name__ == "__main__":

    filename = 'input/Day20.txt'
    string, pixels = process_file(filename)
    image = Image(string, pixels)
    image.enhance(times=2)

    answer = image.get_answer()
    print(f'The answer to part one is {answer}')

    image = Image(string, pixels)
    image.enhance(times=50)

    answer = image.get_answer()
    print(f'The answer to part two is {answer}')
