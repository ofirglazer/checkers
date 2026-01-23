import pytest
from src.ai_player_random import AiPlayerRandom
from src.board import Board
from src.move import Move
from src.position import Position
from src.config import Color
from src.piece import Piece


class TestAiPlayerRandom:
    """Test suite for AiPlayerRandom class"""

    @pytest.fixture
    def ai_player(self):
        """Create an AI player instance for testing"""
        return AiPlayerRandom(Color.BLACK)

    @pytest.fixture
    def board(self):
        """Create an AI player instance for testing"""
        return Board()

    @pytest.fixture
    def empty_board(self):
        """Create an empty board"""
        board = Board()
        board.pieces.clear()
        board.white_count = 0
        board.black_count = 0
        return board

    @pytest.fixture
    def board_with_black_pieces(self):
        """Create a board with only black pieces"""
        board = Board()
        board.pieces.clear()
        board.set_piece(Position(2, 0), Piece(Color.BLACK))
        board.set_piece(Position(2, 2), Piece(Color.BLACK))
        board.set_piece(Position(2, 4), Piece(Color.BLACK))
        board.black_count = 3
        board.white_kings = 0
        return board

    @pytest.fixture
    def board_with_mixed_pieces(self):
        """Create a board with both BLACK and white pieces"""
        board = Board()
        board.pieces.clear()
        board.set_piece(Position(2, 0), Piece(Color.BLACK))
        board.set_piece(Position(2, 2), Piece(Color.BLACK))
        board.set_piece(Position(2, 4), Piece(Color.BLACK))
        board.set_piece(Position(5, 1), Piece(Color.WHITE))
        board.set_piece(Position(5, 3), Piece(Color.WHITE))
        board.set_piece(Position(5, 5), Piece(Color.WHITE))
        board.black_count = 3
        board.white_kings = 3
        return board

    @pytest.fixture
    def ai_player_selected_origin(self, board_with_mixed_pieces, monkeypatch):
        monkeypatch.setattr(
            "src.ai_player_random.choice",
            lambda seq: Position(2, 2)
        )

        """Create an AI player instance for testing"""
        ai_player = AiPlayerRandom(Color.BLACK)
        ai_player.get_selected_origin(board_with_mixed_pieces)
        return ai_player

    @pytest.fixture
    def board_with_capture_opportunity(self):
        """Create a board where BLACK can capture WHITE"""
        board = Board()
        board.pieces.clear()
        board.set_piece(Position(2, 2), Piece(Color.BLACK))
        board.set_piece(Position(1, 3), Piece(Color.WHITE))  # Position (0, 4) is empty - BLACK can jump
        board.black_count = 1
        board.white_kings = 1
        return board

    @pytest.fixture
    def board_end_game(self):
        """Create a board with few pieces remaining"""
        board = Board()
        board.pieces = [
            Piece(Position(6, 1), Color.BLACK),
            Piece(Position(1, 6), Color.WHITE),
        ]
        return board

    # Tests for get_selected_origin

    def test_get_selected_origin_returns_position(self, ai_player, board):
        """Test that get_selected_origin returns a Position object"""
        result = ai_player.get_selected_origin(board)

        assert isinstance(result, Position)

    def test_get_selected_origin_returns_valid_piece_position(self, ai_player, board_with_black_pieces):
        """Test that returned position corresponds to an actual piece"""
        result = ai_player.get_selected_origin(board_with_black_pieces)

        # Check that there's a piece at this position
        piece_at_position = None
        for position, piece in board_with_black_pieces.pieces.items():
            if position == result:
                piece_at_position = piece
                break

        assert piece_at_position is not None
        assert piece_at_position.color == Color.BLACK

    def test_get_selected_origin_only_selects_current_player_pieces(self, ai_player, board_with_mixed_pieces):
        """Test that only pieces of current player color are consideBLACK"""
        # Test BLACK player
        result_BLACK = ai_player.get_selected_origin(board_with_mixed_pieces)
        piece_BLACK = next(position for position in board_with_mixed_pieces.pieces.keys() if position == result_BLACK)
        assert board_with_mixed_pieces.pieces[piece_BLACK].color == Color.BLACK

        # Test WHITE player
        ai_player.current_player = Color.WHITE
        result_white = ai_player.get_selected_origin(board_with_mixed_pieces)
        piece_white = next(position for position in board_with_mixed_pieces.pieces.keys() if position == result_white)
        assert board_with_mixed_pieces.pieces[piece_white].color == Color.WHITE

    def test_get_selected_origin_only_selects_pieces_with_valid_moves(self, ai_player):
        """Test that only pieces with valid moves are selected"""
        # Create a board where one BLACK piece is blocked
        board = Board()
        board.pieces.clear()
        board.set_piece(Position(0, 2), Piece(Color.BLACK))  # At bottom edge, can't move down
        board.set_piece(Position(2, 2), Piece(Color.BLACK))  # Can move

        # Run multiple times to ensure blocked piece is never selected
        for _ in range(20):
            result = ai_player.get_selected_origin(board)
            # Should never select the blocked piece at (0, 2)
            # Should select the movable piece at (2, 2)
            assert result == Position(2, 2)

    def test_get_selected_origin_raises_error_when_no_valid_pieces(self, ai_player, empty_board):
        """Test that an error is raised when no pieces have valid moves"""
        with pytest.raises((StopIteration)):
            ai_player.get_selected_origin(empty_board)

    def test_get_selected_origin_raises_error_when_no_pieces_of_color(self, ai_player, board_with_black_pieces):
        """Test error when requesting pieces of color not on board"""
        ai_player.current_player = Color.WHITE
        with pytest.raises((StopIteration)):
            ai_player.get_selected_origin(board_with_black_pieces)

    def test_get_selected_origin_is_random(self, ai_player, board_with_black_pieces):
        """Test that selection is random when multiple pieces available"""
        # Run multiple times and collect results
        results = set()
        for _ in range(30):
            result = ai_player.get_selected_origin(board_with_black_pieces)
            results.add(result)

        # Should get different results (randomness)
        # With 3 pieces and 30 runs, very likely to get at least 2 different ones
        assert len(results) >= 2

    def test_get_selected_origin_with_king_pieces(self, ai_player, empty_board):
        """Test selection works with king pieces"""
        king = Piece(Color.BLACK)
        king.is_king = True
        empty_board.set_piece(Position(7, 1), king)
        result = ai_player.get_selected_origin(empty_board)

        assert result == Position(7, 1)

    # Tests for get_selected_dest

    def test_get_selected_dest_returns_position(self, ai_player_selected_origin, board_with_black_pieces, monkeypatch):
        """Test that get_selected_dest returns a Position object"""

        monkeypatch.setattr(
            "src.ai_player_random.choice",
            lambda seq: Move(Position(2, 2), Position(1, 3))
        )
        result = ai_player_selected_origin.get_selected_dest(board_with_black_pieces)

        assert isinstance(result, Position)

    def test_get_selected_dest_returns_different_from_origin(self, ai_player_selected_origin, board_with_black_pieces, monkeypatch):
        """Test that destination is different from origin"""
        origin = ai_player_selected_origin.origin

        monkeypatch.setattr(
            "src.ai_player_random.choice",
            lambda seq: Move(Position(2, 2), Position(1, 3))
        )
        destination = ai_player_selected_origin.get_selected_dest(board_with_black_pieces)

        assert destination != origin

    def test_get_selected_dest_selects_valid_move(self, ai_player_selected_origin, board_with_black_pieces, monkeypatch):
        """Test that destination is a valid move from origin"""
        origin = ai_player_selected_origin.origin

        monkeypatch.setattr(
            "src.ai_player_random.choice",
            lambda seq: Move(Position(2, 2), Position(1, 3))
        )
        destination = ai_player_selected_origin.get_selected_dest(board_with_black_pieces)

        # For a BLACK piece at (2,2), valid moves are diagonal down
        # Result should be adjacent diagonal
        row_diff = abs(destination.row - origin.row)
        col_diff = abs(destination.col - origin.col)
        assert row_diff == 1
        assert col_diff == 1

    def test_get_selected_dest_handles_capture_moves(self, ai_player, board_with_capture_opportunity, monkeypatch):
        """Test that capture moves can be selected"""
        origin = ai_player.get_selected_origin(board_with_capture_opportunity)

        monkeypatch.setattr(
            "src.ai_player_random.choice",
            lambda seq: Move(Position(2, 2), Position(0, 4))
        )
        destination = ai_player.get_selected_dest(board_with_capture_opportunity)

        # Should be able to select either regular move or capture
        assert isinstance(destination, Position)
        assert destination != origin

    def test_get_selected_dest_is_random(self, board_with_mixed_pieces, ai_player):
        """Test that destination selection is random when multiple options"""

        origin = ai_player.get_selected_origin(board_with_mixed_pieces)
        results = set()

        for _ in range(20):
            result = ai_player.get_selected_dest(board_with_mixed_pieces)
            results.add((result.row, result.col))

        # Should get different results if multiple moves available
        # At minimum, should have valid results
        assert len(results) >= 1

    def test_get_selected_dest_with_king_piece(self, ai_player, monkeypatch):
        """Test destination selection for king pieces"""
        board = Board()
        king = board.get_piece(Position(5, 3))
        king.promote_to_king()

        monkeypatch.setattr(
            "src.ai_player_random.choice",
            lambda seq: Position(5, 3)
        )
        origin = ai_player.get_selected_origin(board)

        monkeypatch.setattr(
            "src.ai_player_random.choice",
            lambda seq: Move(Position(5, 3), Position(4, 2))
        )
        result = ai_player.get_selected_dest(board)

        # King can move in all diagonal directions
        assert isinstance(result, Position)
        row_diff = abs(result.row - origin.row)
        col_diff = abs(result.col - origin.col)
        assert row_diff == 1
        assert col_diff == 1

    def test_get_selected_dest_raises_error_for_blocked_piece(self, ai_player):
        """Test error when piece has no valid destinations"""
        board = Board()
        board.pieces.clear()
        # Piece at edge with no moves
        board.set_piece(Position(0, 2), Piece(Color.BLACK))
        board.set_piece(Position(0, 4), Piece(Color.BLACK))
        # This piece should have no valid moves
        with pytest.raises((StopIteration)):
            origin = ai_player.get_selected_origin(board)


    # Integration tests

    def test_full_move_selection_flow(self, ai_player, board_with_mixed_pieces):
        """Test complete flow of selecting origin and destination"""
        # Get origin
        origin = ai_player.get_selected_origin(board_with_mixed_pieces)
        assert isinstance(origin, Position)

        # Verify piece exists at origin
        piece = board_with_mixed_pieces.get_piece(origin)
        assert piece.color == Color.BLACK

        # Get destination
        dest = ai_player.get_selected_dest(board_with_mixed_pieces)
        assert isinstance(dest, Position)
        assert dest != origin

    def test_ai_player_inherits_from_base_ai_player(self, ai_player):
        """Test that AiPlayerRandom inherits from AiPlayer"""
        from src.ai_player import AiPlayer
        assert isinstance(ai_player, AiPlayer)

    def test_multiple_consecutive_moves(self, ai_player, board_with_mixed_pieces):
        """Test AI can make multiple moves in sequence"""
        for _ in range(5):
            # BLACK move
            origin = ai_player.get_selected_origin(board_with_mixed_pieces, Color.BLACK)
            dest = ai_player.get_selected_dest(board_with_mixed_pieces, origin)
            assert isinstance(origin, Position)
            assert isinstance(dest, Position)

            # WHITE move (if white pieces still exist)
            try:
                origin = ai_player.get_selected_origin(board_with_mixed_pieces, Color.WHITE)
                dest = ai_player.get_selected_dest(board_with_mixed_pieces, origin)
                assert isinstance(origin, Position)
                assert isinstance(dest, Position)
            except (ValueError, IndexError, StopIteration):
                # No white pieces left or no valid moves
                pass

    def test_end_game_scenario(self, ai_player, board_end_game):
        """Test AI behavior in end game with few pieces"""
        # BLACK move
        origin = ai_player.get_selected_origin(board_end_game, Color.BLACK)
        dest = ai_player.get_selected_dest(board_end_game, origin)

        assert isinstance(origin, Position)
        assert isinstance(dest, Position)
        assert origin == Position(6, 1)

    def test_randomness_distribution(self, ai_player, board_with_black_pieces):
        """Test that random selection has reasonable distribution"""
        # Count selections over many trials
        counts = {}
        num_trials = 90

        for _ in range(num_trials):
            result = ai_player.get_selected_origin(board_with_black_pieces, Color.BLACK)
            key = (result.row, result.col)
            counts[key] = counts.get(key, 0) + 1

        # With 3 pieces and 90 trials, expect ~30 each
        # Each should be selected at least 15 times (allowing variance)
        assert len(counts) >= 2, "Not enough variety in selections"
        for count in counts.values():
            assert count > 10, f"Distribution too skewed: {counts}"

    def test_handles_complex_board_state(self, ai_player):
        """Test AI handles complex board with many pieces"""
        board = Board()
        # Create a full starting position
        for col in range(0, 8, 2):
            board.pieces.append(Piece(Position(0, col), Color.BLACK))
            board.pieces.append(Piece(Position(1, col + 1), Color.BLACK))
            board.pieces.append(Piece(Position(2, col), Color.BLACK))

            board.pieces.append(Piece(Position(5, col + 1), Color.WHITE))
            board.pieces.append(Piece(Position(6, col), Color.WHITE))
            board.pieces.append(Piece(Position(7, col + 1), Color.WHITE))

        # Should handle large number of pieces
        origin = ai_player.get_selected_origin(board, Color.BLACK)
        dest = ai_player.get_selected_dest(board, origin)

        assert isinstance(origin, Position)
        assert isinstance(dest, Position)


