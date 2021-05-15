from Game.game_obect_types import GameObjectType

"""
First list = directions
Second List = animation states
"""
GO_SPRITE_LOCS = {
    GameObjectType.BABA: [
        [(1, 0), (2, 0), (3, 0), (4, 0), (0, 0)],
        [(6, 0), (7, 0), (8, 0), (9, 0), (5, 0)],
        [(11, 0), (12, 0), (13, 0), (14, 0), (10, 0)],
        [(16, 0), (17, 0), (18, 0), (19, 0), (15, 0)],
    ],
    GameObjectType.T_BABA: (6, 9),
    GameObjectType.T_IS: (18, 10),
    GameObjectType.T_YOU: (20, 14),
    GameObjectType.WALL: (0, 19),
    GameObjectType.T_WALL: (27, 11),
    GameObjectType.ROCK: (15, 7),
    GameObjectType.T_ROCK: (11, 11),
    GameObjectType.TILE: (19, 7),
    GameObjectType.T_TILE: (22, 11),
    GameObjectType.FLAG: (6, 7),
    GameObjectType.T_FLAG: (1, 10),
    GameObjectType.T_WIN: (17, 14),
    GameObjectType.T_PUSH: (2, 14),
    GameObjectType.T_STOP: (12, 14),
}


def get_sprite_loc(go_type, direction, state) -> (int, int):
    table = GO_SPRITE_LOCS[go_type]
    if isinstance(table, list):
        directions = table[direction.value]
        if isinstance(directions, list):
            return directions[state]
        else:
            return directions
    else:
        return table


def tiled_sprite_loc(go_type, e, n, w, s):
    offset = 0 | e | (n << 1) | (w << 2) | (s << 3)
    table = GO_SPRITE_LOCS[go_type]
    return table[0] + offset, table[1]
