from enum import Enum, auto
from typing import List
import math
import numpy as np

PAD = 2

class Die():

    def __init__(self):

        self.value = 0
        self.rolls = 0

    def roll(self):

        self.value += 1
        self.rolls += 1

class Player():

    def __init__(self, name: str, position: int):

        self.name = name
        self.position = position
        self.score = 0

class Game():

    def __init__(self, p1: Player, p2: Player, die: Die):

        self.p1 = p1
        self.p2 = p2
        self.die = die

    def take_turn(self, player: Player):

        score = 0
        for i in range(3):
            self.die.roll()
            score += self.die.value

        player.position = (player.position + score) % 10
        player.position = 10 if player.position == 0 else player.position
        player.score += player.position

    def play(self):

        while self.p1.score < 1000 and self.p2.score < 1000:

            self.take_turn(self.p1)

            if self.p1.score < 1000:
                self.take_turn(self.p2)

        self.winner = self.p1 if self.p1.score >= 1000 else self.p2
        self.loser = self.p2 if self.p1.score >= 1000 else self.p1
        print(f'{self.winner.name} wins with a score of {self.winner.score}')

    def get_answer(self):

        return self.die.rolls * self.loser.score

def process_file(filename):

    with open(filename, 'r') as f:
        data = f.read().rstrip('\n').split('\n')

    pos1 = int(data[0][data[0].index(':')+2:])
    pos2 = int(data[1][data[1].index(':') + 2:])

    return [pos1, pos2]

if __name__ == "__main__":

    filename = 'input/Day21.txt'
    positions = process_file(filename)

    player1, player2 = Player('Player 1', positions[0]), Player('Player 2', positions[1])
    game = Game(player1, player2, Die())

    game.play()
    print(f'The answer to part one is {game.get_answer()}')

