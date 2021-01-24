import tkinter as tk
from Chess import Chess

class ChessGUI:
    root = tk.Tk()
    __previous_board = 0
    pieces = None
    squares = None

    choices = {'Q': 'Images/w_queen.png', 'K': 'Images/w_king.png', 'B': 'Images/w_bishop.png',
               'N': 'Images/w_knight.png', 'R': 'Images/w_rook.png', 'P': 'Images/w_pawn.png',
               'q': 'Images/b_queen.png', 'k': 'Images/b_king.png', 'b': 'Images/b_bishop.png',
               'n': 'Images/b_knight.png', 'r': 'Images/b_rook.png', 'p': 'Images/b_pawn.png'}

    def __init__(self, board=None):
        if board == None:
            board_history = ['rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1']
            tmp = (board_history[-1][0:board_history[-1].find(' ')]).split('/')
            # vytvori prazdne herni pole
            board = [[None for _ in range(8)] for _ in range(8)]
            # polohu figur z posledniho tvaru zapise do herniho pole
            for i in range(8):
                j = 0
                for c in tmp[i]:
                    if c.lower() in "prnbqk":
                        board[i][j] = c
                        j += 1
                    elif c in "12345678":
                        j += ord(c) - ord('0')
        self.__previous_board = board
        canvas = tk.Canvas(bg='grey', width='900', height='900')
        canvas.pack()
        self.squares = self.__CreateBoard(canvas)
        self.pieces = self.__PutPieces(canvas, board)

    def __del__(self):
        pass

    def End(self):
        self.root.mainloop()

    def __CreateBoard(self, canvas):
        squares = []
        for i in range(8):
            for k in range(8):
                if (i + k) % 2 == 0:
                    squares.append(canvas.create_rectangle(50 + i * 100,
                                                           50 + k * 100,
                                                           150 + i * 100,
                                                           150 + k * 100,
                                                           fill='pale goldenrod',
                                                           outline=""))
                else:
                    squares.append(canvas.create_rectangle(50 + i * 100,
                                                           50 + k * 100,
                                                           150 + i * 100,
                                                           150 + k * 100,
                                                           fill='dark olive green',
                                                           outline=""))
        pismena = "abcdefgh"
        for i in range(8):
            canvas.create_text((i + 1) * 100,
                               900 - 25,
                               text=pismena[i],
                               font='Arial',
                               fill='black')
            canvas.create_text(25,
                               900 - (i + 1) * 100,
                               text=i + 1,
                               font='Arial',
                               fill='black')
        return squares

    def __PutPieces(self, canvas, board):
        pieces = []
        for line in range(len(board)):
            for square in range(len(board[line])):
                if board[line][square] in self.choices:
                    piece = tk.PhotoImage(file=self.choices.get(board[line][square]))
                    pieces.append(piece)
                    canvas.create_image(55 + square * 100, 55 + line * 100, anchor='nw', image=piece)
                else:
                    pieces.append(None)
        return pieces

    def AfterMove(self, canvas, board):
        if self.__previous_board != board:
            for line in range(len(board)):
                for square in range(len(board[line])):
                    if board[line][square] != self.__previous_board[line][square]:
                        if self.pieces[line * 8 + square] != None:
                            canvas.delete(self.pieces[line * 8 + square])
                            if board[line][square] == None:
                                self.pieces[line * 8 + square] = None
                            else:
                                self.pieces[line * 8 + square] = tk.PhotoImage(file=self.choices.get(board[line][square]))
                                canvas.create_image(55 + square * 100, 55 + line * 100, anchor='nw', image=self.pieces[line * 8 + square])
                        else:
                            self.pieces[line * 8 + square] = tk.PhotoImage(file=self.choices.get(board[line][square]))
                            canvas.create_image(55 + square * 100, 55 + line * 100, anchor='nw',
                                                image=self.pieces[line * 8 + square])
        self.__previous_board = board
