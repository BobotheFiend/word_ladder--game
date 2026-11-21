from enum import Enum


class Status(str, Enum):
    IN_PROGRESS = "in_progress"
    WON = "won"
    LOST = "lost"
    TIME_UP = "time_up"
    NO_MOVES_LEFT = "no_moves_left"
    LAND_OF_NO_RETURN = "land_of_no_return"
