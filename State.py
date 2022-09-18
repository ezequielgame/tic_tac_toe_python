from enum import Enum


class State(Enum):
    """
    The enum State contains the various game states of the TTT game
    """
    PLAYING = 0
    DRAW = 1
    CROSS_WON = 2
    NOUGHT_WON = 3
