"""This module is field state of game."""
from Client.contracts.value_objects.checker import Checker
from Client.contracts.value_objects.checker_type import CheckerType
from Client.contracts.value_objects.possible_move import PossibleMove

from .value_objects.point import Point
from .value_objects.side_type import SideType
from functools import reduce
from typing import List


# Массивы типов белых и чёрных шашек [Обычная пешка, дамка]
WHITE_CHECKERS = [CheckerType.WHITE, CheckerType.WHITE_SUPER]
BLACK_CHECKERS = [CheckerType.BLACK, CheckerType.BLACK_SUPER]
MOVE_OFFSETS = [Point(-1, -1), Point(1, -1), Point(-1, 1), Point(1, 1)]


class FieldState:
    """Field state in the game."""

    def __init__(self):
        """Initialize field state of game."""
        self.__x_size = 8
        self.__y_size = 8
        self.__checkers = {}
        self.__generate()
        self.__side = SideType.WHITE
        self.__update_moves(self.__side)

    @property
    def checkers(self) -> List[Checker]:
        """List of all checkers in game."""
        return list(self.__checkers.values())

    @property
    def x_size(self) -> int:
        """Size of field by axis x."""
        return self.__x_size

    @property
    def y_size(self) -> int:
        """Size of field by axis y."""
        return self.__y_size

    @property
    def size(self) -> int:
        """Size of field in game."""
        return max(self.x_size, self.y_size)

    def __generate(self):
        """Генерация поля с шашками."""
        i = 0
        for y in range(self.y_size):
            for x in range(self.x_size):
                if (y + x) % 2:
                    if y < 3:
                        self.__checkers[y, x] = Checker(i, False, x, y, CheckerType.BLACK, [])
                    elif y >= self.y_size - 3:
                        self.__checkers[y, x] = Checker(i, False, x, y, CheckerType.WHITE, [])
                    i += 1

    def type_at(self, x: int, y: int) -> CheckerType:
        """Получение типа шашки на поле по координатам."""
        if (y, x) not in self.__checkers:
            return CheckerType.NONE
        return self.__checkers[y, x].checker_type

    def at(self, x: int, y: int) -> Checker:
        """Получение шашки на поле по координатам."""
        return self.__checkers[y, x]

    def is_within(self, x: int, y: int) -> bool:
        """Определяет лежит ли точка в пределах поля."""
        return 0 <= x < self.x_size and 0 <= y < self.y_size

    @property
    def white_checkers_count(self) -> int:
        """Количество белых шашек на поле."""
        return sum(reduce(lambda acc, checker: acc + (checker.type in WHITE_CHECKERS), checkers, 0) for checkers in
                   self.__checkers)

    @property
    def black_checkers_count(self) -> int:
        """Количество чёрных шашек на поле."""
        return sum(reduce(lambda acc, checker: acc + (checker.type in BLACK_CHECKERS), checkers, 0) for checkers in
                   self.__checkers)

    @property
    def white_score(self) -> int:
        """Счёт белых."""
        return sum(reduce(lambda acc, checker: acc + (checker.type == CheckerType.WHITE) + (
                checker.type == CheckerType.WHITE_SUPER) * 3, checkers, 0) for checkers in self.__checkers)

    @property
    def black_score(self) -> int:
        """Счёт чёрных."""
        return sum(reduce(lambda acc, checker: acc + (checker.type == CheckerType.BLACK) + (
                checker.type == CheckerType.BLACK_SUPER) * 3, checkers, 0) for checkers in self.__checkers)

    def make_move(self, checker_num: int, move: PossibleMove):
        """Make move in game."""
        checker = next((x for x in self.__checkers.values() if x.checker_num == checker_num), None)
        checker_move = next((m for m in checker.possible_moves if m.x == move.x and m.y == move.y), None)

        if checker_move:
            del self.__checkers[checker.y, checker.x]
            checker.x = checker_move.x
            checker.y = checker_move.y
            if checker_move.remove_checker_num is not None:
                remove_checker = next((x for x in self.__checkers.values()
                                       if x.checker_num == checker_move.remove_checker_num), None)
                del self.__checkers[remove_checker.y, remove_checker.x]
            self.__checkers[checker.y, checker.x] = checker
        else:
            raise RuntimeError(
                f"possible move with x: {move.x} and y: {move.y} not found")

        has_required_moves = self.__update_required_moves(self.__side)
        if move.remove_checker_num is None or not has_required_moves:
            self.__side = SideType.opposite(self.__side)
        self.__update_moves(self.__side)

    def __update_moves(self, side: SideType) -> None:
        """Получение списка ходов."""
        has_required_moves = self.__update_required_moves(side)
        if not has_required_moves:
            self.__update_optional_moves(side)

    def __update_required_moves(self, side: SideType) -> bool:
        """Получение списка обязательных ходов."""
        # Определение типов шашек
        if side == SideType.WHITE:
            friendly_checkers = WHITE_CHECKERS
            enemy_checkers = BLACK_CHECKERS
        elif side == SideType.BLACK:
            friendly_checkers = BLACK_CHECKERS
            enemy_checkers = WHITE_CHECKERS
        else:
            raise Exception("Impossible SideType")

        has_required_moves = False
        for y in range(self.y_size):
            for x in range(self.x_size):
                moves_list = []
                # Для обычной шашки
                if self.type_at(x, y) == friendly_checkers[0]:
                    for offset in MOVE_OFFSETS:
                        if not (self.is_within(x + offset.x * 2, y + offset.y * 2)):
                            continue

                        if self.type_at(x + offset.x, y + offset.y) in enemy_checkers and self.type_at(
                                x + offset.x * 2, y + offset.y * 2) == CheckerType.NONE:
                            has_required_moves = True
                            checker_to_remove = self.at(x + offset.x, y + offset.y)
                            moves_list.append(PossibleMove(x + offset.x * 2, y + offset.y * 2, None, checker_to_remove.checker_num))
                    self.at(x, y).possible_moves = moves_list

                # Для дамки
                elif self.type_at(x, y) == friendly_checkers[1]:
                    for offset in MOVE_OFFSETS:
                        if not (self.is_within(x + offset.x * 2, y + offset.y * 2)):
                            continue

                        enemy_checker_on_way = None

                        for shift in range(1, self.size):
                            if not (self.is_within(x + offset.x * shift, y + offset.y * shift)):
                                continue

                            # Если на пути не было вражеской шашки
                            if not enemy_checker_on_way:
                                if self.type_at(x + offset.x * shift, y + offset.y * shift) in enemy_checkers:
                                    enemy_checker_on_way = self.at(x + offset.x * shift, y + offset.y * shift)
                                    continue
                                # Если на пути союзная шашка - то закончить цикл
                                elif self.type_at(x + offset.x * shift, y + offset.y * shift) in friendly_checkers:
                                    break

                            # Если на пути была вражеская шашка
                            if enemy_checker_on_way:
                                if self.type_at(x + offset.x * shift, y + offset.y * shift) == CheckerType.NONE:
                                    has_required_moves = True
                                    moves_list.append(PossibleMove(x + offset.x * shift, y + offset.y * shift, None,
                                                                   enemy_checker_on_way.checker_num))
                                else:
                                    break
                    self.at(x, y).possible_moves = moves_list
                elif self.type_at(x, y) != CheckerType.NONE:
                    self.at(x, y).possible_moves = []

        return has_required_moves

    def __update_optional_moves(self, side: SideType) -> None:
        """Получение списка необязательных ходов."""
        # Определение типов шашек
        if side == SideType.WHITE:
            friendly_checkers = WHITE_CHECKERS
        elif side == SideType.BLACK:
            friendly_checkers = BLACK_CHECKERS
        else:
            raise Exception("Impossible SideType")

        for y in range(self.y_size):
            for x in range(self.x_size):
                moves_list = []
                # Для обычной шашки
                if self.type_at(x, y) == friendly_checkers[0]:
                    for offset in MOVE_OFFSETS[:2] if side == SideType.WHITE else MOVE_OFFSETS[2:]:
                        if not (self.is_within(x + offset.x, y + offset.y)):
                            continue

                        if self.type_at(x + offset.x, y + offset.y) == CheckerType.NONE:
                            moves_list.append(PossibleMove(x + offset.x, y + offset.y))
                    self.at(x, y).possible_moves = moves_list

                # Для дамки
                elif self.type_at(x, y) == friendly_checkers[1]:
                    for offset in MOVE_OFFSETS:
                        if not (self.is_within(x + offset.x, y + offset.y)):
                            continue

                        for shift in range(1, self.size):
                            if not (self.is_within(x + offset.x * shift, y + offset.y * shift)):
                                continue

                            if self.type_at(x + offset.x * shift, y + offset.y * shift) == CheckerType.NONE:
                                moves_list.append(PossibleMove(x + offset.x * shift, y + offset.y * shift))
                            else:
                                break
                    self.at(x, y).possible_moves = moves_list
                elif self.type_at(x, y) != CheckerType.NONE:
                    self.at(x, y).possible_moves = []
