from enum import Enum, auto
import regex as re
import math
import numpy as np

SIZE = 2000
OFFSET = 1000
MATCH = 12


class Report():

    def __init__(self, scanners):

        self.scanners = []
        for scanner in scanners:
            self.scanners.append(Scanner(scanner))

class Scanner():

    def __init__(self, scanner):

        self.num = scanner['num']
        self.cube = np.zeros((SIZE, SIZE, SIZE), dtype=bool)
        self.beacons = []
        for pt in scanner['coords']:
            self.cube[int(pt[0]) + OFFSET, int(pt[1]) + OFFSET, int(pt[2]) + OFFSET] = True
            self.beacons.append([int(pt[0]), int(pt[1]), int(pt[2])])
        self.matches = []

    def __do_four_rots(self, cube, axes):

        for i in range(4):
            rotated = np.rot90(cube, i, axes)
            match = self.__match(rotated)
            if match:
                return match

    def rotate_and_match(self, scanner):

        match = self.__do_four_rots(scanner.cube, axes=(1, 2))
        if match:
            self.matches.append([scanner.num, match])
            return

        rotated = np.rot90(scanner.cube, 2, axes=(0, 2))
        match = self.__do_four_rots(rotated, axes=(1, 2))
        if match:
            self.matches.append([scanner.num, match])
            return

        rotated = np.rot90(scanner.cube, 2, axes=(0, 2))
        match = self.__do_four_rots(rotated, axes=(0, 1))
        if match:
            self.matches.append([scanner.num, match])
            return

        rotated = np.rot90(scanner.cube, -1, axes=(0, 2))
        match = self.__do_four_rots(rotated, axes=(0, 1))
        if match:
            self.matches.append([scanner.num, match])
            return

        rotated = np.rot90(scanner.cube, axes=(0, 1))
        match = self.__do_four_rots(rotated, axes=(0, 2))
        if match:
            self.matches.append([scanner.num, match])
            return

        rotated = np.rot90(scanner.cube, -1, axes=(0, 1))
        match = self.__do_four_rots(rotated, axes=(0, 2))
        if match:
            self.matches.append([scanner.num, match])
            return

    def __match(self, cube):

        # For each scanner look at rotated cube and see if we have a match
        matches = 0
        for beacon in self.beacons:
            if cube[beacon[0], beacon[1], beacon[2]]:
                matches += 1
        if matches >= 12:
            return True

        return None

def process_file(filename):

    with open(filename, 'r') as f:
        data = f.read().rstrip('\n').split('\n')

    scanners = []
    while data:

        scanner = {}
        scanner_line = data[0]
        print(scanner_line)
        ind1 = scanner_line.index('--- scanner ') + len('--- scanner ') - 1
        ind2 = scanner_line.rfind(' ---')
        scanner['num'] = scanner_line[ind1 + 1: ind2]
        data = data[1:]

        scanner['coords'] = []
        num_line = data[0]
        while num_line:
            scanner['coords'].append(data[0].split(','))
            data = data[1:] if len(data) > 1 else None
            num_line = data[0] if data else None

        scanners.append(scanner)
        data = data[1:] if data else None

    return scanners


if __name__ == "__main__":

    filename = 'input/test.txt'
    scanners = process_file(filename)

    report = Report(scanners)
    report.scanners[0].rotate_and_match(report.scanners[1])

    print('hi')

