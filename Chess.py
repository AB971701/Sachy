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
            current = current.strip()
            pF = current.find(' ') + 1
            self.white_plays = True if current[pF:pF + 1] == 'w' else False
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

    def save_to_file(self, filepath):
        """
        saves game to file
        :param filepath: path to txt file which is the game saved to
        :return:
        """
        with open(filepath, "w") as file:
            for move in self.board_history:
                file.write("%s\n" % move)

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

            halfmove_reset = False

            tmp = self.board[start_row][start_col]

            # "pohne" figurkou - na puvodni pozici ulozi None, novou pozici prepise nazvem figurky se kterou se hralo
            # tah - rosada
            if tmp in 'kK':
                king_moves = self.get_king_moves(start_position[0], ord(start_position[1]) - ord('0'))
                if tmp == 'K' and 'K' in self.castling_rights and 'g1' in king_moves:
                    self.board[7][self.LETTER_TO_INDEX['h']] = None
                    self.board[7][self.LETTER_TO_INDEX['e']] = None
                    self.board[7][self.LETTER_TO_INDEX['g']] = 'K'
                    self.board[7][self.LETTER_TO_INDEX['f']] = 'R'
                elif tmp == 'K' and 'Q' in self.castling_rights and 'c1' in king_moves:
                    self.board[7][self.LETTER_TO_INDEX['a']] = None
                    self.board[7][self.LETTER_TO_INDEX['e']] = None
                    self.board[7][self.LETTER_TO_INDEX['c']] = 'K'
                    self.board[7][self.LETTER_TO_INDEX['d']] = 'R'
                elif tmp == 'k' and 'k' in self.castling_rights and 'g8' in king_moves:
                    self.board[0][self.LETTER_TO_INDEX['h']] = None
                    self.board[0][self.LETTER_TO_INDEX['e']] = None
                    self.board[0][self.LETTER_TO_INDEX['g']] = 'k'
                    self.board[0][self.LETTER_TO_INDEX['f']] = 'r'
                elif tmp == 'k' and 'q' in self.castling_rights and 'c8' in king_moves:
                    self.board[0][self.LETTER_TO_INDEX['a']] = None
                    self.board[0][self.LETTER_TO_INDEX['e']] = None
                    self.board[0][self.LETTER_TO_INDEX['c']] = 'k'
                    self.board[0][self.LETTER_TO_INDEX['d']] = 'r'
                else:
                    self.board[start_row][start_col] = None
                    self.board[end_row][end_col] = tmp

            # tah - en passant
            elif tmp in 'pP' and self.en_passant == end_position and self.en_passant in self.get_pawn_moves(
                    start_position[0], ord(start_position[1]) - ord('0')):
                self.board[start_row][start_col] = None
                self.board[end_row][end_col] = tmp
                ep_row = (end_row - 1) if (tmp == 'p') else (end_row + 1)
                self.board[ep_row][end_col] = None
            # tah - ostatni
            else:
                self.board[start_row][start_col] = None
                self.board[end_row][end_col] = tmp

            # TOHLE UZ NENI TAH
            # brani mimochodem
            self.en_passant = '-'
            if tmp in 'pP':
                if self.white_plays and start_row == 6 and end_row == 4:
                    self.en_passant = start_position[0] + str(self.INDEX_TO_NUMBER[start_row - 1])
                elif not self.white_plays and start_row == 1 and end_row == 3:
                    self.en_passant = start_position[0] + str(self.INDEX_TO_NUMBER[start_row + 1])
                halfmove_reset = True  # pawn advance - 50 move rule
            # rosada
            elif tmp in 'kK':
                if tmp == 'k':
                    self.castling_rights = self.castling_rights.replace('kq', '')
                else:
                    self.castling_rights = self.castling_rights.replace('KQ', '')
                if self.castling_rights == '':
                    self.castling_rights = '-'
            elif tmp in 'rR':
                if tmp == 'r':
                    if start_position == 'a8':
                        self.castling_rights = self.castling_rights.replace('q', '')
                    elif start_position == 'h8':
                        self.castling_rights = self.castling_rights.replace('k', '')
                else:
                    if start_position == 'a1':
                        self.castling_rights = self.castling_rights.replace('Q', '')
                    elif start_position == 'h1':
                        self.castling_rights = self.castling_rights.replace('K', '')

                if self.board[end_row][end_col] is not None:
                    halfmove_reset = True

            # TODO: nekam asi ukladat vyhozene figurky??
            # TODO: funkce pro vyber figurky, kdyz pesak dojde na konec

            if halfmove_reset:
                self.half_move = 0
            else:
                self.half_move += 1
            if not self.white_plays:
                self.full_move += 1
            if self.check_checkmate():
                self.game_over = True
            # TODO: tady nekde kontrola sachu atd.
            self.white_plays = not self.white_plays
            self.__add_move_to_history()
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
                # kontroluje jestli je na danych pcatecnich souradnicich vlastni figurka
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
        :param board: board from which to get the piece
        :return: piece if there is a piece at given coordinates, else None
        """
        if file in 'abcdefgh' and 0 < rank < 9:
            if board is None:
                return self.board[self.NUMBER_TO_INDEX[rank]][self.LETTER_TO_INDEX[file]]
            else:
                return board[self.NUMBER_TO_INDEX[rank]][self.LETTER_TO_INDEX[file]]
        else:
            raise ValueError

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
        possible_moves = []
        if self.__is_own_piece(self.__find_piece_on_coords(file, rank)):
            file_num = self.LETTER_TO_INDEX[file]

            # bily je na tahu
            if self.white_plays:
                if (rank + 1 < 9) and (self.board[self.NUMBER_TO_INDEX[rank + 1]][file_num] is None):
                    possible_moves.append(file + str(rank + 1))

                # pesak se jeste nepohnul
                if rank == 2 and self.board[self.NUMBER_TO_INDEX[3]][file_num] is None and \
                        self.board[self.NUMBER_TO_INDEX[4]][file_num] is None:
                    possible_moves.append(file + str(4))

                # pesak muze neco sebrat
                # -sikmo nahoru vlevo
                if file_num > 0 and rank < 8:
                    piece = self.__find_piece_on_coords(self.INDEX_TO_LETTER[file_num - 1], rank + 1)
                    if (piece is not None) and (not self.__is_own_piece(piece)):
                        possible_moves.append(self.INDEX_TO_LETTER[file_num - 1] + str(rank + 1))
                # -sikmo nahoru vpravo
                if file_num < 7 and rank < 8:
                    piece = self.__find_piece_on_coords(self.INDEX_TO_LETTER[file_num + 1], rank + 1)
                    if (piece is not None) and (not self.__is_own_piece(piece)):
                        possible_moves.append(self.INDEX_TO_LETTER[file_num + 1] + str(rank + 1))

                # moznost brani mimochodem
                if self.en_passant != '-' and rank == 5 and (
                        (ord(file) == ord(self.en_passant[0]) + 1) or (ord(file) == ord(self.en_passant[0]) - 1)):
                    possible_moves.append(self.en_passant)

            # cerny je na tahu
            else:
                if (rank - 1 > 0) and (self.board[self.NUMBER_TO_INDEX[rank - 1]][file_num] is None):
                    possible_moves.append(file + str(rank - 1))

                # pesak se jeste nepohnul
                if rank == 7 and self.board[self.NUMBER_TO_INDEX[5]][file_num] is None and \
                        self.board[self.NUMBER_TO_INDEX[5]][file_num] is None:
                    possible_moves.append(file + str(5))

                # pesak muze neco sebrat
                # -sikmo dolu vlevo
                if file_num > 0 and rank > 1:
                    piece = self.__find_piece_on_coords(self.INDEX_TO_LETTER[file_num - 1], rank - 1)
                    if (piece is not None) and (not self.__is_own_piece(piece)):
                        possible_moves.append(self.INDEX_TO_LETTER[file_num - 1] + str(rank - 1))
                # -sikmo dolu vpravo
                if file_num < 7 and rank > 1:
                    piece = self.__find_piece_on_coords(self.INDEX_TO_LETTER[file_num + 1], rank - 1)
                    if (piece is not None) and (not self.__is_own_piece(piece)):
                        possible_moves.append(self.INDEX_TO_LETTER[file_num + 1] + str(rank - 1))

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
            # -dolu
            for r in range(rank - 1, 0, -1):
                # nemuze za obsazene pole (a na obsazene pole v pripade vlastni figurky)
                p = self.__find_piece_on_coords(file, r)
                if p is not None:
                    if not self.__is_own_piece(p):
                        possible_moves.append(file + str(r))
                    break
                possible_moves.append(file + str(r))
            # -nahoru
            for r in range(rank + 1, 8):
                # nemuze za obsazene pole (a na obsazene pole v pripade vlastni figurky)
                p = self.__find_piece_on_coords(file, r)
                if p is not None:
                    if not self.__is_own_piece(p):
                        possible_moves.append(file + str(r))
                    break
                possible_moves.append(file + str(r))
            # radek
            # -doleva
            for f in range(file_num - 1, -1, -1):
                # nemuze za obsazene pole (a na obsazene pole v pripade vlastni figurky)
                p = self.__find_piece_on_coords(self.INDEX_TO_LETTER[f], rank)
                if p is not None:
                    if not self.__is_own_piece(p):
                        possible_moves.append(self.INDEX_TO_LETTER[f] + str(rank))
                    break
                possible_moves.append(self.INDEX_TO_LETTER[f] + str(rank))
            # -doprava
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

            # 2x doleva, 1x dolu
            if 0 <= (file_num - 2) <= 7 and 0 < (rank - 1) <= 8 and not self.__is_own_piece(
                    self.__find_piece_on_coords(self.INDEX_TO_LETTER[file_num - 2], rank - 1)):
                possible_moves.append(self.INDEX_TO_LETTER[file_num - 2] + str(rank - 1))
            # 1x doleva, 2x dolu
            if 0 <= (file_num - 1) <= 7 and 0 < (rank - 2) <= 8 and not self.__is_own_piece(
                    self.__find_piece_on_coords(self.INDEX_TO_LETTER[file_num - 1], rank - 2)):
                possible_moves.append(self.INDEX_TO_LETTER[file_num - 1] + str(rank - 2))
            # 1x doprava, 2x dolu
            if 0 <= (file_num + 1) <= 7 and 0 < (rank - 2) <= 8 and not self.__is_own_piece(
                    self.__find_piece_on_coords(self.INDEX_TO_LETTER[file_num + 1], rank - 2)):
                possible_moves.append(self.INDEX_TO_LETTER[file_num + 1] + str(rank - 2))
            # 2x doprava, 1x dolu
            if 0 <= (file_num + 2) <= 7 and 0 < (rank - 1) <= 8 and not self.__is_own_piece(
                    self.__find_piece_on_coords(self.INDEX_TO_LETTER[file_num + 2], rank - 1)):
                possible_moves.append(self.INDEX_TO_LETTER[file_num + 2] + str(rank - 1))
            # 2x doprava, 1x nahoru
            if 0 <= (file_num + 2) <= 7 and 0 < (rank + 1) <= 8 and not self.__is_own_piece(
                    self.__find_piece_on_coords(self.INDEX_TO_LETTER[file_num + 2], rank + 1)):
                possible_moves.append(self.INDEX_TO_LETTER[file_num + 2] + str(rank + 1))
            # 1x doprava, 2x nahoru
            if 0 <= (file_num + 1) <= 7 and 0 < (rank + 2) <= 8 and not self.__is_own_piece(
                    self.__find_piece_on_coords(self.INDEX_TO_LETTER[file_num + 1], rank + 2)):
                possible_moves.append(self.INDEX_TO_LETTER[file_num + 1] + str(rank + 2))
            # 1x doleva, 2x nahoru
            if 0 <= (file_num - 1) <= 7 and 0 < (rank + 2) <= 8 and not self.__is_own_piece(
                    self.__find_piece_on_coords(self.INDEX_TO_LETTER[file_num - 1], rank + 2)):
                possible_moves.append(self.INDEX_TO_LETTER[file_num - 1] + str(rank + 2))
            # 2x doleva, 1x nahoru
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
            # doleva dolu
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
            # doleva nahoru
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
            # doprava dolu
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
            # doprava nahoru
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
        possible_moves = self.get_rook_moves(file, rank) + self.get_bishop_moves(file, rank)

        return possible_moves

    def get_king_moves(self, file, rank):
        """
        function finds all moves available for a king standing at given coordinates
        :param file: = a column of the playboard, 'a' to 'h'
        :param rank: = a row of the playboard, 1 to 8
        :return: list of all possible king moves
        """
        possible_moves = []
        if self.__is_own_piece(self.__find_piece_on_coords(file, rank)):
            file_num = self.LETTER_TO_INDEX[file]

            # TODO: tady se nekde musi kontrolovat jestli nebude kral v sachu pokud na to pole vstoupi!!!
            # dolu
            if 0 < (rank - 1) <= 8:
                piece = self.__find_piece_on_coords(self.INDEX_TO_LETTER[file_num], rank - 1)
                if not self.__is_own_piece(piece):
                    possible_moves.append(file + str(rank - 1))
            # sikmo dolu vpravo
            if 0 <= (file_num + 1) <= 7 and 0 < (rank - 1) <= 8:
                piece = self.__find_piece_on_coords(self.INDEX_TO_LETTER[file_num + 1], rank - 1)
                if not self.__is_own_piece(piece):
                    possible_moves.append(self.INDEX_TO_LETTER[file_num + 1] + str(rank - 1))
            # vpravo
            if 0 <= (file_num + 1) <= 7:
                piece = self.__find_piece_on_coords(self.INDEX_TO_LETTER[file_num + 1], rank)
                if not self.__is_own_piece(piece):
                    possible_moves.append(self.INDEX_TO_LETTER[file_num + 1] + str(rank))
            # sikmo nahoru vpravo
            if 0 <= (file_num + 1) <= 7 and 0 < (rank + 1) <= 8:
                piece = self.__find_piece_on_coords(self.INDEX_TO_LETTER[file_num + 1], rank + 1)
                if not self.__is_own_piece(piece):
                    possible_moves.append(self.INDEX_TO_LETTER[file_num + 1] + str(rank + 1))
            # nahoru
            if 0 <= (rank + 1) <= 7:
                piece = self.__find_piece_on_coords(self.INDEX_TO_LETTER[file_num], rank + 1)
                if not self.__is_own_piece(piece):
                    possible_moves.append(file + str(rank + 1))
            # sikmo nahoru vlevo
            if 0 <= (file_num - 1) <= 7 and 0 < (rank + 1) <= 8:
                piece = self.__find_piece_on_coords(self.INDEX_TO_LETTER[file_num - 1], rank + 1)
                if not self.__is_own_piece(piece):
                    possible_moves.append(self.INDEX_TO_LETTER[file_num - 1] + str(rank + 1))
            # vlevo
            if 0 <= (file_num - 1) <= 7:
                piece = self.__find_piece_on_coords(self.INDEX_TO_LETTER[file_num - 1], rank)
                if not self.__is_own_piece(piece):
                    possible_moves.append(self.INDEX_TO_LETTER[file_num - 1] + str(rank))
            # sikmo dolu vlevo
            if 0 <= (file_num - 1) <= 7 and 0 < (rank - 1) <= 8:
                piece = self.__find_piece_on_coords(self.INDEX_TO_LETTER[file_num - 1], rank - 1)
                if not self.__is_own_piece(piece):
                    possible_moves.append(self.INDEX_TO_LETTER[file_num - 1] + str(rank - 1))

            # rosada
            # TODO: kontrola sachu – kral nemuze byt v sachu ani na zacatku, ani v prubehu, ani na konci
            if self.white_plays:
                # kingside
                if ('K' in self.castling_rights) and (self.board[-1][self.LETTER_TO_INDEX['f']] is None) and (
                        self.board[-1][self.LETTER_TO_INDEX['g']] is None):
                    possible_moves.append('g1')
                # queenside
                if ('Q' in self.castling_rights) and (self.board[-1][self.LETTER_TO_INDEX['b']] is None) and (
                        self.board[-1][self.LETTER_TO_INDEX['c']] is None) and (
                        self.board[-1][self.LETTER_TO_INDEX['d']] is None):
                    possible_moves.append('c1')
            else:
                # kingside
                if ('k' in self.castling_rights) and (self.board[0][self.LETTER_TO_INDEX['f']] is None) and (
                        self.board[0][self.LETTER_TO_INDEX['g']] is None):
                    possible_moves.append('g8')
                # queenside
                if ('k' in self.castling_rights) and (self.board[0][self.LETTER_TO_INDEX['b']] is None) and (
                        self.board[0][self.LETTER_TO_INDEX['c']] is None) and (
                        self.board[0][self.LETTER_TO_INDEX['d']] is None):
                    possible_moves.append('c8')
        return possible_moves

    def get_moves(self, file, rank):
        """
        returns all possible moves for a piece standing on given coordinates; if there is no piece, returns None
        :param file:
        :param rank:
        :return: all possible piece moves or None if there is no piece at given coordinates
        """
        piece = self.__find_piece_on_coords(file, rank)
        if piece is not None:
            if (self.white_plays and piece.islower()) or (not self.white_plays and not piece.islower()):
                return None
            if piece in 'Kk':
                return self.get_king_moves(file, rank)
            elif piece in 'Qq':
                return self.get_queen_moves(file, rank)
            elif piece in 'Pp':
                return self.get_pawn_moves(file, rank)
            elif piece in 'Rr':
                return self.get_rook_moves(file, rank)
            elif piece in 'Nn':
                return self.get_knight_moves(file, rank)
            elif piece in 'Bb':
                return self.get_bishop_moves(file, rank)
            else:
                return None
        else:
            return None

    def king_in_check(self, board):
        """
        function to get all places from which is king put in a check
        :param board: chessboard
        :return: list of all coordinates from which is king put in a check
        """
        king = 'K' if self.white_plays else 'k'
        # print([row for row in board if king in row])
        print(board)
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

    """ Print board """

    def print_board(self):
        for line in self.board:
            for cell in line:
                print(cell if cell is not None else '-', end=' ')
            print()

    # TODO: pridat 50 move rule

    def __add_move_to_history(self):
        """
        function saves current
        :return:
        """
        fen = ''
        empty = 0
        for row in self.board:
            empty = 0
            for square in row:
                if square is None:
                    empty += 1
                else:
                    if empty != 0:
                        fen += str(empty)
                        empty = 0
                    fen += square
            if empty != 0:
                fen += str(empty)
                empty = 0
            fen += '/'
        fen = fen[:-1]
        fen += ' '
        fen += 'w' if self.white_plays else 'b'
        fen += ' '
        fen += self.castling_rights
        fen += ' '
        fen += self.en_passant
        fen += ' '
        fen += str(self.half_move)
        fen += ' '
        fen += str(self.full_move)
        self.board_history.append(fen)

    """ End of game """

    def check_checkmate(self):
        if self.king_in_check(self.board):
            checkmate = True
            king = 'K' if self.white_plays else 'k'
            row = [row for row in self.board if king in row][0]
            king_row = self.board.index(row)
            king_col = row.index(king)
            possible_king_moves = self.get_king_moves(self.INDEX_TO_LETTER[king_col], self.INDEX_TO_NUMBER[king_row])
            for move in possible_king_moves:
                board = deepcopy(self.board)
                board[self.NUMBER_TO_INDEX[ord(move[1]) - ord('0')]][self.LETTER_TO_INDEX[move[0]]] = king
                board[king_row][king_col] = None
                if not self.king_in_check(board):
                    return False
            return True
        return False


def play_from_file(filepath):
    c = Chess('test.txt')
    c.print_board()
    with open(filepath) as file:
        moves = [(move.strip()).split(',') for move in file]
        print(moves)
    i = 1
    for move in moves:
        print(i, 'white plays' if c.white_plays else 'black plays')
        if c.move(move[0], move[1]):
            c.print_board()
            print()
        else:
            print('invalid move')
            break
        if (c.check_checkmate()):
            print('game over')
            break
        i += 1


if __name__ == "__main__":
    """c = Chess('fen.txt')
    c.print_board()
    print()
    c.move('c7', 'c6')
    c.print_board()
    print()
    print(c.move('e1', 'g1'))
    c.print_board()
    print()"""
    # play_from_file('hraII.txt')
    c = Chess('mat.txt')
    print(c.board)
    print(c.get_king_moves('g', 8))
    print(c.check_checkmate())
