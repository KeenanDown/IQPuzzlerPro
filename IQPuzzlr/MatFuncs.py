"""
Various tools for manipulating matrices.
"""

import numpy as np
import copy as cp

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

def get_holes(matrix):
    """Get the hole locations in a matrix.

    Arguments:
        matrix: np.matrix
            The matrix where the 0s are the holes.
    Returns:
        tuple
            The list of hole locations.
    """
    hole_locations = tuple(zip(*np.where(matrix == 0)))
    return hole_locations
