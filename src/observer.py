from abc import ABC, abstractmethod
from src.board import Board
from src.config import Color, GameState
from src.position import Position
from typing import List, Tuple


class GameObserver(ABC):
    """Abstract observer interface"""

    @abstractmethod
    def on_game_state_changed(self, board: Board, current_player: Color, state: GameState):
        pass

    @abstractmethod
    def get_selected_piece(self) -> Position:
        pass

    '''
    @abstractmethod
    def on_move_made(self, from_pos: Position, to_pos: Position, captured):
        pass
    '''

    @abstractmethod
    def on_piece_selected(self, board: Board, position: Position, valid_moves: List[Tuple[Position, Position]]):
        pass
    '''

    @abstractmethod
    def on_game_over(self, winner):
        pass
    '''
