from src.board import Board
from src.position import Position
from src.config import Color, GameState
from src.observer import GameObserver


class CheckersViewConsole(GameObserver):
    def on_game_state_changed(self, board: Board, current_player: Color, state: GameState):
        self.print_board()

    def print_board(board):

        empty = '.'
        red_piece = "r"
        white_piece = "w"
        red_king = "R"
        white_king = "W"
        horizontal = "  +" + "---+" * 8

        # Column header
        print("    " + "   ".join(str(c) for c in range(8)))

        for r in reversed(range(8)):
            print(horizontal)
            print(f"{r} |", end="")

            for c in range(8):
                dark = (r + c) % 2 == 0
                if not dark:
                    cell = "   "  # light square
                else:
                    piece = board.get_piece(Position(r, c))
                    if piece is None:
                        piece_shape = empty
                    elif piece.color == Color.WHITE:
                        piece_shape = white_piece
                    else:
                        piece_shape = red_piece
                    cell = f" {piece_shape} "
                print(cell + "|", end="")
            print()
        print(horizontal)
