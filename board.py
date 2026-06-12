"""
board.py

Manages the Tetris game board.

This module stores the board state and provides
functions to initialize the board, remove filled lines, reset the board and more
"""

import constants
from playsound import playsound
import threading

board = [[constants.VOID_COLOR for _ in range(constants.ROWS_QTY)] for _ in range(constants.COLUMNS_QTY)]

def reset_board():
    """
    Restore the board to its initial state, without shapes.
    """
    global board
    board = [[constants.VOID_COLOR for _ in range(constants.ROWS_QTY)] for _ in range(constants.COLUMNS_QTY)]

def is_line_filled(y):
    """
    Checks whether there are any completely filled rows.

    Returns:
        bool: True if there are,
        False otherwise.
    """
    for x in range(constants.COLUMNS_QTY):
        if board[x][y] == constants.VOID_COLOR:
            return False
    return True

def get_filled_lines():
    """
        Finds all completely filled rows on the board

        Returns:
        list[int]: Indices of rows that are completely filled.
    """
    lines = []

    for y in range(constants.ROWS_QTY):
        if is_line_filled(y):
            lines.append(y)

    return lines

def remove_line(line_y):
    """
    Removes a completed row from the board.
    All rows above the specified row are shifted
    down by one position, and the top row is cleared.

    Args:
        line_y (int): Index of the row to remove.
    """
    for y in range(line_y, 0, -1):
        for x in range(constants.COLUMNS_QTY):
            board[x][y] = board[x][y - 1]

    for x in range(constants.COLUMNS_QTY):
        board[x][0] = constants.VOID_COLOR


def remove_filled_lines():
    """
    Removes all completed rows from the board.
    A sound effect is played for each removed row.
    """
    for line in reversed(get_filled_lines()):
        play_sound()
        remove_line(line)

def play_sound():
    """
    Plays the line-clear sound effect asynchronously.
    The sound is executed in a separate thread to
    avoid blocking the game loop.
    """
    threading.Thread(target=playsound, args=("./assets/sounds/pling.mp3",), daemon=True).start()