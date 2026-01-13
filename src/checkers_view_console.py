from src.board import Board
from src.position import Position
from src.config import Color, GameState
from src.observer import GameObserver


class CheckersViewConsole(GameObserver):
    @staticmethod
    def on_game_state_changed(board: Board, current_player: Color, state: GameState):
        CheckersViewConsole.print_board(board)

    @staticmethod
    def get_selected_piece() -> Position:
        str = input("Enter row and column of selected piece (e.g. 24 for row=2, col=4: ")
        row = int(str) // 10
        col = int(str) % 10
        return Position(row, col)

    @staticmethod
    def on_piece_selected(board: Board, position: Position, valid_moves: List[Position]):
        CheckersViewConsole.print_board(board, valid_moves)

    @staticmethod
    def print_board(board: Board, valid_moves: List[Tuple[Position, Position]] = None) -> None:

        empty = '.'
        red_piece = "r"
        white_piece = "w"
        red_king = "R"
        white_king = "W"
        valid_move = "O"
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
                        if valid_moves is not None and Position(r, c) in valid_moves:
                            piece_shape = valid_move
                        else:
                            piece_shape = empty
                    elif piece.color == Color.WHITE:
                        piece_shape = white_piece
                    else:
                        piece_shape = red_piece
                    cell = f" {piece_shape} "
                print(cell + "|", end="")
            print()
        print(horizontal)


if __name__ == '__main__':
    console = CheckersViewConsole()
    board = Board()
    position = console.get_selected_piece(board, Color.WHITE, GameState.PLAYING)
    print(position)