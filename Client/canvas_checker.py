"""This module realize work with checker on canvas."""
from PIL import Image, ImageTk
from time import sleep
import pathlib
import os
import tkinter as tk
from .canvas_move import CanvasMove
from .contracts.value_objects.checker_type import CheckerType


class CanvasChecker:
    """Checker on canvas field."""
    cur_file_path = pathlib.Path(__file__).parent.resolve()
    _icons_files = {
        CheckerType.BLACK: 'images/black.png',
        CheckerType.WHITE: 'images/white.png',
        CheckerType.BLACK_SUPER: 'images/black_super.png',
        CheckerType.WHITE_SUPER: 'images/white_super.png',
    }
    for key in _icons_files:
        _icons_files[key] = os.path.join(cur_file_path, _icons_files[key])

    def __init__(self, canvas: tk.Canvas, number: int, your_checker: bool, x: int, y: int, size: int,
                 checker_type: CheckerType):
        """Initialize checker on canvas."""
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
        """Move checker to some place on field."""
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
        """Set possible moves for checker."""
        self.moves = moves

    def clear_possible_moves(self):
        """Clear possible moves and delete them from canvas if checker was selected."""
        for selection in self._possible_moves_selection:
            self._canvas.delete(selection)
        self._possible_moves_selection.clear()

    def clear(self):
        """Clear all checker elements from canvas."""
        self._canvas.delete(self.icon)
        self.clear_possible_moves()

    def draw_possible_moves(self):
        """Draw possible moves for checker, for example, if user selected checker."""
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
