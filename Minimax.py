from Chess import Chess
import random
from copy import deepcopy

class Minimax:
    depth = 3

    def __init__(self, Chess):
        self.chess = Chess

    def minmax(self, deep = 0):
        """
        LETTER_TO_INDEX = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}
        INDEX_TO_LETTER = {0: "a", 1: "b", 2: "c", 3: "d", 4: "e", 5: "f", 6: "g", 7: "h"}
        NUMBER_TO_INDEX = {1: 7, 2: 6, 3: 5, 4: 4, 5: 3, 6: 2, 7: 1, 8: 0}
        INDEX_TO_NUMBER = {0: 8, 1: 7, 2: 6, 3: 5, 4: 4, 5: 3, 6: 2, 7: 1}
        :param board:
        :param deep:
        :return:
        """
        possible_moves = []
        values = []
        white_plays = self.chess.white_plays
        if self.chess.check_checkmate() == True:
            if white_plays:
                # Chess.white_plays
                return -1
            else:
                return 1
        else:
            if deep == self.depth:
                return self.GiveValue()
            else:
                board = deepcopy(self.chess.board)
                for column in range(len(board[0])):
                    for row in range(len(board[0])):
                        possible_moves.append([self.chess.INDEX_TO_LETTER[row] + str(self.chess.INDEX_TO_NUMBER[column]),
                                               self.chess.get_moves(self.chess.INDEX_TO_LETTER[row], self.chess.INDEX_TO_NUMBER[column])])
            for piece in possible_moves:  # TODO
                if piece[1] is not None:
                    for move in piece[1]:
                        self.chess.move(piece[0], move, False)
                        self.chess.white_plays = white_plays
                        values.append([piece[0], move, self.minmax(deep + 1)])
                        self.chess.board = deepcopy(board)

            if deep == 0:
                if white_plays:
                    self.chess.move(max(values, key=lambda x: x[2])[0], max(values, key=lambda x: x[2])[1])
                else:
                    self.chess.move(min(values, key=lambda x: x[2])[0], min(values, key=lambda x: x[2])[1])
            if white_plays:
                return max(values, key=lambda x: x[2])[2]
            else:
                return min(values, key=lambda x: x[2])[2]

    def GiveValue(self):
        return random.uniform(-1, 1)