import numpy as np
import copy as cp
import time

checked_module = True


class piece:
    """A shape which can be used in the iqpuzzler puzzles.

    Attributes:
        shape (numpy.matrix): A matrix describing the shape of the piece
            using 0 and 1. Use 0 to represent an empty tile and 1 to
            represent a filled tile.
        nz_location (1x2 tuple): A tuple describing the location of the first
            nonzero location in the part. Useful for certain calculations.

    Examples:
        piece1 = piece(np.matrix('1 1 0; 1 1 1'))
    """
    def __init__(self, shape):

        if type(shape) != np.matrix:
            raise TypeError("'shape' must be a numpy matrix.")
        # Define the shape of the part as a numpy matrix.
        self.shape = shape
        # Use the shape to make a new matrix specifying a nonzero location.
        self.nz_location = self.get_nonzero_location()
        # Get valid flip/rotation combinations which account for symmetry.
        self.valid_flip_rotations = self.get_valid_flip_rotations()

    def get_valid_flip_rotations(self):
        """Return the valid flip/rotation combinations which do not repeat themselves.
        """
        valid_flip_rotation_matrices = [self.shape]
        valid_flip_rotations = [(False, 0)]

        # Iterate through the flips and rotations.
        for flip in [False, True]:
            for rot in [0, 1, 2, 3]:
                test_matrix = rotate_matrix(flip_matrix(self.shape, flip), rot)

                # If in the list then change the variable.
                not_in_list = True
                for matrix_in_list in valid_flip_rotation_matrices:
                    if np.array_equal(test_matrix,matrix_in_list):
                        not_in_list = False

                # If not in list then append it.
                if not_in_list:
                    valid_flip_rotation_matrices.append(test_matrix)
                    valid_flip_rotations.append((flip, rot))

        return valid_flip_rotations

    def get_nonzero_location(self):
        """Find a nonzero coordinate of the piece.
        """
        return tuple(np.transpose(np.nonzero(self.shape))[0])

    def update_metadata(self):
        """Update various bits of useful metadata. Currently only nz_location, the location of a nonzero coordinate of the piece.
        """
        self.nz_location = self.get_nonzero_location()

        return self

    def __str__(self):
        return self.shape.__str__()


def rotate_matrix(mat, number_of_times):
    """Rotate a numpy matrix a number of times anticlockwise.

    Args:
        mat (Numpy.matrix): Matrix to rotate.
        number_of_times (int): How many times to rotate 'mat'.

    Returns:
        Numpy.matrix: Rotated number_of_times clockwise.
    """
    if type(number_of_times) != int:
        raise TypeError("'number_of_times' must be of type int.")
    if type(mat) != np.matrix:
        raise TypeError("'mat' must be of type numpy.matrix.")
    if number_of_times < 0:
        raise ValueError("'number_of_times' must be a positive integer.")

    n = 0
    return_matrix = mat

    while n<number_of_times:
        return_matrix = np.rot90(return_matrix)
        n = n + 1
    return return_matrix

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
    new_piece.shape = rotate_matrix(new_piece.shape, number_of_times)

    # Change the zero location.
    new_piece.nz_location = new_piece.get_nonzero_location()
    return new_piece

def flip_matrix(mat, Bool = False):
    """Transpose a matrix if 'Bool' is true.

    Args:
        mat (numpy.matrix): matrix to transpose.
        Bool (bool): If true then the matrix is transposed.

    Returns:
        numpy.matrix: (Possibly transposed) matrix.
    """
    #Some ValueError raises.
    if type(mat) != np.matrix:
        raise TypeError("'mat' must be of type numpy.matrix.")
    if type(Bool) != bool:
        raise TypeError("'Bool' must be of type bool.")

    if Bool == True:
        return np.transpose(mat)
    else:
        return mat


def add_matrix(matrix_to_add, base_matrix, row, col):
    """Add one smaller matrix to another larger matrix,
    given a location to do so.

    Args:
        matrix_to_add (numpy.matrix): Matrix to add to another matrix.
        base_matrix (numpy.matrix): The matrix being added to.
        row (int): The row where the smaller matrix is placed.
        col (int): The column where the smaller matrix is placed.

    Returns:
        numpy.matrix: A matrix where the matrix_to_add has been added at
            location (row, col) to the matrix base_matrix.
    """
    # Some error raises.
    if type(matrix_to_add) != np.matrix:
        raise TypeError("'matrix_to_add' must be of type numpy.matrix.")
    if type(base_matrix) != np.matrix:
        raise TypeError("'base_matrix' must be of type numpy.matrix.")
    if type(row) != int or type(col) != int:
        raise TypeError("'row' and 'col' must be integers.")
    if row < 0 or row > base_matrix.shape[0] - matrix_to_add.shape[0]:
        raise ValueError("'matrix_to_add' cannot be placed at this row.")
    if col < 0 or col > base_matrix.shape[1] - matrix_to_add.shape[1]:
        raise ValueError("'matrix_to_add' cannot be placed at this column.")

    addmat = cp.copy(matrix_to_add) # Do not alter the inputs.
    basemat = cp.copy(base_matrix) # Do not alter the inputs. Make immuting.

    # Add the smaller matrix at the correct location.
    np.add(basemat[row:row+addmat.shape[0], col:col+addmat.shape[1]], addmat, out=basemat[row:row+addmat.shape[0], col:col+addmat.shape[1]], casting="unsafe")
    return basemat

def check_type(object, type_specified):
    """Checks that an object is a certain type, and raises an error if not.

    Args:
        object (obj): Any object to check.
        type_specified (type): Any type to check.

    Returns:
        bool: Whether or not the objects match.
    """
    if type(object) != type_specified:
        raise TypeError("Type " + str(type(object)) + " should be " + str(type_specified) + ".")

    return True



