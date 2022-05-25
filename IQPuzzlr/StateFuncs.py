"""Functions for manipulating the state."""

import numpy as np
from IQPuzzlr.MiscFuncs import check_type
from IQPuzzlr.Piece import piece
from IQPuzzlr.Configuration import configuration
from IQPuzzlr.PieceFuncs import rotate_piece
from IQPuzzlr.Board import board
import IQPuzzlr.MatFuncs
from IQPuzzlr.MatFuncs import add_matrix
import copy as cp

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
    holes = IQPuzzlr.MatFuncs.get_holes(state)
    # Initialise moves
    moves = []

    # Iterate to add configurations to a list.
    for piece_g in pieces:

        for flip, rot in piece_g.valid_flip_rotations:
            # Imagine what the orientation of the piece looks like.
            test_piece = rotate_piece(piece(IQPuzzlr.MatFuncs.flip_matrix(piece_g.shape, flip)), rot).update_metadata()

            # Filter holes so we only test that we can actually get the piece on the board.
            viable_holes = list(filter(lambda tup: (0<=(tup[0]-test_piece.nz_location[0]) <= state.shape[0]-test_piece.shape.shape[0]) and (0<=(tup[1]-test_piece.nz_location[1])<= state.shape[1]-test_piece.shape.shape[1]), holes))

            # Fix a bug where viable_holes has zero length.
            if len(viable_holes) != 0:
                viable_locations = list(map(tuple, (np.array(viable_holes) - test_piece.nz_location)))
            else:
                viable_locations = []

            #NB Viable holes are locations of holes, not the coordinates where the piece is placed, so we have just adjusted for that difference.

            # Iterate row and column.
            for row, col in viable_locations:
                config = configuration(board(np.matrix(np.zeros(state.shape))), piece_g, int(row), int(col), bool(flip), int(rot))

                if try_configuration(state, config, pieces, in_place = False):
                    moves.append(config)


    move_and_pieces_to_return = [(try_configuration(state, moveconfig, pieces, False)[1], try_configuration(state, moveconfig, pieces, False)[2], configs_done + [moveconfig]) for moveconfig in moves]
    return move_and_pieces_to_return

def try_configuration(state, config, pieces_to_place, in_place = True):
    """Place a specified configuration onto the puzzle if successful.

    Args:
        config: configuration
            The configuration to place.
        in_place: Bool
            Whether or not to

    Returns:
        bool: Whether or not the attempt was successful.
    """
    # Initialise the 'solved' variable to False.
    success = False

    # Attempt to place the matrix into puzzle.
    after_add = add_matrix(config.piecestate.shape, state, config.row, config.col)

    # Check that there are no collisions.
    arr = np.array(after_add.flatten())[0]
    if not(set([2]).issubset(set(arr))):
        # Note that the placement was successful.
        success = True
        # If there are no collisions then we return the puzzle status.
        if in_place:
            state = after_add
            pieces_to_place.remove(config.piece)

            return success
        elif not(in_place):
            new_pieces_to_place = pieces_to_place[:]
            new_pieces_to_place.remove(config.piece)

            # If not in place, return the new state.
            return success, after_add, new_pieces_to_place
    else:
        return success # NB success = false here.
