"""
Implementation of the algorithm
"""
from Board import Board
from Seed import Seed

from typing import Tuple


class ArtificialIntelligence:
    """
    Implementation of the algorithm
    """

    ROWS: int# self.ROWS x self.COLS cells
    COLS: int
    
    def __init__(self):
        self.ROWS = 3
        self.COLS = 3
        pass
    
    def think_next_move(self, cells, turn) -> Tuple[int, int]:
        poss_win_o = poss_win(Seed.NOUGHT, cells)
        poss_win_x = poss_win(Seed.CROSS, cells)
        if turn == 1:
            return go(1)
        elif turn == 2:
            return go(5) if make_two(cells) == 5 else go(1)
        elif turn == 3:
            return go(9) if cells[2][2].content == Seed.NO_SEED else go(3)
        elif turn == 4:
            return go(poss_win_x) if poss_win_x != 0 else go(make_two(cells))
        elif turn == 5:
            if poss_win_x != 0:
                return go(poss_win_x)
            else:
                if poss_win_o != 0:
                    return go(poss_win_o)
                elif cells[2][0].content == Seed.NO_SEED:
                    return go(7)
                else:
                    return go(3)
        elif turn == 6:
            if poss_win_o != 0:
                return go(poss_win_o)
            else:
                print(go(make_two(cells)))
                return go(poss_win_x) if poss_win_x != 0 else go(make_two(cells))
        elif turn == 7:
            if poss_win_x != 0:
                return go(poss_win_x)
            else:
                return go(poss_win_o) if poss_win_o != 0 else get_blank_space_coords(cells)
        elif turn == 8:
            if poss_win_o != 0:
                return go(poss_win_o)
            else:
                if poss_win_x != 0:
                    return go(poss_win_x)
                else:
                    return get_blank_space_coords(cells)
        elif turn == 9:
            if poss_win_x != 0:
                return go(poss_win_x)
            else:
                return go(poss_win_o) if poss_win_o != 0 else get_blank_space_coords(cells)
        else:
            return -1, -1

def make_two(cells) -> int:
    # Returns 5 if the center square of the board is blank
    if cells[1][1].content == Seed.NO_SEED:
        return 5
    else:
        # Combinaciones de aristas y esquinas opuestas (donde_puedo_tirar, opuesta_esta_vacia?)
        combs = [(2,8),(8,2),(4,6),(6,4),(1,9),(9,1),(3,7),(7,3)]
        # Trata de juntar 2, para esto, la tercer casilla, es decir, la opuesta, tampoco debe tener nada
        # de esta manera obliga al otro jugador a tapar en el siguiente turno.
        for comb in combs:
            if get_content(cells, comb[0]) == Seed.NO_SEED and get_content(cells,comb[1]) == Seed.NO_SEED:
                return comb[0]
    return -1

def poss_win(player, cells) -> int:
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
            return coords_to_number(j, blank_cell)
        mult = 1  # Reset product
    # Each column
    mult = 1
    blank_cell = -1
    for col in range(Board.COLS):
        for i, row in enumerate(cells):
            mult *= row[col].content.value
            if row[col].content == Seed.NO_SEED:
                blank_cell = i
        if mult == win_value:  # Player can win
            return coords_to_number(blank_cell, col)
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
        return coords_to_number(board_row, col)
    # Other diagonal
    mult = 1
    board_row = 0
    col = 0
    for i, row in enumerate(cells):
        for j, cell in enumerate(row):
            if i + j == Board.ROWS - 1:
                mult *= cell.content.value
                if cell.content == Seed.NO_SEED:
                    board_row = i
                    col = j
    if mult == win_value:  # Player can win
        return coords_to_number(board_row, col)
    return 0  # Cannot win in this move

def go(n) -> int:
    return number_to_coords(n)

def number_to_coords(n) -> Tuple[int, int]:
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

def coords_to_number(row, col) -> int:
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

def get_blank_space_coords(cells) -> Tuple[int, int]:
    for i, row in enumerate(cells):
        for j, cell in enumerate(row):
            if cell.content == Seed.NO_SEED:
                return i, j
    return -1, -1
    
def get_content(cells, n) -> Seed:
    coords = number_to_coords(n)
    return cells[coords[0]][coords[1]].content
