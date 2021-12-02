import numpy as np

def count_increases(measurements):

    counter = 0
    num_measurmeents = len(measurements)
    for ind in range(1, num_measurmeents):
        counter = counter + 1 if measurements[ind] > measurements[ind-1] else counter

    return counter

def part_one(filename=None):

    measurements = np.loadtxt(filename)

    print(f'{count_increases(measurements)} measurements are larger than the previous measurement')

def part_two(filename=None):

    measurements = np.loadtxt(filename)

    three_window_measurements = np.zeros(len(measurements)-2)

    for ind in range(2,len(measurements)):
        three_window_measurements[ind-2] = measurements[ind] + measurements[ind-1] + measurements[ind-2]

    print(f'{count_increases(three_window_measurements)} measurements are larger than the previous measurement')

if __name__ == "__main__":

    filename = "input/Day1.txt"

    part_one(filename=filename)

    part_two(filename=filename)
