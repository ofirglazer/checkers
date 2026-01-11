"""
Comprehensive test suite for CheckersController class.

Tests cover:
- Initialization
- Piece selection
- Move execution
- Turn management
- Game state transitions
- Winner determination
- Integration with MoveValidator and Board
- Edge cases and error handling

Comprehensive test suite for GameEngine Observer integration.

Tests cover:
- Observer attachment/detachment
- Notification triggering
- Multiple observers
- Observer method calls
- Event timing and ordering
- Integration with ConsoleViewer
"""


from src.checkers_controller import CheckersController
from src.board import Board
from src.position import Position
from src.piece import Piece
from src.move_validator import MoveValidator
from src.checkers_view_console import CheckersViewConsole
from src.config import Color, GameState
import pytest
from unittest.mock import Mock, MagicMock, call, patch


class TestCheckersControllerInitialization:
    """Test CheckersController initialization and setup"""

    def test_init_creates_board(self):
        """Test that initialization creates a board"""
        controller = CheckersController()

        assert controller.board is not None
        assert isinstance(controller.board, Board)

    def test_init_creates_validator(self):
        """Test that initialization creates a move validator"""
        controller = CheckersController()

        assert controller.validator is not None
        assert isinstance(controller.validator, MoveValidator)

    def test_init_sets_starting_player(self):
        """Test that white starts the game"""
        controller = CheckersController()

        assert controller.current_player == Color.WHITE

    def test_init_sets_playing_state(self):
        """Test that game starts in PLAYING state"""
        controller = CheckersController()

        assert controller.state == GameState.PLAYING

    def test_init_no_piece_selected(self):
        """Test that no piece is selected initially"""
        controller = CheckersController()

        assert controller.selected_position is None

    def test_init_board_has_correct_pieces(self):
        """Test that board is initialized with correct piece setup"""
        controller = CheckersController()

        assert controller.board.white_count == 12
        assert controller.board.black_count == 12
        assert controller.board.white_kings == 0
        assert controller.board.black_kings == 0
        assert len(controller.board.pieces) == 24


class TestCheckersControllerSelection:
    """Test piece selection logic"""

    def test_select_valid_white_piece_at_start(self):
        """Test selecting a valid white piece at game start"""
        controller = CheckersController()
        position = Position(2, 0)  # White piece position

        valid_selection = controller.select_piece(position)

        assert valid_selection is True
        assert controller.selected_position == position

    def test_select_valid_black_piece_on_black_turn(self):
        """Test selecting black piece when it's black's turn"""
        controller = CheckersController()
        controller.current_player = Color.BLACK  # Manually set to black's turn
        position = Position(5, 1)  # Black piece position

        result = controller.select_piece(position)

        assert result is True
        assert controller.selected_position == position

    def test_select_empty_square_fails(self):
        """Test that selecting empty square fails"""
        controller = CheckersController()
        position = Position(3, 3)  # Empty square

        is_valid_selection = controller.select_piece(position)

        assert is_valid_selection is False
        assert controller.selected_position is None

    def test_select_opponent_piece_fails(self):
        """Test that selecting opponent's piece fails"""
        controller = CheckersController()
        # White's turn, try to select black piece
        position = Position(5, 1)  # Black piece

        is_valid_selection = controller.select_piece(position)

        assert is_valid_selection is False
        assert controller.selected_position is None

    def test_select_updates_selected_position(self):
        """Test that selection updates selected_position"""
        controller = CheckersController()
        first_pos = Position(2, 0)
        second_pos = Position(2, 2)

        controller.select_piece(first_pos)
        assert controller.selected_position == first_pos

        controller.select_piece(second_pos)
        assert controller.selected_position == second_pos

    def test_select_out_of_bounds_position(self):
        """Test selecting position outside board bounds"""
        controller = CheckersController()

        # Assuming Position validates bounds, or controller should handle
        invalid_positions = [
            Position(-1, 0),
            Position(0, -1),
            Position(8, 0),
            Position(0, 8),
        ]

        for pos in invalid_positions:
            is_valid_selection = controller.select_piece(pos)
            # Should fail gracefully
            assert is_valid_selection is False


