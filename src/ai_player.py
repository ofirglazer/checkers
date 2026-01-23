from abc import ABC, abstractmethod
from src.board import Board
from src.config import Color, GameState
from src.position import Position
from src.move import Move
from typing import List, Tuple


class AiPlayer(ABC):
    """Abstract ai player interface"""

    @abstractmethod
    def __init__(self, player: Color):
        pass

    @abstractmethod
    def get_selected_origin(self, board: Board) -> Position:
        pass

    @abstractmethod
    def get_selected_dest(self, board: Board) -> Position:
        pass
