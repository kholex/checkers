import tkinter as tk
from enum import Enum
from PIL import Image, ImageTk
from time import sleep


class Field:
    def __init__(self, canvas: tk.Canvas, cell_size: int):
        self._canvas = canvas
        self._cell_size = cell_size
        self._size = cell_size * 8
        self._checkers = {}

    def _draw_cells(self):
        black, white = "#443E3E", "#E8E8E8"
        for i in range(8):
            for j in range(8):
                x_0, x_1 = self._cell_size * i, self._cell_size * (i + 1)
                y_0, y_1 = self._cell_size * j, self._cell_size * (j + 1)
                self._canvas.create_rectangle(x_0, y_0, x_1, y_1, fill=(black if (i + j) % 2 == 0 else white), width=0)

    def _init_checkers(self):
        self._checkers = []
        for i in range(12):
            self._checkers.append(Checker(self._canvas, i, (i % 4) * 2 + (i // 4) % 2, i // 4, self._cell_size,
                                          CheckerType.WHITE))
        for i in range(12):
            self._checkers.append(Checker(self._canvas, i + 12, (i % 4) * 2 + ((i // 4) + 1) % 2, 5 + i // 4,
                                          self._cell_size, CheckerType.BLACK))
        # sleep(1e-3)
        # self._checkers[0].move(6, 6)


class CheckerType(Enum):
    BLACK = 0
    WHITE = 1
    BLACK_SUPER = 2
    WHITE_SUPER = 3


class Checker:
    def __init__(self, canvas: tk.Canvas, number: int, x: int, y: int, size: int, checker_type: CheckerType):
        self._number = number
        self._x = x
        self._y = y
        self._canvas = canvas
        self._size = size
        self._super = False
        self._type = checker_type
        self._icon_png = self._upload_icon(size, checker_type)
        self._icon = self._canvas.create_image(self._x * self._size + self._size // 2,
                                               self._y * self._size + self._size // 2,
                                               image=self._icon_png)
        self._canvas.update()

    def move(self, x: int, y: int):
        steps_num = abs(x - self._x) * 40
        x_step = (x - self._x) / steps_num
        y_step = (y - self._y) / steps_num
        for i in range(steps_num):
            self._canvas.move(self._icon, self._size * x_step, self._size * y_step)
            self._canvas.update()
            sleep(1e-3)


    @staticmethod
    def _upload_icon(size: int, checker_type: CheckerType):
        icons_files = {
            CheckerType.BLACK: 'images/black.png',
            CheckerType.WHITE: 'images/white.png',
            CheckerType.BLACK_SUPER: 'images/black_super.png',
            CheckerType.WHITE_SUPER: 'images/white_super.png',
        }
        file_name = icons_files[checker_type]
        return ImageTk.PhotoImage(Image.open(file_name).resize((size - 4, size - 4), Image.ANTIALIAS))
