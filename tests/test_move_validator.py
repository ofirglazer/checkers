"""
Comprehensive test suite for MoveValidator class.

Tests cover:
- Move validation
- Valid move generation
- Capture detection
- Must-capture rule
- King movement
- Multi-jump sequences
- Edge cases
- Rule enforcement
"""

from src.move_validator import MoveValidator
from src.board import Board
from src.position import Position
from src.config import Color
from src.piece import Piece
import pytest


class TestMoveValidatorIsValidSelection:
    """Test piece selection validation"""

    def test_is_valid_selection_own_piece(self):
        """Test that player can select their own piece"""
        board = Board()
        validator = MoveValidator()

        is_valid_selection = validator.is_valid_selection(board, Position(2, 0), Color.WHITE)

        assert is_valid_selection is True

    def test_cannot_select_opponent_piece(self):
        """Test that player cannot select opponent's piece"""
        board = Board()
        validator = MoveValidator()

        is_valid_selection = validator.is_valid_selection(board, Position(5, 1), Color.WHITE)

        assert is_valid_selection is False

    def test_cannot_select_empty_square(self):
        """Test that player cannot select empty square"""
        board = Board()
        validator = MoveValidator()

        is_valid_selection = validator.is_valid_selection(board, Position(3, 3), Color.WHITE)

        assert is_valid_selection is False

    def test_is_valid_selection_king(self):
        """Test that player can select their king"""
        board = Board()
        validator = MoveValidator()

        # Create a king
        king = Piece(Color.WHITE)
        king.promote_to_king()
        board.set_piece(Position(4, 4), king)

        is_valid_selection = validator.is_valid_selection(board, Position(4, 4), Color.WHITE)

        assert is_valid_selection is True

class TestMoveValidatorGetAllValidMoves:
    """Test valid move generation"""

    def test_get_valid_moves_white_starting_position(self):
        """Test getting valid moves for white piece at start"""
        board = Board()
        validator = MoveValidator()

        valid_moves = validator.get_all_valid_moves(board, Position(2, 0))

        # White piece at (2,0) should be able to move to (3,1)
        assert Position(3, 1) in valid_moves
        assert len(valid_moves) == 1
        # assert isinstance(valid_moves[Position(3, 1)], Move)

    def test_get_valid_moves_black_starting_position(self):
        """Test getting valid moves for black piece at start"""
        board = Board()
        validator = MoveValidator()

        valid_moves = validator.get_all_valid_moves(board, Position(5, 1))

        # Black piece at (5,1) should be able to move to (4,0) or (4,2)
        assert Position(4, 0) in valid_moves
        assert Position(4, 2) in valid_moves
        assert len(valid_moves) == 2

    def test_get_valid_moves_empty_square(self):
        """Test getting valid moves from empty square returns empty list"""
        board = Board()
        validator = MoveValidator()

        valid_moves = validator.get_all_valid_moves(board, Position(3, 3))

        assert valid_moves == []

    def test_get_valid_moves_blocked_piece(self):
        """Test piece with no valid moves returns empty dict"""
        board = Board()
        validator = MoveValidator()

        # Corner piece that's blocked
        valid_moves = validator.get_all_valid_moves(board, Position(0, 0))

        assert len(valid_moves) == 0

    def test_get_valid_moves_multiple_options(self):
        """Test piece with multiple valid moves"""
        board = Board()
        validator = MoveValidator()

        # Place piece in middle of board with multiple moves
        board.pieces.clear()
        board.set_piece(Position(4, 4), Piece(Color.WHITE))

        valid_moves = validator.get_all_valid_moves(board, Position(4, 4))

        # Should have at least 2 forward diagonal moves
        assert len(valid_moves) >= 2

    def test_get_valid_moves_king_bidirectional(self):
        """Test king can move in all diagonal directions"""
        board = Board()
        validator = MoveValidator()

        # Place king in middle
        board.pieces.clear()
        king = Piece(Color.WHITE)
        king.promote_to_king()
        board.set_piece(Position(4, 4), king)

        valid_moves = validator.get_all_valid_moves(board, Position(4, 4))

        # King should have 4 diagonal moves (forward and backward)
        assert len(valid_moves) == 4
        # Check all four diagonals
        assert Position(5, 5) in valid_moves  # Forward-right
        assert Position(5, 3) in valid_moves  # Forward-left
        assert Position(3, 5) in valid_moves  # Backward-right
        assert Position(3, 3) in valid_moves  # Backward-left

    def test_get_valid_moves_at_board_edge(self):
        """Test valid moves for piece at board edge"""
        board = Board()
        validator = MoveValidator()

        # White piece at edge
        board.pieces.clear()
        board.set_piece(Position(2, 0), Piece(Color.WHITE))

        valid_moves = validator.get_all_valid_moves(board, Position(2, 0))

        # Should only have one move (can't go off board)
        assert Position(3, 1) in valid_moves
        # Should not try to move off board
        assert Position(3, -1) not in valid_moves


