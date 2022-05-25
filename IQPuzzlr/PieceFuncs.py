import numpy as np
from IQPuzzlr.MiscFuncs import check_type
from IQPuzzlr.Piece import piece
import IQPuzzlr.MatFuncs
import copy as cp

def rotate_piece(piece_g, number_of_times = 0):
    """Rotate a numpy matrix a number of times anticlockwise.

    Args:
        piece (piece): Piece to rotate.
        number_of_times (int): How many times to rotate 'mat'.

    Returns:
        piece: Rotated number_of_times clockwise.
    """

    # Check the types.
    check_type(piece_g, piece)

    # Make a copy so that the piece is not mutable.
    new_piece = cp.copy(piece_g)

    # Change the shape.
    new_piece.shape = IQPuzzlr.MatFuncs.rotate_matrix(new_piece.shape, number_of_times)

    # Change the zero location.
    new_piece.nz_location = new_piece.get_nonzero_location()
    return new_piece
