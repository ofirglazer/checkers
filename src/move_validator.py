from src.config import Color, CheckersConfig
from src.piece import Piece
from src.position import Position
from src.move import Move
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
    def find_jumps(piece: Piece, board: Board, position: Position) -> List[Move]:

        jumps_moves = []

        def _check_jump_direction(piece: Piece, board: Board, position: Position, direction: str) -> bool:
            if direction == 'nw':
                neighbour_pos = position.nw()
            elif direction == 'ne':
                neighbour_pos = position.ne()
            elif direction == 'sw':
                neighbour_pos = position.sw()
            elif direction == 'se':
                neighbour_pos = position.se()
            else:
                raise ValueError('Invalid direction')

            if neighbour_pos.valid:
                if not board.is_empty(neighbour_pos) and board.get_piece(neighbour_pos).color != piece.color:
                    if direction == 'nw':
                        landing_pos = neighbour_pos.nw()
                    elif direction == 'ne':
                        landing_pos = neighbour_pos.ne()
                    elif direction == 'sw':
                        landing_pos = neighbour_pos.sw()
                    elif direction == 'se':
                        landing_pos = neighbour_pos.se()
                    else:
                        raise ValueError('Invalid direction')
                    if landing_pos.valid:
                        if board.is_empty(landing_pos):
                            return True
            return False

        # TODO if king
        if piece.color == Color.WHITE:
            # North West
            direction = 'nw'
            if _check_jump_direction(piece, board, position, direction):
                pos_landing = position.nw().nw()
                jump_move = Move(position, pos_landing, is_capture=True)
                jump_move.captured_pieces.append(position.nw())
                jumps_moves.append(jump_move)
                jumps_moves.extend(MoveValidator.find_jumps(piece, board, pos_landing))
            # North East
            direction = 'ne'
            if _check_jump_direction(piece, board, position, direction):
                pos_landing = position.ne().ne()
                jump_move = Move(position, pos_landing, is_capture=True)
                jump_move.captured_pieces.append(position.ne())
                jumps_moves.append(jump_move)
                jumps_moves.extend(MoveValidator.find_jumps(piece, board, pos_landing))
        else:  # black piece
            # South West
            direction = 'sw'
            if _check_jump_direction(piece, board, position, direction):
                pos_landing = position.sw().sw()
                jump_move = Move(position, pos_landing, is_capture=True)
                jump_move.captured_pieces.append(position.sw())
                jumps_moves.append(jump_move)
                jumps_moves.extend(MoveValidator.find_jumps(piece, board, pos_landing))
            # South East
            direction = 'se'
            if _check_jump_direction(piece, board, position, direction):
                pos_landing = position.se().se()
                jump_move = Move(position, pos_landing, is_capture=True)
                jump_move.captured_pieces.append(position.se())
                jumps_moves.append(jump_move)
                jumps_moves.extend(MoveValidator.find_jumps(piece, board, pos_landing))

        return jumps_moves



    @staticmethod
    def get_all_valid_moves(board: Board, position: Position) -> List[Move]:
        valid_moves = []
        piece = board.get_piece(position)
        if piece is None:
            return valid_moves

        # first looking for mandatory jumps
        valid_moves.extend(MoveValidator.find_jumps(piece, board, position))
        if valid_moves:
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
                # elif board.get_piece(dest_pos).color != piece.color and
                    # board.is_empty():  # posssible capture



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