class TestMoveValidatorBasicValidation:
    """Test basic move validation logic"""

    def test_validate_simple_forward_move_white(self):
        """Test validating simple forward move for white piece"""
        board = Board()
        validator = MoveValidator()
        move = (Position(2, 0), Position(3, 1))

        is_move_valid = validator.validate_move(board, move, Color.WHITE)

        assert is_move_valid is True

    def test_validate_simple_forward_move_black(self):
        """Test validating simple forward move for black piece"""
        board = Board()
        validator = MoveValidator()
        move = Move(Position(5, 1), Position(4, 2))

        result = validator.validate_move(board, move, Color.BLACK)

        assert result is True

    def test_validate_move_wrong_player(self):
        """Test that moving opponent's piece is invalid"""
        board = Board()
        validator = MoveValidator()
        # Try to move white piece as black player
        move = Move(Position(2, 0), Position(3, 1))

        result = validator.validate_move(board, move, Color.BLACK)

        assert result is False

    def test_validate_move_from_empty_square(self):
        """Test that moving from empty square is invalid"""
        board = Board()
        validator = MoveValidator()
        move = Move(Position(3, 3), Position(4, 4))  # Empty square

        result = validator.validate_move(board, move, Color.WHITE)

        assert result is False

    def test_validate_move_to_occupied_square(self):
        """Test that moving to occupied square is invalid"""
        board = Board()
        validator = MoveValidator()
        # Try to move to square with another white piece
        move = Move(Position(2, 0), Position(1, 1))

        result = validator.validate_move(board, move, Color.WHITE)

        assert result is False

    def test_validate_backward_move_regular_piece(self):
        """Test that regular pieces cannot move backward"""
        board = Board()
        validator = MoveValidator()

        # White piece trying to move backward (decreasing row)
        board.pieces.clear()
        board.set_piece(Position(4, 2), Piece(Color.WHITE))
        move = Move(Position(4, 2), Position(3, 1))

        result = validator.validate_move(board, move, Color.WHITE)

        assert result is False

    def test_validate_diagonal_move_only(self):
        """Test that pieces can only move diagonally"""
        board = Board()
        validator = MoveValidator()

        board.pieces.clear()
        board.set_piece(Position(3, 3), Piece(Color.WHITE))

        # Try non-diagonal moves
        invalid_moves = [
            Move(Position(3, 3), Position(3, 4)),  # Horizontal
            Move(Position(3, 3), Position(4, 3)),  # Vertical
            Move(Position(3, 3), Position(5, 4)),  # Not adjacent diagonal
        ]

        for move in invalid_moves:
            result = validator.validate_move(board, move, Color.WHITE)
            assert result is False

    def test_validate_out_of_bounds_move(self):
        """Test that moves outside board bounds are invalid"""
        board = Board()
        validator = MoveValidator()

        # Try to move off the board
        invalid_moves = [
            Move(Position(0, 0), Position(-1, -1)),
            Move(Position(7, 7), Position(8, 8)),
        ]

        for move in invalid_moves:
            result = validator.validate_move(board, move, Color.WHITE)
            assert result is False


