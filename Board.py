from email import message
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
    STATUS_BAR_HEIGHT = 50
    STATUS_BAR_OFFSET = STATUS_BAR_HEIGHT / 2

    # COLOR_GRID:int  =
    Y_OFFSET: int = 1

    COLOR_BG = 'white'
    COLOR_GRID = 'gray'

    cells: list
    seeds: list
    message: int

    def __init__(self) -> None:
        self.init_game()

    def init_game(self) -> None:
        self.seeds = []
        self.cells = [[Cell(i, j) for j in range(self.COLS)]
                      for i in range(self.ROWS)]

    def new_game(self) -> None:
        for row in self.cells:
            for cell in row:
                cell.new_game()

    def step_game(self, player, row, col, canvas, turn) -> State:
        self.cells[row][col].content = player
        self.clean(canvas)
        self.paint(canvas, False,"{}'s Turn: {}".format('X' if player == Seed.NOUGHT else 'O', turn + 1))
        # Only the player can win in the row / col / diag of the move
        rival = Seed.CROSS if player == Seed.NOUGHT else Seed.NOUGHT
        # Assume the win
        winner = True
        # No rival or blank in row
        for cell in self.cells[row]:
            winner = winner and cell.content != rival and cell.content != Seed.NO_SEED
        if winner:
            return State.CROSS_WON if player == Seed.CROSS else State.NOUGHT_WON
        # Not in column
        winner = True
        for board_row in self.cells:
            cell = board_row[col]
            winner = winner and cell.content != rival and cell.content != Seed.NO_SEED
        if winner:
            return State.CROSS_WON if player == Seed.CROSS else State.NOUGHT_WON
        # In main diagonal?
        if row == col:
            winner = True
            for i, board_row in enumerate(self.cells):
                for j, cell in enumerate(board_row):
                    if i == j:
                        winner = winner and cell.content != rival and cell.content != Seed.NO_SEED
            if winner:
                return State.CROSS_WON if player == Seed.CROSS else State.NOUGHT_WON
        # In the other diagonal?
        if row + col == self.ROWS - 1:
            winner = True
            for i, board_row in enumerate(self.cells):
                for j, cell in enumerate(board_row):
                    if i + j == self.ROWS - 1:
                        winner = winner and cell.content != rival and cell.content != Seed.NO_SEED
            if winner:
                return State.CROSS_WON if player == Seed.CROSS else State.NOUGHT_WON
        for board_row in self.cells:
            for cell in board_row:
                if cell.content == Seed.NO_SEED:
                    return State.PLAYING
        return State.DRAW

    def paint(self, canvas, init=True, msg='Click to Play'):
        # Draw grid
        if init:
            for i in range(1, 4):
                canvas.create_line(0, i*Cell.SIZE, self.CANVAS_HEIGHT,
                                i*Cell.SIZE, fill=self.COLOR_GRID, width=self.GRID_WIDTH)
            for i in range(1, 3):
                canvas.create_line(i*Cell.SIZE, 0, i*Cell.SIZE, self.CANVAS_HEIGHT,
                                fill=self.COLOR_GRID, width=self.GRID_WIDTH)
        for row in self.cells:
            for cell in row:
                cell.paint(canvas)
        self.message = canvas.create_text(Board.CANVAS_WIDTH / 2, Board.CANVAS_HEIGHT + self.STATUS_BAR_OFFSET, fill="darkblue",text=msg)
                
    def clean(self, canvas):
        for seed_id in self.seeds:
            canvas.delete(seed_id)
        canvas.delete(self.message)
        
    def repaint(self, canvas, msg='Click to play'):
        self.clean(canvas)
        self.paint(canvas, False, msg)

    def __str__(self) -> str:
        out = ' -------------\n'
        for row in self.cells:
            out += ' | '
            for cell in row:
                out += str(cell) + ' | '
            out += '\n -------------\n'
        return out
