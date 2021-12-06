import numpy as np
from enum import Enum, auto

CYCLE = 7

class Fish():

    def __init__(self, days):
        self.days = days

class School():

    def __init__(self, fish):
        self.fish = fish

    def __live_a_day(self):

        num_fish = len(self.fish)
        for fish in self.fish[:num_fish]:
            if fish.days == 0:
                fish.days = CYCLE - 1
                self.fish.append(Fish(days=8))
            else:
                fish.days -= 1


    def live_n_days(self, days):

        day = 0
        while day < days:
            self.__live_a_day()
            day += 1

def process_file(filename):

    with open(filename, 'r') as f:
        days = np.loadtxt(f, dtype=int, delimiter=',')
    f.close()

    fish = []
    for day in days:
        fish.append(Fish(day))

    return fish

if __name__ == "__main__":

    filename = "input/test.txt"
    fish = process_file(filename)

    school = School(fish)
    total_days = 256
    school.live_n_days(total_days)
    print(f'The total fish after {total_days} is {len(school.fish)}')
