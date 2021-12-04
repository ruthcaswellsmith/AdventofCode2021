import numpy as np

SIZE = 5


class Game():

    def __init__(self, boards, numbers):

        self.numbers = numbers
        self.boards = boards
        self.num_boards = len(self.boards)
        self.winners = [0] * self.num_boards

    def __get_new_number(self):

        new_number = self.numbers[0]
        self.numbers = self.numbers[1:]
        return new_number

    def __play_round(self, number):

        for board in self.boards:
            board.play_number(number)

        for board_num, board in enumerate(self.boards):
            self.winners[board_num] = board.is_winner

    def play_game(self, game_type):

        if game_type == '1':

            while sum(self.winners) == 0:
                current_number = self.__get_new_number()
                self.__play_round(current_number)

            winning_board = self.boards[self.winners.index(True)]
            print(f'The winning score is {winning_board.get_score(current_number)}')

        elif game_type == '2':

            while sum(self.winners) < self.num_boards:
                last_winner = self.winners.index(False)

                current_number = self.__get_new_number()
                self.__play_round(current_number)

            last_winning_board = self.boards[last_winner]
            print(f'The final score of the final board is {last_winning_board.get_score(current_number)}')


class Board():

    def __init__(self, squares):
        self.squares = squares
        self.matched = np.zeros((SIZE, SIZE), dtype=bool)
        self.is_winner = False

    def play_number(self, number):
        self.matched = np.where(self.squares == number, True, self.matched)

        if SIZE in self.matched.sum(axis=0) or SIZE in self.matched.sum(axis=1):
            self.is_winner = True

    def get_score(self, current_number):
        return current_number * self.squares[np.where(self.matched == False)].sum()


def process_file(filename):
    with open(filename, 'r') as f:
        data = f.read().rstrip('\n').split('\n')
    f.close()

    numbers = np.array(data[0].split(',')).astype(int)
    data = data[2:]

    boards = []
    board_num = 0

    while data:

        squares = []
        for i in range(SIZE):
            row = [int(data[i][ind:ind + 2]) for ind in [j * 3 for j in range(SIZE)]]
            squares.append(row)

        boards.append(Board(np.array(squares).astype(int)))

        data = data[6:] if len(data) > 5 else None

    return Game(boards, numbers)


if __name__ == "__main__":
    filename = "input/test.txt"

    game = process_file(filename)

    game.play_game(game_type='1')

    game.play_game(game_type='2')