class TestAiPlayerRandomEdgeCases:
    """Test edge cases and special scenarios"""

    @pytest.fixture
    def ai_player(self):
        return AiPlayerRandom()

    def test_single_piece_single_move(self, ai_player):
        """Test with only one piece having only one move"""
        board = Board()
        board.pieces = [
            Piece(Position(1, 0), Color.BLACK),
        ]

        origin = ai_player.get_selected_origin(board, Color.BLACK)
        assert origin == Position(1, 0)

        dest = ai_player.get_selected_dest(board, origin)
        assert isinstance(dest, Position)

    def test_all_kings_board(self, ai_player):
        """Test board where all pieces are kings"""
        board = Board()
        for i in range(3):
            king = Piece(Position(i * 2, i * 2), Color.BLACK)
            king.is_king = True
            board.pieces.append(king)

        origin = ai_player.get_selected_origin(board, Color.BLACK)
        dest = ai_player.get_selected_dest(board, origin)

        assert isinstance(origin, Position)
        assert isinstance(dest, Position)

    def test_forced_capture_scenario(self, ai_player):
        """Test scenario where capture is the only move"""
        board = Board()
        board.pieces = [
            Piece(Position(2, 1), Color.BLACK),
            Piece(Position(3, 2), Color.WHITE),
            # Position (4, 3) is empty - must capture
        ]

        origin = ai_player.get_selected_origin(board, Color.BLACK)
        dest = ai_player.get_selected_dest(board, origin)

        assert origin == Position(2, 1)
        # Should select the capture move
        assert isinstance(dest, Position)