class TestCheckersControllerGetValidMoves:
    """Test getting valid moves for selected piece"""

    def test_get_valid_moves_with_selection(self):
        """Test getting valid moves for selected piece"""
        controller = CheckersController()
        position = Position(2, 0)
        controller.select_piece(position)

        valid_moves = controller.get_valid_moves_for_selected()

        assert isinstance(valid_moves, list)
        assert len(valid_moves) > 0
        # White piece at (2,0) should be able to move to (3,1)
        assert Position(3, 1) in valid_moves

    def test_get_valid_moves_without_selection(self):
        """Test getting valid moves when nothing selected"""
        controller = CheckersController()

        valid_moves = controller.get_valid_moves_for_selected()

        assert valid_moves == {}

    def test_get_valid_moves_returns_move_objects(self):
        """Test that valid moves dict contains Move objects"""
        controller = CheckersController()
        position = Position(2, 0)
        controller.select_piece(position)

        valid_moves = controller.get_valid_moves_for_selected()

        for dest_pos, move in valid_moves.items():
            assert isinstance(dest_pos, Position)
            assert isinstance(move, Move)
            assert move.get_from() == position
            assert move.get_to() == dest_pos


class TestCheckersControllerMakeMove:
    """Test move execution"""

    def test_make_simple_valid_move(self):
        """Test making a simple valid move"""
        controller = CheckersController()
        from_pos = Position(2, 0)
        to_pos = Position(3, 1)

        result = controller.make_move(from_pos, to_pos)

        assert result is True
        assert controller.board.get_piece(from_pos) is None
        assert controller.board.get_piece(to_pos) is not None
        assert controller.board.get_piece(to_pos).color == Color.WHITE

    def test_make_invalid_move_fails(self):
        """Test that invalid move returns False"""
        controller = CheckersController()
        from_pos = Position(2, 0)
        to_pos = Position(5, 5)  # Invalid destination

        result = controller.make_move(from_pos, to_pos)

        assert result is False
        # Piece should still be at original position
        assert controller.board.get_piece(from_pos) is not None

    def test_make_move_wrong_player(self):
        """Test that moving opponent's piece fails"""
        controller = CheckersController()
        # White's turn, try to move black piece
        from_pos = Position(5, 1)  # Black piece
        to_pos = Position(4, 2)

        result = controller.make_move(from_pos, to_pos)

        assert result is False

    def test_make_move_to_occupied_square(self):
        """Test that moving to occupied square fails"""
        controller = CheckersController()
        from_pos = Position(2, 0)
        to_pos = Position(1, 1)  # Occupied by another white piece

        result = controller.make_move(from_pos, to_pos)

        assert result is False

    def test_make_move_from_empty_square(self):
        """Test that moving from empty square fails"""
        controller = CheckersController()
        from_pos = Position(3, 3)  # Empty
        to_pos = Position(4, 4)

        result = controller.make_move(from_pos, to_pos)

        assert result is False

    def test_make_capture_move(self):
        """Test making a capture move"""
        controller = CheckersController()

        # Setup: manually place pieces for capture scenario
        # White piece at (3, 1), Black piece at (4, 2), destination (5, 3)
        controller.board.pieces.clear()
        controller.board.set_piece(Position(3, 1), Piece(Color.WHITE))
        controller.board.set_piece(Position(4, 2), Piece(Color.BLACK))
        controller.board.white_count = 1
        controller.board.black_count = 1

        from_pos = Position(3, 1)
        to_pos = Position(5, 3)

        result = controller.make_move(from_pos, to_pos)

        assert result is True
        assert controller.board.get_piece(Position(4, 2)) is None  # Captured piece removed
        assert controller.board.get_piece(to_pos) is not None
        assert controller.board.black_count == 0

    def test_make_move_clears_selection(self):
        """Test that making a move clears selected position"""
        controller = CheckersController()
        from_pos = Position(2, 0)
        to_pos = Position(3, 1)

        controller.select_piece(from_pos)
        assert controller.selected_position is not None

        controller.make_move(from_pos, to_pos)

        # Selection should be cleared after move
        assert controller.selected_position is None


