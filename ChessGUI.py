import tkinter as tk
from Chess import Chess

class ChessGUI:
    root = tk.Tk()
    root.title("Chess")
    menubar = tk.Menu(root)
    canvas = tk.Canvas(bg='grey', width='900', height='900')
    #previous board
    __previous_board = [[None for _ in range(8)] for _ in range(8)]
    pieces = None
    white = []
    possible_moves = []
    possible_moves_gui = []
    last_click = None

    #choices of images depending on the piece in list
    choices = {'Q': 'Images/w_queen.png', 'K': 'Images/w_king.png', 'B': 'Images/w_bishop.png',
               'N': 'Images/w_knight.png', 'R': 'Images/w_rook.png', 'P': 'Images/w_pawn.png',
               'q': 'Images/b_queen.png', 'k': 'Images/b_king.png', 'b': 'Images/b_bishop.png',
               'n': 'Images/b_knight.png', 'r': 'Images/b_rook.png', 'p': 'Images/b_pawn.png'}

    def __init__(self, Chess, board=None):
        #constructor
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
        for i in range(8):
            for k in range(8):
                self.__previous_board[i][k] = board[i][k]
        self.canvas.pack()
        self.squares = self.__CreateBoard(self.canvas)
        self.pieces = self.__PutPieces(self.canvas, board)
        self.chess = Chess
        self.root.bind("<Button-1>", self.callback)

    def __del__(self):
        #destructor
        pass

    def callback(self, event):
        # mouse click funtion
        piece = self.chess.board[int((event.y - 50) / 100)][int((event.x - 50) / 100)]
        # last click is the previous click
        if event.x >= 50 and event.x <= 850 and event.y >= 50 and event.y <= 850:
            self.ChangeColor('pale goldenrod', 'dark olive green')
            self.possible_moves_gui.clear()
            if piece != None:
                if piece in 'pP':
                    self.possible_moves = self.chess.get_pawn_moves(self.chess.INDEX_TO_LETTER[int((event.x - 50) / 100)],
                                                          self.chess.INDEX_TO_NUMBER[int((event.y - 50) / 100)])
                elif piece in 'rR':
                    self.possible_moves = self.chess.get_rook_moves(self.chess.INDEX_TO_LETTER[int((event.x - 50) / 100)],
                                                          self.chess.INDEX_TO_NUMBER[int((event.y - 50) / 100)])
                elif piece in 'bB':
                    self.possible_moves = self.chess.get_bishop_moves(self.chess.INDEX_TO_LETTER[int((event.x - 50) / 100)],
                                                            self.chess.INDEX_TO_NUMBER[int((event.y - 50) / 100)])
                elif piece in 'nN':
                    self.possible_moves = self.chess.get_knight_moves(self.chess.INDEX_TO_LETTER[int((event.x - 50) / 100)],
                                                            self.chess.INDEX_TO_NUMBER[int((event.y - 50) / 100)])
                elif piece in 'qQ':
                    self.possible_moves = self.chess.get_queen_moves(self.chess.INDEX_TO_LETTER[int((event.x - 50) / 100)],
                                                           self.chess.INDEX_TO_NUMBER[int((event.y - 50) / 100)])
                elif piece in 'kK':
                    self.possible_moves = self.chess.get_king_moves(self.chess.INDEX_TO_LETTER[int((event.x - 50) / 100)],
                                                          self.chess.INDEX_TO_NUMBER[int((event.y - 50) / 100)])
            for move in self.possible_moves:
                self.possible_moves_gui.append(self.squares[56 + int(self.chess.LETTER_TO_INDEX[move[0]]) - 8 * (int(move[1]) - 1)])
            self.ChangeColor('seashell3', 'seashell4')
        if self.last_click != None:
            if self.chess.move(self.last_click, self.chess.INDEX_TO_LETTER[int((event.x - 50) / 100)] + str(
                    self.chess.INDEX_TO_NUMBER[int((event.y - 50) / 100)])):
                self.AfterMove()
                self.ChangeColor('pale goldenrod', 'dark olive green')
                self.possible_moves_gui.clear()
                self.last_click = None
            else:
                self.last_click = self.chess.INDEX_TO_LETTER[int((event.x - 50) / 100)] + str(
                    self.chess.INDEX_TO_NUMBER[int((event.y - 50) / 100)])
        else:
            self.last_click = self.chess.INDEX_TO_LETTER[int((event.x - 50) / 100)] + str(
                self.chess.INDEX_TO_NUMBER[int((event.y - 50) / 100)])

    def __CreateBoard(self, canvas):
        squares = []
        #creates the board
        for i in range(8):
            for k in range(8):
                if (i + k) % 2 == 0:
                    sq = self.canvas.create_rectangle(50 + k * 100,
                                                       50 + i * 100,
                                                       150 + k * 100,
                                                       150 + i * 100,
                                                       fill='pale goldenrod',
                                                       outline="")
                    self.white.append(sq)
                    squares.append(sq)
                else:
                    squares.append(canvas.create_rectangle(50 + k * 100,
                                                           50 + i * 100,
                                                           150 + k * 100,
                                                           150 + i * 100,
                                                           fill='dark olive green',
                                                           outline=""))
        letters = "abcdefgh"
        for i in range(8):
            canvas.create_text((i + 1) * 100,
                               900 - 25,
                               text=letters[i],
                               font='Arial',
                               fill='black')
            canvas.create_text(25,
                               900 - (i + 1) * 100,
                               text=i + 1,
                               font='Arial',
                               fill='black')
        return squares

    def __PutPieces(self, canvas, board):
        #procedure needed just to create the first board
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

    def AfterMove(self):
        #after every move refreshes the board
        if self.__previous_board != self.chess.board:
            for line in range(len(self.chess.board)):
                for square in range(len(self.chess.board[line])):
                    if self.chess.board[line][square] != self.__previous_board[line][square]:
                        if self.pieces[line * 8 + square] != None:
                            self.canvas.delete(self.pieces[line * 8 + square])
                            if self.chess.board[line][square] == None:
                                self.pieces[line * 8 + square] = None
                            else:
                                self.pieces[line * 8 + square] = tk.PhotoImage(file=self.choices.get(self.chess.board[line][square]))
                                self.canvas.create_image(55 + square * 100, 55 + line * 100, anchor='nw', image=self.pieces[line * 8 + square])
                        else:
                            self.pieces[line * 8 + square] = tk.PhotoImage(file=self.choices.get(self.chess.board[line][square]))
                            self.canvas.create_image(55 + square * 100, 55 + line * 100, anchor='nw',
                                                image=self.pieces[line * 8 + square])
            for i in range(8):
                for k in range(8):
                    self.__previous_board[i][k] = self.chess.board[i][k]

    def ChangeColor(self, color1, color2):
        for square in self.possible_moves_gui:
            if square in self.white:
                self.canvas.itemconfig(square, fill=color1)
            else:
                self.canvas.itemconfig(square, fill=color2)

    def NewGame(self):
        #create new game
        self.chess = Chess()
        self.AfterMove()

    def __function(self):
        try:
            self.chess = Chess(self.text.get())
            self.AfterMove()
            self.main.destroy()
            self.main.update()
        except:
            tk.Label(self.main, text=("No such file or directory: " + self.text.get())).grid(column=1, row=0)

    def __GetFilepath(self):
        self.main = tk.Toplevel(self.root)
        self.text = tk.StringVar()
        tk.Entry(self.main, textvariable=self.text).grid(column=0, row=0)
        tk.Button(self.main, text="Enter", command=self.__function).grid(column=0, row=1)

    def End(self):
        #Adding options to a menu
        self.menubar.add_command(label="New game", command=self.NewGame)
        self.menubar.add_command(label="Load game", command=lambda: self.__GetFilepath())
        self.menubar.add_command(label="Quit", command=self.root.quit)

        self.root.config(menu=self.menubar)
        #ends the cycle
        self.root.mainloop()
