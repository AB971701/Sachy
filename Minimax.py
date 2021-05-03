from Chess import Chess, PromotePawnException
import random
from copy import deepcopy

class Minimax:
    depth = 2

    def __init__(self, Chess):
        self.chess = Chess

    def minmax(self, deep = 0):
        """
        This is the recursive main function
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
        """
        Checks if we reached checkmate or stalemate, if yes, return value acording to who won 
        """
        if self.chess.check_checkmate() == True:
            if self.chess.check_stalemate():
                return 0
            if white_plays:
                # Chess.white_plays
                return -50
            else:
                return 50
        else:
            """
            Check how deep in recursion you are, if at he bottom, get Value of position
            """
            if deep == self.depth:
                return self.GiveValue()
            else:
                """
                Otherwise copy current board and find all the possible moves of all pieces
                """
                board = deepcopy(self.chess.board)
                for column in range(len(board[0])):
                    for row in range(len(board[0])):
                        possible_moves.append([self.chess.INDEX_TO_LETTER[row] + str(self.chess.INDEX_TO_NUMBER[column]),
                                               self.chess.get_moves(self.chess.INDEX_TO_LETTER[row], self.chess.INDEX_TO_NUMBER[column])])
            """
            Check all the possible moves and go deeper in minimax
            """
            for piece in possible_moves:
                if piece[1] is not None:
                    for move in piece[1]:
                        try:
                            self.chess.move(piece[0], move, False)
                        except PromotePawnException:
                            self.chess.promote_pawn('q', False)
                        self.chess.white_plays = white_plays
                        self.chess.game_over = False
                        values.append([piece[0], move, self.minmax(deep + 1)])
                        self.chess.board = deepcopy(board)

            if deep == 0:
                """
                if at depth 0, this means we already finished all the other loops and now have an evaluated position so make real move
                """
                try:
                    if white_plays:
                        self.chess.move(max(values, key=lambda x: x[2])[0], max(values, key=lambda x: x[2])[1])
                    else:
                        self.chess.move(min(values, key=lambda x: x[2])[0], min(values, key=lambda x: x[2])[1])
                except PromotePawnException:
                    """
                    Queen is the best in most situations, so automaticaly promote to queen
                    """
                    self.chess.promote_pawn('q')
            if white_plays:
                """
                returns minmax value of current position
                """
                return max(values, key=lambda x: x[2])[2]
            else:
                return min(values, key=lambda x: x[2])[2]

    def GiveValue(self):
        """
        evaluates current position
        :return:
        """
        pieces_w = 0
        pieces_b = 0
        for row in self.chess.board:
            for piece in row:
                if piece is not None:
                    if piece.isupper():
                        if piece == "Q":
                            pieces_w += 9
                        elif piece == "R":
                            pieces_w += 5
                        elif piece == "B":
                            pieces_w += 3
                        elif piece == "N":
                            pieces_w += 3
                        elif piece == "P":
                            pieces_w += 1
                    else:
                        if piece == "q":
                            pieces_b += 9
                        elif piece == "r":
                            pieces_b += 5
                        elif piece == "b":
                            pieces_b += 3
                        elif piece == "n":
                            pieces_b += 3
                        elif piece == "p":
                            pieces_b += 1
        return (pieces_w - pieces_b) + random.uniform(-5, 5)

    def NewChess(self, chess):
        """
        Takes a new chess board after starting a new game or loading a new game
        :param chess: new chess board
        :return:
        """
        self.chess = chess
