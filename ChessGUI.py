import tkinter as tk
from Chess import Chess, PromotePawnException
from Minimax import Minimax
import ctypes
from math import ceil
from copy import deepcopy


class ChessGUI:
    root = tk.Tk()
    root.title("Chess")
    menubar = tk.Menu(root)
    user32 = ctypes.windll.user32
    size = user32.GetSystemMetrics(1) - 100
    canvas = tk.Canvas(bg='grey', width=size, height=size)
    #previous board
    __previous_board = [[None for _ in range(8)] for _ in range(8)]
    pieces = None
    white = []
    possible_moves = []
    possible_moves_gui = []
    last_click = None
    against_player = True
    clicked_square = None
    last_turn = None

    #choices of images depending on the piece in list
    choices = {'Q': 'Images/w_queen.png', 'K': 'Images/w_king.png', 'B': 'Images/w_bishop.png',
               'N': 'Images/w_knight.png', 'R': 'Images/w_rook.png', 'P': 'Images/w_pawn.png',
               'q': 'Images/b_queen.png', 'k': 'Images/b_king.png', 'b': 'Images/b_bishop.png',
               'n': 'Images/b_knight.png', 'r': 'Images/b_rook.png', 'p': 'Images/b_pawn.png'}

    def __init__(self, Chess, board=None):
        """
        #constructor
        :param Chess: Chess game
        :param board: chessboard
        """
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
                        j += int(c)
        self.canvas.pack()
        self.squares = self.__CreateBoard(self.canvas)
        self.pieces = self.__PutPieces(self.canvas, board)
        self.chess = Chess
        self.__previous_board = deepcopy(self.chess.board)
        self.root.bind("<Button-1>", self.callback)
        self.mimax = Minimax(self.chess)

    def __del__(self):
        #destructor
        pass

    def callback(self, event):
        """
        A function after mouse click
        :param event: mouse click
        :return:
        """
        if self.canvas.cget('state') != 'disabled':
            # last click is the previous click
            if event.x >= 50 and event.x <= self.size - 50 and event.y >= 50 and event.y <= self.size - 50:
                # mouse click funtion
                piece = self.chess.board[int((event.y - 50) / ((self.size - 100) / 8))][int((event.x - 50) / ((self.size - 100) / 8))]
                if piece != None and ((self.chess.white_plays and piece.isupper()) or (not self.chess.white_plays and piece.islower())):
                    self.ChangeColor('pale goldenrod', 'dark olive green')
                    self.possible_moves_gui.clear()
                    self.possible_moves = self.chess.get_moves(
                        self.chess.INDEX_TO_LETTER[int((event.x - 50) / ((self.size - 100) / 8))],
                        self.chess.INDEX_TO_NUMBER[int((event.y - 50) / ((self.size - 100) / 8))])
                    """
                    clicked square gets a different color 
                    """
                    self.ClickedColorBack()
                    self.clicked_square = self.squares[int((event.x - 50) / ((self.size - 100) / 8)) + 8 * int((event.y - 50) / ((self.size - 100) / 8))]
                    self.canvas.itemconfig(self.squares[int((event.x - 50) / ((self.size - 100) / 8)) + 8 * int((event.y - 50) / ((self.size - 100) / 8))], fill="DarkOliveGreen3")
                    for move in self.possible_moves:
                        self.possible_moves_gui.append(
                            self.squares[56 + int(self.chess.LETTER_TO_INDEX[move[0]]) - 8 * (int(move[1]) - 1)])
                    self.ChangeColor('seashell3', 'seashell4')
                if self.last_click != None:
                    try:
                        self.__previous_board = deepcopy(self.chess.board)
                        if self.chess.move(self.last_click, self.chess.INDEX_TO_LETTER[int((event.x - 50) / ((self.size - 100) / 8))] + str(
                                self.chess.INDEX_TO_NUMBER[int((event.y - 50) / ((self.size - 100) / 8))])):
                            self.ChangeColor('pale goldenrod', 'dark olive green')
                            self.possible_moves_gui.clear()
                            self.possible_moves.clear()
                            # colors the squares of last turn back
                            self.ColorTurn(True)
                            if not self.against_player:
                                box = self.mimax.minmax()
                                self.ClickedColorBack()
                                if type(box) != int:
                                    self.last_turn = [self.squares[self.chess.LETTER_TO_INDEX[box[0][0]] + 8 * self.chess.NUMBER_TO_INDEX[int(box[0][1])]],
                                                      self.squares[self.chess.LETTER_TO_INDEX[box[1][0]] + 8 * self.chess.NUMBER_TO_INDEX[int(box[1][1])]]]  #gets the squares of last turn
                            else:
                                self.last_turn = [self.clicked_square, self.squares[
                                    int((event.x - 50) / ((self.size - 100) / 8)) + 8 * int(
                                        (event.y - 50) / ((self.size - 100) / 8))]] #gets the squares of last turn
                            if self.last_turn != None:
                                self.ColorTurn() #colors the squares of last turn
                            self.AfterMove()

                            self.clicked_square = None
                            self.last_click = None
                        elif piece != None and ((self.chess.white_plays and piece.isupper()) or (not self.chess.white_plays and piece.islower())):
                            self.last_click = self.chess.INDEX_TO_LETTER[int((event.x - 50) / ((self.size - 100) / 8))] + str(
                                self.chess.INDEX_TO_NUMBER[int((event.y - 50) / ((self.size - 100) / 8))])
                    except PromotePawnException:
                        self.Promotion()
                        self.ColorTurn(True)
                        self.last_turn = [self.clicked_square, self.squares[
                            int((event.x - 50) / ((self.size - 100) / 8)) + 8 * int(
                                (event.y - 50) / ((self.size - 100) / 8))]]  # gets the squares of last turn
                        self.ClickedColorBack()
                elif piece != None and ((self.chess.white_plays and piece.isupper()) or (not self.chess.white_plays and piece.islower())):
                    self.last_click = self.chess.INDEX_TO_LETTER[int((event.x - 50) / ((self.size - 100) / 8))] + str(
                        self.chess.INDEX_TO_NUMBER[int((event.y - 50) / ((self.size - 100) / 8))])

    def __CreateBoard(self, canvas):
        """
        A function that creates a visual board
        :param canvas: canvas
        :return:
        """
        self.canvas.focus_set()
        squares = []
        #creates the board
        for i in range(8):
            for k in range(8):
                if (i + k) % 2 == 0:
                    sq = self.canvas.create_rectangle(50 + int(k * (self.size - 100) / 8),
                                                        50 + int(i * int(self.size - 100) / 8),
                                                        50 + int((k+1) * (self.size - 100) / 8),
                                                        50 + int((i+1) * int(self.size - 100) / 8),
                                                       fill='pale goldenrod',
                                                       outline="")
                    self.white.append(sq)
                    squares.append(sq)
                else:
                    squares.append(canvas.create_rectangle(50 + int(k * (self.size - 100) / 8),
                                                        50 + int(i * int(self.size - 100) / 8),
                                                        50 + int((k+1) * (self.size - 100) / 8),
                                                        50 + int((i+1) * int(self.size - 100) / 8),
                                                           fill='dark olive green',
                                                           outline=""))
        letters = "abcdefgh"
        for i in range(8):
            canvas.create_text(50 + (self.size - 100) // 16 + i * (self.size - 100) // 8,
                               self.size - 25,
                               text=letters[i],
                               font='Arial',
                               fill='black')
            canvas.create_text(25,
                               self.size - 50 - (self.size - 100) // 16 - i * (self.size - 100) // 8,
                               text=i + 1,
                               font='Arial',
                               fill='black')
        return squares

    def __PutPieces(self, canvas, board):
        """
        A function that visually puts pieces on the board
        :param canvas: canvas
        :param board: chessboard
        :return:
        """
        #procedure needed just to create the first board
        pieces = []
        for line in range(len(board)):
            for square in range(len(board[line])):
                if board[line][square] in self.choices:
                    piece = tk.PhotoImage(file=self.choices.get(board[line][square]))
                    if (self.size - 100) // 8 < 91:
                        piece = piece.subsample(int(ceil(piece.width()/((self.size-100)/8))))
                    else:
                        piece = piece.zoom(int(((self.size - 100) / 8) / piece.width()),
                                                int(((self.size - 100) / 8) / piece.width()))
                    pieces.append(piece)
                    canvas.create_image(50 + ((self.size - 100) // 8 - piece.width()) // 2 + square * int((self.size - 100) / 8), 50 + ((self.size - 100) // 8 - piece.width()) // 2 + line * int((self.size - 100) / 8), anchor='nw', image=piece)
                else:
                    pieces.append(None)
        return pieces

    def AfterMove(self):
        """
        A function that is refreshes the board to the current state, always needed after a move.
        :return:
        """
        #after every move refreshes the board
        for line in range(len(self.chess.board)):
            for square in range(len(self.chess.board[line])):
                if self.pieces[line * 8 + square] != None and self.pieces[line * 8 + square] != self.choices.get(self.chess.board[line][square]):
                    self.canvas.delete(self.pieces[line * 8 + square])
                if self.chess.board[line][square] == None:
                    self.pieces[line * 8 + square] = None
                else:
                    self.pieces[line * 8 + square] = tk.PhotoImage(file=self.choices.get(self.chess.board[line][square]))
                    if (self.size - 100) // 8 < 91:
                        self.pieces[line * 8 + square] = self.pieces[line * 8 + square].subsample(int(ceil(self.pieces[line * 8 + square].width() / ((self.size - 100) / 8))))
                    else:
                        self.pieces[line * 8 + square] = self.pieces[line * 8 + square].zoom(
                            int(((self.size - 100) / 8) / self.pieces[line * 8 + square].width()),
                            int(((self.size - 100) / 8) / self.pieces[line * 8 + square].width()))
                    self.canvas.create_image(50 + ((self.size - 100) // 8 - self.pieces[line * 8 + square].width()) // 2 + square * int((self.size - 100) / 8),
                                             50 + ((self.size - 100) // 8 - self.pieces[line * 8 + square].width()) // 2 + line * int((self.size - 100) / 8),
                                             anchor='nw', image=self.pieces[line * 8 + square])
        if self.chess.game_over:
            self.canvas.create_text(self.size // 2,
                                    self.size // 2,
                                    text="Game finished",
                                    font=('Arial', 50),
                                    fill='red',
                                    tag='fin')

    def ChangeColor(self, color1, color2):
        """
        A function that changes the color of squares a piece can move to.
        :param color1: color for white squares
        :param color2: color for black squares
        :return:
        """
        for square in self.possible_moves_gui:
            if square in self.white:
                self.canvas.itemconfig(square, fill=color1)
            else:
                self.canvas.itemconfig(square, fill=color2)

    def __NewGame(self):
        """
        Creates a new game
        :return:
        """
        if self.chess.game_over:
            self.canvas.delete('fin')
        #create new game
        self.chess = Chess()
        self.ChangeColor('pale goldenrod', 'dark olive green')
        self.possible_moves_gui.clear()
        self.last_click = None
        self.ClickedColorBack()
        self.ColorTurn(True)
        self.AfterMove()
        self.mimax.NewChess(self.chess)

    def __load(self):
        """
        Loads another game.
        :return:
        """
        if self.chess.game_over:
            self.canvas.delete('fin')
        try:
            self.chess = Chess(self.text.get() + ".txt")
            self.AfterMove()
            self.main.destroy()
            self.canvas.focus_set()
            self.ChangeColor('pale goldenrod', 'dark olive green')
            self.possible_moves_gui.clear()
            self.last_click = None
            self.ClickedColorBack()
            self.ColorTurn(True)
            self.mimax.NewChess(self.chess)
        except:
            tk.Label(self.main, text=("No such file or directory: " + self.text.get())).grid(column=1, row=0)

    def __GetFilepathL(self):
        """
        Creates a box where you can write the filepath of your saved game.
        :return:
        """
        self.main = tk.Toplevel(self.root)
        self.text = tk.StringVar()
        self.name = tk.Entry(self.main, textvariable=self.text)
        self.name.grid(column=0, row=0)
        tk.Button(self.main, text="Enter", command=self.__load).grid(column=0, row=1)
        self.name.focus_set()

    def __save(self):
        """
        Saves the current game.
        :return:
        """
        self.chess.save_to_file(self.text.get() + ".txt")
        self.main.destroy()
        self.canvas.focus_set()

    def __GetFilepathS(self):
        """
        Creates a box where you can write where to save the game.
        :return:
        """
        self.main = tk.Toplevel(self.root)
        self.text = tk.StringVar()
        self.name = tk.Entry(self.main, textvariable=self.text)
        self.name.grid(column=0, row=0)
        tk.Button(self.main, text="Enter", command=self.__save).grid(column=0, row=1)
        self.name.focus_set()


    def Promotion(self):
        """
        Makes a box to choose which piece you want to promote to
        :return:
        """
        self.promo = tk.Toplevel(self.root)
        if self.chess.white_plays:
            self.promotion_Q = tk.PhotoImage(file=self.choices['Q'])
            tk.Button(self.promo, image=self.promotion_Q, command=lambda: self.OnButtonClick(0)).grid(column=0, row=0)
            self.promotion_R = tk.PhotoImage(file=self.choices['R'])
            tk.Button(self.promo, image=self.promotion_R, command=lambda: self.OnButtonClick(1)).grid(column=0, row=1)
            self.promotion_B = tk.PhotoImage(file=self.choices['B'])
            tk.Button(self.promo, image=self.promotion_B, command=lambda: self.OnButtonClick(2)).grid(column=0, row=2)
            self.promotion_N = tk.PhotoImage(file=self.choices['N'])
            tk.Button(self.promo, image=self.promotion_N, command=lambda: self.OnButtonClick(3)).grid(column=0, row=3)
        else:
            self.promotion_q = tk.PhotoImage(file=self.choices['q'])
            tk.Button(self.promo, image=self.promotion_q, command=lambda: self.OnButtonClick(0)).grid(column=0, row=0)
            self.promotion_r = tk.PhotoImage(file=self.choices['r'])
            tk.Button(self.promo, image=self.promotion_r, command=lambda: self.OnButtonClick(1)).grid(column=0, row=1)
            self.promotion_b = tk.PhotoImage(file=self.choices['b'])
            tk.Button(self.promo, image=self.promotion_b, command=lambda: self.OnButtonClick(2)).grid(column=0, row=2)
            self.promotion_n = tk.PhotoImage(file=self.choices['n'])
            tk.Button(self.promo, image=self.promotion_n, command=lambda: self.OnButtonClick(3)).grid(column=0, row=3)
        self.canvas.configure(state='disabled')
        self.menubar.entryconfig("New game", state='disabled')
        self.menubar.entryconfig("Save game", state='disabled')
        self.menubar.entryconfig("Load game", state='disabled')
        if not self.against_player:
            self.menubar.entryconfig("vs Player", state='disabled')
        else:
            self.menubar.entryconfig("vs Ai", state='disabled')
        self.menubar.entryconfig("Back", state='disabled')
        self.promo.overrideredirect(True)

    def OnButtonClick(self, button_id):
        """
        :param button_id: decides which promotion is it going to be
        :return:
        """
        if button_id == 0:
            # promote to Queen
            self.chess.promote_pawn('q')
        elif button_id == 1:
            # promote to rook
            self.chess.promote_pawn('r')
        elif button_id == 2:
            # promote to bishop
            self.chess.promote_pawn('b')
        elif button_id == 3:
            # promote to knight
            self.chess.promote_pawn('n')
        self.promo.destroy()
        self.canvas.configure(state='normal')
        self.menubar.entryconfig("New game", state='normal')
        self.menubar.entryconfig("Save game", state='normal')
        self.menubar.entryconfig("Load game", state='normal')
        if not self.against_player:
            self.menubar.entryconfig("vs Player", state='normal')
        else:
            self.menubar.entryconfig("vs Ai", state='normal')
        self.menubar.entryconfig("Back", state='normal')
        self.canvas.focus_set()
        self.ChangeColor('pale goldenrod', 'dark olive green')
        self.possible_moves_gui.clear()
        self.possible_moves.clear()
        self.last_click = None
        self.ClickedColorBack()
        if not self.against_player:
            box = self.mimax.minmax()
            self.ClickedColorBack()
            if type(box) != int:
                self.last_turn = [
                    self.squares[self.chess.LETTER_TO_INDEX[box[0][0]] + 8 * self.chess.NUMBER_TO_INDEX[int(box[0][1])]],
                    self.squares[self.chess.LETTER_TO_INDEX[box[1][0]] + 8 * self.chess.NUMBER_TO_INDEX[
                        int(box[1][1])]]]  # gets the squares of last turn
        if self.last_turn != None:
            self.ColorTurn()  # colors the squares of last turn
        self.AfterMove()

    def AiVSP(self):
        """
        switches between playing with a player and playing with an ai
        :return:
        """
        if not self.against_player:
            self.menubar.entryconfig(4, label='vs Ai')
        else:
            self.menubar.entryconfig(4, label='vs Player')
        self.__previous_board = deepcopy(self.chess.board)
        self.against_player = not self.against_player

    def Back(self):
        """
        allows you to go one turn back if missclicked
        :return:
        """
        if self.chess.game_over:
            self.canvas.delete('fin')
            self.chess.game_over = False
        if self.chess.board != self.__previous_board:
            self.chess.board_history.pop()
            if self.against_player:
                self.chess.white_plays = not self.chess.white_plays
            else:
                self.chess.board_history.pop()
        self.chess.board = deepcopy(self.__previous_board)
        if self.last_click != None:
            self.ChangeColor('pale goldenrod', 'dark olive green')
            self.possible_moves_gui.clear()
            self.last_click = None
            self.ClickedColorBack()
        self.ColorTurn(True)
        self.AfterMove()

    def ClickedColorBack(self):
        if self.clicked_square in self.white:
            self.canvas.itemconfig(self.clicked_square, fill="pale goldenrod")
        else:
            self.canvas.itemconfig(self.clicked_square, fill="dark olive green")
        self.clicked_square = None

    def ColorTurn(self, back=False):
        if back:
            if self.last_turn != None:
                for square in self.last_turn:
                    if square in self.white:
                        self.canvas.itemconfig(square, fill="pale goldenrod")
                    else:
                        self.canvas.itemconfig(square, fill="dark olive green")
                self.last_turn = None
        else:
            for square in self.last_turn:
                self.canvas.itemconfig(square, fill="OliveDrab2")

    def End(self):
        """
        creates the buttons on top
        :return:
        """
        #Adding options to a menu
        self.menubar.add_command(label="New game", command=self.__NewGame)
        self.menubar.add_command(label="Save game", command=lambda: self.__GetFilepathS())
        self.menubar.add_command(label="Load game", command=lambda: self.__GetFilepathL())
        self.menubar.add_command(label="vs Ai", command=self.AiVSP)
        self.menubar.add_command(label="Back", command=self.Back)
        self.menubar.add_command(label="Quit", command=self.root.quit)

        self.root.config(menu=self.menubar)
        #ends the cycle
        self.root.mainloop()
