
"""
shapes.py

Defines the tetromino shapes used in the game.

Each shape is represented as a matrix of colors,
where VOID_COLOR indicates an empty cell.
"""
import constants

# L-shaped tetromino.
l_shape= [
    [constants.L_COLOR, constants.VOID_COLOR, constants.VOID_COLOR, constants.VOID_COLOR, constants.VOID_COLOR],
    [constants.L_COLOR, constants.L_COLOR, constants.L_COLOR, constants.L_COLOR, constants.L_COLOR]
]

# T-shaped tetromino.
t_shape= [
    [constants.T_COLOR, constants.T_COLOR, constants.T_COLOR],
    [constants.VOID_COLOR, constants.T_COLOR, constants.VOID_COLOR]
]

# Square tetromino.
square_shape= [
    [constants.SQUARE_COLOR, constants.SQUARE_COLOR],
    [constants.SQUARE_COLOR, constants.SQUARE_COLOR]
]

# I-shaped tetromino.
i_shape= [
    [constants.I_COLOR, constants.I_COLOR, constants.I_COLOR, constants.I_COLOR, constants.I_COLOR]
]

# ray-shaped or S-Shaped tetromino.
ray_shape= [
    [constants.RAY_COLOR, constants.VOID_COLOR],
    [constants.RAY_COLOR, constants.RAY_COLOR],
    [constants.VOID_COLOR, constants.RAY_COLOR]
]

# Represents the absence of an active piece.
void_shape= [constants.VOID_COLOR]