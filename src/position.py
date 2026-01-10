from typing import Self
from src.config import CheckersConfig


class Position:
    def __init__(self, row: int, col: int) -> None:
        if not isinstance(row, int) or not isinstance(col, int):
            raise TypeError("row and col must be integers")
        self.row = row
        self.col = col
        self.valid = self.is_valid()

    def is_valid(self) -> bool:
        # valid squares = black squares: even row and col or odd row and col
        if (self.row in range(CheckersConfig.board_size) and self.col in range(CheckersConfig.board_size) and
                self.col % 2 == self.row % 2):
            return True
        return False
        # noinspection PyUnresolvedReferences

    def distance(self, other: Self) -> int:
        pass

    def __eq__(self, other: Self) -> bool:
        if self.row == other.row and self.col == other.col:
            return True
        return False

    def __hash__(self):
        return hash((self.row, self.col))

    def __str__(self) -> str:
        return f"({self.row}, {self.col})"
