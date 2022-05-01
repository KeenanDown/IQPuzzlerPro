import numpy as np

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