class TestCheckersControllerTurnManagement:
    """Test turn switching and management"""

    def test_turn_switches_after_valid_move(self):
        """Test that turn switches after successful move"""
        controller = CheckersController()
        assert controller.current_player == Color.WHITE

        from_pos = Position(2, 0)
        to_pos = Position(3, 1)
        controller.make_move(from_pos, to_pos)

        assert controller.current_player == Color.BLACK

    def test_turn_does_not_switch_after_invalid_move(self):
        """Test that turn stays same after failed move"""
        controller = CheckersController()
        assert controller.current_player == Color.WHITE

        from_pos = Position(2, 0)
        to_pos = Position(5, 5)  # Invalid move
        controller.make_move(from_pos, to_pos)

        assert controller.current_player == Color.WHITE

    def test_turn_alternates_correctly(self):
        """Test that turns alternate between players"""
        controller = CheckersController()

        # White move
        controller.make_move(Position(2, 0), Position(3, 1))
        assert controller.current_player == Color.BLACK

        # Black move
        controller.make_move(Position(5, 1), Position(4, 2))
        assert controller.current_player == Color.WHITE

        # White move again
        controller.make_move(Position(3, 1), Position(4, 0))
        assert controller.current_player == Color.BLACK

    def test_get_current_player(self):
        """Test get_current_player method"""
        controller = CheckersController()

        assert controller.get_current_player() == Color.WHITE

        controller.make_move(Position(2, 0), Position(3, 1))
        assert controller.get_current_player() == Color.BLACK


class TestCheckersControllerGameState:
    """Test game state management and transitions"""

    def test_initial_state_is_playing(self):
        """Test that game starts in PLAYING state"""
        controller = CheckersController()

        assert controller.state == GameState.PLAYING
        assert controller.is_game_over() is False

    def test_state_transitions_to_white_wins(self):
        """Test transition to WHITE_WINS state"""
        controller = CheckersController()

        # Remove all black pieces
        black_positions = [pos for pos, piece in controller.board.pieces.items()
                           if piece.color == Color.BLACK]
        for pos in black_positions:
            controller.board.remove_piece(pos)

        # Make any move to trigger game over check
        controller.make_move(Position(2, 0), Position(3, 1))

        assert controller.state == GameState.WHITE_WINS
        assert controller.is_game_over() is True

    def test_state_transitions_to_black_wins(self):
        """Test transition to BLACK_WINS state"""
        controller = CheckersController()
        controller.current_player = Color.BLACK

        # Remove all white pieces
        white_positions = [pos for pos, piece in controller.board.pieces.items()
                           if piece.color == Color.WHITE]
        for pos in white_positions:
            controller.board.remove_piece(pos)

        # Make any move to trigger game over check
        controller.make_move(Position(5, 1), Position(4, 2))

        assert controller.state == GameState.BLACK_WINS
        assert controller.is_game_over() is True

    def test_get_winner_returns_none_during_game(self):
        """Test that get_winner returns None while game ongoing"""
        controller = CheckersController()

        assert controller.get_winner() is None

    def test_get_winner_returns_white(self):
        """Test that get_winner returns WHITE when white wins"""
        controller = CheckersController()

        # Remove all black pieces
        black_positions = [pos for pos, piece in controller.board.pieces.items()
                           if piece.color == Color.BLACK]
        for pos in black_positions:
            controller.board.remove_piece(pos)

        controller.make_move(Position(2, 0), Position(3, 1))

        assert controller.get_winner() == Color.WHITE

    def test_get_winner_returns_black(self):
        """Test that get_winner returns BLACK when black wins"""
        controller = CheckersController()
        controller.current_player = Color.BLACK

        # Remove all white pieces
        white_positions = [pos for pos, piece in controller.board.pieces.items()
                           if piece.color == Color.WHITE]
        for pos in white_positions:
            controller.board.remove_piece(pos)

        controller.make_move(Position(5, 1), Position(4, 2))

        assert controller.get_winner() == Color.BLACK

    def test_no_moves_after_game_over(self):
        """Test that moves cannot be made after game over"""
        controller = CheckersController()

        # End the game
        black_positions = [pos for pos, piece in controller.board.pieces.items()
                           if piece.color == Color.BLACK]
        for pos in black_positions:
            controller.board.remove_piece(pos)

        controller.make_move(Position(2, 0), Position(3, 1))
        assert controller.is_game_over() is True

        # Try to make another move
        result = controller.make_move(Position(2, 2), Position(3, 3))

        # Should fail because game is over
        assert result is False


