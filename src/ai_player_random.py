from src.ai_player import AiPlayer
from src.board import Board
from src.position import Position
from src.config import Color
from src.move_validator import MoveValidator
from random import choice


class AiPlayerRandom(AiPlayer):

    def __init__(self, player: Color):
        self.current_player = player
        self.origin = None
        self.destination = None
        self.valid_pieces_moves = None

    def get_selected_origin(self, board: Board) -> Position:
        self.origin = None
        self.destination = None
        validator = MoveValidator()
        self.valid_pieces_moves = {}

        for position, piece in board.pieces.items():
            if validator.is_valid_selection(board, position, self.current_player):
                valid_moves = validator.get_all_valid_moves(board, position)
                if valid_moves:  # this position has valid moves
                    self.valid_pieces_moves[position] = valid_moves
        if not self.valid_pieces_moves:
            raise StopIteration("No valid moves found")
        self.origin = choice(list(self.valid_pieces_moves.keys()))
        return self.origin

    def get_selected_dest(self, board: Board) -> Position:
        moves_from_selected_origin  = self.valid_pieces_moves[self.origin]
        selected_move = choice(moves_from_selected_origin)
        self.destination = selected_move.dest_pos
        return self.destination