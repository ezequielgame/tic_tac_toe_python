from ArtificialIntelligence import ArtificialIntelligence
from Seed import Seed
from State import State
from Board import Board
from Cell import Cell

from tkinter import Tk, Canvas, Frame, BOTH


class GameMain(Frame):

    board: Board
    current_state: State = State.PLAYING
    turn: int
    person_player: Seed
    ia_player: ArtificialIntelligence
    ia_symbol: Seed
    canvas: Canvas
    current_player: Seed
    TITLE: str = "TicTacToe"
    COLOR_BG_STATUS = 'gray'
    STATUS_BAR_HEIGHT = 50
    STATUS_BAR_OFFSET = STATUS_BAR_HEIGHT / 2

    def __init__(self) -> None:
        super().__init__()
        self.init_game()

    def init_game(self) -> None:
        self.board = Board()
        self.init_ui()
        self.new_game()
        self.canvas.create_text(Board.CANVAS_WIDTH / 2, Board.CANVAS_HEIGHT + self.STATUS_BAR_OFFSET, fill="darkblue",
                                text='Click to start playing')

    def init_ui(self):
        self.master.title(self.TITLE)
        self.pack(fill=BOTH, expand=1)
        self.canvas = Canvas(self)
        self.canvas.pack(fill=BOTH, expand=1)
        self.board.paint(self.canvas)
        self.canvas.bind("<Button-1>", self.play_move)

    def play_move(self, event):
        self.cell_clicked(event)
        if self.current_state != State.PLAYING:
            if self.current_state == State.DRAW:
                self.repaint("It's a Draw! Click to play again.")
            else:
                self.repaint("'X' Won! Click to play again."if self.current_state ==
                             State.CROSS_WON else "'O' Won! Click to play again.")

    def cell_clicked(self, event):
        row, col = int(event.y/Cell.SIZE), int(event.x/Cell.SIZE)
        if self.current_state == State.PLAYING:
            if 0 <= row <= self.board.ROWS and 0 <= col <= self.board.COLS and self.board.cells[row][col].content == Seed.NO_SEED:
                self.current_state = self.board.step_game(
                    self.person_player, row, col)
                self.repaint("{}'s Turn: {}".format('O', self.turn + 1))
                self.turn += 1
                if self.turn < 10:
                    row, col = self.ia_player.think_next_move(
                        self.board.cells, self.turn)
                    self.current_state = self.board.step_game(
                        self.ia_symbol, row, col)
                    self.repaint("{}'s Turn: {}".format('X', self.turn + 1))
                    self.turn += 1
        else:
            self.new_game()

    def new_game(self):
        self.ia_player = ArtificialIntelligence()
        self.board.new_game()
        self.person_player = Seed.CROSS
        self.ia_symbol = Seed.NOUGHT
        self.current_player = self.person_player
        self.turn = 1
        self.current_state = State.PLAYING
        self.canvas.destroy()
        self.init_ui()

    def repaint(self, msg='Click to play'):
        self.current_player = self.person_player if self.current_player == self.ia_player else self.ia_player
        self.canvas.destroy()
        self.init_ui()
        self.canvas.create_text(Board.CANVAS_WIDTH / 2, Board.CANVAS_HEIGHT + self.STATUS_BAR_OFFSET, fill="darkblue",
                                text=msg)
        self.board.paint(self.canvas)


if __name__ == '__main__':
    root = Tk()
    gm = GameMain()
    root.geometry("{}x{}".format(gm.board.CANVAS_WIDTH,
                  gm.board.CANVAS_HEIGHT + gm.STATUS_BAR_HEIGHT))
    root.resizable(False, False)
    root.mainloop()