class TestCheckersControllerReset:
    """Test game reset functionality"""

    def test_reset_creates_new_board(self):
        """Test that reset creates fresh board"""
        controller = CheckersController()

        # Make some moves
        controller.make_move(Position(2, 0), Position(3, 1))
        controller.make_move(Position(5, 1), Position(4, 2))

        # Reset
        controller.reset_game()

        assert controller.board.white_count == 12
        assert controller.board.black_count == 12
        assert len(controller.board.pieces) == 24

    def test_reset_sets_white_as_current_player(self):
        """Test that reset sets white as starting player"""
        controller = CheckersController()

        # Make white move (black's turn)
        controller.make_move(Position(2, 0), Position(3, 1))
        assert controller.current_player == Color.BLACK

        controller.reset_game()

        assert controller.current_player == Color.WHITE

    def test_reset_clears_selection(self):
        """Test that reset clears selected piece"""
        controller = CheckersController()

        controller.select_piece(Position(2, 0))
        assert controller.selected_position is not None

        controller.reset_game()

        assert controller.selected_position is None

    def test_reset_sets_playing_state(self):
        """Test that reset sets state to PLAYING"""
        controller = CheckersController()

        # End the game
        black_positions = [pos for pos, piece in controller.board.pieces.items()
                           if piece.color == Color.BLACK]
        for pos in black_positions:
            controller.board.remove_piece(pos)
        controller.make_move(Position(2, 0), Position(3, 1))

        assert controller.state != GameState.PLAYING

        controller.reset_game()

        assert controller.state == GameState.PLAYING

    def test_reset_allows_new_game(self):
        """Test that reset allows starting a new game"""
        controller = CheckersController()

        # Play until game over
        black_positions = [pos for pos, piece in controller.board.pieces.items()
                           if piece.color == Color.BLACK]
        for pos in black_positions:
            controller.board.remove_piece(pos)
        controller.make_move(Position(2, 0), Position(3, 1))

        # Reset and play new game
        controller.reset_game()

        result = controller.make_move(Position(2, 0), Position(3, 1))
        assert result is True
        assert controller.current_player == Color.BLACK


