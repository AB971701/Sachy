from Chess import Chess
import random

class Minimax:
    depth = 5

    def __init__(self, Chess):
        self.chess = Chess

    def minmax(self, board = self.chess.board, white_plays = self.chess.white_plays , deep = 0):
        """
        INDEX_TO_LETTER = {0: "a", 1: "b", 2: "c", 3: "d", 4: "e", 5: "f", 6: "g", 7: "h"}
        INDEX_TO_NUMBER = {0: 8, 1: 7, 2: 6, 3: 5, 4: 4, 5: 3, 6: 2, 7: 1}
        :param board:
        :param deep:
        :return:
        """
        possible_moves = []
        if Chess.check_checkmate() == True:
            if white_plays == True:
                # Chess.white_plays
                minimax = -1
            else:
                minimax = 1
        else:
            if deep == self.depth:
                self.GiveValue()
            else:
                if white_plays:
                for column in board:
                    for row in column:
                        if board[column][row] in "Kk":
                            possible_moves.append([self.chess.INDEX_TO_LETTER + self.chess.INDEX_TO_NUMBER,
                                                   self.chess.get_king_moves(self.chess.INDEX_TO_LETTER, self.chess.INDEX_TO_NUMBER)])
                        else if




    def GiveValue(self):
        return random.uniform(-1, 1)