from dataclasses import dataclass
from enum import Enum
# from typing import Tuple


class Color(Enum):
    WHITE = 1
    BLACK = 2


class GameState(Enum):
    PLAYING = 1
    WHITE_WINS = 2
    BLACK_WINS = 3


@dataclass
class CheckersConfig:
    """Configuration for the game"""

    board_size = 8
    ui_type = 'console'  # 'pygame'

    # Display
    # screen_width: int = 600
    # screen_height: int = 600
    # fps: int = 10
