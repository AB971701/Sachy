from Chess import Chess
from ChessGUI import ChessGUI

last_click = None
possible_moves = []

def play_from_file(filepath):
    c = Chess()
    with open(filepath) as file:
        moves = [(move.strip()).split(',') for move in file]
    for move in moves:
        print('white plays' if c.white_plays else 'black plays')
        if c.move(move[0], move[1]):
            c.print_board()
            print()
        else:
            print('invalid move')
            break
    c.save_to_file("save.txt")

"""
        if piece == 'pP':
            possible_moves = chess.get_pawn_moves(chess.INDEX_TO_LETTER[int((event.x - 50 )/ 100)], chess.INDEX_TO_NUMBER[int((event.y - 50 )/ 100)]):
            print(possible_moves)
        elif piece == 'rR':
            if end_position in self.get_rook_moves(file, rank):
                return True
        elif piece == 'nN':
            if end_position in self.get_knight_moves(file, rank):
                return True
        elif piece == 'bB':
            if end_position in self.get_bishop_moves(file, rank):
                return True
        elif piece == 'qQ':
            if end_position in self.get_queen_moves(file, rank):
                return True
        elif piece == 'kK':
            if end_position in self.get_king_moves(file, rank):
                return True
"""

def callback(event):
    #mouse click funtion
    global last_click, chess, gui, possible_moves
    piece = chess.board[int((event.y - 50) / 100)][int((event.x - 50) / 100)]
    #last click is the previous click
    if event.x >= 50 and event.x <= 850 and event.y >= 50 and event.y <= 850:
        gui.ChangeColor('pale goldenrod', 'dark olive green')
        gui.possible_moves.clear()
        if piece != None:
            if piece in 'pP':
                possible_moves = chess.get_pawn_moves(chess.INDEX_TO_LETTER[int((event.x - 50) / 100)],
                                                      chess.INDEX_TO_NUMBER[int((event.y - 50) / 100)])

            elif piece in 'rR':
                possible_moves = chess.get_rook_moves(chess.INDEX_TO_LETTER[int((event.x - 50) / 100)],
                                                      chess.INDEX_TO_NUMBER[int((event.y - 50) / 100)])

            elif piece in 'bB':
                possible_moves = chess.get_bishop_moves(chess.INDEX_TO_LETTER[int((event.x - 50) / 100)],
                                                      chess.INDEX_TO_NUMBER[int((event.y - 50) / 100)])

            elif piece in 'nN':
                possible_moves = chess.get_knight_moves(chess.INDEX_TO_LETTER[int((event.x - 50) / 100)],
                                                      chess.INDEX_TO_NUMBER[int((event.y - 50) / 100)])

            elif piece in 'qQ':
                possible_moves = chess.get_queen_moves(chess.INDEX_TO_LETTER[int((event.x - 50) / 100)],
                                                        chess.INDEX_TO_NUMBER[int((event.y - 50) / 100)])

            elif piece in 'kK':
                possible_moves = chess.get_king_moves(chess.INDEX_TO_LETTER[int((event.x - 50) / 100)],
                                                        chess.INDEX_TO_NUMBER[int((event.y - 50) / 100)])


        for move in possible_moves:
            print(str(chess.LETTER_TO_INDEX[move[0]]) + move[1])
            gui.possible_moves.append(gui.squares[56 + int(chess.LETTER_TO_INDEX[move[0]]) - 8 * (int(move[1]) - 1)])
        gui.ChangeColor('seashell3', 'seashell4')
    if last_click != None:
            if chess.move(last_click, chess.INDEX_TO_LETTER[int((event.x - 50 )/ 100)] + str(chess.INDEX_TO_NUMBER[int((event.y - 50 )/ 100)])):
                gui.AfterMove(gui.canvas, chess.board)
                gui.ChangeColor('pale goldenrod', 'dark olive green')
                gui.possible_moves.clear()
                last_click = None
            else:
                last_click = chess.INDEX_TO_LETTER[int((event.x - 50 )/ 100)] + str(chess.INDEX_TO_NUMBER[int((event.y - 50 )/ 100)])
    else:
        last_click = chess.INDEX_TO_LETTER[int((event.x - 50 )/ 100)] + str(chess.INDEX_TO_NUMBER[int((event.y - 50 )/ 100)])

"""
for the mouse click to work it can´t be in main. (or I don´t know how)
"""
chess = Chess()
gui = ChessGUI(chess.board)
gui.root.bind("<Button-1>", callback)
gui.End()
