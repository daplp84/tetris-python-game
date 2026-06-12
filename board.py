import constants
from playsound import playsound
import threading

board = [[constants.VOID_COLOR for _ in range(constants.ROWS_QTY)] for _ in range(constants.COLUMNS_QTY)]

def reset_board():
    global board
    board = [[constants.VOID_COLOR for _ in range(constants.ROWS_QTY)] for _ in range(constants.COLUMNS_QTY)]

def is_line_filled(y):
    for x in range(constants.COLUMNS_QTY):
        if board[x][y] == constants.VOID_COLOR:
            return False
    return True

def get_filled_lines():
    lines = []

    for y in range(constants.ROWS_QTY):
        if is_line_filled(y):
            lines.append(y)

    return lines

def remove_line(line_y):
    for y in range(line_y, 0, -1):
        for x in range(constants.COLUMNS_QTY):
            board[x][y] = board[x][y - 1]

    for x in range(constants.COLUMNS_QTY):
        board[x][0] = constants.VOID_COLOR

def remove_filled_lines():
    for line in reversed(get_filled_lines()):
        play_sound()
        remove_line(line)

def play_sound():
    threading.Thread(target=playsound, args=("./assets/sounds/pling.mp3",), daemon=True).start()