from State import State
from Cell import Cell
from Seed import Seed
"""
The Board class models the ROWS-by-COLS game self.
"""


class Board:
    """
    The Board class models the ROWS-by-COLS game self.
    """
    ROWS: int = 3
    COLS: int = 3

    CANVAS_WIDTH: int = Cell.SIZE * COLS
    CANVAS_HEIGHT: int = Cell.SIZE * ROWS
    GRID_WIDTH: int = 8
    GRID_WIDTH_HALF: int = GRID_WIDTH / 2
    # COLOR_GRID:int  =
    Y_OFFSET: int = 1

    COLOR_BG = 'white'
    COLOR_GRID = 'gray'

    cells: list

    def __init__(self) -> None:
        self.init_game()

    def init_game(self) -> None:
        self.cells = [[Cell(i, j) for j in range(self.COLS)]
                      for i in range(self.ROWS)]

    def new_game(self) -> None:
        for row in self.cells:
            for cell in row:
                cell.new_game()

    def step_game(self, player, row, col) -> State:
        self.cells[row][col].content = player
        # Check winner
        # Row win
        for row in self.cells:
            win = True
            for cell in row:
                win = win and cell.content == player
            if win:
                return State.CROSS_WON if player == Seed.CROSS else State.NOUGHT_WON
        # Col win
        for col in range(3):
            win = True
            for row in self.cells:
                win = win and row[col].content == player
            if win:
                return State.CROSS_WON if player == Seed.CROSS else State.NOUGHT_WON
        # Main diagonal
        win = True
        for i, row in enumerate(self.cells):
            for j, cell in enumerate(row):
                if i == j:
                    win = win and cell.content == player
        if win:
            return State.CROSS_WON if player == Seed.CROSS else State.NOUGHT_WON
        # Other diagonal
        win = True
        for i, row in enumerate(self.cells):
            for j, cell in enumerate(row):
                if i + j == self.ROWS - 1:
                    win = win and cell.content == player
        if win:
            return State.CROSS_WON if player == Seed.CROSS else State.NOUGHT_WON
        # Draw
        for row in self.cells:
            for cell in row:
                if cell.content == Seed.NO_SEED:  # Still blank cells
                    return State.PLAYING
        return State.DRAW  # No blank cells and nobody won

    def paint(self, canvas):
        # Draw grid
        for i in range(1, 4):
            canvas.create_line(0, i*Cell.SIZE, self.CANVAS_HEIGHT,
                               i*Cell.SIZE, fill=self.COLOR_GRID, width=self.GRID_WIDTH)
        for i in range(1, 3):
            canvas.create_line(i*Cell.SIZE, 0, i*Cell.SIZE, self.CANVAS_HEIGHT,
                               fill=self.COLOR_GRID, width=self.GRID_WIDTH)
        for row in self.cells:
            for cell in row:
                cell.paint(canvas)

    def __str__(self) -> str:
        out = ' -------------\n'
        for row in self.cells:
            out += ' | '
            for cell in row:
                out += str(cell) + ' | '
            out += '\n -------------\n'
        return out
