# import pygame.draw
# from .constants import RED, WHITE, GRAY, SQUARE_SIZE, CROWN
from src.config import Color


class Piece:
    # PADDING = 15
    # OUTLINE = 2
    # RADIUS = SQUARE_SIZE // 2 - PADDING

    def __init__(self, color: Color) -> None:
        self.color = color
        self.is_king = False

        # self.x = 0
        # self.y = 0
        # self.calc_pos()

    def promote_to_king(self) -> None:
        self.is_king = True

    def __str__(self) -> str:
        return f"{self.color} Piece, {'IS' if self.is_king else 'not'} a king"


"""  def move(self, row, col):
    self.row = row
    self.col = col
    self.calc_pos()

def calc_pos(self):
    self.x = SQUARE_SIZE * self.col + SQUARE_SIZE // 2
    self.y = SQUARE_SIZE * self.row + SQUARE_SIZE // 2


def draw(self, win):
    pygame.draw.circle(win, GRAY, (self.x, self.y), self.RADIUS + self.OUTLINE)
    pygame.draw.circle(win, self.color, (self.x, self.y), self.RADIUS)
    if self.is_king:
        win.blit(CROWN, (self.x - CROWN.get_width() // 2, self.y - CROWN.get_height() // 2))

def __repr__(self):
    return str(self.color)
    """
