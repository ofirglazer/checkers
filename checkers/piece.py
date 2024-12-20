import pygame.draw

from .constants import RED, WHITE, GRAY, SQUARE_SIZE, CROWN


class Piece:
    PADDING = 15
    OUTLINE = 2
    RADIUS = SQUARE_SIZE // 2 - PADDING

    def __init__(self, row, col, color):
        self.row = row
        self.col = col
        self.color = color
        self.king = False

        self.x = 0
        self.y = 0
        self.calc_pos()

    def move(self, row, col):
        self.row = row
        self.col = col
        self.calc_pos()

    def calc_pos(self):
        self.x = SQUARE_SIZE * self.col + SQUARE_SIZE // 2
        self.y = SQUARE_SIZE * self.row + SQUARE_SIZE // 2

    def make_king(self):
        self.king = True

    def draw(self, win):
        pygame.draw.circle(win, GRAY, (self.x, self.y), self.RADIUS + self.OUTLINE)
        pygame.draw.circle(win, self.color, (self.x, self.y), self.RADIUS)
        if self.king:
            win.blit(CROWN, (self.x - CROWN.get_width() // 2, self.y - CROWN.get_height() // 2))

    def __repr__(self):
        return str(self.color)
