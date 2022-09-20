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
    ROWS: int = 3 # Filas
    COLS: int = 3 # columnas

    # Propiedades de la interfaz grafica, se estan definiendo apenas
    CANVAS_WIDTH: int = Cell.SIZE * COLS # ancho de la ventana
    CANVAS_HEIGHT: int = Cell.SIZE * ROWS # el largo
    GRID_WIDTH: int = 8 # ancho de las lineas
    STATUS_BAR_HEIGHT = 50 # Altura de la barra que muestra mensajes
    STATUS_BAR_OFFSET = STATUS_BAR_HEIGHT / 2 # Para colocar el texto al centro

    Y_OFFSET: int = 1

    # Color de las lineas
    COLOR_GRID = 'gray'

    cells: list # Las celdas del tablero
    seeds: list # Contienen los ids de los objetos creados con Tkinter en el canvas
    message: int # El id del objeto que muestra el mensaje en la status bar

    # Se crea el tablero
    def __init__(self) -> None:
        # Inicias el juego
        self.init_game()

    def init_game(self) -> None:
        self.seeds = [] # Inicializas la lista de id de objetos tkinter
        # List comprenhension para crear las Cell
        self.cells = [[Cell(i, j) for j in range(self.COLS)] for i in range(self.ROWS)]
        
    def new_game(self) -> None:
        # Reiniciar el juego
        for row in self.cells:
            for cell in row:
                cell.new_game() # La celda se limpia sola

    # tira un jugador
    def step_game(self, player, row, col, canvas, turn) -> State:
        # acutalizas el tablero (la celda donde tiro)
        self.cells[row][col].content = player
        # Limipas y vuelves a mostar el tablero en la intefaz grafica
        self.clean(canvas)
        # El FALSE no pinta de nuevo las lineas (rejilla del tablero)
        self.paint(canvas, False,"{}'s Turn: {}".format('X' if player == Seed.NOUGHT else 'O', turn + 1))
        
        # Check winner
        # Only the player can win in the row / col / diag of the move
        rival = Seed.CROSS if player == Seed.NOUGHT else Seed.NOUGHT
        # Assume the win
        winner = True
        # No rival or blank in row
        # self.cells = [(0)[(0)1,(1)2,(2)3], (1)[4,5,6], (2)[7,8,9]]
        # [X,X,X]
        # 1 Celda) True AND X != rival AND X != ' ' ->> True
        # 1 Celda) True AND X != rival AND X != ' ' ->> True
        # 1 Celda) True AND X != rival AND X != ' ' ->> True
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
        # Search blank cells, i.e. continue playing
        for board_row in self.cells:
            for cell in board_row:
                if cell.content == Seed.NO_SEED:
                    return State.PLAYING
        # No win, no more blank cells
        return State.DRAW

    def paint(self, canvas, init=True, msg='Click to Play'):
        if init:
            # Draw grid
            # rows
            # 1,2,3
            for i in range(1, 4):
                canvas.create_line(0, i*Cell.SIZE, self.CANVAS_HEIGHT,
                                i*Cell.SIZE, fill=self.COLOR_GRID, width=self.GRID_WIDTH)
            # cols
            for i in range(1, 3):
                canvas.create_line(i*Cell.SIZE, 0, i*Cell.SIZE, self.CANVAS_HEIGHT,
                                fill=self.COLOR_GRID, width=self.GRID_WIDTH)
        for row in self.cells:
            for cell in row:
                cell.paint(canvas)
        self.message = canvas.create_text(Board.CANVAS_WIDTH / 2, Board.CANVAS_HEIGHT + self.STATUS_BAR_OFFSET, fill="darkblue",text=msg)
                
    def clean(self, canvas):
        # el id del objeto tkinter creado (X O)
        for seed_id in self.seeds:
            canvas.delete(seed_id) # Eliminas del canvas
        canvas.delete(self.message) # Eliminas el mensaje
        
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
