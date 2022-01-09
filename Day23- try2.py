from enum import Enum, auto
import numpy as np

AMPHIPODS = {'A': 1, 'B': 2, 'C': 3, 'D': 4}
ENERGY = [1, 10, 100, 1000]
ROOMS = [3, 5, 7, 9]
HALLWAY = range(1, 12)


class Burrow:

    def __init__(self, data, energy):
        self.grid = 8 * np.ones((5, 13), dtype=int)
        for j in HALLWAY:
            self.grid[1, j] = 0
        for j in ROOMS:
            for i in [2, 3]:
                self.grid[i, j] = AMPHIPODS[data[i][j]]
        self.hallway = [(1, j) for j in HALLWAY]
        self.upper_rooms = [(2, j) for j in ROOMS]
        self.lower_rooms = [(3, j) for j in ROOMS]
        self.energy = energy
        self.minimum_energy

    def sort(self):

        if self.__burrow_is_sorted():
            return self.energy

        self.__put_amphipods_away()

        self.__move_amphipod_to_hallay()

        for i, room in enumerate(self.lower_rooms):
            if not self.__lower_is_sorted(i + 1):
                # move upper out of the way
                pass

    def __put_amphipods_away(self):
        for i, room in enumerate(self.lower_rooms):
            if self.grid[room] == 0:
                location = self.__find_matching_amphipod(i+1, room)
                if location:
                    self.__move_amphipod(location, room)

    def __find_matching_amphipod(self, value, room):
        locations = np.where(self.grid == value)
        for location in locations:
            if location[1] != ROOMS[value - 1] and self.__path_is_clear(room, location):
                return location

    def __path_is_clear(self, loc1, loc2):

        if loc1 in self.hallway:
            if loc2[1] > loc1[1]:
                for j in range(loc1[1] + 1, loc2[1] + 1):
                    if self.grid[loc1[0], j] != 0:
                        return False
            else:
                for j in range(loc2[1], loc2[1]):
                    if self.grid[loc1[0], j] != 0:
                        return False


    def __burrow_is_sorted(self):
        for i in range(1, 5):
            if not self.__room_is_sorted(i):
                return False
        return True

    def __upper_is_sorted(self, i):
        return True if self.grid[self.upper_rooms[i-1]] == i else False

    def __lower_is_sorted(self, i):
        return True if self.grid[self.lower_rooms[i-1]] == i else False

    def __room_is_sorted(self, i):
        return True if self.__lower_is_sorted(i) and self.__upper_is_sorted(i) else False

    def __calculate_energy(self, location1, location2):
        return self.grid[location1] * (abs(location1[0] - location2[0]) + abs(location1[1] - location2[1]))

def process_file(filename):

    with open(filename, 'r') as f:
        data = f.read().rstrip('\n').split('\n')

    return data

if __name__ == "__main__":

    filename = 'input/test23.txt'
    burrow = Burrow(process_file(filename))
    print('hi')