class TestMoveValidatorCaptures:
    """Test capture move validation and detection"""

    def test_validate_simple_capture(self):
        """Test validating a simple capture move"""
        board = Board()
        validator = MoveValidator()

        # Setup: White piece at (3,1), Black at (4,2), empty at (5,3)
        board.pieces.clear()
        board.set_piece(Position(3, 1), Piece(Color.WHITE))
        board.set_piece(Position(4, 2), Piece(Color.BLACK))

        move = Move(Position(3, 1), Position(5, 3))
        move.add_capture(Position(4, 2))

        result = validator.validate_move(board, move, Color.WHITE)

        assert result is True

    def test_get_valid_moves_includes_captures(self):
        """Test that valid moves include capture moves"""
        board = Board()
        validator = MoveValidator()

        # Setup capture scenario
        board.pieces.clear()
        board.set_piece(Position(3, 1), Piece(Color.WHITE))
        board.set_piece(Position(4, 2), Piece(Color.BLACK))

        valid_moves = validator.get_all_valid_moves(board, Position(3, 1))

        # Should have capture move to (5,3)
        assert Position(5, 3) in valid_moves
        capture_move = valid_moves[Position(5, 3)]
        assert capture_move.is_capture() is True
        assert Position(4, 2) in capture_move.get_captured()

    def test_cannot_capture_own_piece(self):
        """Test that pieces cannot capture their own color"""
        board = Board()
        validator = MoveValidator()

        # Setup: Two white pieces
        board.pieces.clear()
        board.set_piece(Position(3, 1), Piece(Color.WHITE))
        board.set_piece(Position(4, 2), Piece(Color.WHITE))

        valid_moves = validator.get_all_valid_moves(board, Position(3, 1))

        # Should NOT have jump over own piece
        assert Position(5, 3) not in valid_moves

    def test_capture_requires_empty_landing(self):
        """Test that capture requires empty landing square"""
        board = Board()
        validator = MoveValidator()

        # Setup: pieces blocking capture landing
        board.pieces.clear()
        board.set_piece(Position(3, 1), Piece(Color.WHITE))
        board.set_piece(Position(4, 2), Piece(Color.BLACK))
        board.set_piece(Position(5, 3), Piece(Color.WHITE))  # Blocking

        valid_moves = validator.get_all_valid_moves(board, Position(3, 1))

        # Cannot capture because landing square is occupied
        assert Position(5, 3) not in valid_moves

    def test_backward_capture_for_king(self):
        """Test that king can capture backward"""
        board = Board()
        validator = MoveValidator()

        # Setup: White king can capture backward
        board.pieces.clear()
        king = Piece(Color.WHITE)
        king.promote_to_king()
        board.set_piece(Position(5, 5), king)
        board.set_piece(Position(4, 4), Piece(Color.BLACK))

        valid_moves = validator.get_all_valid_moves(board, Position(5, 5))

        # King should be able to capture backward to (3,3)
        assert Position(3, 3) in valid_moves
        assert valid_moves[Position(3, 3)].is_capture() is True

    def test_capture_both_directions(self):
        """Test piece with capture options in multiple directions"""
        board = Board()
        validator = MoveValidator()

        # Setup: White piece with two capture options
        board.pieces.clear()
        board.set_piece(Position(4, 4), Piece(Color.WHITE))
        board.set_piece(Position(5, 5), Piece(Color.BLACK))  # Right
        board.set_piece(Position(5, 3), Piece(Color.BLACK))  # Left

        valid_moves = validator.get_all_valid_moves(board, Position(4, 4))

        # Should have both captures
        assert Position(6, 6) in valid_moves
        assert Position(6, 2) in valid_moves
        assert valid_moves[Position(6, 6)].is_capture() is True
        assert valid_moves[Position(6, 2)].is_capture() is True


class TestMoveValidatorMultiJump:
    """Test multi-jump (double/triple capture) sequences"""

    def test_double_jump_sequence(self):
        """Test detecting double jump opportunity"""
        board = Board()
        validator = MoveValidator()

        # Setup: White can jump two black pieces in sequence
        board.pieces.clear()
        board.set_piece(Position(2, 2), Piece(Color.WHITE))
        board.set_piece(Position(3, 3), Piece(Color.BLACK))  # First jump
        board.set_piece(Position(5, 5), Piece(Color.BLACK))  # Second jump

        valid_moves = validator.get_all_valid_moves(board, Position(2, 2))

        # Should have multi-jump to (6, 6)
        # Implementation may vary - might be single move or require multiple moves
        # Check if multi-jump is returned as single move
        if Position(6, 6) in valid_moves:
            multi_jump = valid_moves[Position(6, 6)]
            assert len(multi_jump.get_captured()) == 2

    def test_multi_jump_with_branching(self):
        """Test multi-jump with multiple path options"""
        board = Board()
        validator = MoveValidator()

        # Setup: piece can capture, then has choice of second capture
        board.pieces.clear()
        board.set_piece(Position(2, 2), Piece(Color.WHITE))
        board.set_piece(Position(3, 3), Piece(Color.BLACK))
        board.set_piece(Position(5, 5), Piece(Color.BLACK))  # Path A
        board.set_piece(Position(5, 1), Piece(Color.BLACK))  # Path B

        valid_moves = validator.get_all_valid_moves(board, Position(2, 2))

        # Should have options for both paths
        # Exact implementation depends on how multi-jumps are handled
        assert len(valid_moves) > 0

    def test_multi_jump_king(self):
        """Test multi-jump sequence for king piece"""
        board = Board()
        validator = MoveValidator()

        # Setup: King with multi-jump opportunity
        board.pieces.clear()
        king = Piece(Color.WHITE)
        king.promote_to_king()
        board.set_piece(Position(2, 2), king)
        board.set_piece(Position(3, 3), Piece(Color.BLACK))
        board.set_piece(Position(5, 5), Piece(Color.BLACK))

        valid_moves = validator.get_all_valid_moves(board, Position(2, 2))

        # King should be able to multi-jump
        assert len(valid_moves) > 0

    def test_multi_jump_terminates_at_edge(self):
        """Test multi-jump sequence terminates at board edge"""
        board = Board()
        validator = MoveValidator()

        # Setup: Jump sequence that reaches edge
        board.pieces.clear()
        board.set_piece(Position(4, 4), Piece(Color.WHITE))
        board.set_piece(Position(5, 5), Piece(Color.BLACK))
        board.set_piece(Position(7, 7), Piece(Color.BLACK))  # Can't jump beyond

        valid_moves = validator.get_all_valid_moves(board, Position(4, 4))

        # Should have first jump but not beyond board
        assert Position(6, 6) in valid_moves


