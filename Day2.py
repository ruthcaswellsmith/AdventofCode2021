import numpy as np

def part_one(filename=None):

    with open(filename, 'r') as f:
        data = f.read().rstrip('\n').split('\n')
    f.close()

    position = np.zeros(2)
    num_inputs = len(data)
    for ind in range(num_inputs):

        (direction, amount) = data[ind].split(' ')
        if direction == 'forward':
            position[0] += int(amount)
        elif direction == 'up':
            position[1] -= int(amount)
        elif direction == 'down':
            position[1] += int(amount)

    print(f'The answer is {position.prod()}')

def part_two(filename=None):

    with open(filename, 'r') as f:
        data = f.read().rstrip('\n').split('\n')

    position = np.zeros(3)
    num_inputs = len(data)
    for ind in range(num_inputs):

        (direction, amount) = data[ind].split(' ')
        if direction == 'forward':
            position[0] += int(amount)
            position[1] += position[2]*int(amount)
        elif direction == 'up':
            position[2] -= int(amount)
        elif direction == 'down':
            position[2] += int(amount)

    print(f'The answer is {position[0]*position[1]}')

if __name__ == "__main__":

    filename = "input/Day2.txt"

    part_one(filename=filename)

    part_two(filename=filename)
