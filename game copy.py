import shapes
import board
import random
import renderer
import numpy as np
import constants

current_shape_x = None
current_shape_y = None
current_shape = shapes.void_shape

speed = 100


def new_shape():
    global current_shape
    global current_shape_x
    global current_shape_y

    shape = random.choice([
        shapes.l_shape,
        shapes.t_shape,
        shapes.square_shape,
        shapes.i_shape
    ])

    current_shape = np.rot90(shape, random.randint(0, 3))

    current_shape_x = constants.COLUMNS_QTY // 2
    current_shape_y = 0

    draw_shape()


def is_current_shape_cell(x, y):
    for sy in range(len(current_shape)):
        for sx in range(len(current_shape[sy])):

            if current_shape[sy][sx] == constants.VOID_COLOR:
                continue

            if (
                current_shape_x + sx == x and
                current_shape_y + sy == y
            ):
                return True

    return False


def erase_shape():
    for sy in range(len(current_shape)):
        for sx in range(len(current_shape[sy])):

            if current_shape[sy][sx] == constants.VOID_COLOR:
                continue

            bx = current_shape_x + sx
            by = current_shape_y + sy

            if (
                0 <= bx < constants.COLUMNS_QTY and
                0 <= by < constants.ROWS_QTY
            ):
                board.board[bx][by] = constants.VOID_COLOR


def draw_shape():
    for sy in range(len(current_shape)):
        for sx in range(len(current_shape[sy])):

            if current_shape[sy][sx] == constants.VOID_COLOR:
                continue

            bx = current_shape_x + sx
            by = current_shape_y + sy

            if (
                0 <= bx < constants.COLUMNS_QTY and
                0 <= by < constants.ROWS_QTY
            ):
                board.board[bx][by] = current_shape[sy][sx]


def can_move_down():
    for sy in range(len(current_shape)):
        for sx in range(len(current_shape[sy])):

            if current_shape[sy][sx] == constants.VOID_COLOR:
                continue

            bx = current_shape_x + sx
            by = current_shape_y + sy

            next_y = by + 1

            # piso
            if next_y >= constants.ROWS_QTY:
                return False

            # si la celda debajo pertenece a la misma pieza, ignorarla
            if is_current_shape_cell(bx, next_y):
                continue

            # colisión con bloque ya colocado
            if board.board[bx][next_y] != constants.VOID_COLOR:
                return False

    return True


def move_shape_down():
    global current_shape_y

    erase_shape()

    if can_move_down():
        current_shape_y += 1
        draw_shape()
    else:
        draw_shape()
        new_shape()


def update(root):
    if np.array_equal(current_shape, shapes.void_shape):
        new_shape()

    move_shape_down()

    renderer.draw()

    root.after(speed, lambda: update(root))