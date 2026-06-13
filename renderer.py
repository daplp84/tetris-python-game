"""
renderer.py

Handles all graphical rendering operations.

This module is responsible for creating the game
canvas and drawing the current board state and
active tetromino using Tkinter.
"""

import constants
import tkinter as tk
import board
import numpy as np
import game
import shapes

canvas = None

def initialize_canvas(root):
    """
    Creates and configures the game canvas.

    Args:
        root: Main Tkinter window.
    """
    global canvas
    canvas = tk.Canvas(
        root, 
        width=constants.GAMEBOARD_WIDTH, 
        height=constants.GAMEBOARD_HEIGHT, 
        highlightbackground="black",  
        highlightthickness=1, 
        bg='white'
    )
    canvas.pack()


def draw():
    """
    Renders the current game state.

    Draws the board and overlays the active
    tetromino on top of the existing cells.
    """
    canvas.delete('all')
    for x in range(constants.COLUMNS_QTY):
        for y in range(constants.ROWS_QTY):
            color = board.board[x][y]
            outline = 1
            if not np.array_equal(game.current_shape, shapes.void_shape):
                if x >= game.current_shape_x and x < game.current_shape_x + len(game.current_shape[0]) and y >= game.current_shape_y and y < game.current_shape_y + len(game.current_shape):
                    new_color = game.current_shape[y-game.current_shape_y][x-game.current_shape_x] 
                    if new_color != constants.VOID_COLOR:
                        color = new_color
            if color != constants.VOID_COLOR:
                outline = 3            
            canvas.create_rectangle(
                int(x*constants.GAMEBOARD_WIDTH/constants.COLUMNS_QTY), 
                int(y*constants.GAMEBOARD_HEIGHT/constants.ROWS_QTY),
                int(x*constants.GAMEBOARD_WIDTH/constants.COLUMNS_QTY + constants.GAMEBOARD_WIDTH/constants.COLUMNS_QTY), 
                int(y*constants.GAMEBOARD_HEIGHT/constants.ROWS_QTY + constants.GAMEBOARD_HEIGHT/constants.ROWS_QTY),
                fill=color,
                width=outline
                )
            