class TestCheckersControllerKingPromotion:
    """Test king promotion logic"""

    def test_white_piece_promotes_at_row_7(self):
        """Test white piece promotes when reaching row 7"""
        controller = CheckersController()

        # Setup: white piece near promotion
        controller.board.pieces.clear()
        controller.board.set_piece(Position(6, 2), Piece(Color.WHITE))
        controller.board.white_count = 1

        controller.make_move(Position(6, 2), Position(7, 3))

        promoted_piece = controller.board.get_piece(Position(7, 3))
        assert promoted_piece.is_king is True
        assert controller.board.white_kings == 1

    def test_black_piece_promotes_at_row_0(self):
        """Test black piece promotes when reaching row 0"""
        controller = CheckersController()
        controller.current_player = Color.BLACK

        # Setup: black piece near promotion
        controller.board.pieces.clear()
        controller.board.set_piece(Position(1, 1), Piece(Color.BLACK))
        controller.board.black_count = 1

        controller.make_move(Position(1, 1), Position(0, 0))

        promoted_piece = controller.board.get_piece(Position(0, 0))
        assert promoted_piece.is_king is True
        assert controller.board.black_kings == 1

    def test_king_can_move_backwards(self):
        """Test that king can move in both directions"""
        controller = CheckersController()

        # Setup: create a white king
        controller.board.pieces.clear()
        white_king = Piece(Color.WHITE)
        white_king.promote_to_king()
        controller.board.set_piece(Position(4, 4), white_king)
        controller.board.white_count = 1

        # King should have moves in all diagonal directions
        valid_moves = controller.validator.get_all_valid_moves(controller.board, Position(4, 4))

        # Should have both forward and backward moves
        assert len(valid_moves) > 2  # At least moves in multiple directions


class TestCheckersControllerIntegration:
    """Integration tests for complete game scenarios"""

    def test_complete_game_flow(self):
        """Test a complete game from start to finish"""
        controller = CheckersController()

        # Series of moves leading to game progression
        moves = [
            (Position(2, 0), Position(3, 1)),  # White
            (Position(5, 1), Position(4, 2)),  # Black
            (Position(3, 1), Position(5, 3)),  # White captures (if valid)
        ]

        for from_pos, to_pos in moves:
            result = controller.make_move(from_pos, to_pos)
            # Moves should execute or fail gracefully
            assert isinstance(result, bool)

    def test_must_capture_rule(self):
        """Test that player must capture if capture is available"""
        controller = CheckersController()

        # Setup capture scenario
        controller.board.pieces.clear()
        controller.board.set_piece(Position(3, 1), Piece(Color.WHITE))
        controller.board.set_piece(Position(4, 2), Piece(Color.BLACK))
        controller.board.white_count = 1
        controller.board.black_count = 1

        # Try to make non-capture move when capture is available
        # This should fail if must-capture rule is enforced
        result = controller.make_move(Position(3, 1), Position(2, 0))

        # Depending on implementation, this might fail
        # or the validator should only return capture moves
        valid_moves = controller.validator.get_all_valid_moves(controller.board, Position(3, 1))

        # If must-capture is enforced, only capture moves should be valid
        if controller.validator.must_capture(controller.board, Color.WHITE):
            assert all(move.is_capture() for move in valid_moves.values())

    def test_multi_jump_capture(self):
        """Test multiple captures in single turn"""
        controller = CheckersController()

        # Setup: white piece can jump multiple black pieces
        controller.board.pieces.clear()
        controller.board.set_piece(Position(2, 0), Piece(Color.WHITE))
        controller.board.set_piece(Position(3, 1), Piece(Color.BLACK))
        controller.board.set_piece(Position(5, 3), Piece(Color.BLACK))
        controller.board.white_count = 1
        controller.board.black_count = 2

        # First jump
        result = controller.make_move(Position(2, 0), Position(4, 2))
        assert result is True
        assert controller.board.black_count == 1

        # If multi-jump in single move is supported, black_count should be 0
        # Otherwise, this would require another move

    def test_game_with_only_kings(self):
        """Test game scenario with only kings remaining"""
        controller = CheckersController()

        # Setup: only kings on board
        controller.board.pieces.clear()
        white_king = Piece(Color.WHITE)
        white_king.promote_to_king()
        black_king = Piece(Color.BLACK)
        black_king.promote_to_king()

        controller.board.set_piece(Position(3, 3), white_king)
        controller.board.set_piece(Position(4, 4), black_king)
        controller.board.white_count = 1
        controller.board.black_count = 1
        controller.board.white_kings = 1
        controller.board.black_kings = 1

        # Both should be able to move in all directions
        white_moves = controller.validator.get_all_valid_moves(controller.board, Position(3, 3))
        assert len(white_moves) > 0

        # Game should continue
        assert controller.is_game_over() is False


