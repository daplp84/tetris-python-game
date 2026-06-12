"""
main.py

Application entry point.

Creates the main window, initializes the renderer,
registers keyboard controls, and starts the game loop.
"""

import tkinter as tk
import constants
import renderer
import game

def on_key(event):
    """
    Handles keyboard input.

    Controls piece movement, rotation, game speed,
    and pause functionality.

    Args:
        event: Tkinter keyboard event.
    """
    if event.keysym == "p":
        game.speed += 10
    if event.keysym == "m":
        game.speed -= 10
    if event.keysym == "Left":
        game.move_left()
    if event.keysym == "Right":
        game.move_right()
    if event.keysym == "Up":
        game.rotate_left()
    if event.keysym == "Down":
        game.rotate_right()
    if event.keysym == "space":
        game.pause()



def main():
    """
    Creates and configures the main application window.
    Initializes the renderer, registers keyboard events,
    starts the game loop, and launches Tkinter's main loop.
    """
    root = tk.Tk()
    root.geometry(f'{constants.WINDOW_WIDTH}x{constants.WINDOW_HEIGHT}')
    root.resizable(False, False)
    renderer.initialize_canvas(root)
    root.bind("<Key>", on_key)
    renderer.draw()
    game.update(root)
    root.mainloop()

 

if __name__ == "__main__":
    main()