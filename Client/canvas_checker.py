from PIL import Image, ImageTk
from time import sleep
import tkinter as tk
from canvas_move import CanvasMove
from contracts.value_objects.checker_type import CheckerType


class CanvasChecker:
    _icons_files = {
        CheckerType.BLACK: 'images/black.png',
        CheckerType.WHITE: 'images/white.png',
        CheckerType.BLACK_SUPER: 'images/black_super.png',
        CheckerType.WHITE_SUPER: 'images/white_super.png',
    }

    def __init__(self, canvas: tk.Canvas, number: int, your_checker: bool, x: int, y: int, size: int, checker_type: CheckerType):
        self.your_checker = your_checker
        self.moves: list[CanvasMove] = []
        self.number = number
        self.x = x
        self.y = y
        self._canvas = canvas
        self._size = size
        self._super = False
        self._type = checker_type
        self._icon_png = self._upload_icon(size, checker_type)
        self.icon = self._canvas.create_image(self.x * self._size + self._size // 2,
                                              self.y * self._size + self._size // 2,
                                              image=self._icon_png)
        self._possible_moves_selection: list[int] = []

    def move(self, move: CanvasMove):
        if move.remove_checker_icon:
            self._canvas.tag_raise(self.icon, move.remove_checker_icon)
        steps_num = abs(move.x - self.x) * 40
        x_step = (move.x - self.x) / steps_num
        y_step = (move.y - self.y) / steps_num
        for i in range(steps_num):
            self._canvas.move(self.icon, self._size * x_step, self._size * y_step)
            self._canvas.update()
            sleep(1e-3)
        self.x = move.x
        self.y = move.y
        if move.remove_checker_icon:
            self._canvas.delete(move.remove_checker_icon)

        if move.new_type:
            self._canvas.delete(self.icon)
            self._icon_png = self._upload_icon(self._size, move.new_type)
            self.icon = self._canvas.create_image(self.x * self._size + self._size // 2,
                                                  self.y * self._size + self._size // 2,
                                                  image=self._icon_png)
            self._canvas.update()

    def set_possible_moves(self, moves: list[CanvasMove]):
        self.moves = moves

    def clear_possible_moves(self):
        for selection in self._possible_moves_selection:
            self._canvas.delete(selection)
        self._possible_moves_selection.clear()

    def clear(self):
        self._canvas.delete(self.icon)
        self.clear_possible_moves()

    def draw_possible_moves(self):
        for move in self.moves:
            rect = self._canvas.create_rectangle(move.x * self._size, move.y * self._size,
                                                 move.x * self._size + self._size, move.y * self._size + self._size,
                                                 outline='#51ed13',
                                                 width=4, tag='border')
            self._possible_moves_selection.append(rect)

    @staticmethod
    def _upload_icon(size: int, checker_type: CheckerType):
        file_name = CanvasChecker._icons_files[checker_type]
        return ImageTk.PhotoImage(Image.open(file_name).resize((size - 4, size - 4), Image.ANTIALIAS))
