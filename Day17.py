from enum import Enum, auto
import pandas as pd

DF_COLS = ['result', 'vxo', 'vyo', 'x', 'y', 'steps', 'maxy']

class Part(str, Enum):

    PART_ONE = auto()
    PART_TWO = auto()

class Result(str, Enum):

    OVERSHOT = "overshot"
    UNDERSHOT = "undershot"
    PASSED = "passed through"
    HIT = "hit"

class Target():

    def __init__(self, positions):

        self.x_min = positions[0]
        self.x_max = positions[1]
        self.y_min = positions[2]
        self.y_max = positions[3]

class Projectile():

    def __init__(self, target: Target):

        self.target = target

    def get_answer(self, part: Part):

        if part == Part.PART_ONE:
            return self.df[self.df['result'] == Result.HIT]['maxy'].max()
        else:
            return self.df[self.df['result'] == Result.HIT].shape[0]

    def iterate(self, vx_min, vx_max, vy_min, vy_max):

        results = []
        for vx in range(vx_min, vx_max):
            for vy in range(vy_min, vy_max):
                self.launch(vx, vy)
                if self.result == Result.HIT:
                    print('got a hit')
                results.append([self.result, vx, vy, self.x, self.y, self.steps, self.max_y ])
        self.df = pd.DataFrame(results)
        self.df.columns = DF_COLS

    def launch(self, vx: int, vy: int):

        self.vx, self.vy = vx, vy
        self.x, self.y = 0, 0
        self.result = ""
        self.max_y = 0
        self.steps = 0

        while not (self.result):
            self.step()
            self.steps += 1

    def step(self):

        self.x += self.vx
        self.y += self.vy
        self.vx += 1 if self.vx < 0 else (-1 if self.vx > 0 else 0)
        self.vy -= 1
        self.max_y = max(self.max_y, self.y)

        if self.x > target.x_max and self.y < target.y_min:
            self.result = Result.OVERSHOT
        elif self.x < target.x_min and self.y < target.y_min:
            self.result = Result.UNDERSHOT
        elif (target.x_min <= self.x <= target.x_max) and (target.y_min <= self.y <= target.y_max):
            self.result = Result.HIT
        elif self.y < target.y_min:
            self.result = Result.PASSED

def process_file(filename):

    with open(filename, 'r') as f:
        data = f.read().rstrip('\n').split('\n')

    data = data[0]
    x_min = int(data[data.index("=") + 1: data.index("..")])
    x_max = int(data[data.index("..") + 2: data.index(",")])
    data = data[data.index(","):]
    y_min = int(data[data.index("=") + 1: data.index("..")])
    y_max = int(data[data.index("..") + 2:])

    return x_min, x_max, y_min, y_max

if __name__ == "__main__":

    filename = "input/Day17.txt"
    target = Target(process_file(filename))
    projectile = Projectile(target)
    projectile.iterate(0, 200, -200, 200)
    print(f'The highest point reached while still hitting the target was {projectile.get_answer(part=Part.PART_ONE)}')
    print(f'The number of velocity values that result in hits is {projectile.get_answer(part=Part.PART_TWO)}')
