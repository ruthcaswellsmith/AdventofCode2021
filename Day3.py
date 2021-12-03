import numpy as np
from scipy import stats
from functools import reduce
from stream import Stream

def part_one(array=None):

    modes = stats.mode(array)[0][0]

    gamma = to_decimal(modes)
    epsilon = to_decimal(1 - modes)

    print(f'The power consumption is {gamma*epsilon}')

def bit_critera(array, type='oxygen'):

    count_0 = np.count_nonzero(array==0)
    count_1 = np.count_nonzero(array==1)

    if count_0 == count_1:
        if type == 'oxygen':
            return 1
        else:
            return 0
    else:
        if type == 'oxygen':
            return 1 if count_1 > count_0 else 0
        else:
            return 1 if count_1 < count_0 else 0

def part_two(array=None):

    saved_array = array
    j = 0
    while len(array) > 1:

        bit = bit_critera(array[:,j], type='oxygen')

        # Now filter our array to just those which match that bit
        array = np.array(Stream(array).filter(lambda x: x[j] == bit).toList())

        j += 1

    oxygen_rating = to_decimal(array[0])
    print(f'The oxygen generator rating is {oxygen_rating}')

    array = saved_array
    j = 0
    while len(array) > 1:

        bit = bit_critera(array[:, j], type='C02')

        rows = np.where(array[:,j] == bit)
        array = array[rows]

        j += 1

    CO2_rating = to_decimal(array[0])
    print(f'The CO2 scrubber rating is {CO2_rating}')

    print(f'the life support rating is {oxygen_rating * CO2_rating}')

def to_decimal(binary_array):
    return reduce(lambda a, b: 2 * a + b, binary_array)

def convert_to_array(filename):

    with open(filename, 'r') as f:
        data = f.read().rstrip('\n').split('\n')
    f.close()

    array = []
    num_rows = len(data)
    for i in range(num_rows):
        array.append([int(c) for c in data[i]])

    return np.array(array)

if __name__ == "__main__":

    filename = "input/Day3.txt"
    array = convert_to_array(filename)

    part_one(array=array)

    part_two(array=array)