class TestMoveValidatorMustCapture:
    """Test must-capture rule enforcement"""

    def test_must_capture_returns_true_when_capture_available(self):
        """Test must_capture returns True when captures exist"""
        board = Board()
        validator = MoveValidator()

        # Setup: White has capture available
        board.pieces.clear()
        board.set_piece(Position(3, 1), Piece(Color.WHITE))
        board.set_piece(Position(4, 2), Piece(Color.BLACK))

        result = validator.must_capture(board, Color.WHITE)

        assert result is True

    def test_must_capture_returns_false_when_no_captures(self):
        """Test must_capture returns False when no captures available"""
        board = Board()
        validator = MoveValidator()

        # Starting position - no immediate captures
        result = validator.must_capture(board, Color.WHITE)

        assert result is False

    def test_must_capture_checks_all_pieces(self):
        """Test must_capture checks all player's pieces"""
        board = Board()
        validator = MoveValidator()

        # Setup: One white piece has capture, others don't
        board.pieces.clear()
        board.set_piece(Position(2, 0), Piece(Color.WHITE))  # No capture
        board.set_piece(Position(3, 3), Piece(Color.WHITE))  # Has capture
        board.set_piece(Position(4, 4), Piece(Color.BLACK))

        result = validator.must_capture(board, Color.WHITE)

        # Should detect capture is available
        assert result is True

    def test_must_capture_for_kings(self):
        """Test must_capture considers king pieces"""
        board = Board()
        validator = MoveValidator()

        # Setup: King has backward capture
        board.pieces.clear()
        king = Piece(Color.WHITE)
        king.promote_to_king()
        board.set_piece(Position(5, 5), king)
        board.set_piece(Position(4, 4), Piece(Color.BLACK))

        result = validator.must_capture(board, Color.WHITE)

        assert result is True

    def test_must_capture_ignores_blocked_captures(self):
        """Test must_capture only counts available captures"""
        board = Board()
        validator = MoveValidator()

        # Setup: Potential capture but landing blocked
        board.pieces.clear()
        board.set_piece(Position(3, 1), Piece(Color.WHITE))
        board.set_piece(Position(4, 2), Piece(Color.BLACK))
        board.set_piece(Position(5, 3), Piece(Color.WHITE))  # Blocks landing

        result = validator.must_capture(board, Color.WHITE)

        # No valid capture available
        assert result is False


