from Chess import Chess
from ChessGUI import ChessGUI

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
    INDEX_TO_LETTER = {0: "a", 1: "b", 2: "c", 3: "d", 4: "e", 5: "f", 6: "g", 7: "h"}
    NUMBER_TO_INDEX = {0: 8, 1: 7, 2: 6, 3: 5, 4: 4, 5: 3, 6: 2, 7: 1}
    print(INDEX_TO_LETTER[int((event.x - 50 )/ 100)] + str(NUMBER_TO_INDEX[int((event.y - 50 )/ 100)]))
    # Chess.Chess.move(, INDEX_TO_LETTER[int(event.x) / 100 - 50] + NUMBER_TO_INDEX[int(event.y) / 100 - 50])


def main():
    chess = Chess()
    gui = ChessGUI()
    gui.root.bind("<Button-1>", callback)
    gui.End()

if __name__ == "__main__":
    main()