from src.position import Position
import pytest
from src.config import CheckersConfig


class TestPosition:
    def test_valid_value(self):
        position = Position(1, 1)
        assert position.row == 1
        assert position.col == 1
        assert position.valid == True
        position = Position(4, 6)
        assert position.row == 4
        assert position.col == 6
        assert position.valid == True

    def test_invalid_input_type(self):
        with pytest.raises(TypeError):
            position = Position("f", "x")
        with pytest.raises(TypeError):
            position = Position(3.0, 5.0)

    def test_invalid_value_outside_board(self):
        position = Position(CheckersConfig.board_size + 1, 1)
        assert position.valid == False
        position = Position(2, -1)
        assert position.valid == False

    def test_invalid_value_not_black_squares(self):
        position = Position(0, 1)
        assert position.valid == False
        position = Position(1, 0)
        assert position.valid == False

    def test_equality(self):
        position1 = Position(7, 5)
        position2 = Position(7, 5)
        position3 = Position(6, 0)
        assert position1 == position2
        assert not position1 == position3

    def test_str(self):
        position = Position(2, 4)
        assert str(position) == "(2, 4)"

    def test_hash(self):
        position = Position(3, 1)
        assert position.__hash__() == hash(position)
