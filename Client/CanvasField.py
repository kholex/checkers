import tkinter as tk

from contracts.CheckerType import CheckerType
from CanvasMove import CanvasMove
from CanvasChecker import CanvasChecker


class CanvasField:
    def __init__(self, canvas: tk.Canvas, cell_size: int):
        self._canvas = canvas
        self._cell_size = cell_size
        self._size = cell_size * 8
        self._checkers = {}
        self._selected_checker: CanvasChecker = None
        self._canvas.bind("<Button-1>", self.click)

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
            self._checkers.append(CanvasChecker(self._canvas, i, (i % 4) * 2 + (i // 4) % 2, i // 4, self._cell_size,
                                                CheckerType.WHITE))
        for i in range(12):
            self._checkers.append(CanvasChecker(self._canvas, i + 12, (i % 4) * 2 + ((i // 4) + 1) % 2, 5 + i // 4,
                                                self._cell_size, CheckerType.BLACK))

        self._checkers[15].move(CanvasMove(5, 3))
        self._checkers[11].set_possible_moves([CanvasMove(4, 4, CheckerType.WHITE_SUPER, 15, self._checkers[15].icon)])

    def click(self, event: tk.Event):
        x, y = event.x // self._cell_size, event.y // self._cell_size

        if not (0 <= x <= self._size) and (0 <= y <= self._size):
            return

        selected_checker = [checker for checker in self._checkers if checker.x == x and checker.y == y]

        if selected_checker:
            if self._selected_checker is not None:
                self._selected_checker.clear_possible_moves()

            self._selected_checker = selected_checker[0]
            self._selected_checker.draw_possible_moves()
        else:
            if self._selected_checker is not None:
                possible_move = [move for move in self._selected_checker.moves if (move.x == x) and (move.y == y)]
                if possible_move:
                    self._selected_checker.clear_possible_moves()
                    self._selected_checker.move(possible_move[0])
                    self._checkers = [checker for checker in self._checkers
                                      if checker.number != possible_move[0].remove_checker_num]