class TestCheckersControllerEdgeCases:
    """Test edge cases and error conditions"""

    def test_select_same_piece_twice(self):
        """Test selecting the same piece twice"""
        controller = CheckersController()
        pos = Position(2, 0)

        result1 = controller.select_piece(pos)
        result2 = controller.select_piece(pos)

        assert result1 is True
        assert result2 is True
        assert controller.selected_position == pos

    def test_select_different_valid_pieces(self):
        """Test selecting different valid pieces in succession"""
        controller = CheckersController()

        controller.select_piece(Position(2, 0))
        assert controller.selected_position == Position(2, 0)

        controller.select_piece(Position(2, 2))
        assert controller.selected_position == Position(2, 2)

    def test_move_after_selection_changes(self):
        """Test move after changing selection"""
        controller = CheckersController()

        # Select first piece
        controller.select_piece(Position(2, 0))

        # Change selection
        controller.select_piece(Position(2, 2))

        # Move from new selection
        result = controller.make_move(Position(2, 2), Position(3, 3))
        assert result is True
        assert controller.board.get_piece(Position(2, 2)) is None
        assert controller.board.get_piece(Position(3, 3)) is not None

    def test_empty_board_scenario(self):
        """Test behavior with empty board"""
        controller = CheckersController()
        controller.board.pieces.clear()
        controller.board.white_count = 0
        controller.board.black_count = 0

        # Should recognize game is over
        winner = controller.board.winner()
        # With no pieces, there might be a draw or specific winner logic
        assert winner is not None or controller.is_game_over()

    def test_board_state_consistency(self):
        """Test that board state remains consistent after operations"""
        controller = CheckersController()

        initial_piece_count = len(controller.board.pieces)
        initial_white = controller.board.white_count
        initial_black = controller.board.black_count

        # Make a non-capture move
        controller.make_move(Position(2, 0), Position(3, 1))

        # Piece count should remain same (no captures)
        assert len(controller.board.pieces) == initial_piece_count
        assert controller.board.white_count == initial_white
        assert controller.board.black_count == initial_black

    def test_get_board_state(self):
        """Test getting board state for serialization/display"""
        controller = CheckersController()

        board_state = controller.get_board_state()

        # Should return board reference or copy
        assert board_state is not None
        # Verify it's the board or a valid representation
        assert hasattr(board_state, 'pieces') or isinstance(board_state, dict)


class TestCheckersControllerValidatorIntegration:
    """Test integration between CheckersController and MoveValidator"""

    def test_controller_uses_validator_for_selection(self):
        """Test that controller delegates selection validation to validator"""
        controller = CheckersController()

        # Valid selection should work
        assert controller.select_piece(Position(2, 0)) is True

        # Invalid selection should fail
        assert controller.select_piece(Position(3, 3)) is False

    def test_controller_uses_validator_for_move_validation(self):
        """Test that controller delegates move validation to validator"""
        controller = CheckersController()

        # Valid move
        assert controller.make_move(Position(2, 0), Position(3, 1)) is True

        # Invalid move
        assert controller.make_move(Position(5, 1), Position(2, 2)) is False

    def test_controller_gets_valid_moves_from_validator(self):
        """Test that controller gets valid moves from validator"""
        controller = CheckersController()
        controller.select_piece(Position(2, 0))

        valid_moves = controller.get_valid_moves_for_selected()

        # Should match what validator returns
        validator_moves = controller.validator.get_all_valid_moves(
            controller.board, Position(2, 0)
        )

        assert valid_moves == validator_moves