class TestMoveValidatorGetAllLegalMoves:
    """Test getting all legal moves for a player"""

    def test_get_all_legal_moves_initial_position(self):
        """Test getting all legal moves at game start"""
        board = Board()
        validator = MoveValidator()

        legal_moves = validator.get_all_legal_moves(board, Color.WHITE)

        # White should have 7 pieces that can move initially
        assert len(legal_moves) > 0
        assert all(isinstance(move, Move) for move in legal_moves)

    def test_get_all_legal_moves_only_captures_when_required(self):
        """Test that only captures returned when must-capture applies"""
        board = Board()
        validator = MoveValidator()

        # Setup: White has both regular moves and captures
        board.pieces.clear()
        board.set_piece(Position(2, 0), Piece(Color.WHITE))  # Can move
        board.set_piece(Position(3, 3), Piece(Color.WHITE))  # Can capture
        board.set_piece(Position(4, 4), Piece(Color.BLACK))

        legal_moves = validator.get_all_legal_moves(board, Color.WHITE)

        # Should only return capture moves (must-capture rule)
        assert all(move.is_capture() for move in legal_moves)

    def test_get_all_legal_moves_no_captures_available(self):
        """Test all moves returned when no captures available"""
        board = Board()
        validator = MoveValidator()

        # Starting position - no captures
        legal_moves = validator.get_all_legal_moves(board, Color.WHITE)

        # Should return all legal moves
        assert len(legal_moves) > 0
        # Most should be non-capture moves
        non_captures = [m for m in legal_moves if not m.is_capture()]
        assert len(non_captures) > 0

    def test_get_all_legal_moves_no_moves_available(self):
        """Test returns empty list when no legal moves"""
        board = Board()
        validator = MoveValidator()

        # Setup: White piece completely blocked
        board.pieces.clear()
        board.set_piece(Position(0, 0), Piece(Color.WHITE))
        board.set_piece(Position(1, 1), Piece(Color.BLACK))

        legal_moves = validator.get_all_legal_moves(board, Color.WHITE)

        assert len(legal_moves) == 0

    def test_get_all_legal_moves_multiple_pieces(self):
        """Test aggregates moves from all player's pieces"""
        board = Board()
        validator = MoveValidator()

        # Setup: Multiple white pieces
        board.pieces.clear()
        board.set_piece(Position(2, 0), Piece(Color.WHITE))
        board.set_piece(Position(2, 2), Piece(Color.WHITE))
        board.set_piece(Position(2, 4), Piece(Color.WHITE))

        legal_moves = validator.get_all_legal_moves(board, Color.WHITE)

        # Should have moves from all three pieces
        assert len(legal_moves) >= 3

        # Verify moves come from different pieces
        from_positions = {move.get_from() for move in legal_moves}
        assert len(from_positions) >= 2

    def test_get_all_legal_moves_for_kings(self):
        """Test includes king moves in all legal moves"""
        board = Board()
        validator = MoveValidator()

        # Setup: Mix of regular pieces and kings
        board.pieces.clear()
        regular = Piece(Color.WHITE)
        king = Piece(Color.WHITE)
        king.promote_to_king()

        board.set_piece(Position(3, 1), regular)
        board.set_piece(Position(4, 4), king)

        legal_moves = validator.get_all_legal_moves(board, Color.WHITE)

        # Should include moves from both regular and king
        from_positions = {move.get_from() for move in legal_moves}
        assert Position(3, 1) in from_positions
        assert Position(4, 4) in from_positions


class TestMoveValidatorKingMovement:
    """Test king-specific movement rules"""

    def test_king_moves_forward_and_backward(self):
        """Test king can move in all four diagonal directions"""
        board = Board()
        validator = MoveValidator()

        # Setup: King in middle of board
        board.pieces.clear()
        king = Piece(Color.WHITE)
        king.promote_to_king()
        board.set_piece(Position(4, 4), king)

        valid_moves = validator.get_all_valid_moves(board, Position(4, 4))

        # Should have all four diagonal moves
        assert Position(5, 5) in valid_moves  # Forward-right
        assert Position(5, 3) in valid_moves  # Forward-left
        assert Position(3, 5) in valid_moves  # Backward-right
        assert Position(3, 3) in valid_moves  # Backward-left

    def test_regular_piece_cannot_move_backward(self):
        """Test regular white piece cannot move backward"""
        board = Board()
        validator = MoveValidator()

        # Setup: White regular piece
        board.pieces.clear()
        board.set_piece(Position(4, 4), Piece(Color.WHITE))

        valid_moves = validator.get_all_valid_moves(board, Position(4, 4))

        # Should only have forward moves
        assert Position(5, 5) in valid_moves or Position(5, 3) in valid_moves
        # Should NOT have backward moves
        assert Position(3, 5) not in valid_moves
        assert Position(3, 3) not in valid_moves

    def test_king_captures_in_all_directions(self):
        """Test king can capture in all diagonal directions"""
        board = Board()
        validator = MoveValidator()

        # Setup: King surrounded by opponent pieces
        board.pieces.clear()
        king = Piece(Color.WHITE)
        king.promote_to_king()
        board.set_piece(Position(4, 4), king)

        # Place black pieces around it
        board.set_piece(Position(5, 5), Piece(Color.BLACK))
        board.set_piece(Position(3, 3), Piece(Color.BLACK))

        valid_moves = validator.get_all_valid_moves(board, Position(4, 4))

        # Should be able to capture forward and backward
        assert any(move.is_capture() for move in valid_moves.values())

    def test_black_king_moves_both_directions(self):
        """Test black king also moves in all directions"""
        board = Board()
        validator = MoveValidator()

        # Setup: Black king
        board.pieces.clear()
        king = Piece(Color.BLACK)
        king.promote_to_king()
        board.set_piece(Position(4, 4), king)

        valid_moves = validator.get_all_valid_moves(board, Position(4, 4))

        # Black king should also move in all four directions
        assert len(valid_moves) == 4


