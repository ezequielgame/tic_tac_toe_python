"""
Implementation of the algorithm
"""
from Seed import Seed

from typing import Tuple


class ArtificialIntelligence:
    """
    Implementation of the algorithm
    """

    ROWS: int = 3  # self.ROWS x COLS cells
    COLS: int = 3

    def __init__(self) -> None:
        pass

    def think_next_move(self, cells, turn) -> Tuple[int, int]:
        posO = self.poss_win(Seed.NOUGHT, cells)
        posX = self.poss_win(Seed.CROSS, cells)
        if turn == 1:
            return self.go(1)
        elif turn == 2:
            return self.go(5) if self.make_two(cells) == 5 else self.go(1)
        elif turn == 3:
            return self.go(9) if cells[2][2].content == Seed.NO_SEED else self.go(3)
        elif turn == 4:
            return self.go(posX) if posX != 0 else self.go(self.make_two(cells))
        elif turn == 5:
            if posX != 0:
                return self.go(posX)
            else:
                if posO != 0:
                    return self.go(posO)
                elif cells[2][0].content == Seed.NO_SEED:
                    return self.go(7)
                else:
                    return self.go(3)
        elif turn == 6:
            if posO != 0:
                return self.go(posO)
            else:
                return self.go(posX) if (posX != 0) else self.go(self.make_two(cells))
        elif turn == 7:
            if posX != 0:
                return self.go(posX)
            else:
                return self.go(posO) if posO != 0 else self.get_blank_space_coords(cells)
        elif turn == 8:
            if posO != 0:
                return self.go(posO)
            else:
                if posX != 0:
                    return self.go(posX)
                else:
                    return self.get_blank_space_coords(cells)
        elif turn == 9:
            if posX != 0:
                return self.go(posX)
            else:
                return self.go(posO) if posO != 0 else self.get_blank_space_coords(cells)
        else:
            return -1, -1

    def make_two(self, cells) -> int:
        # Returns 5 if the center square of the board is blank
        if cells[1][1].content == Seed.NO_SEED:
            return 5
        else:
            # Returns any noncorner cell
            if cells[0][1].content == Seed.NO_SEED:
                return 2
            elif cells[1][0].content == Seed.NO_SEED:
                return 4
            elif cells[1][2].content == Seed.NO_SEED:
                return 6
            elif cells[2][1].content == Seed.NO_SEED:
                return 8
        return -1

    def poss_win(self, player, cells) -> int:
        win_value = 0
        if player == Seed.CROSS:
            win_value = 18
        elif player == Seed.NOUGHT:
            win_value = 50
        # Each row
        mult = 1
        blank_cell = -1
        for j, row in enumerate(cells):
            for i, cell in enumerate(row):
                mult *= cell.content.value
                if cell.content == Seed.NO_SEED:
                    blank_cell = i
            if mult == win_value:  # Player can win
                return self.coords_to_number(j, blank_cell)
            mult = 1  # Reset product
        # Each column
        mult = 1
        blank_cell = -1
        for col in range(3):
            for i, row in enumerate(cells):
                mult *= row[col].content.value
                if row[col].content == Seed.NO_SEED:
                    blank_cell = i
            if mult == win_value:  # Player can win
                return self.coords_to_number(blank_cell, col)
            mult = 1
        # Main diagonal
        mult = 1
        board_row = 0
        col = 0
        for i, row in enumerate(cells):
            for j, cell in enumerate(row):
                if i == j:
                    mult *= cell.content.value
                    if cell.content == Seed.NO_SEED:
                        board_row = i
                        col = j
        if mult == win_value:  # Player can win
            return self.coords_to_number(board_row, col)
        # Other diagonal
        mult = 1
        board_row = 0
        col = 0
        for i, row in enumerate(cells):
            for j, cell in enumerate(row):
                if i + j == self.ROWS - 1:
                    mult *= cell.content.value
                    if cell.content == Seed.NO_SEED:
                        board_row = i
                        col = j
        if mult == win_value:  # Player can win
            return self.coords_to_number(board_row, col)
        return 0  # Cannot win in this move

    def go(self,  n) -> int:
        return self.number_to_coords(n)

    def number_to_coords(self, n) -> Tuple[int, int]:
        row = col = 0
        # row
        if 1 <= n <= 3:
            row = 0
        elif 4 <= n <= 6:
            row = 1
        elif 7 <= n <= 9:
            row = 2
        # col
        if n in [1, 4, 7]:
            col = 0
        elif n in [2, 5, 8]:
            col = 1
        elif n in [3, 6, 9]:
            col = 2
        return row, col

    def coords_to_number(self, row, col) -> int:
        n = -1
        if row == 0:
            if col == 0:
                n = 1
            elif col == 1:
                n = 2
            else:
                n = 3
        elif row == 1:
            if col == 0:
                n = 4
            elif col == 1:
                n = 5
            else:
                n = 6
        else:
            if col == 0:
                n = 7
            elif col == 1:
                n = 8
            else:
                n = 9
        return n

    def get_blank_space_coords(self, cells) -> Tuple[int, int]:
        for i, row in enumerate(cells):
            for j, cell in enumerate(row):
                if cell.content == Seed.NO_SEED:
                    return i, j
        return -1, -1
