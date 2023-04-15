import tkinter as tk
from CanvasField import CanvasField

cell_size = 60
field_size = cell_size * 8

if __name__ == '__main__':
    screen = tk.Tk()

    canvas = tk.Canvas(screen, width=field_size, height=field_size)
    canvas.pack()

    field = CanvasField(canvas, cell_size)
    field._draw_cells()
    field._init_checkers()

    screen.title('Checkers')
    screen.resizable(0, 0)
    screen.mainloop()
