from Game.directions import Direction
from Game.game_obect_types import type_from_string
from Game.game_object import GameObject
from Game.playing_level import PlayingLevel


def load_level(name: str) -> PlayingLevel:
    file = open(f"Levels/{name}", "r")
    text = file.read().split("\n")
    file.close()

    name_line = text[0]

    size_line = text[1].split("x")
    width, height = int(size_line[0]), int(size_line[1])

    level = PlayingLevel(name_line, width, height)

    objects = text[2:]
    for o in objects:
        parts = o.split(",")
        t, x, y = type_from_string(parts[0]), int(parts[1]), int(parts[2])
        d = Direction.EAST
        if len(parts) > 3:
            d = [Direction.EAST, Direction.NORTH, Direction.WEST, Direction.SOUTH][int(parts[3])]
        if not name: raise Exception()

        level.add_go(GameObject(level, x, y, t, d))

    return level
