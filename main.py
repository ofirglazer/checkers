# main.py - Entry point of the application
"""
Checkers game # TODO and solver
===============================

This is an checkers game TODO and solver.

MVC Architecture:
- Model (checkers_model.py): Contains game state, logic, and data structures
- View (checkers_view_console.py): Handles all rendering and visual presentation
- Controller (checkers_controller.py): Manages input handling and coordinates model/view
- Main (main.py): Entry point that initializes and starts the game

To run: python main.py
"""
# TODO remove all comments from previous architecture
# TODO add solver to specific status
from src.checkers_controller import CheckersController
from src.checkers_view_console import CheckersViewConsole


def main():
    """Main entry point"""
    print(__doc__)

    controller = CheckersController()
    observer = CheckersViewConsole()
    controller.attach_observer(observer)
    controller.run()


##################

# import pygame

# FPS = 12
# WIN = pygame.display.set_mode((WIDTH, HEIGHT))
# pygame.display.set_caption('Checkers')


# def get_row_col_from_mouse(pos):
#     x, y = pos
#     row = y // SQUARE_SIZE
#     col = x // SQUARE_SIZE
#     return row, col


#     run = True
#     clock = pygame.time.Clock()
#     game = Game(WIN)
#
#     while run:
#         clock.tick(FPS)
#         if game.winner() is not None:
#             print(game.winner())
#
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 run = False
#             if event.type == pygame.MOUSEBUTTONDOWN:
#                 pos = pygame.mouse.get_pos()
#                 row, col = get_row_col_from_mouse(pos)
#                 game.select(row, col)
#
#         game.update()
#
#     pygame.quit()


if __name__ == "__main__":
    main()
