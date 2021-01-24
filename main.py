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
    global last_click, chess, gui
    INDEX_TO_LETTER = {0: "a", 1: "b", 2: "c", 3: "d", 4: "e", 5: "f", 6: "g", 7: "h"}
    NUMBER_TO_INDEX = {0: 8, 1: 7, 2: 6, 3: 5, 4: 4, 5: 3, 6: 2, 7: 1}
    new_click = INDEX_TO_LETTER[int((event.x - 50)/ 100)] + str(NUMBER_TO_INDEX[int((event.y - 50 )/ 100)])
    if last_click != None:
        if chess.move(last_click, INDEX_TO_LETTER[int((event.x - 50 )/ 100)] + str(NUMBER_TO_INDEX[int((event.y - 50 )/ 100)])):
            gui.AfterMove(gui.canvas, chess.board)
            last_click = None
    else:
        last_click = new_click

"""
for the mouse click to work it can´t be in main.
"""
chess = Chess()
gui = ChessGUI(chess.board)
gui.root.bind("<Button-1>", callback)
gui.End()
