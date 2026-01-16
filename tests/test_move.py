import pytest
from src.move import Move
from src.position import Position


class TestMoveClass:
    """Unit tests for the Move class using pytest"""

    @pytest.fixture
    def valid_pos1(self):
        """Fixture for first valid position"""
        return Position(0, 0)

    @pytest.fixture
    def valid_pos2(self):
        """Fixture for second valid position"""
        return Position(1, 1)

    @pytest.fixture
    def valid_pos3(self):
        """Fixture for third valid position"""
        return Position(7, 7)

    @pytest.fixture
    def invalid_pos1(self):
        """Fixture for first invalid position"""
        return Position(0, 1)

    @pytest.fixture
    def invalid_pos2(self):
        """Fixture for first invalid position"""
        return Position(5, 6)

    def test_init_with_valid_positions(self, valid_pos1, valid_pos2):
        """Test Move initialization with valid Position objects"""
        move = Move(valid_pos1, valid_pos2)

        assert move.from_pos == valid_pos1
        assert move.dest_pos == valid_pos2
        assert move.is_capture is False
        assert move.valid is True

    def test_init_with_capture_flag(self, valid_pos1, valid_pos2):
        """Test Move initialization with is_capture flag set to True"""
        move = Move(valid_pos1, valid_pos2, is_capture=True)

        assert move.from_pos == valid_pos1
        assert move.dest_pos == valid_pos2
        assert move.is_capture is True
        assert move.valid is True

    def test_init_with_non_position_from_pos(self, valid_pos2):
        """Test Move raises TypeError when from_pos is not a Position"""
        with pytest.raises(TypeError, match="from_pos and dest_pos must be positions"):
            Move("not a position", valid_pos2)

    def test_init_with_non_position_dest_pos(self, valid_pos1):
        """Test Move raises TypeError when dest_pos is not a Position"""
        with pytest.raises(TypeError, match="from_pos and dest_pos must be positions"):
            Move(valid_pos1, "not a position")

    def test_init_with_both_non_positions(self):
        """Test Move raises TypeError when both arguments are not Positions"""
        with pytest.raises(TypeError, match="from_pos and dest_pos must be positions"):
            Move("not a position", 123)

    def test_init_with_none_from_pos(self, valid_pos2):
        """Test Move raises TypeError when from_pos is None"""
        with pytest.raises(TypeError, match="from_pos and dest_pos must be positions"):
            Move(None, valid_pos2)

    def test_init_with_none_dest_pos(self, valid_pos1):
        """Test Move raises TypeError when dest_pos is None"""
        with pytest.raises(TypeError, match="from_pos and dest_pos must be positions"):
            Move(valid_pos1, None)

    def test_init_with_both_none(self):
        """Test Move raises TypeError when both arguments are None"""
        with pytest.raises(TypeError, match="from_pos and dest_pos must be positions"):
            Move(None, None)

    def test_is_valid_with_invalid_from_pos(self, invalid_pos1, valid_pos1):
        """Test is_valid returns False when from_pos is invalid"""
        move = Move(invalid_pos1, valid_pos1)

        assert move.valid is False

    def test_is_valid_with_invalid_dest_pos(self, invalid_pos1, valid_pos1):
        """Test is_valid returns False when dest_pos is invalid"""
        move = Move(valid_pos1, invalid_pos1)

        assert move.valid is False

    def test_is_valid_with_both_positions_invalid(self, invalid_pos1, invalid_pos2):
        """Test is_valid returns False when both positions are invalid"""
        move = Move(invalid_pos1, invalid_pos2)

        assert move.valid is False

    def test_move_attributes_are_accessible(self, valid_pos1, valid_pos2):
        """Test that all Move attributes are accessible"""
        move = Move(valid_pos1, valid_pos2, is_capture=False)

        assert hasattr(move, 'from_pos')
        assert hasattr(move, 'dest_pos')
        assert hasattr(move, 'valid')
        assert hasattr(move, 'is_capture')

    @pytest.mark.parametrize("from_row,from_col,dest_row,dest_col,is_capture", [
        (0, 0, 1, 1, False),
        (0, 0, 7, 7, True),
        (3, 3, 4, 4, True),
        (7, 6, 6, 5, False),
    ])
    def test_different_position_objects(self, from_row, from_col, dest_row, dest_col, is_capture):
        """Test Move with different Position objects"""
        from_pos = Position(from_row, from_col)
        dest_pos = Position(dest_row, dest_col)

        move = Move(from_pos, dest_pos, is_capture)
        assert move.from_pos == from_pos
        assert move.dest_pos == dest_pos
        assert move.is_capture == is_capture

    def test_is_capture_defaults_to_false(self, valid_pos1, valid_pos2):
        """Test that is_capture defaults to False when not specified"""
        move = Move(valid_pos1, valid_pos2)
        assert move.is_capture is False

    @pytest.mark.parametrize("is_capture_value", [True, False])
    def test_is_capture_parameter_honored(self, valid_pos1, valid_pos2, is_capture_value):
        """Test that is_capture parameter is correctly honored"""
        move = Move(valid_pos1, valid_pos2, is_capture=is_capture_value)
        assert move.is_capture == is_capture_value

    def test_equality(self):
        position1 = Position(7, 5)
        position2 = Position(3, 5)
        position3 = Position(6, 0)
        move1 = Move(position1, position2, is_capture=True)
        move2 = Move(position1, position2, is_capture=True)
        move3 = Move(position1, position3)
        assert move1 == move2
        assert not move1 == move3


# Parametrized tests for invalid inputs
class TestMoveInvalidInputs:
    """Test suite for invalid input handling"""

    @pytest.mark.parametrize("invalid_from,invalid_dest", [
        ("string", Position(0, 0)),
        (123, Position(0, 0)),
        ([], Position(0, 0)),
        ({}, Position(0, 0)),
        (Position(0, 0), "string"),
        (Position(0, 0), 456),
        (Position(0, 0), []),
        (Position(0, 0), {}),
    ])
    def test_invalid_type_inputs(self, invalid_from, invalid_dest):
        """Test various invalid type combinations raise TypeError"""
        with pytest.raises(TypeError, match="from_pos and dest_pos must be positions"):
            Move(invalid_from, invalid_dest)
