"""
game.py

Contains the core Tetris game logic.

This module manages piece movement, rotation,
collision detection, scoring, game state,
and the main update loop.
"""

import shapes
import board
import random
import renderer
import numpy as np
import constants
from tkinter import messagebox
from playsound import playsound
import threading

# Current active tetromino position.
current_shape_x = None
current_shape_y = None

# Current active tetromino.
current_shape = shapes.void_shape

# Update interval in milliseconds.
speed = 1000

# Game state flags.
is_paused = False
is_game_over = False

# Current player score.
score = 0

def play_sound():
    """
    Plays the game over sound effect asynchronously.
    """
    threading.Thread(target=playsound, args=("./assets/sounds/gameover.mp3",), daemon=True).start()

def can_move_down(shape):
    """
    Determines whether the current piece can move down.

    Args:
        shape: Tetromino to evaluate.

    Returns:
        bool: True if the piece can move down,
        False otherwise.
    """
    if current_shape_y + len(shape)  >= constants.ROWS_QTY:
        return False
    
    for y in range(len(shape)):
        for x in range(len(shape[y])):
            if board.board[current_shape_x + x][current_shape_y+ y +1] != constants.VOID_COLOR and shape[y][x] != constants.VOID_COLOR:
                return False

    return True

def reset_score():
    """
    Resets the game score to zero.
    """
    global score
    score = 0

def reset_shape():
    """
    Clears the currently active piece and
    resets its position.
    """
    global current_shape
    global current_shape_x
    global current_shape_y
    current_shape = shapes.void_shape
    current_shape_x = 0
    current_shape_y = 0


def new_shape():
    """
    Creates a new random tetromino and places it
    at the top of the board.

    Sets the game over state if the new piece
    cannot be placed.
    """
    global current_shape
    global current_shape_x
    global current_shape_y
    global is_game_over

    shape = random.choice([
        shapes.l_shape,
        shapes.t_shape,
        shapes.square_shape,
        shapes.i_shape,
        shapes.ray_shape
    ])

    current_shape = np.rot90(shape, random.randint(0, 3))

    current_shape_x = constants.COLUMNS_QTY // 2
    current_shape_y = 0
    if not can_move_down(current_shape):
        is_game_over = True
        




def can_move_left(shape):
    """
    Determines whether the specified piece can
    move one cell to the left.

    Args:
        shape: Tetromino to evaluate.

    Returns:
        bool: True if movement is possible.
    """
    if is_paused:
        return False
     #detecto que no haya pared a izquierda
    if current_shape_x == 0:
        return False
    
    #detecto colisión
    for y in range(len(shape)):
            if board.board[current_shape_x - 1][current_shape_y + y] != constants.VOID_COLOR and shape[y][0] != constants.VOID_COLOR:
                return False

    return True

def can_move_right(shape):
    """
    Determines whether the specified piece can
    move one cell to the right.

    Args:
        shape: Tetromino to evaluate.

    Returns:
        bool: True if movement is possible.
    """
    if is_paused:
        return False
     #detecto que no haya pared a izquierda
    if current_shape_x + len(shape[0])  >= constants.COLUMNS_QTY:
        return False
    
    #detecto colisión
    for y in range(len(shape)):
            if board.board[current_shape_x + len(shape[y]) ][current_shape_y + y] != constants.VOID_COLOR and shape[y][len(shape[y]) -1] != constants.VOID_COLOR:
                return False

    return True

def move_right():
    """
    Moves the active piece one cell to the right.
    """
    global current_shape_x
    if can_move_right(current_shape):
        current_shape_x += 1

def move_left():
    """
    Moves the active piece one cell to the left.
    """
    global current_shape_x
    if can_move_left(current_shape):
        current_shape_x -= 1
        

def attach_shape():
    """
    Attaches the active piece to the board.

    Called when the piece can no longer move down.
    """
    for y in range(len(current_shape)):
        for x in range(len(current_shape[y])):
            new_color = current_shape[y][x]
            if new_color != constants.VOID_COLOR:
                board.board[current_shape_x + x][current_shape_y + y] = current_shape[y][x]

def move_shape_down():
    """
    Moves the active piece downward.

    If movement is not possible, the piece is
    attached to the board and a new piece is spawned.
    """
    global current_shape_y
    if can_move_down(current_shape):
        current_shape_y += 1
    else:
        attach_shape()
        new_shape()

def can_rotate_left():
    """
    Checks whether the active piece can be rotated
    counterclockwise.
    """
    if is_paused:
        return False
    #debo comprobar la rotada que entre donde está
    rotated_shape = np.rot90(current_shape, -1)
    return can_move_left(rotated_shape) and can_move_right(rotated_shape) and can_move_down(rotated_shape)

def can_rotate_right():
    """
    Checks whether the active piece can be rotated
    clockwise.
    """
    if is_paused:
        return False
    #debo comprobar la rotada que entre donde está
    rotated_shape = np.rot90(current_shape, 1)
    return can_move_left(rotated_shape) and can_move_right(rotated_shape) and can_move_down(rotated_shape)

def rotate_left():
    """
    Rotates the active piece counterclockwise.
    """
    global current_shape
    if can_rotate_left():
        current_shape = np.rot90(current_shape, -1)

def rotate_right():
    """
    Rotates the active piece clockwise.
    """
    global current_shape
    if can_rotate_right():
        current_shape = np.rot90(current_shape, 1)



def pause():
    """
    Toggles the game's paused state.
    """
    global is_paused
    if is_paused:
        is_paused = False
    else:
        is_paused = True


def decide_new_game(root):
    """
    Displays the game over dialog and lets the player
    choose whether to start a new game or exit.

    Args:
        root: Main Tkinter window.
    """
    play_sound()
    global is_game_over
    decision = messagebox.askyesno(title="Game Over", message="Game over!. Do you want to play again?")
    if decision:
        board.reset_board()
        reset_shape()
        reset_score()
    else:
        root.destroy()

    is_game_over = False

def update(root):
    """
    Main game loop.

    Updates score, removes completed lines,
    processes piece movement, redraws the game,
    and schedules the next update cycle.

    Args:
        root: Main Tkinter window.
    """
    global score
    score += len(board.get_filled_lines())
    board.remove_filled_lines()
    root.title(f"Tetris - Score: {score}")
    if not is_paused and not is_game_over:
        if np.array_equal(current_shape, shapes.void_shape):
            new_shape()
        move_shape_down()


    renderer.draw()

    if is_game_over:
        decide_new_game(root)


    root.after(speed, lambda: update(root))