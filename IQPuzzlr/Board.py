import numpy as np

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
