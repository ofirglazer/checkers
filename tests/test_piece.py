from src.piece import Piece
from src.config import Color


class TestPiece:
    def test_init(self):
        piece_white = Piece(Color.WHITE)
        assert piece_white.color is Color.WHITE
        assert piece_white.is_king is False

        piece_black = Piece(Color.BLACK)
        assert piece_black.color is Color.BLACK
        assert piece_black.is_king is False

    def test_promote_to_king(self):
        piece = Piece(Color.WHITE)
        assert piece.is_king is False
        piece.promote_to_king()
        assert piece.is_king is True
