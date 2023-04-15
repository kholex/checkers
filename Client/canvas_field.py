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
        self._checkers: dict[int, CanvasChecker] = {}
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
        # TODO: чистить поле от предыдущих шашек
        self._checkers.clear()
        for checker in checkers:
            self._checkers[checker.checker_num] = CanvasChecker(
                self._canvas, checker.checker_num, checker.x, checker.y, self._cell_size, checker.checker_type)
        for checker in checkers:
            moves = [CanvasMove(move.x, move.y, move.new_type,
                                move.remove_checker_num,
                                self._checkers[move.remove_checker_num].icon if move.remove_checker_num else None)
                     for move in checker.possible_moves]
            self._checkers[checker.checker_num].set_possible_moves(moves)

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

        selected_checker = [checker for checker in self._checkers.values() if checker.x == x and checker.y == y]

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
                    move = possible_move[0]
                    self._selected_checker.move(move)

                    if move.remove_checker_num:
                        del self._checkers[move.remove_checker_num]
                    move_json = json.dumps(Move(self._selected_checker.number, move.x, move.y, move.new_type,
                                                move.remove_checker_num).__dict__)

                    self._receive_queue.put_nowait(move_json)
                    self._receive_queue._loop._write_to_self()