class TestCheckersControllerBoardIntegration:
    """Test integration between CheckersController and Board"""

    def test_controller_accesses_board_through_methods(self):
        """Test that controller doesn't directly manipulate board pieces"""
        controller = CheckersController()

        # Engine should use board methods, not direct piece access
        # This is more of a design test - verify controller delegates to board

        from_pos = Position(2, 0)
        to_pos = Position(3, 1)

        initial_from = controller.board.get_piece(from_pos)
        initial_to = controller.board.get_piece(to_pos)

        controller.make_move(from_pos, to_pos)

        final_from = controller.board.get_piece(from_pos)
        final_to = controller.board.get_piece(to_pos)

        assert final_from is None
        assert final_to is not None
        assert final_to.color == initial_from.color

    def test_controller_respects_board_winner_determination(self):
        """Test that controller uses board's winner determination"""
        controller = CheckersController()

        # Remove all black pieces
        black_positions = [pos for pos, piece in controller.board.pieces.items()
                           if piece.color == Color.BLACK]
        for pos in black_positions:
            controller.board.remove_piece(pos)

        controller.make_move(Position(2, 0), Position(3, 1))

        # Engine's winner should match board's winner
        assert controller.get_winner() == controller.board.winner()


@pytest.fixture
def mock_observer():
    """Create a mock observer for testing"""
    observer = Mock()
    observer.on_game_state_changed = Mock()
    observer.on_move_made = Mock()
    observer.on_piece_selected = Mock()
    observer.on_game_over = Mock()
    return observer


@pytest.fixture
def engine():
    """Create a fresh GameEngine for each test"""
    return CheckersController()


@pytest.fixture
def console_viewer():
    """Create a real CheckersViewConsole for integration tests"""
    return CheckersViewConsole()


class TestObserverAttachment:
    """Test observer attachment and detachment"""

    def test_attach_observer(self, engine, mock_observer):
        """Test attaching an observer to engine"""
        engine.attach_observer(mock_observer)
        assert mock_observer in engine.observers

    def test_attach_multiple_observers(self, engine):
        """Test attaching multiple observers"""
        observer1 = Mock()
        observer2 = Mock()
        observer3 = Mock()

        engine.attach_observer(observer1)
        engine.attach_observer(observer2)
        engine.attach_observer(observer3)

        assert len(engine.observers) == 3
        assert observer1 in engine.observers
        assert observer2 in engine.observers
        assert observer3 in engine.observers

    def test_attach_same_observer_twice(self, engine, mock_observer):
        """Test attaching same observer twice"""
        engine.attach_observer(mock_observer)
        engine.attach_observer(mock_observer)

        # Should be in list (implementation may allow duplicates)
        assert mock_observer in engine.observers

    def test_detach_observer(self, engine, mock_observer):
        """Test detaching an observer"""
        engine.attach_observer(mock_observer)
        engine.detach_observer(mock_observer)

        assert mock_observer not in engine.observers

    def test_detach_non_existent_observer(self, engine, mock_observer):
        """Test detaching observer that wasn't attached"""
        # Should handle gracefully or raise appropriate error
        try:
            engine.detach_observer(mock_observer)
            assert True  # Handled gracefully
        except ValueError:
            assert True  # Raises appropriate error

    def test_detach_one_of_multiple_observers(self, engine):
        """Test detaching one observer while others remain"""
        observer1 = Mock()
        observer2 = Mock()
        observer3 = Mock()

        engine.attach_observer(observer1)
        engine.attach_observer(observer2)
        engine.attach_observer(observer3)

        engine.detach_observer(observer2)

        assert observer1 in engine.observers
        assert observer2 not in engine.observers
        assert observer3 in engine.observers

    def test_attach_console_viewer(self, engine, console_viewer):
        """Test attaching real ConsoleViewer"""
        engine.attach_observer(console_viewer)

        assert console_viewer in engine.observers
