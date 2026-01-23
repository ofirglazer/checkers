from src.position import Position
# from typing import Self  # only supported in Python 3.11+


class Move:
    """ valid move ensures valid from and valid destination positions """
    def __init__(self, from_pos: Position, dest_pos: Position, is_capture: bool = False) -> None:
        if not isinstance(from_pos, Position) or not isinstance(dest_pos, Position):
            raise TypeError("from_pos and dest_pos must be positions")
        self.from_pos = from_pos
        self.dest_pos = dest_pos
        self.valid = self.is_valid()
        self.is_capture = self.is_capture()
        self.captured_pieces = []

    def is_valid(self) -> bool:
        # valid move = from and to valid positions
        if self.from_pos.valid and self.dest_pos.valid and self.from_pos != self.dest_pos:
            return True
        return False

    def is_capture(self) -> bool:
        if abs(self.from_pos.row - self.dest_pos.row) == 1 and abs(self.from_pos.col - self.dest_pos.col) == 1:
            return False
        return True

    def __eq__(self, other) -> bool:  # : Self
        if self.from_pos == other.from_pos and self.dest_pos == other.dest_pos and self.is_capture == other.is_capture:
            return True
        return False

    def __hash__(self):
        return hash((self.from_pos, self.dest_pos, self.is_capture))

    def __str__(self) -> str:
        return f"{'Valid' if self.valid else 'Invalid'} move from {self.from_pos} to {self.dest_pos}, {self.is_capture} capture"