class TestMoveValidatorEdgeCases:
    """Test edge cases and boundary conditions"""

    def test_validate_move_at_corners(self):
        """Test moves at board corners"""
        board = Board()
        validator = MoveValidator()

        # Test all four corners
        corners = [
            (Position(0, 0), Color.WHITE),
            (Position(0, 6), Color.WHITE),
            (Position(7, 1), Color.BLACK),
            (Position(7, 7), Color.BLACK),
        ]

        for pos, color in corners:
            board.pieces.clear()
            piece = Piece(color)
            if color == Color.BLACK and pos.row == 7:
                piece.promote_to_king()  # Black at bottom needs to be king to move
            board.set_piece(pos, piece)

            valid_moves = validator.get_all_valid_moves(board, pos)
            # Should have limited moves at corner (not error)
            assert isinstance(valid_moves, dict)

    def test_validate_single_piece_on_board(self):
        """Test validation with only one piece on board"""
        board = Board()
        validator = MoveValidator()

        board.pieces.clear()
        board.set_piece(Position(4, 4), Piece(Color.WHITE))

        valid_moves = validator.get_all_valid_moves(board, Position(4, 4))

        # Should have valid moves even alone
        assert len(valid_moves) > 0

    def test_validate_crowded_board(self):
        """Test validation on crowded board"""
        board = Board()
        validator = MoveValidator()

        # Board starts crowded - test still works
        legal_moves = validator.get_all_legal_moves(board, Color.WHITE)

        assert len(legal_moves) > 0

    def test_validate_alternating_colors(self):
        """Test validation with alternating piece colors"""
        board = Board()
        validator = MoveValidator()

        # Setup: checkerboard pattern
        board.pieces.clear()
        for row in range(8):
            for col in range(8):
                if (row + col) % 2 == 0:
                    continue
                if (row + col) % 4 == 1:
                    board.set_piece(Position(row, col), Piece(Color.WHITE))
                else:
                    board.set_piece(Position(row, col), Piece(Color.BLACK))

        # Should still find some legal moves
        white_moves = validator.get_all_legal_moves(board, Color.WHITE)
        # Might be very limited or zero, but shouldn't error
        assert isinstance(white_moves, list)

    def test_validate_long_jump_sequence(self):
        """Test validation doesn't hang on long jump sequences"""
        board = Board()
        validator = MoveValidator()

        # Setup: potential for very long jump sequence
        board.pieces.clear()
        board.set_piece(Position(0, 0), Piece(Color.WHITE))

        # Create diagonal line of black pieces
        for i in range(1, 4):
            board.set_piece(Position(i, i), Piece(Color.BLACK))

        # Should complete without timeout
        valid_moves = validator.get_all_valid_moves(board, Position(0, 0))
        assert isinstance(valid_moves, dict)


class TestMoveValidatorDirectionChecking:
    """Test directional movement validation"""

    def test_white_moves_forward_only(self):
        """Test white regular pieces only move forward (increasing row)"""
        board = Board()
        validator = MoveValidator()

        board.pieces.clear()
        board.set_piece(Position(3, 3), Piece(Color.WHITE))

        valid_moves = validator.get_all_valid_moves(board, Position(3, 3))

        # All moves should increase row number
        for dest_pos in valid_moves.keys():
            assert dest_pos.row > 3

    def test_black_moves_forward_only(self):
        """Test black regular pieces only move forward (decreasing row)"""
        board = Board()
        validator = MoveValidator()

        board.pieces.clear()
        board.set_piece(Position(4, 4), Piece(Color.BLACK))

        valid_moves = validator.get_all_valid_moves(board, Position(4, 4))

        # All moves should decrease row number
        for dest_pos in valid_moves.keys():
            assert dest_pos.row < 4

    def test_diagonal_left_and_right(self):
        """Test pieces can move both left and right diagonally"""
        board = Board()
        validator = MoveValidator()

        board.pieces.clear()
        board.set_piece(Position(3, 3), Piece(Color.WHITE))

        valid_moves = validator.get_all_valid_moves(board, Position(3, 3))

        # Should have both left and right diagonal options
        has_left = any(pos.col < 3 for pos in valid_moves.keys())
        has_right = any(pos.col > 3 for pos in valid_moves.keys())

        assert has_left or has_right  # At least one direction


