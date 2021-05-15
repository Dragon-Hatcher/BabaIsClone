from enum import Enum


class Direction(Enum):
    EAST = 0
    NORTH = 1
    WEST = 2
    SOUTH = 3


def moved_in_direction(x: int, y: int, d: Direction, mag: int = 1) -> (int, int):
    return {
        Direction.EAST: (x + mag, y + 0),
        Direction.NORTH: (x + 0, y - mag),
        Direction.WEST: (x - mag, y + 0),
        Direction.SOUTH: (x + 0, y + mag),
    }[d]
