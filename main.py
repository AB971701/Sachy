from Chess import Chess
from ChessGUI import ChessGUI

last_click = None

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

def callback(event):
    #mouse click funtion
    global last_click, chess, gui
    new_click = chess.INDEX_TO_LETTER[int((event.x - 50 )/ 100)] + str(chess.INDEX_TO_NUMBER[int((event.y - 50 )/ 100)])
    #last click is the previous click
    if last_click != None:
        if chess.move(last_click, chess.INDEX_TO_LETTER[int((event.x - 50 )/ 100)] + str(chess.INDEX_TO_NUMBER[int((event.y - 50 )/ 100)])):
            gui.AfterMove(gui.canvas, chess.board)
            last_click = None
        else:
            last_click = new_click
    else:
        last_click = new_click

"""
for the mouse click to work it can´t be in main. (or I don´t know how)
"""
chess = Chess()
gui = ChessGUI(chess.board)
gui.root.bind("<Button-1>", callback)
gui.End()