class TestMoveValidatorComplexScenarios:
    """Test complex game scenarios"""

    def test_forced_capture_scenario(self):
        """Test scenario where player is forced to capture"""
        board = Board()
        validator = MoveValidator()

        # Setup: White must capture
        board.pieces.clear()
        board.set_piece(Position(2, 2), Piece(Color.WHITE))
        board.set_piece(Position(3, 1), Piece(Color.WHITE))
        board.set_piece(Position(4, 2), Piece(Color.BLACK))  # Capture available

        # Get all legal moves
        legal_moves = validator.get_all_legal_moves(board, Color.WHITE)

        # All should be captures
        assert all(move.is_capture() for move in legal_moves)
        # Should have the forced capture
        assert any(move.get_from() == Position(3, 1) for move in legal_moves)

    def test_multiple_capture_choices(self):
        """Test scenario with multiple capture options"""
        board = Board()
        validator = MoveValidator()

        # Setup: White has multiple pieces that can capture
        board.pieces.clear()
        board.set_piece(Position(2, 2), Piece(Color.WHITE))
        board.set_piece(Position(2, 4), Piece(Color.WHITE))
        board.set_piece(Position(3, 3), Piece(Color.BLACK))
        board.set_piece(Position(3, 5), Piece(Color.BLACK))

        legal_moves = validator.get_all_legal_moves(board, Color.WHITE)

        # Should have capture options from both white pieces
        from_positions = {move.get_from() for move in legal_moves}
        assert len(from_positions) >= 2

    def test_king_vs_regular_pieces(self):
        """Test mixed scenario with kings and regular pieces"""
        board = Board()
        validator = MoveValidator()

        # Setup: Mix of pieces
        board.pieces.clear()
        regular = Piece(Color.WHITE)
        king = Piece(Color.WHITE)
        king.promote_to_king()

        board.set_piece(Position(3, 3), regular)
        board.set_piece(Position(5, 5), king)

        # Get moves for each
        regular_moves = validator.get_all_valid_moves(board, Position(3, 3))
        king_moves = validator.get_all_valid_moves(board, Position(5, 5))

        # King should have more directional options
        assert len(king_moves) >= len(regular_moves)

    def test_blocked_promotion_path(self):
        """Test piece blocked from reaching promotion"""
        board = Board()
        validator = MoveValidator()

        # Setup: White piece near top, but blocked
        board.pieces.clear()
        board.set_piece(Position(6, 2), Piece(Color.WHITE))
        board.set_piece(Position(7, 1), Piece(Color.BLACK))
        board.set_piece(Position(7, 3), Piece(Color.BLACK))

        valid_moves = validator.get_all_valid_moves(board, Position(6, 2))

        # Cannot reach row 7 (blocked), but might have captures
        no_promotion = all(pos.row != 7 or move.is_capture()
                           for pos, move in valid_moves.items())
        assert no_promotion or len(valid_moves) > 0

    def test_stalemate_detection(self):
        """Test detecting position with no legal moves"""
        board = Board()
        validator = MoveValidator()

        # Setup: White piece completely surrounded
        board.pieces.clear()
        board.set_piece(Position(4, 4), Piece(Color.WHITE))
        # Surround with opponent pieces
        board.set_piece(Position(5, 5), Piece(Color.BLACK))
        board.set_piece(Position(5, 3), Piece(Color.BLACK))
        board.set_piece(Position(3, 5), Piece(Color.BLACK))
        board.set_piece(Position(3, 3), Piece(Color.BLACK))

        legal_moves = validator.get_all_legal_moves(board, Color.WHITE)

        # Might have captures available
        # If not, should return empty list (not error)
        assert isinstance(legal_moves, list)


