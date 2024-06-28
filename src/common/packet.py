import enum


class PacketType(enum.Enum):
    PLAYER_ID = enum.auto()
    GRID_STATE = enum.auto()
    PLAYER_MOVE = enum.auto()
    GAME_OVER = enum.auto()
