import numpy as np

def check_type(object, type_specified):
    """Checks that an object is a certain type, and raises an error if not.

    Args:
        object (obj): Any object to check.
        type_specified (type): Any type to check.

    Returns:
        bool: Whether or not the objects match.
    """
    if not isinstance(object, type_specified):
        raise TypeError("Type " + str(type(object)) + " should be " + str(type_specified) + ".")

    return True
