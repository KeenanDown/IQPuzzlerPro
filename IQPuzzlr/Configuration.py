import numpy as np
from IQPuzzlr.Board import board
from IQPuzzlr.Piece import piece
from IQPuzzlr.MiscFuncs import check_type
import IQPuzzlr.PieceFuncs
import IQPuzzlr.MatFuncs

class configuration:
    """Define a configuration, a data structure containing a board and
    a piece at a location on that board.

    Attributes:
        board_g (board): A board in which the piece is placed.
        piece_g (piece): A piece which is in the desired configuration.
        row (int): The row representing where the piece is placed.
        col (int): The column representing where the piece is placed.
        rot (int): How many times the piece is rotated.
        flip (bool): Whether or not the piece is transposed.

    Notes:
        Transposition is done before rotation.
    """
    def __init__(self, board_g = board(), piece_g = np.matrix([1]), row = 0, col = 0, flip = False, rot = 0):
        # Check various object types.
        check_type(board_g, board)
        check_type(piece_g, piece)
        check_type(row, int)
        check_type(col, int)
        check_type(rot, int)
        check_type(flip, bool)

        self.board = board_g
        self.piece = piece_g
        self.row = row
        self.col = col
        self.rot = rot
        self.flip = flip

        # Rotate the piece.
        self.rotatedpiece = IQPuzzlr.PieceFuncs.rotate_piece(self.piece, self.rot)

        # Flip the piece.
        self.flippedpiece = piece(IQPuzzlr.MatFuncs.flip_matrix(self.piece.shape, self.flip))

        # Rotate after flipping the piece.
        self.piecestate = IQPuzzlr.PieceFuncs.rotate_piece(self.flippedpiece, self.rot)

        # Add the piece to the board and save it.
        self.state = IQPuzzlr.MatFuncs.add_matrix(self.piecestate.shape, self.board.shape, row, col)

    def __str__(self):
        return self.state.__str__()
