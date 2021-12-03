import numpy as np
from scipy import stats
from functools import reduce

class Report():

    def __init__(self, array):

        self.array = array

    def get_power_consumption(self):

        modes = stats.mode(self.array)[0][0]

        gamma = self.__to_decimal(modes)
        epsilon = self.__to_decimal(1 - modes)

        print(f'The power consumption is {gamma * epsilon}')

    def get_life_support_rating(self):

        oxygen_rating = self.__get_rating(type='oxygen')
        print(f'The oxygen generator rating is {oxygen_rating}')

        CO2_rating = self.__get_rating(type='CO2')
        print(f'The CO2 scrubber rating is {CO2_rating}')

        print(f'the life support rating is {oxygen_rating * CO2_rating}')

    def __get_rating(self, type='oxygen'):

        array = self.array
        j = 0
        while len(array) > 1:
            bit = self.__bit_critera(array[:, j], type=type)

            rows = np.where(array[:, j] == bit)
            array = array[rows]

            j += 1

        return self.__to_decimal(array[0])

    @staticmethod
    def __to_decimal(binary_array):
        return reduce(lambda a, b: 2 * a + b, binary_array)

    @staticmethod
    def __bit_critera(array, type='oxygen'):

        count_0 = np.count_nonzero(array == 0)
        count_1 = np.count_nonzero(array == 1)

        if count_0 == count_1:
            return 1 if type == 'oxygen' else 0

        elif count_1 > count_0:
            return 1 if type == 'oxygen' else 0

        else:
            return 0 if type == 'oxygen' else 1


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

    report = Report(array)

    report.get_power_consumption()

    report.get_life_support_rating()