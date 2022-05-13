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

def get_moves(state, pieces_to_place, configs_done = None):
    """Return possible moves given a board state, pieces to place and a list of configurations already placed.

    Args:
        state (Numpy.matrix): The state of the board.
        pieces_to_place (list): List of piece objects which need to be placed.
        configs_done (list): List of configurations already placed.
    Returns:
        valid_moves (list): List of tuples (config, state, pieces, configs_done)
            Where config is the suggested configuration,
            state is the state after placing config,
            pieces is a list of pieces still to be placed
            configs_done is a list of configs placed.
    """
    pieces = pieces_to_place

    # Get the puzzle holes
    holes = self.holes
    # Initialise moves
    moves = []

    # Iterate to add configurations to a list.
    for piece_g in pieces:

        for flip, rot in piece_g.valid_flip_rotations:
            # Imagine what the orientation of the piece looks like.
            test_piece = IQPuzzlr.MatFuncs.rotate_piece(piece(IQPuzzlr.MatFuncs.flip_matrix(piece_g.shape, flip)), rot).update_metadata()

            # Filter holes so we only test that we can actually get the piece on the board.
            viable_holes = list(filter(lambda tup: (0<=(tup[0]-test_piece.nz_location[0]) <= self.board.shape.shape[0]-test_piece.shape.shape[0]) and (0<=(tup[1]-test_piece.nz_location[1])<= self.board.shape.shape[1]-test_piece.shape.shape[1]), holes))

            # Fix a bug where viable_holes has zero length.
            if len(viable_holes) != 0:
                viable_locations = list(map(tuple, (np.array(viable_holes) - test_piece.nz_location)))
            else:
                viable_locations = []

            #NB Viable holes are locations of holes, not the coordinates where the piece is placed, so we have just adjusted for that difference.

            # Iterate row and column.
            for row, col in viable_locations:
                config = configuration(self.board, piece_g, int(row), int(col), bool(flip), int(rot))

                if self.try_configuration(config, in_place = False):
                    moves.append(config)

    move_and_pieces_to_return = [(moveconfig, self.try_configuration(moveconfig, False)[1], self.try_configuration(moveconfig, False)[2]) for moveconfig in moves]
    return move_and_pieces_to_return
