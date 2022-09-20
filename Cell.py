from Seed import Seed
"""
The Cell class models each individual cell of the game board.
"""


class Cell:
    """
    The Cell class models each individual cell of the game board.
    """
    SIZE: int = 120
    PADDING: float = SIZE / 5
    SEED_SIZE: float = SIZE - PADDING * 2
    SEED_STROKE_WIDTH: int = 8
    COLOR_CROSS: str = 'red'
    COLOR_NOUGHT = 'blue'

    content: Seed
    row: int
    col: int

    def __init__(self, row: int = 0, col: int = 0) -> None:
        """
        Constructor to initialize this cell with the specified row and col

        Parameters
        ----------
        row (int) : Row number in the board
        col (row) : Col number in the board

        """
        self.row = row
        self.col = col
        self.content = Seed.NO_SEED

    def new_game(self) -> None:
        self.content = Seed.NO_SEED

    def paint(self, canvas) -> None:
        x1 = int(self.col * self.SIZE + self.PADDING)
        y1 = int(self.row * self.SIZE + self.PADDING)
        x2 = int((self.col + 1) * self.SIZE - self.PADDING)
        y2 = int((self.row + 1) * self.SIZE - self.PADDING)
        if self.content == Seed.CROSS:
            # Pintar X
            canvas.create_line(
                x1, y1, x2, y2, fill=self.COLOR_CROSS, width=self.SEED_STROKE_WIDTH)
            canvas.create_line(
                x2, y1, x1, y2, fill=self.COLOR_CROSS, width=self.SEED_STROKE_WIDTH)
        elif self.content == Seed.NOUGHT:
            # Pintar donita
            canvas.create_oval(
                x1, y1, x2, y2, outline=self.COLOR_NOUGHT, width=self.SEED_STROKE_WIDTH)

    # to string
    def __str__(self) -> str:
        if self.content == Seed.NOUGHT:
            return 'O'
        elif self.content == Seed.CROSS:
            return 'X'
        else:
            return '_'
