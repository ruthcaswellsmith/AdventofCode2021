import numpy as np
from enum import Enum, auto

SIZE = 9

class School():

    def __init__(self):
        self.fish = np.zeros(SIZE)

    def populate(self, days: np.ndarray):

        for days_to_spawn in days:
            self.fish[days_to_spawn] += 1

    def __live_a_day(self):

        spawning_fish = self.fish[0]
        for day in range(8):
            self.fish[day] = self.fish[day + 1] + spawning_fish if day == 6 else self.fish[day + 1]
        self.fish[8] = spawning_fish

    def live_n_days(self, days: int):

        for day in range(days):
            self.__live_a_day()

def process_file(filename):

    with open(filename, 'r') as f:
        days = np.loadtxt(f, dtype=int, delimiter=',')
    f.close()

    return days

if __name__ == "__main__":

    filename = "input/Day6.txt"
    days = process_file(filename)

    school = School()
    school.populate(days)
    total_days = 256
    school.live_n_days(total_days)
    print(f'The total fish after {total_days} is {int(sum(school.fish))}')
