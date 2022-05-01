import numpy as np

##### With intentions to add a .solve method to a puzzle, we want to be able to specify the method. As such we're going to create a new class called solve_method which contains a recursive function which successively suggests configurations for unplaced pieces.
class score_method:
    """A class specifying the score method, a function taking in a puzzle state and a possible set of moves.

    Args:
        initialiser: Function which makes preparations for scoring.
        score_function: A function with the following arguments:
            config: A configuration to place.
            state: The state of the board.
            [pieces_to_place]: A list of pieces still needing to be placed (after the config is placed).
            [configs_done]: A list of configurations placed (including the current).

            and returns a score. Higher scores have higher priority and will be tested faster. Lower scores have lower priority.

            The initialiser will be called at the beginning of a solve. The score_function will be called repeatedly throughout.


    """
    def __init__(self, score_function, initialiser = None):
        self.initialise = initialiser
        self.score_function = score_function

        ### Need to implement an arg check at some point to make sure its working.




def brute_force_initialiser():
    """Initialise the brute force scorer.
    global move_count
    move_count = 0
    """

def brute_force_func(config, state, pieces_to_place, configs_done):
    """The brute force scorer. Scores simply increment by 1 each time, leading to a logicless sweep of all pieces being placed.
    """
    global move_count
    move_count += 1
    return move_count

brute_force = score_method(brute_force_func, brute_force_initialiser)
