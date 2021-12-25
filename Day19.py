from enum import Enum, auto
from typing import List
import math
import numpy as np

SIZE = 1000
MATCH = 12
IDENTITY = np.identity(3)
ZERO_OFFSET = np.array([0,0,0])

def rotation_matrices():

    # Four rotations about x
    four_matrices = []
    for theta in [0, math.pi / 2, math.pi, 3 * math.pi / 2]:
        four_matrices.append(np.array([[1, 0, 0],
                                       [0, round(math.cos(theta)), -round(math.sin(theta))],
                                       [0, round(math.sin(theta)), round(math.cos(theta))]]))

    six_matrices = []
    # 0, 90, 180, 270 degrees about y
    for theta in [0, math.pi / 2, math.pi, 3 * math.pi / 2]:
        six_matrices.append(np.array([[round(math.cos(theta)), 0, -round(math.sin(theta))],
                                       [0, 1, 0],
                                       [round(math.sin(theta)), 0, round(math.cos(theta))]]))

    # 90, 270 degrees about z
    for theta in [math.pi / 2, 3 * math.pi / 2]:
        six_matrices.append(np.array([[round(math.cos(theta)), -round(math.sin(theta)), 0],
                                       [round(math.sin(theta)), round(math.cos(theta)), 0],
                                       [0, 0, 1]]))

    rotation_matrices = []
    for mat2 in six_matrices:
        for mat1 in four_matrices:
            rotation_matrices.append(np.matmul(mat2, mat1))

    return rotation_matrices

class Report():

    def __init__(self, scanners):

        self.scanners = []
        for scanner in scanners:
            self.scanners.append(Scanner(scanner))
        self.num_scanners = len(self.scanners)
        self.ROTATION_MATRICES = rotation_matrices()

    @staticmethod
    def unique(a):
        # Credit Bi Rico Stack Overflow
        order = np.lexsort(a.T)
        a = a[order]
        diff = np.diff(a, axis=0)
        ui = np.ones(len(a), 'bool')
        ui[1:] = (diff != 0).any(axis=1)
        return a[ui]

    def get_max_manhattan_dist(self):

        max_dist = 0
        for ind1 in range(self.num_scanners):
            for ind2 in range(ind1 + 1, self.num_scanners):
                max_dist = max(max_dist, self.__manhattan_dist(
                    self.scanners[:, ind1], self.scanners[:, ind2]))
        return max_dist

    @staticmethod
    def __manhattan_dist(beacon1, beacon2):

        dist = 0
        for i in range(3):
            dist += abs(beacon1[i] - beacon2[i])
        return int(dist)

    def match_scanners_recursive(self, scanner):

        unmatched = self.__get_unmatched_scanners()
        while unmatched:
            for ind2 in unmatched:
                if int(scanner.num) != ind2 and not self.scanners[ind2].matched:
                    if self.match(scanner, self.scanners[ind2]):
                        print(f'matched {scanner.num} and {ind2}')
                        self.match_scanners_recursive(self.scanners[ind2])
            return

    def get_list_of_scanners(self, scanner, matrix, offsets):

        print(f'getting scanner coordinates from scanner {scanner.num}')
        if not scanner.matches:
            return np.array([])

        scanners = []
        for match in scanner.matches:
            scanners.append(match.offsets)
        scanners = np.array(scanners).T

        for match in scanner.matches:
            scanners_from_matches = self.get_list_of_scanners(\
                self.scanners[int(match.scanner)], match.matrix, match.offsets)
            if scanners_from_matches.shape[0] > 0:
                scanners = np.vstack((scanners.T, scanners_from_matches)).T

        return np.matmul(matrix, scanners).T + offsets

    def get_list_of_beacons(self, scanner, matrix, offsets):

        print(f'getting beacons from scanner {scanner.num}')
        beacons = scanner.beacons
        for match in scanner.matches:
            beacons = np.concatenate((beacons, self.get_list_of_beacons(\
                self.scanners[int(match.scanner)], match.matrix, match.offsets)), axis=1)

        return (np.matmul(matrix, beacons).T - offsets).T

    def match_scanners(self):

        for ind1 in range(self.num_scanners):
            for ind2 in range(ind1 + 1, self.num_scanners):
                if self.match(self.scanners[ind1], self.scanners[ind2]):
                    print(f'matched {ind1} and {ind2}')

    def __get_unmatched_scanners(self):

        return [ind for ind in range(self.num_scanners) if not self.scanners[ind].matched]

    def match(self, scanner1, scanner2):

        print(f'trying to match {scanner1.num} and {scanner2.num}')

        # First we rotate scanner2, then we try to match 12 beacons
        for matrix in self.ROTATION_MATRICES:
            rotated = np.matmul(matrix, scanner2.beacons)

            for ind1 in range(scanner1.num_beacons):
                for ind2 in range(ind1, scanner2.num_beacons):
                    offsets = rotated[:, ind2] - scanner1.beacons[:, ind1]
                    rotated_offset = (rotated.T - offsets).T
                    matches = []
                    for i in range(scanner1.num_beacons):
                        if (rotated_offset.T == scanner1.beacons[:, i]).all(axis=1).any():
                            matches.append(rotated_offset.T[(rotated_offset.T == scanner1.beacons[:, i]).all(axis=1)])
                    if len(matches) >= 12:
                        match = Match(scanner2.num, matrix, offsets, matches)
                        scanner1.matches.append(match)
                        scanner1.matched = True
                        scanner2.matched = True
                        return True
        return False

class Scanner():

    def __init__(self, scanner):

        self.num = scanner['num']
        self.beacons = []
        for pt in scanner['coords']:
            self.beacons.append([int(pt[0]), int(pt[1]), int(pt[2])])
        self.beacons = np.array(self.beacons).T
        self.num_beacons = self.beacons.shape[1]
        self.matches = []
        self.matched = False

class Match():
    def __init__(self, num: str, matrix: np.ndarray, offsets: np.ndarray, matches: List):

        self.scanner = num
        self.matrix = matrix
        self.offsets = offsets
        self.matches = matches

def process_file(filename):

    with open(filename, 'r') as f:
        data = f.read().rstrip('\n').split('\n')

    scanners = []
    while data:

        scanner = {}
        scanner_line = data[0]
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

    filename = 'input/Day19.txt'
    scanners = process_file(filename)

    report = Report(scanners)
    report.match_scanners_recursive(report.scanners[0])
    report.beacons = report.unique(report.get_list_of_beacons(report.scanners[0], IDENTITY, ZERO_OFFSET).T).T
    print(f'The answer to part one is {report.beacons.shape[1]}')

    report.scanners = (report.get_list_of_scanners(report.scanners[0], IDENTITY, ZERO_OFFSET.T)).T
    report.scanners = np.concatenate((report.scanners, np.array([ZERO_OFFSET]).T), axis=1)
    manhattan = report.get_max_manhattan_dist()
    print(f'The answer to part two is {manhattan}')