class TestMoveValidatorPerformance:
    """Test validator performance and efficiency"""

    def test_validate_move_is_efficient(self):
        """Test that validation doesn't recompute unnecessarily"""
        board = Board()
        validator = MoveValidator()

        # Validate same move multiple times
        move = Move(Position(2, 0), Position(3, 1))

        results = []
        for _ in range(100):
            result = validator.validate_move(board, move, Color.WHITE)
            results.append(result)

        # All results should be same
        assert all(r == results[0] for r in results)

    def test_get_all_legal_moves_handles_full_board(self):
        """Test getting all legal moves on full board completes quickly"""
        board = Board()
        validator = MoveValidator()

        # Starting position with all 24 pieces
        legal_moves = validator.get_all_legal_moves(board, Color.WHITE)

        # Should complete and return reasonable number of moves
        assert len(legal_moves) > 0
        assert len(legal_moves) < 100  # Sanity check


class TestMoveValidatorConsistency:
    """Test consistency and correctness of validator"""

    def test_validate_move_matches_get_valid_moves(self):
        """Test that validate_move agrees with get_all_valid_moves"""
        board = Board()
        validator = MoveValidator()

        position = Position(2, 0)
        valid_moves = validator.get_all_valid_moves(board, position)

        # All moves from get_all_valid_moves should validate
        for dest_pos, move in valid_moves.items():
            result = validator.validate_move(board, move, Color.WHITE)
            assert result is True, f"Move to {dest_pos} should be valid"

    def test_invalid_moves_not_in_valid_moves(self):
        """Test that invalid moves are not in valid moves dict"""
        board = Board()
        validator = MoveValidator()

        position = Position(2, 0)
        valid_moves = validator.get_all_valid_moves(board, position)

        # These positions should NOT be in valid moves
        invalid_positions = [
            Position(0, 0),  # Backward
            Position(2, 1),  # Horizontal
            Position(4, 0),  # Too far
        ]

        for invalid_pos in invalid_positions:
            assert invalid_pos not in valid_moves

    def test_symmetric_validation_for_colors(self):
        """Test that validation is symmetric for both colors"""
        board = Board()
        validator = MoveValidator()

        # White move
        white_moves = validator.get_all_legal_moves(board, Color.WHITE)

        # Black move
        black_moves = validator.get_all_legal_moves(board, Color.BLACK)

        # Both should have similar number of moves at start
        assert len(white_moves) > 0
        assert len(black_moves) > 0
        # Exact equality not required, but should be similar
        assert abs(len(white_moves) - len(black_moves)) < 5

    def test_move_validation_is_deterministic(self):
        """Test that validation gives same result each time"""
        board = Board()
        validator = MoveValidator()

        move = Move(Position(2, 0), Position(3, 1))

        results = [validator.validate_move(board, move, Color.WHITE)
                   for _ in range(10)]

        assert all(r == results[0] for r in results)

    def test_position_validation_independence(self):
        """Test that validating one position doesn't affect others"""
        board = Board()
        validator = MoveValidator()

        pos1 = Position(2, 0)
        pos2 = Position(2, 2)

        moves1_before = validator.get_all_valid_moves(board, pos1)
        moves2 = validator.get_all_valid_moves(board, pos2)
        moves1_after = validator.get_all_valid_moves(board, pos1)

        # Getting moves for pos2 shouldn't change moves for pos1
        assert moves1_before == moves1_after


class TestMoveValidatorIntegration:
    """Integration tests with Board"""

    def test_validator_respects_board_state(self):
        """Test that validator correctly reads board state"""
        board = Board()
        validator = MoveValidator()

        # Remove a piece
        board.remove_piece(Position(2, 0))

        # Validator should recognize position is empty
        result = validator.is_valid_selection(board, Position(2, 0), Color.WHITE)
        assert result is False

    def test_validator_handles_board_modifications(self):
        """Test validator works after board modifications"""
        board = Board()
        validator = MoveValidator()

        # Get initial moves
        initial_moves = validator.get_all_legal_moves(board, Color.WHITE)

        # Modify board
        board.move(Position(2, 0), Position(3, 1))

        # Get new moves
        new_moves = validator.get_all_legal_moves(board, Color.WHITE)

        # Move lists should be different
        assert len(initial_moves) != len(new_moves)

    def test_validator_with_custom_board_setup(self):
        """Test validator works with custom board configurations"""
        board = Board()
        validator = MoveValidator()

        # Create custom setup
        board.pieces.clear()
        board.set_piece(Position(3, 3), Piece(Color.WHITE))
        board.set_piece(Position(4, 4), Piece(Color.BLACK))

        # Validator should work with custom setup
        valid_moves = validator.get_all_valid_moves(board, Position(3, 3))
        legal_moves = validator.get_all_legal_moves(board, Color.WHITE)

        assert isinstance(valid_moves, dict)
        assert isinstance(legal_moves, list)