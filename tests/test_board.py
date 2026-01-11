from src.board import Board
from src.position import Position
from src.piece import Piece
from src.config import Color
import pytest


class TestBoard:
    """Comprehensive test suite for Board class"""

    # ========== Initialization Tests ==========

    def test_init(self):
        """Test board initialization with correct piece counts"""
        board = Board()
        assert board.black_count == 12
        assert board.white_count == 12
        assert board.black_kings == 0
        assert board.white_kings == 0
        assert len(board.pieces) == 24  # 12 white + 12 black

    def test_init_piece_placement(self):
        """Test that pieces are placed correctly on dark squares"""
        board = Board()

        # White pieces should be in rows 0-2 on dark squares
        for row in range(3):
            for col in range(8):
                position = Position(row, col)
                if position.valid:
                    piece = board.get_piece(position)
                    if (row % 2 == 0 and col % 2 == 0) or (row % 2 == 1 and col % 2 == 1):
                        assert piece.color == Color.WHITE
                    else:
                        assert piece is None

        # Black pieces should be in rows 5-7 on dark squares
        for row in range(5, 8):
            for col in range(8):
                position = Position(row, col)
                if position.valid:
                    piece = board.get_piece(position)
                    if (row % 2 == 0 and col % 2 == 0) or (row % 2 == 1 and col % 2 == 1):
                        assert piece.color == Color.BLACK
                    else:
                        assert piece is None

        # Middle rows should be empty
        for row in range(3, 5):
            for col in range(8):
                position = Position(row, col)
                if position.valid:
                    assert board.get_piece(position) is None

    # ========== Get Piece Tests ==========

    def test_get_piece_white(self):
        """Test getting white pieces from initial positions"""
        board = Board()

        position = Position(0, 2)
        piece = board.get_piece(position)
        assert piece.color == Color.WHITE

        position = Position(1, 5)
        piece = board.get_piece(position)
        assert piece.color == Color.WHITE

    def test_get_piece_black(self):
        """Test getting black pieces from initial positions"""
        board = Board()

        position = Position(7, 1)
        piece = board.get_piece(position)
        assert piece.color == Color.BLACK

        position = Position(6, 2)
        piece = board.get_piece(position)
        assert piece.color == Color.BLACK

    def test_get_piece_empty(self):
        """Test getting piece from empty position returns None"""
        board = Board()

        position = Position(3, 5)
        piece = board.get_piece(position)
        assert piece is None

        position = Position(4, 0)
        piece = board.get_piece(position)
        assert piece is None

    # ========== Remove Piece Tests ==========

    def test_remove_piece_white(self):
        """Test removing a white piece decrements count"""
        board = Board()
        assert board.white_count == 12

        position = Position(2, 6)
        assert board.get_piece(position) is not None

        board.remove_piece(position)
        assert board.get_piece(position) is None
        assert board.white_count == 11

    def test_remove_piece_black(self):
        """Test removing a black piece decrements count"""
        board = Board()
        assert board.black_count == 12

        position = Position(5, 1)
        assert board.get_piece(position) is not None

        board.remove_piece(position)
        assert board.get_piece(position) is None
        assert board.black_count == 11

    def test_remove_piece_from_empty_position(self):
        """Test removing from empty position raises ValueError"""
        board = Board()

        with pytest.raises(ValueError):
            position = Position(4, 0)
            board.remove_piece(position)

    def test_remove_multiple_pieces(self):
        """Test removing multiple pieces updates counts correctly"""
        board = Board()

        positions_to_remove = [
            Position(0, 0),  # white
            Position(1, 1),  # white
            Position(5, 1),  # black
            Position(6, 4),  # black
        ]

        for pos in positions_to_remove:
            board.remove_piece(pos)

        assert board.white_count == 10
        assert board.black_count == 10

    # ========== Set Piece Tests ==========

    def test_set_piece_on_empty_square(self):
        """Test placing a piece on an empty square"""
        board = Board()
        position = Position(3, 1)
        piece = Piece(color=Color.WHITE)

        board.set_piece(position, piece)

        assert board.get_piece(position) == piece
        assert board.get_piece(position).color == Color.WHITE

    def test_set_piece_replaces_existing(self):
        """Test that setting a piece replaces existing piece"""
        board = Board()
        position = Position(0, 0)

        # Initially has white piece
        assert board.get_piece(position).color == Color.WHITE

        # Replace with black piece
        new_piece = Piece(color=Color.BLACK)
        board.set_piece(position, new_piece)

        assert board.get_piece(position).color == Color.BLACK

    def test_set_piece_updates_counts(self):
        """Test that setting piece updates piece counts"""
        board = Board()
        position = Position(3, 3)

        # Add white piece
        piece = Piece(color=Color.WHITE)
        board.set_piece(position, piece)
        assert board.white_count == 13

        # Remove it
        board.remove_piece(position)
        assert board.white_count == 12

    # ========== Is Empty Tests ==========

    def test_is_empty_on_empty_square(self):
        """Test is_empty returns True for empty square"""
        board = Board()
        position = Position(3, 3)

        assert board.is_empty(position) is True

    def test_is_empty_on_occupied_square(self):
        """Test is_empty returns False for occupied square"""
        board = Board()
        position = Position(0, 0)

        assert board.is_empty(position) is False

    def test_is_empty_after_removal(self):
        """Test is_empty returns True after piece removal"""
        board = Board()
        position = Position(1, 1)

        assert board.is_empty(position) is False
        board.remove_piece(position)
        assert board.is_empty(position) is True

    # ========== Get All Pieces Tests ==========

    def test_get_pieces_with_positions_white(self):
        """Test getting white pieces with their positions"""
        board = Board()
        white_pieces = board.get_pieces_with_positions(Color.WHITE)

        assert len(white_pieces) == 12
        for position, piece in white_pieces:
            assert piece.color == Color.WHITE
            assert isinstance(position, Position)
            assert board.get_piece(position) == piece

    def test_get_pieces_with_positions_black(self):
        """Test getting black pieces with their positions"""
        board = Board()
        black_pieces = board.get_pieces_with_positions(Color.BLACK)

        assert len(black_pieces) == 12
        for position, piece in black_pieces:
            assert piece.color == Color.BLACK
            assert isinstance(position, Position)
            assert board.get_piece(position) == piece

    def test_get_pieces_with_positions_all(self):
        """Test getting all pieces with their positions"""
        board = Board()
        all_pieces = board.get_pieces_with_positions()

        assert len(all_pieces) == 24
        for position, piece in all_pieces:
            assert isinstance(position, Position)
            assert board.get_piece(position) == piece

    def test_iter_pieces(self):
        """Test iterating over pieces"""
        board = Board()

        black_count = 0
        for position, piece in board.iter_pieces(Color.BLACK):
            assert piece.color == Color.BLACK
            black_count += 1

        assert black_count == 12
    # ========== Move Tests ==========

    def test_move_piece_simple(self):
        """Test moving a piece from one position to another
        Move legality is checked outside"""
        board = Board()
        from_pos = Position(2, 0)
        to_pos = Position(3, 1)

        piece = board.get_piece(from_pos)
        assert piece is not None

        board.move(from_pos, to_pos)

        assert board.get_piece(from_pos) is None
        assert board.get_piece(to_pos) == piece

    def test_move_to_occupied_square(self):
        """Test moving to an occupied square (should handle or raise error)"""
        board = Board()
        from_pos = Position(2, 0)
        to_pos = Position(1, 1)  # Already occupied

        # This should either raise an error or handle the conflict
        # Depending on your implementation, adjust the assertion
        with pytest.raises(Exception):  # Replace with specific exception
            board.move(from_pos, to_pos)

    def test_move_promotes_to_king_black(self):
        """Test that black piece promotes to king when reaching row 0"""
        board = Board()

        # Place black piece near promotion
        from_pos = Position(1, 1)
        board.set_piece(from_pos, Piece(color=Color.BLACK))

        to_pos = Position(0, 0)
        board.remove_piece(to_pos)
        board.move(from_pos, to_pos)

        piece = board.get_piece(to_pos)
        assert piece.is_king is True
        assert board.black_kings == 1

    def test_move_promotes_to_king_white(self):
        """Test that white piece promotes to king when reaching row 7"""
        board = Board()

        # Place white piece near promotion
        from_pos = Position(6, 2)
        board.set_piece(from_pos, Piece(color=Color.WHITE))

        to_pos = Position(7, 3)
        board.remove_piece(to_pos)
        board.move(from_pos, to_pos)

        piece = board.get_piece(to_pos)
        assert piece.is_king is True
        assert board.white_kings == 1

    def test_move_king_does_not_increment_count_again(self):
        """Test that moving an already-king piece doesn't increment king count"""
        board = Board()

        # Create and place a king
        piece = Piece(color=Color.WHITE)
        piece.promote_to_king()
        from_pos = Position(6, 2)
        board.remove_piece(from_pos)
        board.set_piece(from_pos, piece)
        board.white_kings = 1

        # Move the king
        to_pos = Position(7, 3)
        board.remove_piece(to_pos)
        board.move(from_pos, to_pos)

        assert board.white_kings == 1  # Should not increment again

    # ========== Copy Tests ==========

    def test_copy_creates_independent_board(self):
        """Test that copy creates an independent board"""
        board = Board()
        board_copy = board.copy()

        # Modify original
        board.remove_piece(Position(0, 0))

        # Copy should be unchanged
        assert board.white_count == 11
        assert board_copy.white_count == 12

    def test_copy_preserves_all_pieces(self):
        """Test that copy preserves all pieces"""
        board = Board()
        board_copy = board.copy()

        assert len(board_copy.pieces) == len(board.pieces)
        assert board_copy.white_count == board.white_count
        assert board_copy.black_count == board.black_count

    def test_copy_pieces_are_independent(self):
        """Test that pieces in copy are independent from original"""
        board = Board()
        board_copy = board.copy()

        # Promote a piece in original
        position = Position(0, 0)
        piece = board.get_piece(position)
        piece.promote_to_king()

        # Copy's piece should not be affected
        copy_piece = board_copy.get_piece(position)
        assert piece.is_king is True
        assert copy_piece.is_king is False

    # ========== To Array Tests ==========

    def test_to_array_shape(self):
        """Test that to_array returns correct shape"""
        board = Board()
        array = board.to_array()

        # Should return 8x8 array or 8x8xN for multi-channel
        assert array.shape[0] == 8
        assert array.shape[1] == 8

    def test_to_array_empty_squares(self):
        """Test that empty squares are represented correctly in array"""
        board = Board()
        array = board.to_array()

        # Check middle empty rows
        # Representation depends on your encoding scheme
        # Adjust based on your implementation
        pass

    def test_to_array_piece_representation(self):
        """Test that pieces are correctly represented in array"""
        board = Board()
        array = board.to_array()

        # Test specific piece positions
        # Adjust based on your encoding scheme
        pass

    # ========== Winner Tests ==========

    def test_winner_initial_state(self):
        """Test no winner in initial state"""
        board = Board()
        assert board.winner() is None

    def test_winner_white_wins(self):
        """Test white wins when all black pieces removed"""
        board = Board()

        # Remove all black pieces
        black_positions = [
            Position(5, 1), Position(5, 3), Position(5, 5), Position(5, 7),
            Position(6, 0), Position(6, 2), Position(6, 4), Position(6, 6),
            Position(7, 1), Position(7, 3), Position(7, 5), Position(7, 7)
        ]

        for pos in black_positions:
            board.remove_piece(pos)

        assert board.winner() == Color.WHITE

    def test_winner_black_wins(self):
        """Test black wins when all white pieces removed"""
        board = Board()

        # Remove all white pieces
        white_positions = [
            Position(0, 0), Position(0, 2), Position(0, 4), Position(0, 6),
            Position(1, 1), Position(1, 3), Position(1, 5), Position(1, 7),
            Position(2, 0), Position(2, 2), Position(2, 4), Position(2, 6)
        ]

        for pos in white_positions:
            board.remove_piece(pos)

        assert board.winner() == Color.BLACK

    # ========== Edge Cases ==========

    def test_operations_on_invalid_positions(self):
        """Test that operations on out-of-bounds positions are handled"""
        board = Board()

        # This depends on whether Position validates itself
        # or if Board validates positions
        invalid_positions = [
            Position(-1, 0),
            Position(0, -1),
            Position(8, 0),
            Position(0, 8),
            Position(10, 10)
        ]

        for pos in invalid_positions:
            assert pos.valid is False
            piece = board.get_piece(pos)
            assert piece is None

    def test_remove_all_pieces(self):
        """Test removing all pieces from board"""
        board = Board()

        all_positions_pieces = board.get_pieces_with_positions()
        for (position, piece) in all_positions_pieces:
            board.remove_piece(position)

        assert len(board.pieces) == 0
        assert board.white_count == 0
        assert board.black_count == 0

    def test_king_count_tracking(self):
        """Test that king counts are tracked correctly"""
        board = Board()

        # Promote some pieces
        white_pos = Position(0, 0)
        black_pos = Position(7, 1)

        white_piece = board.get_piece(white_pos)
        black_piece = board.get_piece(black_pos)

        white_piece.promote_to_king()
        black_piece.promote_to_king()

        board.white_kings += 1
        board.black_kings += 1

        assert board.white_kings == 1
        assert board.black_kings == 1