class board:
    """A board into which pieces are placed. Required to form puzzles.

    Attributes:
        shape (numpy.matrix): A matrix of zeroes and ones representing the board. If not specified, the board will have standard 5x11 shape.
    """
    def __init__(self, shape = np.matrix(np.zeros((5,11)))):
        # Initialises the shape of the board.
        if type(shape) != np.matrix and type(shape) != none:
            raise TypeError("'shape' must be a numpy matrix or not specified.")
        board.shape = shape

        # Check that the board initially only contains 0 or 1.
        arr = np.array(self.shape.flatten())[0]
        if not(set(arr).issubset(set([0,1]))):
            raise ValueError("Elements in the initial board matrix can be only zero or one.")

    def __str__(self):
        return self.shape.__str__()


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
        self.rotatedpiece = rotate_piece(self.piece, self.rot)

        # Flip the piece.
        self.flippedpiece = piece(flip_matrix(self.piece.shape, self.flip))

        # Rotate after flipping the piece.
        self.piecestate = rotate_piece(self.flippedpiece, self.rot)

        # Add the piece to the board and save it.
        self.state = add_matrix(self.piecestate.shape, self.board.shape, row, col)

    def __str__(self):
        return self.state.__str__()


# Define the standard board.
std_board = board()


class puzzle:
    """A puzzle that can be attempted. Can be augmented with configurations.

    Attributes:
        board (board, optional): The board on which the puzzle is being played.
        init_configuration_list (list, optional): A list of piece configurations which start the puzzle. This will be augmented using the .try_configuration() method.
    """
    def get_holes(self):
        """Return a list of tuples representing unfilled coordinates. Also updates self.holes.
        """
        hole_locations = tuple(zip(*np.where(self.state == 0)))
        return hole_locations


    def __init__(self, init_configuration_list = [], pieces_to_place = [], board = board()):

        # Set the initial status of the puzzle.
        self.board = board
        self.state = self.board.shape

        # Initialise the solution list (a list of configurations.)
        self.solution = []

        # Attempt to place initial configuration elements.
        for config in init_configuration_list:

            # Check so see if the board configurations match.
            #if config.board != self.board:
            #    raise ValueError("Board of configuration does not match puzzle board.")

            # Apply the try_config and if false, then we know the init config
            # cannot fit.
            if not(self.try_configuration(config)):
                raise ValueError("Initial configuration does not fit.")

        # Create a list of pieces to place.
        self.pieces_to_place = pieces_to_place

        # Create a list of hole locations.
        self.holes = self.get_holes()

    def update_metadata(self):
        """Update metadata variables belonging to self. Variables included are:
        self.holes.
        """
        self.holes = self.get_holes()

    def try_configuration(self, configuration, in_place = True):
        """Place a specified configuration onto the puzzle in place if successful.

        Args:
            configuration (configuration): The configuration to place.

        Returns:
            bool: Whether or not the attempt was successful.
        """
        # Initialise the 'solved' variable to False.
        success = False

        # Attempt to place the matrix into puzzle.
        after_add = add_matrix(configuration.piecestate.shape, self.state, configuration.row, configuration.col)

        # Check that there are no collisions.
        arr = np.array(after_add.flatten())[0]
        if not(set([2]).issubset(set(arr))):
            # Note that the placement was successful.
            success = True
            # If there are no collisions then we return the puzzle status.
            if in_place:
                self.state = after_add

                return success
            elif not(in_place):
                # If not in place, return the new state.
                return success, after_add
        else:
            return success # NB success = false here.

    def check_filled(self):
        """Check that the board is completely filled. Takes no arguments.
        """
        arr = self.shape.flatten()
        if np.any(arr == 0):
            return False
        else:
            return True

    def get_moves(self, state = None, pieces = None):
        """Get the moves that can be made in the current state.

        Returns: List of valid moves as configurations.
        """
        # If unspecified, set it to the state of the puzzle.
        if state == None:
            state = self.state
        if pieces == None:
            pieces = self.pieces_to_place

        # Get the puzzle holes
        holes = self.holes

        # Initialise moves
        moves = []

        # Iterate to add configurations to a list.
        for piece_g in pieces:

            for flip, rot in piece_g.valid_flip_rotations:

                # Imagine what the orientation of the piece looks like.

                test_piece = rotate_piece(piece(flip_matrix(piece_g.shape, flip)), rot).update_metadata()

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

        return moves
        ## USE THE HOLES OF THE PUZZLE TO LOCATE POSSIBLE MOVES.
        # THEN FILTER THOSE MOVES IF THEY DON'T ACTUALLY FIT

    def __str__(self):
        return self.state.__str__()




    def solve(self, method):
        """Solves the puzzle using a specified method.

        Args:
            method: solve_method, The method to use to solve.
        Returns:
            solution: list, A list of configurations which solve the puzzle.
        """
        # Initialise variable to store if solution found.
        unsolved = True

        # Define the recursive looping function.
        def recursor(state, remaining_pieces, configlist = []):
            for config in method.function(state, remaining_pieces):
                try_configuration(config, in_place = False)
                if self.check_filled():
                    unsolved = False
                if unsolved:
                    pass
        # Create the recursive loop.
        while unsolved:
            pass




##### With intentions to add a .solve method to a puzzle, we want to be able to specify the method. As such we're going to create a new class called solve_method which contains a recursive function which successively suggests configurations for unplaced pieces.
class solve_method:
    """A class specifying the solve method, a recursive function taking a puzzle state.

    Args:
        placement_returner: A function taking in a board state and pieces to place and returning a list of moves to try.
    """
    def __init__(self, function):
        self.function = function
