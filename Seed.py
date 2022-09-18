from enum import Enum


class Seed(Enum):
    """
    This enum is used by:
    1. Player: takes value of CROSS or NOUGHT
    2. Cell content: takes value of CROSS, NOUGHT, or NO_SEED.

    Ideally, we should define two enums with inheritance, which is,
    however, not supported.
    """
    NO_SEED = 2
    CROSS = 3
    NOUGHT = 5
