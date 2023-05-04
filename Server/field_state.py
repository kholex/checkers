from typing import List

from Client.contracts.value_objects.checker import Checker
from Client.contracts.value_objects.checker_type import CheckerType
from Client.contracts.value_objects.possible_move import PossibleMove
from value_objects.point import Point

MOVE_OFFSETS = [Point(-1, -1), Point(1, -1), Point(-1, 1), Point(1, 1)]


def first_true(iterable, default=False, pred=None):
  return next(filter(pred, iterable), default)


class FieldState:

  def __init__(self):
    self.checkers = self.init_state()
    self.calculate_possible_moves()

  def reverse_checker(checker):
      checker.your_checker = not checker.your_checker
      return checker

  def init_state(self):
    i = 0

    checkers_list: List[Checker] = []

    for y in range(0, 3):
      for x in range(y % 2, 8, 2):
        checker = Checker(
          checker_num=i,
          your_checker=True,
          x=x,
          y=y,
          checker_type=CheckerType.WHITE,
          possible_moves=[],
        )
        checkers_list.append(checker)
        i += 1

    for y in range(5, 8):
      for x in range(y % 2, 8, 2):
        checker = Checker(
          checker_num=i,
          your_checker=False,
          x=x,
          y=y,
          checker_type=CheckerType.BLACK,
          possible_moves=[],
        )
        checkers_list.append(checker)
        i += 1

    return checkers_list

  def make_move(self, checker_num: int, move: PossibleMove):

    checker = first_true(self.checkers, False,
                         lambda c: c.checker_num == checker_num)
    checkerMove = first_true(checker.possible_moves, None,
                             lambda m: m.x == move.x and m.y == move.y)

    if (checkerMove):
      checker.x = checkerMove.x
      checker.y = checkerMove.y
      if (checkerMove.remove_checker_num is not None):
        self.checkers = list(
          filter(lambda ch: ch.checker_num != checkerMove.remove_checker_num,
                 self.checkers))
    else:
      raise RuntimeError(
        f"possible move with x: {move.x} and y: {move.y} not found")

    self.calculate_possible_moves()

    return self.checkers

  def make_new_move(self,
                    col,
                    row,
                    now_type,
                    new_type=None,
                    field_remove=None):

    if (now_type == CheckerType.BLACK):
      new_type = type if row == 0 else None
      return PossibleMove(col, row, new_type, field_remove)

    if (now_type == CheckerType.WHITE):
      new_type = type if row == 7 else None
      return PossibleMove(col, row, new_type, field_remove)

    return None

  def calculate_possible_moves_without_super(self, checker):
    row = checker.y
    col = checker.x
    moves = []
    requiredMoves = False
    rowVal = -1 if checker.checker_type == CheckerType.BLACK else 1
    super = None
    if checker.checker_type == CheckerType.WHITE:
      super = CheckerType.WHITE_SUPER

    if checker.checker_type == CheckerType.WHITE:
      super = CheckerType.WHITE_SUPER

    rowChange = row + rowVal
    for colVar in [1, -1]:
      colChange = col + colVar
      if (colChange > 7 or colChange < 0 or rowChange > 7): continue

      field = first_true(self.checkers, False,
                         lambda c: c.y == rowChange and c.x == colChange)

      if (field is False):
        move = self.make_new_move(colChange, rowChange, checker.checker_type,
                                  super)
        moves.append(move)
      else:
        if (field.checker_type == checker.checker_type):
          continue
        col_after_remove = colChange + colVar
        row_after_remove = rowChange + rowVal
        if (col_after_remove > 7 or col_after_remove < 0
            or row_after_remove > 7):
          continue
        field_after_remove = first_true(
          self.checkers, False,
          lambda c: c.y == row_after_remove and c.x == col_after_remove)
        if (field_after_remove is False):
          print(field.checker_num)
          move = self.make_new_move(col_after_remove, row_after_remove,
                                    checker.checker_type, super,
                                    field.checker_num)
          moves.append(move)
          requiredMoves = True

    checker.possible_moves = moves

  def calculate_possible_moves(self):
    for checker in self.checkers:

      if checker.checker_type == CheckerType.BLACK or checker.checker_type == CheckerType.WHITE:
        self.calculate_possible_moves_without_super(checker)
      if checker.checker_type == CheckerType.BLACK or checker.checker_type == CheckerType.WHITE:
        self.calculate_possible_moves_without_super(checker)
