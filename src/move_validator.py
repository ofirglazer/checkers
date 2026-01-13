from src.config import Color, CheckersConfig
from src.position import Position
from src.board import Board
from typing import List


class MoveValidator:
    @staticmethod
    def is_valid_selection(board: Board, position: Position, current_player: Color) -> bool:
        """ Return True if the selected piece at position is a valid choice = exists and in player color"""
        selected_piece = board.get_piece(position)
        if selected_piece is None:
            return False

        if current_player == board.get_piece(position).color:
            return True
        return False

    @staticmethod
    def get_all_valid_moves(board: Board, position: Position) -> List[Position]:
        valid_moves = []
        piece = board.get_piece(position)
        if piece is None:
            return valid_moves

        if not piece.is_king:
            if piece.color == Color.WHITE:
                dest_row = position.row + 1
            else:
                dest_row = position.row - 1

            # check left diagonal
            dest_pos = Position(dest_row, position.col - 1)
            if dest_pos.valid:  # position is valid
                if board.is_empty(dest_pos):  # and square is empty
                    valid_moves.append(dest_pos)

            # check right diagonal
            dest_pos = Position(dest_row, position.col + 1)
            if dest_pos.valid:  # position is valid
                if board.is_empty(dest_pos):  # and square is empty
                    valid_moves.append(dest_pos)

        else:  # piece is king

            # left forward
            dest_row = position.row + 1
            dest_col = position.col - 1
            dest_pos = Position(dest_row, dest_col)
            while dest_pos.valid and board.is_empty(dest_pos):
                valid_moves.append(dest_pos)
                dest_row += 1
                dest_col -= 1
                dest_pos = Position(dest_row, dest_col)
                if CheckersConfig.king_movement == 'single_step':
                    dest_pos.valid = False  # stop further steps

            # right forward
            dest_row = position.row + 1
            dest_col = position.col + 1
            dest_pos = Position(dest_row, dest_col)
            while dest_pos.valid and board.is_empty(dest_pos):
                valid_moves.append(dest_pos)
                dest_row += 1
                dest_col += 1
                dest_pos = Position(dest_row, dest_col)
                if CheckersConfig.king_movement == 'single_step':
                    dest_pos.valid = False  # stop further steps

            # left backward
            dest_row = position.row - 1
            dest_col = position.col - 1
            dest_pos = Position(dest_row, dest_col)
            while dest_pos.valid and board.is_empty(dest_pos):
                valid_moves.append(dest_pos)
                dest_row -= 1
                dest_col -= 1
                dest_pos = Position(dest_row, dest_col)
                if CheckersConfig.king_movement == 'single_step':
                    dest_pos.valid = False  # stop further steps

            # right backward
            dest_row = position.row - 1
            dest_col = position.col + 1
            dest_pos = Position(dest_row, dest_col)
            while dest_pos.valid and board.is_empty(dest_pos):
                valid_moves.append(dest_pos)
                dest_row -= 1
                dest_col += 1
                dest_pos = Position(dest_row, dest_col)
                if CheckersConfig.king_movement == 'single_step':
                    dest_pos.valid = False  # stop further steps

        return valid_moves
