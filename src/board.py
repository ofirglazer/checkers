# import pygame
# from checkers.constants import BLACK, RED, WHITE, ROWS, COLS, SQUARE_SIZE
from typing import List, Tuple

from src.piece import Piece
from src.position import Position
from src.config import CheckersConfig, Color


class Board:
    def __init__(self) -> None:
        self.pieces = {}  # dict[Position, Piece] - only stores actual pieces
        self.black_count = 0
        self.white_count = 0
        self.black_kings = 0
        self.white_kings = 0

        # initial pieces placement on board
        for row in range(CheckersConfig.board_size):
            for col in range(CheckersConfig.board_size):
                if (row % 2 == 0 and col % 2 == 0) or (row % 2 == 1 and col % 2 == 1):
                    position = Position(row, col)
                    if row <= 2:
                        self.pieces[position] = Piece(color=Color.WHITE)
                        self.white_count += 1
                    elif row >= 5:
                        self.pieces[position] = Piece(color=Color.BLACK)
                        self.black_count += 1

    def get_piece(self, position: Position) -> Piece:
        if position is None or position.valid is False:
            return None
            # raise ValueError("Trying to get a piece from an invalid position")
        return self.pieces.get(position)

    def remove_piece(self, position) -> None:
        valid = self.pieces.pop(position, None)
        if valid is None:
            raise ValueError("Trying to remove a piece from a position without a piece")
        elif valid.color == Color.WHITE:
            self.white_count -= 1
        elif valid.color == Color.BLACK:
            self.black_count -= 1
        else:
            raise RuntimeError("Illegal branch")

    def set_piece(self, position: Position, piece: Piece) -> None:
        self.pieces[position] = piece
        if piece.color == Color.WHITE:
            self.white_count += 1
        elif piece.color == Color.BLACK:
            self.black_count += 1

    def get_pieces_with_positions(self, color: Color = None) -> List[Tuple[Position, Piece]]:
        # Get pieces along with their positions
        if color is None:
            return [(position, piece) for position, piece in self.pieces.items()]
        else:
            return [(position, piece) for position, piece in self.pieces.items() if piece.color == color]

    # +copy() Board
    # +to_array() ndarray
    def is_empty(self, position: Position) -> bool:
        if self.pieces.get(position):
            return False
        return True

        # self.board.append([])
        # for col in range(COLS):
        #     if col % 2 == ((row + 1) % 2):
        #         if row < 3:
        #             self.board[row].append(Piece(row, col, WHITE))
        #         elif row > 4:
        #             self.board[row].append(Piece(row, col, RED))
        #         else:
        #             self.board[row].append(0)
        #     else:
        #         self.board[row].append(0)

        # self.board = []
        # self.selected_piece = None


    '''
    def draw_squares(self, win):
        win.fill(BLACK)
        for row in range(ROWS):
            for col in range(row % 2, ROWS, 2):
                pygame.draw.rect(win, RED, (row * SQUARE_SIZE, col * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
                '''


    def move(self, from_pos: Position, to_pos: Position) -> None:
        """Move a piece from one position to another
                Move legality is checked outside"""
        if self.is_empty(from_pos):
            raise ValueError("Trying to move a piece from a position without a piece")
        if not self.is_empty(to_pos):
            raise ValueError("Trying to move a piece to an occupied position")

        piece = self.get_piece(from_pos)
        self.remove_piece(from_pos)
        self.set_piece(to_pos, piece)

        # promote to king
        if not piece.is_king:
            if to_pos.row == 0 and piece.color == Color.BLACK:
                piece.promote_to_king()
                self.black_kings += 1
            elif to_pos.row == CheckersConfig.board_size - 1 and piece.color == Color.WHITE:
                piece.promote_to_king()
                self.white_kings += 1


'''
    def remove(self, pieces):
        for piece in pieces:
            self.board[piece.row][piece.col] = 0
            if piece.color == RED:
                self.black_count -= 1
            else:
                self.white_count -= 1

    def winner(self):
        if self.black_count <= 0:
            return WHITE
        elif self.white_count <= 0:
            return RED
        return None

    def draw(self, win):
        self.draw_squares(win)
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.board[row][col]
                if piece != 0:
                    piece.draw(win)

    def get_valid_moves(self, piece):
        moves = {}
        left = piece.col - 1
        right = piece.col + 1
        row = piece.row

        if piece.color == RED or piece.is_king:
            moves.update(self._traverse_left(row - 1, max(row - 3, -1), -1, piece.color, left))
            moves.update(self._traverse_right(row - 1, max(row - 3, -1), -1, piece.color, right))
        if piece.color == WHITE or piece.is_king:
            moves.update(self._traverse_left(row + 1, min(row + 3, ROWS), 1, piece.color, left))
            moves.update(self._traverse_right(row + 1, min(row + 3, ROWS), 1, piece.color, right))

        return moves

    def _traverse_left(self, start, stop, step, color, left, skipped=[]):
        moves = {}
        last = []
        for r in range(start, stop, step):
            if left < 0:
                break

            current = self.board[r][left]

            # checking an empty piece
            if current == 0:
                if skipped and not last:
                    break
                elif skipped:
                    moves[(r, left)] = last + skipped

                # SKIPPED and LAST = empty piece after jumping over other color
                # just an empty space
                else:
                    # add to moves dictionary the empty position and pointer to the jumped over piece
                    # if empty piece and no 'last' = add empty position to dictionary and last=[]
                    moves[(r, left)] = last

                # if we jumped over, we prepare for more jumps
                if last:
                    if step == -1:
                        row = max(r - 3, 0)
                    else:
                        row = min(r + 3, ROWS)
                    moves.update(self._traverse_left(r + step, row, step, color, left - 1, skipped=last))
                    moves.update(self._traverse_right(r + step, row, step, color, left + 1, skipped=last))
                break

            # if has piece in own color - invalid move
            elif current.color == color:
                break
            # if has piece in other color - may be able to jump over it in next move
            else:
                # defining 'last' as the piece to jump above
                last = [current]
            left -= 1
        return moves

    def _traverse_right(self, start, stop, step, color, right, skipped=[]):
        moves = {}
        last = []
        for r in range(start, stop, step):
            if right >= COLS:
                break

            current = self.board[r][right]

            # checking an empty piece
            if current == 0:
                if skipped and not last:
                    break
                elif skipped:
                    moves[(r, right)] = last + skipped

                # SKIPPED and LAST = empty piece after jumping over other color
                # just an empty space
                else:
                    # add to moves dictionary the empty position and pointer to the jumped over piece
                    # if empty piece and no 'last' = add empty position to dictionary and last=[]
                    moves[(r, right)] = last

                # if we jumped over, we prepare for more jumps
                if last:
                    if step == -1:
                        row = max(r - 3, 0)
                    else:
                        row = min(r + 3, ROWS)
                    moves.update(self._traverse_left(r + step, row, step, color, right - 1, skipped=last))
                    moves.update(self._traverse_right(r + step, row, step, color, right + 1, skipped=last))
                break

            # if has piece in own color - invalid move
            elif current.color == color:
                break
            # if has piece in other color - may be able to jump over it in next move
            else:
                # defining 'last' as the piece to jump above
                last = [current]
            right += 1
        return moves
        '''
