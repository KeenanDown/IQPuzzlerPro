# IQPuzzlerPro

The goal of this project is to develop a python package which can solve the IQPuzzlerPro puzzle game using various different methods.
![IQ Puzzler Game](https://www.funlearning.co.uk/wp-content/uploads/2016/09/SMG0020E_IQ_Puzzler_Pro_C_1.jpg)

The game involves a specified board configuration where several pieces are already placed and the player must place the remaining pieces to complete the board.

Methods aim to include brute-force placement, a more sensible branch-pheasibility approach, and finally a machine learning approach.
The first two of these three methods have been built but not yet implemented into this package.

Currently I am building a more robust framework (sensibly object-oriented) to do this.

The main classes in IQPuzzlr are piece, board, configuration and puzzle.
The objects are built on NumPy arrays. A piece is a small array describing a piece shape. The board is a rectangular shape (not just the one in the classic puzzle), the configuration is a placement of a piece onto the board, and a puzzle is a challenge to solve.

Contact me (Keenan) if you have any questions!
