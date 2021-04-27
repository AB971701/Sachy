from Chess import Chess
import random

class Minimax:
    depth = 5

    def __init__(self, Chess):
        #Chess.white_plays
        if Chess.check_checkmate() == True:
            if Chess.white_plays == True:
                minimax = -1
            else:
                minimax = 1
    def GiveValue(self):
        return random.uniform(-1, 1)