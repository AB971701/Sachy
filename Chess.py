# noinspection SpellCheckingInspection
class Chess:
    LETTER_TO_INDEX = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}
    INDEX_TO_LETTER = {0: "a", 1: "b", 2: "c", 3: "d", 4: "e", 5: "f", 6: "g", 7: "h"}

    def __init__(self, filepath):
        self.board_history = ['rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1']
        self.board = None
        self.__create_board()
        self.white_plays = True
        self.castling_rights = "KQkq"
        self.en_passant = '-'
        self.half_move = 0
        self.full_move = 1

    def __del__(self):
        # body of destructor
        pass

    def load_from_file(self, filepath):
        """
        loads game from file
        :param filepath: path to txt file from which is the game loaded
        :return: full board history
        """
        # nacte hru z filu a rozdeli tahy
        with open(filepath, "r") as file:
            self.board_history = [line.strip() for line in file]
        # vytvori hraci plochu z posledniho zahraneho tahu
        self.__create_board()

        # nacte, kdo je na tahu
        posFirst = self.board_history[-1].find(' ')
        posLast = self.board_history[-1].find(' ', posFirst + 1)
        self.white_plays = True if self.board_history[-1][posFirst:posLast] else False

        # nacte, kde jde udelat rosadu
        posFirst = posLast
        posLast = self.board_history[-1].find(' ', posFirst + 1)
        self.castling_rights = self.board_history[-1][posFirst:posLast]

        # nacte, jestli jde brat mimochodem
        posFirst = posLast
        posLast = self.board_history[-1].find(' ', posFirst + 1)
        self.en_passant = self.board_history[-1][posFirst:posLast]

        # nacte kolik "pultahu" ubehlo od posledniho sebrani figurky nebo pohnuti pescem
        posFirst = posLast
        posLast = self.board_history[-1].find(' ', posFirst + 1)
        self.half_move = ord(self.board_history[-1][posFirst:posLast]) - ord('0')

        # nacte kolik tahu probehlo od zacatku hry
        posFirst = posLast
        posLast = self.board_history[-1].find(' ', posFirst + 1)
        self.full_move = ord(self.board_history[-1][posFirst:posLast]) - ord('0')

    def save_to_file(self, filepath):
        """
        saves game to file
        :param filepath: path to txt file which is the game saved to
        :return:
        """
        with open(filepath, "w") as file:
            file.write("%s\n" % self.board_history)

    def __create_board(self):
        # z historie hry nacte posledni tah
        tmp = (self.board_history[-1][0:self.board_history[-1].find(' ')]).split('/')
        # vytvori prazdne herni pole
        self.board = [[None for _ in range(8)] for _ in range(8)]
        # polohu figur z posledniho tvaru zapise do herniho pole
        for i in range(8):
            j = 0
            for c in tmp[i]:
                if c.lower() in "prnbqk":
                    self.board[i][j] = c
                    j += 1
                elif c in "12345678":
                    j += ord(c) - ord('0')

    def move(self, start_position, end_position):
        if self.__is_valid(start_position, end_position):
            start_row = 8 - (ord(start_position[1]) - ord('0'))
            start_col = self.LETTER_TO_INDEX[start_position[0]]
            end_row = 8 - (ord(end_position[1]) - ord('0'))
            end_col = self.LETTER_TO_INDEX[end_position[0]]

            # "pohne" figurkou - na puvodni pozici ulozi None, novou pozici prepise nazvem figury se kterou se hralo
            tmp = self.board[start_row][start_col]
            self.board[start_row][start_col] = None
            self.board[end_row][end_col] = tmp

            self.white_plays = not self.white_plays
            return True
        return False

    def __is_valid(self, start_position, end_position):
        """
        checks if move is legal
        :param start_position: position where is the piece standing before the move
        :param end_position: position to which is the piece moved
        :return: True if move is valid else False
        """
        # kontroluje spravnost souradnic
        if self.__coord_valid(start_position) and self.__coord_valid(end_position):
            # kontroluje
            if self.__own_piece_on_coords(start_position[0], ord(start_position[1]) - ord('0')):
                if not self.__own_piece_on_coords(end_position[0], ord(end_position[1]) - ord('0')):
                    if self.__move_legal(start_position, end_position):
                        return True
        return False

    def __coord_valid(self, coord):
        """
        checks if coordinates are inside the game board
        :param coord: coordinates in form "<file><rank>"
        :return: True if coordinates are valid, else False
        """
        if coord[0] in "abcdefgh" and coord[1] in "12345678":
            return True
        return False

    def __find_piece_on_coords(self, file, rank):
        """
        :param file:
        :param rank:
        :return: piece if there is a piece at given coordinates, else None
        """
        return self.board[8 - rank][self.LETTER_TO_INDEX[file]]

    def __own_piece_on_coords(self, file, rank):
        """
        checks if there is a piece of a player who is on move
        :param file:
        :param rank:
        :return: True if there is player's own piece, else False
        """
        piece = self.__find_piece_on_coords(file, rank)
        if piece is not None and ((piece.isupper()) if self.white_plays else piece.islower()):
            return True
        return False

    def __is_own_piece(self, piece):
        if piece.isupper() and self.white_plays:
            return True
        if piece.islower() and not self.white_plays:
            return True
        return False

    def __move_legal(self, start_position, end_position):
        """
        checks if it is legal for the piece at starting position to move to the given end position
        :param start_position: position where is the piece standing before the move
        :param end_position: position to which is the piece moved
        :return: True if the move for the piece is possible, else False
        """
        file = start_position[0]
        rank = ord(start_position[1]) - ord('0')
        piece = (self.__find_piece_on_coords(file, rank)).lower()
        if piece == 'p':
            if end_position in self.get_pawn_moves(file, rank):
                return True
        elif piece == 'r':
            if end_position in self.get_rook_moves(file, rank):
                return True
        elif piece == 'n':
            if end_position in self.get_knight_moves(file, rank):
                return True
        elif piece == 'b':
            if end_position in self.get_bishop_moves(file, rank):
                return True
        elif piece == 'q':
            if end_position in self.get_queen_moves(file, rank):
                return True
        elif piece == 'k':
            if end_position in self.get_king_moves(file, rank):
                return True

    """ Piece moves """

    def get_pawn_moves(self, file, rank):
        file_num = self.LETTER_TO_INDEX[file]
        possible_moves = []
        # bily je na tahu
        if self.white_plays:
            possible_moves.append(file + str(rank+1))
            # pesak se jeste nepohnul
            if rank == 2:
                possible_moves.append(file + str(rank + 2))
            # pesak muze neco sebrat
            try:
                if (self.__find_piece_on_coords(self.INDEX_TO_LETTER[file_num - 1], rank + 1)).islower():
                    possible_moves.append(self.INDEX_TO_LETTER[file_num - 1] + str(rank + 1))
            except:
                pass
            try:
                if (self.__find_piece_on_coords(self.INDEX_TO_LETTER[file_num+1], rank+1)).islower():
                    possible_moves.append(self.INDEX_TO_LETTER[file_num+1] + str(rank+1))
            except:
                pass
            # moznost brani mimochodem
            if self.en_passant != '-' and rank == 5 and ((ord(file) == ord(self.en_passant[0])+1) or (ord(file) == ord(self.en_passant[0])-1)):
                possible_moves.append(self.en_passant)
        # cerny je na tahu
        else:
            possible_moves.append(file + str(rank - 1))
            # pesak se jeste nepohnul
            if rank == 2:
                possible_moves.append(file + str(rank - 2))
            # pesak muze neco sebrat
            try:
                if (self.__find_piece_on_coords(self.INDEX_TO_LETTER[file_num - 1], rank - 1)).isupper():
                    possible_moves.append(self.INDEX_TO_LETTER[file_num - 1] + str(rank - 1))
            except:
                pass
            try:
                if (self.__find_piece_on_coords(self.INDEX_TO_LETTER[file_num + 1], rank - 1)).isupper():
                    possible_moves.append(self.INDEX_TO_LETTER[file_num + 1] + str(rank - 1))
            except:
                pass
            # moznost brani mimochodem
            if self.en_passant != '-' and rank == 4 and (
                    (ord(file) == ord(self.en_passant[0]) + 1) or (ord(file) == ord(self.en_passant[0]) - 1)):
                possible_moves.append(self.en_passant)
        return possible_moves

    def get_rook_moves(self, file, rank):
        file_num = self.LETTER_TO_INDEX[file]
        possible_moves = []

        for r in range(1, 9):
            if r != rank:
                p = self.__find_piece_on_coords(file, r)
                if p is not None:
                    if not self.__is_own_piece(p):
                        possible_moves.append(file + str(r))
                    break
                possible_moves.append(file + str(r))
        for f in range(8):
            if f != file_num:
                p = self.__find_piece_on_coords(self.INDEX_TO_LETTER[f], rank)
                if p is not None:
                    if not self.__is_own_piece(p):
                        possible_moves.append(self.INDEX_TO_LETTER[f] + str(rank))
                    break
                possible_moves.append(self.INDEX_TO_LETTER[f] + str(rank))

        return possible_moves

    def get_knight_moves(self, file, rank):
        file_num = self.LETTER_TO_INDEX[file]
        possible_moves = []

        if 0 <= (file_num - 2) <= 7 and 0 <= (rank - 1) <= 7:
            possible_moves.append(self.INDEX_TO_LETTER[file_num - 2] + str(rank - 1))
        if 0 <= (file_num - 1) <= 7 and 0 <= (rank - 2) <= 7:
            possible_moves.append(self.INDEX_TO_LETTER[file_num - 1] + str(rank - 2))
        if 0 <= (file_num + 1) <= 7 and 0 <= (rank - 2) <= 7:
            possible_moves.append(self.INDEX_TO_LETTER[file_num + 1] + str(rank - 2))
        if 0 <= (file_num + 2) <= 7 and 0 <= (rank - 1) <= 7:
            possible_moves.append(self.INDEX_TO_LETTER[file_num + 2] + str(rank - 1))
        if 0 <= (file_num + 2) <= 7 and 0 <= (rank + 1) <= 7:
            possible_moves.append(self.INDEX_TO_LETTER[file_num + 2] + str(rank + 1))
        if 0 <= (file_num + 1) <= 7 and 0 <= (rank + 2) <= 7:
            possible_moves.append(self.INDEX_TO_LETTER[file_num + 1] + str(rank + 2))
        if 0 <= (file_num - 1) <= 7 and 0 <= (rank + 2) <= 7:
            possible_moves.append(self.INDEX_TO_LETTER[file_num - 1] + str(rank + 2))
        if 0 <= (file_num - 2) <= 7 and 0 <= (rank + 1) <= 7:
            possible_moves.append(self.INDEX_TO_LETTER[file_num - 2] + str(rank + 1))
        return possible_moves

    def get_bishop_moves(self, file, rank):
        file_num = self.LETTER_TO_INDEX[file]
        possible_moves = []

        i = 1
        while (file_num - i >= 0) and (rank - i > 0):
            possible_moves.append(self.INDEX_TO_LETTER[file_num - i] + str(rank - i))
            i += 1
        i = 1
        while (file_num - i >= 0) and (rank + i < 9):
            possible_moves.append(self.INDEX_TO_LETTER[file_num - i] + str(rank + i))
            i += 1
        i = 1
        while (file_num + i < 8) and (rank - i > 0):
            possible_moves.append(self.INDEX_TO_LETTER[file_num + i] + str(rank - i))
            i += 1
        i = 1
        while (file_num + i < 8) and (rank + i < 9):
            possible_moves.append(self.INDEX_TO_LETTER[file_num + i] + str(rank + i))
            i += 1

        return possible_moves

    def get_queen_moves(self, file, rank):
        file_num = self.LETTER_TO_INDEX[file]
        possible_moves = []

        for r in range(1, 9):
            if r != rank:
                possible_moves.append(file + str(r))
        for f in range(8):
            if f != file_num:
                possible_moves.append(self.INDEX_TO_LETTER[f] + str(rank))

        i = 1
        while (file_num - i >= 0) and (rank - i > 0):
            possible_moves.append(self.INDEX_TO_LETTER[file_num - i] + str(rank - i))
            i += 1
        i = 1
        while (file_num - i >= 0) and (rank + i < 9):
            possible_moves.append(self.INDEX_TO_LETTER[file_num - i] + str(rank + i))
            i += 1
        i = 1
        while (file_num + i < 8) and (rank - i > 0):
            possible_moves.append(self.INDEX_TO_LETTER[file_num + i] + str(rank - i))
            i += 1
        i = 1
        while (file_num + i < 8) and (rank + i < 9):
            possible_moves.append(self.INDEX_TO_LETTER[file_num + i] + str(rank + i))
            i += 1

        return possible_moves

    def get_king_moves(self, file, rank):
        file_num = self.LETTER_TO_INDEX[file]
        possible_moves = []

        if 0 <= (rank - 1) <= 7:
            possible_moves.append(file + str(rank - 1))
        if 0 <= (file_num + 1) <= 7 and 0 <= (rank - 1) <= 7:
            possible_moves.append(self.INDEX_TO_LETTER[file_num + 1] + str(rank - 1))
        if 0 <= (file_num + 1) <= 7:
            possible_moves.append(self.INDEX_TO_LETTER[file_num + 1] + str(rank))
        if 0 <= (file_num + 1) <= 7 and 0 <= (rank + 1) <= 7:
            possible_moves.append(self.INDEX_TO_LETTER[file_num + 1] + str(rank + 1))
        if 0 <= (rank + 1) <= 7:
            possible_moves.append(file + str(rank + 1))
        if 0 <= (file_num - 1) <= 7 and 0 <= (rank + 1) <= 7:
            possible_moves.append(self.INDEX_TO_LETTER[file_num - 1] + str(rank + 1))
        if 0 <= (file_num - 1) <= 7:
            possible_moves.append(self.INDEX_TO_LETTER[file_num - 1] + str(rank))
        if 0 <= (file_num - 1) <= 7 and 0 <= (rank - 1) <= 7:
            possible_moves.append(self.INDEX_TO_LETTER[file_num - 1] + str(rank - 1))
        return possible_moves

    def print_board(self):
        for line in self.board:
            for cell in line:
                print(cell if cell is not None else '-', end=' ')
            print()

    # TODO: napsat fci is_valid
    # TODO: - pro dany typ figurky je tah podle pravidel mozny
    # TODO: -- pridat podminky pro obsazena pole, rosadu a brani mimochodem
    # TODO: - po tahu neni vlastni kral v sachu
    # TODO: pridat 50 move rule
    # TODO: napsat fci move - provede tah


if __name__ == "__main__":
    c = Chess('test.txt')
    """
    print('white plays' if c.white_plays else 'black plays')
    c.print_board()
    print()
    print('white plays' if c.white_plays else 'black plays')
    c.move('a2', 'a3')
    c.print_board()
    print()
    print('white plays' if c.white_plays else 'black plays')
    c.move('b7', 'b6')
    c.print_board()
    print()
    print('white plays' if c.white_plays else 'black plays')
    c.move('g1', 'f3')
    c.print_board()
    print()
    print('white plays' if c.white_plays else 'black plays')

    print(c.get_pawn_moves('b', 2))
    """
    print(c.get_rook_moves('a', 1))
