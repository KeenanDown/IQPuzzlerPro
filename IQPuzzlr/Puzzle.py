import numpy as np

from IQPuzzlr.Board import board
from IQPuzzlr.StateFuncs import get_moves
from IQPuzzlr.MatFuncs import add_matrix, flip_matrix
from IQPuzzlr.PieceFuncs import rotate_piece

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

        # Create a list of pieces to place.
        self.pieces_to_place = pieces_to_place

        # Attempt to place initial configuration elements.
        for config in init_configuration_list:
            # Check so see if the board configurations match.
            #if config.board != self.board:
            #    raise ValueError("Board of configuration does not match puzzle board.")

            # Apply the try_config and if false, then we know the init config
            # cannot fit.
            if not(self.try_configuration(config)):
                raise ValueError("Initial configuration does not fit.")

        # Create a list of initial configurations.
        self.configs_done = init_configuration_list

        # Create a list of hole locations.
        self.holes = self.get_holes()

    def update_metadata(self):
        """Update metadata variables belonging to self. Variables included are:
        self.holes.
        """
        self.holes = self.get_holes()

    def try_configuration(self, config, in_place = True):
        """Place a specified configuration onto the puzzle in place if successful.

        Args:
            configuration (configuration): The configuration to place.

        Returns:
            bool: Whether or not the attempt was successful.
        """
        # Initialise the 'solved' variable to False.
        success = False

        # Attempt to place the matrix into puzzle.
        after_add = add_matrix(config.piecestate.shape, self.state, config.row, config.col)

        # Check that there are no collisions.
        arr = np.array(after_add.flatten())[0]
        if not(set([2]).issubset(set(arr))):
            # Note that the placement was successful.
            success = True
            # If there are no collisions then we return the puzzle status.
            if in_place:
                self.state = after_add
                self.pieces_to_place.remove(config.piece)

                return success
            elif not(in_place):
                new_pieces_to_place = pieces_to_place[:]
                new_pieces_to_place.remove(config.piece)

                # If not in place, return the new state.
                return success, after_add, new_pieces_to_place
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

    def get_moves(self, state = None, pieces = None, configs_done = None):
        """Get the moves that can be made in the current state.

        Returns: List of valid moves as configurations.
        """
        # If unspecified, set it to the state of the puzzle.
        if state == None:
            state = self.state
        if pieces == None:
            pieces = self.pieces_to_place
        if configs_done == None:
            configs_done = []

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

        move_and_pieces_to_return = [(moveconfig, self.try_configuration(moveconfig, False)[1], self.try_configuration(moveconfig, False)[2]) for moveconfig in moves]
        return move_and_pieces_to_return
        ## USE THE HOLES OF THE PUZZLE TO LOCATE POSSIBLE MOVES.
        # THEN FILTER THOSE MOVES IF THEY DON'T ACTUALLY FIT

    def __str__(self):
        return self.state.__str__()




    def solve(self, method, resolution = 1000):
        """Solves the puzzle using a specified method.

        Args:
            method: solve_method, The method to use to solve.
        Returns:
            solution: list, A list of configurations which solve the puzzle.
        """
        # Initialise variable to store if solution found.
        unsolved = True

        # If there is an initialiser, use it
        if method.initialiser != None:
            method.initialiser()

        # Initialise the scoring table list;
        score_table = []

        # Set the first state.
        current = (self.state, self.pieces_to_place, self.configs_done)

        # Set a counter.
        t = 0

        # Create a looping solve
        while unsolved:
            t += 1
            if t % resolution == 0:
                print(t)

            # Get the list of next possible moves from current.
            print(current)

            moves_to_add_unscored = get_moves(current[0], current[1], current[2])

            # Check if any of these solve the problem.
            for move in moves_to_add_unscored:
                # If there are no pieces left to place afterwards
                if move[1] == []:

                    # Then set as current.
                    current = move

                    # And mark as solved.
                    unsolved = False

            # Score them and make a list.
            if unsolved:
                moves_with_scores = [(move, method.score_function(move[0], move[1], move[2])) for move in moves_to_add_unscored]
                # Add these elements to a table and remove repeats.
                score_table = score_table + moves_with_scores
                #score_table = list(np.unique(score_table))
                # YOU NEED TO MAKE IT UNIQUE STILL
                # ALSO YOU NEED TO NOT REPEAT PREVIOUSLY SEEN MOVES
                # ELSE YOU'LL HAVE AN ETERNAL LOOP.
                # Sort them by the score
                score_table = sorted(score_table, key = lambda mov: mov[1])
                # Set the current as the highest scoring.
                # Simultaneously remove it from the list.
                current = score_table.pop()[0]

        return current[2]
