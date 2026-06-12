import shapes
import board
import random
import renderer
import numpy as np
import constants
from tkinter import messagebox

current_shape_x = None
current_shape_y = None
current_shape = shapes.void_shape

speed = 100

is_paused = False
is_game_over = False
score = 0

def can_move_down(shape):
    #detecto que no haya piso
    if current_shape_y + len(shape)  >= constants.ROWS_QTY:
        return False
    
    #detecto colisión
    for y in range(len(shape)):
        for x in range(len(shape[y])):
            if board.board[current_shape_x + x][current_shape_y+ y +1] != constants.VOID_COLOR and shape[y][x] != constants.VOID_COLOR:
                return False

    return True

def reset_score():
    global score
    score = 0

def reset_shape():
    global current_shape
    global current_shape_x
    global current_shape_y
    current_shape = shapes.void_shape
    current_shape_x = 0
    current_shape_y = 0


def new_shape():
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
    global current_shape_x
    if can_move_right(current_shape):
        current_shape_x += 1

def move_left():
    global current_shape_x
    if can_move_left(current_shape):
        current_shape_x -= 1
        

def attach_shape():
    for y in range(len(current_shape)):
        for x in range(len(current_shape[y])):
            new_color = current_shape[y][x]
            if new_color != constants.VOID_COLOR:
                board.board[current_shape_x + x][current_shape_y + y] = current_shape[y][x]

def move_shape_down():
    global current_shape_y
    if can_move_down(current_shape):
        current_shape_y += 1
    else:
        attach_shape()
        new_shape()

def can_rotate_left():
    if is_paused:
        return False
    #debo comprobar la rotada que entre donde está
    rotated_shape = np.rot90(current_shape, -1)
    return can_move_left(rotated_shape) and can_move_right(rotated_shape) and can_move_down(rotated_shape)

def can_rotate_right():
    if is_paused:
        return False
    #debo comprobar la rotada que entre donde está
    rotated_shape = np.rot90(current_shape, 1)
    return can_move_left(rotated_shape) and can_move_right(rotated_shape) and can_move_down(rotated_shape)

def rotate_left():
    global current_shape
    if can_rotate_left():
        current_shape = np.rot90(current_shape, -1)

def rotate_right():
    global current_shape
    if can_rotate_right():
        current_shape = np.rot90(current_shape, 1)



def pause():
    global is_paused
    if is_paused:
        is_paused = False
    else:
        is_paused = True


def decide_new_game(root):
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