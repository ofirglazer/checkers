import pygame
from .board import Board
from .constants import RED, WHITE, BLUE, SQUARE_SIZE


class Game:
    def __init__(self, win):
        self.selected = None
        self.turn = None
        self.valid_moves = None
        self._init()
        self.win = win

    def reset(self):
        self._init()

    def _init(self):
        self.selected = None
        self.board = Board()
        self.turn = RED
        self.valid_moves = {}

    def update(self):
        self.board.draw(self.win)
        self.draw_valid_moves(self.valid_moves)
        pygame.display.update()

    def draw_valid_moves(self, moves):
        for move in moves:
            row, col = move
            pygame.draw.circle(self.win, BLUE,
                               (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2),
                               5)

    def select(self, row, col):

        # if there is already a selected piece and now we select the next position / another piece
        if self.selected:

            # try to move to that next position
            result = self._move(row, col)

            # if the move to the next position is invalid
            if not result:

                # deselect the piece and try to reselect as a new piece
                self.selected = None
                self.select(row, col)

        # if there is no currently selected piece, now trying to select a piece
        piece = self.board.get_piece(row, col)

        # if the selection of the piece is successful (there is a piece of the turn's color)
        if piece != 0 and piece.color == self.turn:
            self.selected = piece
            self.valid_moves = self.board.get_valid_moves(piece)

            # return = if we successfully selected a new piece (successful move is obvious to see)
            return True

        return False

    def _move(self, row, col):

        # extract the piece/empty of the next position
        piece = self.board.get_piece(row, col)
        # if the next position is empty and valid
        if piece == 0 and (row, col) in self.valid_moves:
            # then move the selected piece to new position
            self.board.move(self.selected, row, col)
            skipped = self.valid_moves[(row, col)]
            if skipped:
                self.board.remove(skipped)
            self.change_turn()
        else:
            return False
        return True

    def change_turn(self):
        self.valid_moves = {}
        if self.turn == RED:
            self.turn = WHITE
        else:
            self.turn = RED

    def winner(self):
        return self.board.winner()
