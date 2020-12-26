from copy import deepcopy


class Chess:
    LETTER_TO_INDEX = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}
    INDEX_TO_LETTER = {0: "a", 1: "b", 2: "c", 3: "d", 4: "e", 5: "f", 6: "g", 7: "h"}
    NUMBER_TO_INDEX = {1: 7, 2: 6, 3: 5, 4: 4, 5: 3, 6: 2, 7: 1, 8: 0}
    INDEX_TO_NUMBER = {0: 8, 1: 7, 2: 6, 3: 5, 4: 4, 5: 3, 6: 2, 7: 1}

    """ Inicializace tridy """

    def __init__(self, filepath=None):
        if filepath is not None:
            with open(filepath, 'r') as f:
                self.board_history = [moves for moves in f]
            current = self.board_history[-1]
            pF = current.find(' ')
            self.white_plays = True if current[pF:pF + 2] == 'w' else False
            pF += 3
            pL = current.find(' ', pF)
            self.castling_rights = current[pF:pL]
            pF = pL + 1
            pL = current.find(' ', pF)
            self.en_passant = current[pF:pL]
            pF = pL + 1
            pL = current.find(' ', pF)
            self.half_move = ord(current[pF:pL]) - ord('0')
            pF = pL + 1
            self.full_move = ord(current[pF:]) - ord('0')
        else:
            self.board_history = ['rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1']
            self.white_plays = True
            self.castling_rights = "KQkq"
            self.en_passant = '-'
            self.half_move = 0
            self.full_move = 1
        self.board = None
        self.__create_board()
        self.game_over = False

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

    """ Destruktor """

    def __del__(self):
        # body of destructor
        pass

    """ Prace se soubory """

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

    """ Move execution """

    def move(self, start_position, end_position):
        """
        function performs a move
        :param start_position: position where is the piece standing before the move
        :param end_position: position to which is the piece moved
        :return: True if move was valid and it was made, else False
        """
        if self.__is_valid(start_position, end_position):
            start_row = self.NUMBER_TO_INDEX[ord(start_position[1]) - ord('0')]
            start_col = self.LETTER_TO_INDEX[start_position[0]]
            end_row = self.NUMBER_TO_INDEX[ord(end_position[1]) - ord('0')]
            end_col = self.LETTER_TO_INDEX[end_position[0]]

            # "pohne" figurkou - na puvodni pozici ulozi None, novou pozici prepise nazvem figurky se kterou se hralo
            tmp = self.board[start_row][start_col]
            self.board[start_row][start_col] = None
            self.board[end_row][end_col] = tmp
            # TODO: pridat funkce pro rosadu a brani mimochodem; asi taky funkci pro vyhazovani figurek
            # TODO: nekam asi ukladat vyhozene figurky??
            # TODO: funkce pro vyber figurky, kdyz pesak dojde na konec

            self.white_plays = not self.white_plays
            # TODO: pridat ulozeni tahu do historie
            return True
        return False

    """ Move validation """

    def __is_valid(self, start_position, end_position):
        """
        checks if move is legal
        :param start_position: position where is the piece standing before the move
        :param end_position: position to which is the piece moved
        :return: True if move is valid else False
        """
        # kontroluje, jestli hra neskoncila
        if not self.game_over:
            # kontroluje spravnost souradnic
            if self.__coord_valid(start_position) and self.__coord_valid(end_position):
                # kontroluje jestli je na danych pcatecnih souradnicich vlastni figurka
                if self.__is_own_piece(
                        self.__find_piece_on_coords(start_position[0], ord(start_position[1]) - ord('0'))):
                    # kontroluje jestli je tah pro figurku podle pravidel sachu legalni
                    if self.__move_legal(start_position, end_position):
                        board = deepcopy(self.board)
                        start_row = self.NUMBER_TO_INDEX[ord(start_position[1]) - ord('0')]
                        start_col = self.LETTER_TO_INDEX[start_position[0]]
                        end_row = self.NUMBER_TO_INDEX[ord(end_position[1]) - ord('0')]
                        end_col = self.LETTER_TO_INDEX[end_position[0]]
                        tmp = board[start_row][start_col]
                        board[start_row][start_col] = None
                        board[end_row][end_col] = tmp
                        if not self.king_in_check(board):
                            return True
        return False

    def __coord_valid(self, coord):
        """
        function checks if coordinates are inside the game board
        :param coord: coordinates in form "<file><rank>"
        :return: True if coordinates are valid, else False
        """
        if coord[0] in "abcdefgh" and coord[1] in "12345678":
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
        piece = (self.__find_piece_on_coords(file, rank))
        piece = piece.lower()
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

    """ Other functions concerning pieces """

    def __find_piece_on_coords(self, file, rank, board=None):
        """
        function finds a piece that is standing at given coordinates
        :param file: = a column of the playboard, 'a' to 'h'
        :param rank: = a row of the playboard, 1 to 8
        :return: piece if there is a piece at given coordinates, else None
        """
        if board is None:
            return self.board[self.NUMBER_TO_INDEX[rank]][self.LETTER_TO_INDEX[file]]
        else:
            return board[self.NUMBER_TO_INDEX[rank]][self.LETTER_TO_INDEX[file]]

    def __is_own_piece(self, piece):
        """
        function determines if the given piece belongs to the player who has just tried to make a move
        :param piece: a letter representing piece at the playboard
        :return: True if piece to the player who has just tried to make a move, else False
        """
        if piece is not None:
            if (piece.isupper() and self.white_plays) or (piece.islower() and not self.white_plays):
                return True
        return False

    """ Piece moves """

    def get_pawn_moves(self, file, rank):
        """
        function finds all moves available for a pawn standing at given coordinates
        :param file: = a column of the playboard, 'a' to 'h'
        :param rank: = a row of the playboard, 1 to 8
        :return: list of all possible pawn moves
        """
        # TODO: Kontrola figurky pri pohybu dopredu - mam to delat i tady? uz to dela __is_valid()
        possible_moves = []
        if self.__is_own_piece(self.__find_piece_on_coords(file, rank)):
            file_num = self.LETTER_TO_INDEX[file]
            # bily je na tahu
            if self.white_plays:
                possible_moves.append(file + str(rank + 1))
                # pesak se jeste nepohnul
                if rank == 2:
                    possible_moves.append(file + str(rank + 2))
                # pesak muze neco sebrat
                try:
                    piece = self.__find_piece_on_coords(self.INDEX_TO_LETTER[file_num - 1], rank + 1)
                    if (piece is not None) and (not self.__is_own_piece(piece)):
                        possible_moves.append(self.INDEX_TO_LETTER[file_num - 1] + str(rank - 1))
                except:
                    pass
                try:
                    piece = self.__find_piece_on_coords(self.INDEX_TO_LETTER[file_num + 1], rank + 1)
                    if (piece is not None) and (not self.__is_own_piece(piece)):
                        possible_moves.append(self.INDEX_TO_LETTER[file_num + 1] + str(rank - 1))
                except:
                    pass
                # moznost brani mimochodem
                if self.en_passant != '-' and rank == 5 and (
                        (ord(file) == ord(self.en_passant[0]) + 1) or (ord(file) == ord(self.en_passant[0]) - 1)):
                    possible_moves.append(self.en_passant)
            # cerny je na tahu
            else:
                possible_moves.append(file + str(rank - 1))
                # pesak se jeste nepohnul
                if rank == 7:
                    possible_moves.append(file + str(rank - 2))
                # pesak muze neco sebrat
                try:
                    piece = self.__find_piece_on_coords(self.INDEX_TO_LETTER[file_num - 1], rank - 1)
                    if (piece is not None) and (not self.__is_own_piece(piece)):
                        possible_moves.append(self.INDEX_TO_LETTER[file_num - 1] + str(rank - 1))
                except:
                    pass
                try:
                    piece = self.__find_piece_on_coords(self.INDEX_TO_LETTER[file_num + 1], rank - 1)
                    if (piece is not None) and (not self.__is_own_piece(piece)):
                        possible_moves.append(self.INDEX_TO_LETTER[file_num + 1] + str(rank - 1))
                except:
                    pass
                # moznost brani mimochodem
                if self.en_passant != '-' and rank == 4 and (
                        (ord(file) == ord(self.en_passant[0]) + 1) or (ord(file) == ord(self.en_passant[0]) - 1)):
                    possible_moves.append(self.en_passant)
        return possible_moves

    def get_rook_moves(self, file, rank):
        """
        function finds all moves available for a rook standing at given coordinates
        :param file: = a column of the gameboard, 'a' to 'h'
        :param rank: = a row of the gameboard, 1 to 8
        :return: list of all possible rook moves
        """
        possible_moves = []
        if self.__is_own_piece(self.__find_piece_on_coords(file, rank)):
            file_num = self.LETTER_TO_INDEX[file]
            # sloupec
            for r in range(rank - 1, 0, -1):
                # nemuze za obsazene pole (a na obsazene pole v pripade vlastni figurky)
                p = self.__find_piece_on_coords(file, r)
                if p is not None:
                    if not self.__is_own_piece(p):
                        possible_moves.append(file + str(r))
                    break
                possible_moves.append(file + str(r))
            for r in range(rank + 1, 8):
                # nemuze za obsazene pole (a na obsazene pole v pripade vlastni figurky)
                p = self.__find_piece_on_coords(file, r)
                if p is not None:
                    if not self.__is_own_piece(p):
                        possible_moves.append(file + str(r))
                    break
                possible_moves.append(file + str(r))
            # radek
            for f in range(file_num - 1, 0, -1):
                # nemuze za obsazene pole (a na obsazene pole v pripade vlastni figurky)
                p = self.__find_piece_on_coords(self.INDEX_TO_LETTER[f], rank)
                if p is not None:
                    if not self.__is_own_piece(p):
                        possible_moves.append(self.INDEX_TO_LETTER[f] + str(rank))
                    break
                possible_moves.append(self.INDEX_TO_LETTER[f] + str(rank))
            for f in range(file_num + 1, 8):
                # nemuze za obsazene pole (a na obsazene pole v pripade vlastni figurky)
                p = self.__find_piece_on_coords(self.INDEX_TO_LETTER[f], rank)
                if p is not None:
                    if not self.__is_own_piece(p):
                        possible_moves.append(self.INDEX_TO_LETTER[f] + str(rank))
                    break
                possible_moves.append(self.INDEX_TO_LETTER[f] + str(rank))
        return possible_moves

    def get_knight_moves(self, file, rank):
        """
        function finds all moves available for a knight standing at given coordinates
        :param file: = a column of the playboard, 'a' to 'h'
        :param rank: = a row of the playboard, 1 to 8
        :return: list of all possible knight moves
        """
        possible_moves = []
        if self.__is_own_piece(self.__find_piece_on_coords(file, rank)):
            file_num = self.LETTER_TO_INDEX[file]

            if 0 <= (file_num - 2) <= 7 and 0 < (rank - 1) <= 8 and not self.__is_own_piece(
                    self.__find_piece_on_coords(self.INDEX_TO_LETTER[file_num - 2], rank - 1)):
                possible_moves.append(self.INDEX_TO_LETTER[file_num - 2] + str(rank - 1))
            if 0 <= (file_num - 1) <= 7 and 0 < (rank - 2) <= 8 and not self.__is_own_piece(
                    self.__find_piece_on_coords(self.INDEX_TO_LETTER[file_num - 1], rank - 2)):
                possible_moves.append(self.INDEX_TO_LETTER[file_num - 1] + str(rank - 2))
            if 0 <= (file_num + 1) <= 7 and 0 < (rank - 2) <= 8 and not self.__is_own_piece(
                    self.__find_piece_on_coords(self.INDEX_TO_LETTER[file_num + 1], rank - 2)):
                possible_moves.append(self.INDEX_TO_LETTER[file_num + 1] + str(rank - 2))
            if 0 <= (file_num + 2) <= 7 and 0 < (rank - 1) <= 8 and not self.__is_own_piece(
                    self.__find_piece_on_coords(self.INDEX_TO_LETTER[file_num + 2], rank - 1)):
                possible_moves.append(self.INDEX_TO_LETTER[file_num + 2] + str(rank - 1))
            if 0 <= (file_num + 2) <= 7 and 0 < (rank + 1) <= 8 and not self.__is_own_piece(
                    self.__find_piece_on_coords(self.INDEX_TO_LETTER[file_num + 2], rank + 1)):
                possible_moves.append(self.INDEX_TO_LETTER[file_num + 2] + str(rank + 1))
            if 0 <= (file_num + 1) <= 7 and 0 < (rank + 2) <= 8 and not self.__is_own_piece(
                    self.__find_piece_on_coords(self.INDEX_TO_LETTER[file_num + 1], rank + 2)):
                possible_moves.append(self.INDEX_TO_LETTER[file_num + 1] + str(rank + 2))
            if 0 <= (file_num - 1) <= 7 and 0 < (rank + 2) <= 8 and not self.__is_own_piece(
                    self.__find_piece_on_coords(self.INDEX_TO_LETTER[file_num - 1], rank + 2)):
                possible_moves.append(self.INDEX_TO_LETTER[file_num - 1] + str(rank + 2))
            if 0 <= (file_num - 2) <= 7 and 0 < (rank + 1) <= 8 and not self.__is_own_piece(
                    self.__find_piece_on_coords(self.INDEX_TO_LETTER[file_num - 2], rank + 1)):
                possible_moves.append(self.INDEX_TO_LETTER[file_num - 2] + str(rank + 1))
        return possible_moves

    def get_bishop_moves(self, file, rank):
        """
        function finds all moves available for a bishop standing at given coordinates
        :param file: = a column of the playboard, 'a' to 'h'
        :param rank: = a row of the playboard, 1 to 8
        :return: list of all possible bishop moves
        """
        possible_moves = []
        if self.__is_own_piece(self.__find_piece_on_coords(file, rank)):
            file_num = self.LETTER_TO_INDEX[file]

            i = 1
            while (file_num - i >= 0) and (rank - i > 0):
                # nemuze za obsazene pole (a na obsazene pole v pripade vlastni figurky)
                p = self.__find_piece_on_coords(self.INDEX_TO_LETTER[file_num - i], rank - i)
                if p is not None:
                    if not self.__is_own_piece(p):
                        possible_moves.append(self.INDEX_TO_LETTER[file_num - i] + str(rank - i))
                    break
                possible_moves.append(self.INDEX_TO_LETTER[file_num - i] + str(rank - i))
                i += 1
            i = 1
            while (file_num - i >= 0) and (rank + i < 9):
                # nemuze za obsazene pole (a na obsazene pole v pripade vlastni figurky)
                p = self.__find_piece_on_coords(self.INDEX_TO_LETTER[file_num - i], rank + i)
                if p is not None:
                    if not self.__is_own_piece(p):
                        possible_moves.append(self.INDEX_TO_LETTER[file_num - i] + str(rank + i))
                    break
                possible_moves.append(self.INDEX_TO_LETTER[file_num - i] + str(rank + i))
                i += 1
            i = 1
            while (file_num + i < 8) and (rank - i > 0):
                # nemuze za obsazene pole (a na obsazene pole v pripade vlastni figurky)
                p = self.__find_piece_on_coords(self.INDEX_TO_LETTER[file_num + i], rank - i)
                if p is not None:
                    if not self.__is_own_piece(p):
                        possible_moves.append(self.INDEX_TO_LETTER[file_num + i] + str(rank - i))
                    break
                possible_moves.append(self.INDEX_TO_LETTER[file_num + i] + str(rank - i))
                i += 1
            i = 1
            while (file_num + i < 8) and (rank + i < 9):
                # nemuze za obsazene pole (a na obsazene pole v pripade vlastni figurky)
                p = self.__find_piece_on_coords(self.INDEX_TO_LETTER[file_num + i], rank + i)
                if p is not None:
                    if not self.__is_own_piece(p):
                        possible_moves.append(self.INDEX_TO_LETTER[file_num + i] + str(rank + i))
                    break
                possible_moves.append(self.INDEX_TO_LETTER[file_num + i] + str(rank + i))
                i += 1
        return possible_moves

    def get_queen_moves(self, file, rank):
        """
        function finds all moves available for a queen standing at given coordinates
        :param file: = a column of the playboard, 'a' to 'h'
        :param rank: = a row of the playboard, 1 to 8
        :return: list of all possible queen moves
        """
        possible_moves = []
        if self.__is_own_piece(self.__find_piece_on_coords(file, rank)):
            file_num = self.LETTER_TO_INDEX[file]

            if self.__is_own_piece(self.__find_piece_on_coords(file, rank)):
                file_num = self.LETTER_TO_INDEX[file]
                # sloupec
                for r in range(rank - 1, 0, -1):
                    # nemuze za obsazene pole (a na obsazene pole v pripade vlastni figurky)
                    p = self.__find_piece_on_coords(file, r)
                    if p is not None:
                        if not self.__is_own_piece(p):
                            possible_moves.append(file + str(r))
                        break
                    possible_moves.append(file + str(r))
                for r in range(rank + 1, 8):
                    # nemuze za obsazene pole (a na obsazene pole v pripade vlastni figurky)
                    p = self.__find_piece_on_coords(file, r)
                    if p is not None:
                        if not self.__is_own_piece(p):
                            possible_moves.append(file + str(r))
                        break
                    possible_moves.append(file + str(r))
                # radek
                for f in range(file_num - 1, 0, -1):
                    # nemuze za obsazene pole (a na obsazene pole v pripade vlastni figurky)
                    p = self.__find_piece_on_coords(self.INDEX_TO_LETTER[f], rank)
                    if p is not None:
                        if not self.__is_own_piece(p):
                            possible_moves.append(self.INDEX_TO_LETTER[f] + str(rank))
                        break
                    possible_moves.append(self.INDEX_TO_LETTER[f] + str(rank))
                for f in range(file_num + 1, 8):
                    # nemuze za obsazene pole (a na obsazene pole v pripade vlastni figurky)
                    p = self.__find_piece_on_coords(self.INDEX_TO_LETTER[f], rank)
                    if p is not None:
                        if not self.__is_own_piece(p):
                            possible_moves.append(self.INDEX_TO_LETTER[f] + str(rank))
                        break
                    possible_moves.append(self.INDEX_TO_LETTER[f] + str(rank))

            i = 1
            while (file_num - i >= 0) and (rank - i > 0):
                # nemuze za obsazene pole (a na obsazene pole v pripade vlastni figurky)
                p = self.__find_piece_on_coords(self.INDEX_TO_LETTER[file_num - i], rank - i)
                if p is not None:
                    if not self.__is_own_piece(p):
                        possible_moves.append(self.INDEX_TO_LETTER[file_num - i] + str(rank - i))
                    break
                possible_moves.append(self.INDEX_TO_LETTER[file_num - i] + str(rank - i))
                i += 1
            i = 1
            while (file_num - i >= 0) and (rank + i < 9):
                # nemuze za obsazene pole (a na obsazene pole v pripade vlastni figurky)
                p = self.__find_piece_on_coords(self.INDEX_TO_LETTER[file_num - i], rank + i)
                if p is not None:
                    if not self.__is_own_piece(p):
                        possible_moves.append(self.INDEX_TO_LETTER[file_num - i] + str(rank + i))
                    break
                possible_moves.append(self.INDEX_TO_LETTER[file_num - i] + str(rank + i))
                i += 1
            i = 1
            while (file_num + i < 8) and (rank - i > 0):
                # nemuze za obsazene pole (a na obsazene pole v pripade vlastni figurky)
                p = self.__find_piece_on_coords(self.INDEX_TO_LETTER[file_num + i], rank - i)
                if p is not None:
                    if not self.__is_own_piece(p):
                        possible_moves.append(self.INDEX_TO_LETTER[file_num + i] + str(rank - i))
                    break
                possible_moves.append(self.INDEX_TO_LETTER[file_num + i] + str(rank - i))
                i += 1
            i = 1
            while (file_num + i < 8) and (rank + i < 9):
                # nemuze za obsazene pole (a na obsazene pole v pripade vlastni figurky)
                p = self.__find_piece_on_coords(self.INDEX_TO_LETTER[file_num + i], rank + i)
                if p is not None:
                    if not self.__is_own_piece(p):
                        possible_moves.append(self.INDEX_TO_LETTER[file_num + i] + str(rank + i))
                    break
                possible_moves.append(self.INDEX_TO_LETTER[file_num + i] + str(rank + i))
                i += 1
        return possible_moves

    def get_king_moves(self, file, rank):
        """
        function finds all moves available for a king standing at given coordinates
        :param file: = a column of the playboard, 'a' to 'h'
        :param rank: = a row of the playboard, 1 to 8
        :return: list of all possible king moves
        """
        # TODO: kontrola sachu (tady nebo to nechat na jine fci spolecne s ostatnimi?)
        possible_moves = []
        if self.__is_own_piece(self.__find_piece_on_coords(file, rank)):
            file_num = self.LETTER_TO_INDEX[file]

            if 0 < (rank - 1) <= 8:
                piece = self.__find_piece_on_coords(self.INDEX_TO_LETTER[file_num], rank - 1)
                if not self.__is_own_piece(piece):
                    possible_moves.append(file + str(rank - 1))
            if 0 <= (file_num + 1) <= 7 and 0 < (rank - 1) <= 8:
                piece = self.__find_piece_on_coords(self.INDEX_TO_LETTER[file_num + 1], rank - 1)
                if not self.__is_own_piece(piece):
                    possible_moves.append(self.INDEX_TO_LETTER[file_num + 1] + str(rank - 1))
            if 0 <= (file_num + 1) <= 7:
                piece = self.__find_piece_on_coords(self.INDEX_TO_LETTER[file_num + 1], rank)
                if not self.__is_own_piece(piece):
                    possible_moves.append(self.INDEX_TO_LETTER[file_num + 1] + str(rank))
            if 0 <= (file_num + 1) <= 7 and 0 < (rank + 1) <= 8:
                piece = self.__find_piece_on_coords(self.INDEX_TO_LETTER[file_num + 1], rank + 1)
                if not self.__is_own_piece(piece):
                    possible_moves.append(self.INDEX_TO_LETTER[file_num + 1] + str(rank + 1))
            if 0 <= (rank + 1) <= 7:
                piece = self.__find_piece_on_coords(self.INDEX_TO_LETTER[file_num], rank + 1)
                if not self.__is_own_piece(piece):
                    possible_moves.append(file + str(rank + 1))
            if 0 <= (file_num - 1) <= 7 and 0 < (rank + 1) <= 8:
                piece = self.__find_piece_on_coords(self.INDEX_TO_LETTER[file_num - 1], rank + 1)
                if not self.__is_own_piece(piece):
                    possible_moves.append(self.INDEX_TO_LETTER[file_num - 1] + str(rank + 1))
            if 0 <= (file_num - 1) <= 7:
                piece = self.__find_piece_on_coords(self.INDEX_TO_LETTER[file_num - 1], rank)
                if not self.__is_own_piece(piece):
                    possible_moves.append(self.INDEX_TO_LETTER[file_num - 1] + str(rank))
            if 0 <= (file_num - 1) <= 7 and 0 < (rank - 1) <= 8:
                piece = self.__find_piece_on_coords(self.INDEX_TO_LETTER[file_num - 1], rank - 1)
                if not self.__is_own_piece(piece):
                    possible_moves.append(self.INDEX_TO_LETTER[file_num - 1] + str(rank - 1))
            # rosada
            if self.white_plays:
                if 'K' in self.castling_rights:
                    possible_moves.append('g1')
                if 'Q' in self.castling_rights:
                    possible_moves.append('c1')
            else:
                if 'k' in self.castling_rights:
                    possible_moves.append('g8')
                if 'q' in self.castling_rights:
                    possible_moves.append('c8')
        return possible_moves

    def king_in_check(self, board):
        king = 'K' if self.white_plays else 'k'
        row = [row for row in board if king in row][0]
        rank = self.INDEX_TO_NUMBER[board.index(row)]
        file_num = row.index(king)

        checks = []
        # checks for checks from rooks and queen
        # horizontal direction
        for f in range(file_num - 1, 0, -1):
            piece = self.__find_piece_on_coords(self.INDEX_TO_LETTER[f], rank, board)
            if self.__is_own_piece(piece):
                break
            elif piece is not None:
                if piece.lower() in 'rq':
                    checks.append(self.INDEX_TO_LETTER[f] + str(rank))
                    break
        for f in range(file_num + 1, 8):
            piece = self.__find_piece_on_coords(self.INDEX_TO_LETTER[f], rank, board)
            if self.__is_own_piece(piece):
                break
            elif piece is not None:
                if piece.lower() in 'rq':
                    checks.append(self.INDEX_TO_LETTER[f] + str(rank))
                    break

        # vertical direction
        for r in range(rank - 1, 0, -1):
            piece = self.__find_piece_on_coords(self.INDEX_TO_LETTER[file_num], r, board)
            if self.__is_own_piece(piece):
                break
            elif piece is not None:
                if piece.lower() in 'rq':
                    checks.append(self.INDEX_TO_LETTER[file_num] + str(r))
                    break
        for r in range(rank + 1, 9):
            piece = self.__find_piece_on_coords(self.INDEX_TO_LETTER[file_num], r, board)
            if self.__is_own_piece(piece):
                break
            elif piece is not None:
                if piece.lower() in 'rq':
                    checks.append(self.INDEX_TO_LETTER[file_num] + str(r))
                    break

        # checks for checks from bishops and queen
        # from left to right
        i = 1
        while (file_num - i) >= 0 and (rank - i) > 0:
            piece = self.__find_piece_on_coords(self.INDEX_TO_LETTER[file_num - i], rank - i, board)
            if self.__is_own_piece(piece):
                break
            elif piece is not None:
                if piece.lower() in 'bq':
                    checks.append(self.INDEX_TO_LETTER[file_num - i] + str(rank - i))
                    break
            i += 1
        i = 1
        while (file_num + i) < 8 and (rank + i) <= 8:
            piece = self.__find_piece_on_coords(self.INDEX_TO_LETTER[file_num + i], rank + i, board)
            if self.__is_own_piece(piece):
                break
            elif piece is not None:
                if piece.lower() in 'bq':
                    checks.append(self.INDEX_TO_LETTER[file_num + i] + str(rank + i))
                    break
            i += 1

        # from right to left
        i = 1
        while (file_num + i) < 8 and (rank - i) > 0:
            piece = self.__find_piece_on_coords(self.INDEX_TO_LETTER[file_num + i], rank - i, board)
            if self.__is_own_piece(piece):
                break
            elif piece is not None:
                if piece.lower() in 'bq':
                    checks.append(self.INDEX_TO_LETTER[file_num + i] + str(rank - i))
                    break
            i += 1
        i = 1
        while (file_num - i) >= 0 and (rank + i) <= 8:
            piece = self.__find_piece_on_coords(self.INDEX_TO_LETTER[file_num - i], rank + i, board)
            if self.__is_own_piece(piece):
                break
            elif piece is not None:
                if piece.lower() in 'bq':
                    checks.append(self.INDEX_TO_LETTER[file_num - i] + str(rank + i))
                    break
            i += 1

        # checks for checks from knights
        if 0 <= (file_num - 2) <= 7 and 0 < (rank - 1) <= 8:
            piece = self.__find_piece_on_coords(self.INDEX_TO_LETTER[file_num - 2], rank - 1, board)
            if (piece is not None) and (not self.__is_own_piece(piece)):
                if piece.lower() == 'n':
                    checks.append(self.INDEX_TO_LETTER[file_num - 2] + str(rank - 1))
        if 0 <= (file_num - 1) <= 7 and 0 < (rank - 2) <= 8:
            piece = self.__find_piece_on_coords(self.INDEX_TO_LETTER[file_num - 1], rank - 2, board)
            if (piece is not None) and (not self.__is_own_piece(piece)):
                if piece.lower() == 'n':
                    checks.append(self.INDEX_TO_LETTER[file_num - 1] + str(rank - 2))
        if 0 <= (file_num + 1) <= 7 and 0 < (rank - 2) <= 8:
            piece = self.__find_piece_on_coords(self.INDEX_TO_LETTER[file_num + 1], rank - 2, board)
            if (piece is not None) and (not self.__is_own_piece(piece)):
                if piece.lower() == 'n':
                    checks.append(self.INDEX_TO_LETTER[file_num + 1] + str(rank - 2))
        if 0 <= (file_num + 2) <= 7 and 0 < (rank - 1) <= 8:
            piece = self.__find_piece_on_coords(self.INDEX_TO_LETTER[file_num + 2], rank - 1, board)
            if (piece is not None) and (not self.__is_own_piece(piece)):
                if piece.lower() == 'n':
                    checks.append(self.INDEX_TO_LETTER[file_num + 2] + str(rank - 1))
        if 0 <= (file_num + 2) <= 7 and 0 < (rank + 1) <= 8:
            piece = self.__find_piece_on_coords(self.INDEX_TO_LETTER[file_num + 2], rank + 1, board)
            if (piece is not None) and (not self.__is_own_piece(piece)):
                if piece.lower() == 'n':
                    checks.append(self.INDEX_TO_LETTER[file_num + 2] + str(rank + 1))
        if 0 <= (file_num + 1) <= 7 and 0 < (rank + 2) <= 8:
            piece = self.__find_piece_on_coords(self.INDEX_TO_LETTER[file_num + 1], rank + 2, board)
            if (piece is not None) and (not self.__is_own_piece(piece)):
                if piece.lower() == 'n':
                    checks.append(self.INDEX_TO_LETTER[file_num + 1] + str(rank + 2))
        if 0 <= (file_num - 1) <= 7 and 0 < (rank + 2) <= 8:
            piece = self.__find_piece_on_coords(self.INDEX_TO_LETTER[file_num - 1], rank + 2, board)
            if (piece is not None) and (not self.__is_own_piece(piece)):
                if piece.lower() == 'n':
                    checks.append(self.INDEX_TO_LETTER[file_num - 1] + str(rank + 2))
        if 0 <= (file_num - 2) <= 7 and 0 < (rank + 1) <= 8:
            piece = self.__find_piece_on_coords(self.INDEX_TO_LETTER[file_num - 2], rank + 1, board)
            if (piece is not None) and (not self.__is_own_piece(piece)):
                if piece.lower() == 'n':
                    checks.append(self.INDEX_TO_LETTER[file_num - 2] + str(rank + 1))

        # checks for checks from pawns
        if self.white_plays:
            if 0 <= (file_num - 1) <= 7 and 0 < (rank - 1) <= 8:
                piece = self.__find_piece_on_coords(self.INDEX_TO_LETTER[file_num - 1], rank - 1, board)
                if (piece is not None) and (not self.__is_own_piece(piece)):
                    if piece == 'p':
                        checks.append(self.INDEX_TO_LETTER[file_num - 1] + str(rank - 1))
            if 0 <= (file_num + 1) <= 7 and 0 < (rank - 1) <= 8:
                piece = self.__find_piece_on_coords(self.INDEX_TO_LETTER[file_num + 1], rank - 1, board)
                if (piece is not None) and (not self.__is_own_piece(piece)):
                    if piece == 'p':
                        checks.append(self.INDEX_TO_LETTER[file_num + 1] + str(rank - 1))
        else:
            if 0 <= (file_num - 1) <= 7 and 0 < (rank + 1) <= 8:
                piece = self.__find_piece_on_coords(self.INDEX_TO_LETTER[file_num - 1], rank + 1, board)
                if (piece is not None) and (not self.__is_own_piece(piece)):
                    if piece == 'P':
                        checks.append(self.INDEX_TO_LETTER[file_num - 1] + str(rank + 1))
            if 0 <= (file_num + 1) <= 7 and 0 < (rank + 1) <= 8:
                piece = self.__find_piece_on_coords(self.INDEX_TO_LETTER[file_num + 1], rank + 1, board)
                if (piece is not None) and (not self.__is_own_piece(piece)):
                    if piece == 'P':
                        checks.append(self.INDEX_TO_LETTER[file_num + 1] + str(rank + 1))

        return checks

    def print_board(self):
        # TODO: add function description
        for line in self.board:
            for cell in line:
                print(cell if cell is not None else '-', end=' ')
            print()

    # TODO: - po tahu neni vlastni kral v sachu
    # TODO: pridat 50 move rule


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


if __name__ == "__main__":
    play_from_file('hra.txt')
