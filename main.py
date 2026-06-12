import tkinter as tk
from tkinter import messagebox
import constants
import renderer
import game

def on_key(event):
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