from enum import Enum, auto

PAD = 2


class PlayerName(str, Enum):
    PLAYER_ONE = 'Player 1'
    PLAYER_TWO = 'Player 2'


class TypeOfDie(str, Enum):
    DETERMINISTIC = auto()
    QUANTUM = auto()


class Die:

    def __init__(self):
        self.value = 0


class DeterministicDie(Die):

    def __init__(self):
        super().__init__()
        self.rolls = 0

    def roll(self):
        self.value += 1
        self.rolls += 1


class QuantumDie(Die):

    @staticmethod
    def roll(num: int):
        return num


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
        self.die = QuantumDie()

    def play(self, wins):

        player = self.get_active_player()
        if player.roll == 3:
            player.move()
            if player.score >= self.SCORE_TO_WIN:
                self.set_winner_loser()
                wins[self.winner.name] += 1
                if player.name == PlayerName.PLAYER_ONE:
                    print(f'{player.name} wins {wins[PlayerName.PLAYER_ONE]}')
                return
            self.switch_active_player()
        else:
            player.roll += 1

        p1, p2 = self.__get_new_players(points=1)
        qg1 = QuantumGame(p1, p2)
        qg1.play(wins)
        p1, p2 = self.__get_new_players(points=2)
        qg2 = QuantumGame(p1, p2)
        qg2.play(wins)
        p1, p2 = self.__get_new_players(points=3)
        qg3 = QuantumGame(p1, p2)
        qg3.play(wins)

    def __get_new_players(self, points):

        p1 = Player(name=PlayerName.PLAYER_ONE,
                    active=self.p1.active,
                    position=self.p1.position,
                    score=self.p1.score,
                    roll=self.p1.roll,
                    points=self.p1.points + points if self.p1.active else 0)
        p2 = Player(name=PlayerName.PLAYER_TWO,
                    active=self.p2.active,
                    position=self.p2.position,
                    score=self.p2.score,
                    roll=self.p2.roll,
                    points=self.p2.points + points if self.p2.active else 0)
        return p1, p2

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
    game = QuantumGame(player1, player2)
    wins = {PlayerName.PLAYER_ONE: 0, PlayerName.PLAYER_TWO: 0}
    game.play(wins=wins)
  #   print(f'The answer to part two is {game.get_answer()}')

