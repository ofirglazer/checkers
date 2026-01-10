from src.config import Color
from src.position import Position
from src.board import Board


class MoveValidator:
    @staticmethod
    def is_valid_selection(board: Board, position: Position, current_player: Color) -> bool:
        if current_player == board.get_piece(position).color:
            return True
        return False
