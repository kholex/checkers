import asyncio
import tkinter as tk
from contracts.checker_type import CheckerType
from contracts.checker import Checker
from canvas_move import CanvasMove
from canvas_checker import CanvasChecker
from contracts.move import Move
import json


class CanvasField:
    def __init__(self, canvas: tk.Canvas, cell_size: int, receive_queue: asyncio.Queue):
        self._receive_queue = receive_queue
        self._canvas = canvas
        self._cell_size = cell_size
        self._size = cell_size * 8
        self.checkers: dict[int, CanvasChecker] = {}
        self._selected_checker: CanvasChecker = None
        self._canvas.bind("<Button-1>", self.click)
        self._draw_cells()

    def _draw_cells(self):
        black, white = "#443E3E", "#E8E8E8"
        for i in range(8):
            for j in range(8):
                x_0, x_1 = self._cell_size * i, self._cell_size * (i + 1)
                y_0, y_1 = self._cell_size * j, self._cell_size * (j + 1)
                self._canvas.create_rectangle(x_0, y_0, x_1, y_1, fill=(black if (i + j) % 2 == 0 else white), width=0)

    def init_checkers(self, checkers: list[Checker]):
        for checker in self.checkers.values():
            checker.clear()

        self.checkers.clear()
        for checker in checkers:
            self.checkers[checker.checker_num] = CanvasChecker(
                self._canvas, checker.checker_num, checker.your_checker, checker.x, checker.y, self._cell_size,
                checker.checker_type)
        for checker in checkers:
            moves = [CanvasMove(move.x, move.y, move.new_type,
                                move.remove_checker_num,
                                self.checkers[move.remove_checker_num].icon if move.remove_checker_num else None)
                     for move in checker.possible_moves]
            self.checkers[checker.checker_num].set_possible_moves(moves)
        self._canvas.update()

    def click(self, event: tk.Event):
        x, y = event.x // self._cell_size, event.y // self._cell_size

        if not (0 <= x <= self._size) and (0 <= y <= self._size):
            return

        selected_checker = [checker for checker in self.checkers.values() if checker.x == x and checker.y == y]

        if selected_checker:
            if not selected_checker[0].your_checker:
                return
            if self._selected_checker is not None:
                self._selected_checker.clear_possible_moves()

            self._selected_checker = selected_checker[0]
            self._selected_checker.draw_possible_moves()
        else:
            if self._selected_checker is not None:
                possible_move = [move for move in self._selected_checker.moves if (move.x == x) and (move.y == y)]
                if possible_move:
                    self._selected_checker.clear_possible_moves()
                    move = possible_move[0]
                    self._selected_checker.move(move)

                    if move.remove_checker_num:
                        del self.checkers[move.remove_checker_num]
                    move_json = json.dumps(Move(self._selected_checker.number, move.x, move.y, move.new_type,
                                                move.remove_checker_num).__dict__)

                    self._receive_queue.put_nowait(move_json)
                    self._receive_queue._loop._write_to_self()

