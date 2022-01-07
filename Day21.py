from enum import Enum
import numpy as np

class PlayerName(str, Enum):
    PLAYER_ONE = 'Player 1'
    PLAYER_TWO = 'Player 2'

POINTS = {3: 1, 4: 3, 5: 6, 6: 7, 7: 6, 8:3, 9:1}

def get_new_players(player1, player2, turn):

    p1 = Player(name=PlayerName.PLAYER_ONE,
                active=player1.active,
                position=player1.position,
                score=player1.score,
                roll=player1.roll,
                points=turn if player1.active else 0)
    p2 = Player(name=PlayerName.PLAYER_TWO,
                active=player2.active,
                position=player2.position,
                score=player2.score,
                roll=player2.roll,
                points=turn if player2.active else 0)
    return p1, p2

class DeterministicDie:

    def __init__(self):
        self.value = 0
        self.rolls = 0

    def roll(self):
        self.value += 1
        self.rolls += 1

class Player:

    def __init__(self, name: str, active: bool, position: int, score: int, roll: int, points: int):
        self.name = name
        self.position = position
        self.score = score
        self.active = active
        self.roll = roll
        self.points = points

    def move(self):
        self.position = (self.position + self.points) % 10
        self.position = 10 if self.position == 0 else self.position
        self.score += self.position


class Game:

    def __init__(self, p1: Player, p2: Player):
        self.p1 = p1
        self.p2 = p2

    def get_active_player(self):
        return self.p1 if self.p1.active else self.p2

    def switch_active_player(self):
        if self.p1.active:
            self.p1.active, self.p2.active = False, True
        else:
            self.p1.active, self.p2.active = True, False
        self.p1.roll, self.p1.points, self.p2.roll, self.p2.points = 1, 0, 1, 0

    def set_winner_loser(self):
        self.winner = self.p1 if self.p1.score >= self.SCORE_TO_WIN else self.p2
        self.loser = self.p2 if self.p1.score >= self.SCORE_TO_WIN else self.p1


class DeterministicGame(Game):

    def __init__(self, p1: Player, p2: Player):
        super().__init__(p1=p1, p2=p2)
        self.SCORE_TO_WIN = 1000
        self.die = DeterministicDie()

    def play(self):

        while self.p1.score < self.SCORE_TO_WIN and self.p2.score < self.SCORE_TO_WIN:
            self.take_turn(self.get_active_player())
            self.switch_active_player()

        self.set_winner_loser()
        print(f'{self.winner.name} wins with a score of {self.winner.score}')

    def take_turn(self, player: Player):

        player.points = 0
        while player.roll < 4:
            self.die.roll()
            player.points += self.die.value
            player.roll += 1
        player.move()

    def get_answer(self):
        return self.die.rolls * self.loser.score


class QuantumGame(Game):

    def __init__(self, p1: Player, p2: Player):
        super().__init__(p1=p1, p2=p2)
        self.SCORE_TO_WIN = 21

    def play(self, turns, wins):

        player = self.get_active_player()
        player.move()
        if player.score >= self.SCORE_TO_WIN:
            wins[player.name] += np.prod([POINTS[turn] for turn in turns])
            return
        self.switch_active_player()

        for turn in POINTS.keys():
            p1, p2 = get_new_players(self.p1, self.p2, turn)
            game = QuantumGame(p1, p2)
            game.play(turns + [turn], wins)

    def get_answer(self):

        pass


def process_file(filename):

    with open(filename, 'r') as f:
        data = f.read().rstrip('\n').split('\n')

    pos1 = int(data[0][data[0].index(':')+2:])
    pos2 = int(data[1][data[1].index(':') + 2:])

    return [pos1, pos2]

if __name__ == "__main__":

    filename = 'input/test.txt'
    positions = process_file(filename)
    player1 = Player(name=PlayerName.PLAYER_ONE,
                     active=True,
                     position=positions[0],
                     score=0,
                     roll=1,
                     points=0)
    player2 = Player(name=PlayerName.PLAYER_TWO,
                     active=False,
                     position=positions[1],
                     score=0,
                     roll=1,
                     points=0)
    game = DeterministicGame(player1, player2)
    game.play()
    print(f'The answer to part one is {game.get_answer()}')

    player1 = Player(name=PlayerName.PLAYER_ONE,
                     active=True,
                     position=positions[0],
                     score=0,
                     roll=0,
                     points=0)
    player2 = Player(name=PlayerName.PLAYER_TWO,

                     active=False,
                     position=positions[1],
                     score=0,
                     roll=0,
                     points=0)

    wins = {PlayerName.PLAYER_ONE: 0, PlayerName.PLAYER_TWO: 0}
    for turn in POINTS.keys():
        p1, p2 = get_new_players(player1, player2, turn)
        game = QuantumGame(p1, p2)
        game.play([turn], wins)
    print(f'{wins}')
