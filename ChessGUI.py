import tkinter as tk

"""
I need the board list
"""

class ChessGUI:
    def __init__(self):
        root = tk.Tk()
        canvas = tk.Canvas(bg='brown', width='900', height='900')
        canvas.pack()
        squares = self.__CreateBoard(canvas)

        root.mainloop()

    def __del__(self):
        pass

    def __CreateBoard(self, canvas):
        squares = []
        for i in range(8):
            for k in range(8):
                if ((i + k) % 2 == 0):
                    squares.append(canvas.create_rectangle(50 + k * 100,
                                                   50 + i * 100,
                                                   150 + k * 100,
                                                   150 + i * 100,
                                                   fill='white'))
                else:
                    squares.append(canvas.create_rectangle(50 + k * 100,
                                            50 + i * 100,
                                            150 + k * 100,
                                            150 + i * 100,
                                            fill='black'))
        pismena = "abcdefgh"
        for i in range(8):
            canvas.create_text((i + 1) * 100,
                               int(canvas['height']) - 25,
                               text=pismena[i],
                               font='Arial',
                               fill='black')
            canvas.create_text(25,
                               int(canvas['height']) - (i + 1) * 100,
                               text=i + 1,
                               font='Arial',
                               fill='black')
        return squares

    def PutPieces(self, canvas, board):
        pieces = []
        #qkbnrp QKBNRP
        choices = {'Q': 'Images/w_queen.png', 'K': 'Images/w_king.png', 'B': 'Images/w_bishop.png',
                   'N': 'Images/w_knight.png', 'R': 'Images/w_rook.png', 'P': 'Images/w_pawn.png',
                   'q': 'Images/b_queen.png', 'k': 'Images/b_king.png', 'b': 'Images/b_bishop.png',
                   'n': 'Images/b_knight.png', 'r': 'Images/b_rook.png', 'p': 'Images/b_pawn.png',
                   '-': }
        for square in board:
            if square in choices:
                result = choices.get(square)
        """
        bk = Image.open("Images/black_king.png")
        bk = bk.resize((50, 50), Image.ANTIALIAS)
        bk = ImageTk.PhotoImage(bk)
        black_king = canvas.create_image(0,0, anchor='nw', image=bk)
        pieces.append(black_king)
        return pieces
        """


def main():
    play = ChessGUI()

if __name__ == "__main__":
    main()