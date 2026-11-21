from enum import Enum

class GameMode(str, Enum):
    CLASSIC = "classic"
    TIME_ATTACK = "time_attack"
    HARDCORE = "hardcore"