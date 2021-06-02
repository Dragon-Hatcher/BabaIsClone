import sys
from Game.game_obect_types import GameObjectType
from Graphics.color_palette import PALETTE_GROUP_MEMBERSHIP, MUTED_LOCATIONS
from Graphics.load_sprite_triple import load_sprite_triple

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
    GameObjectType.GRASS: (0, 17),
    GameObjectType.WATER: (16, 19),
    GameObjectType.T_WATER: (28, 11),
    GameObjectType.T_SINK: (9, 14),
    GameObjectType.SKULL: [(8, 5), (9, 5), (10, 5), (11, 5)],
    GameObjectType.T_SKULL: (16, 11),
    GameObjectType.T_DEFEAT: (5, 13),
    GameObjectType.LAVA: (16, 19),
    GameObjectType.T_LAVA: (24, 10),
    GameObjectType.T_HOT: (12, 13),
    GameObjectType.T_MELT: (14, 13),
}


X_LOC = (25, 8)


def get_sprites_for(go_type, direction, state, palette, muted=False):
    loc = get_sprite_loc(go_type, direction, state)
    if not muted:
        color = palette[PALETTE_GROUP_MEMBERSHIP[go_type]]
    else:
        group = PALETTE_GROUP_MEMBERSHIP[go_type]
        if group not in MUTED_LOCATIONS:
            color = palette[group]
            print(f"WARNING: group {group} not in MUTED_LOCATIONS", file=sys.stderr)
        else:
            color = palette[MUTED_LOCATIONS[group]]
    return load_sprite_triple(loc, color)


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


def get_sprites_for_tiled(go_type, e, n, w, s, palette):
    loc = tiled_sprite_loc(go_type, e, n, w, s)
    color = palette[PALETTE_GROUP_MEMBERSHIP[go_type]]
    return load_sprite_triple(loc, color)


def tiled_sprite_loc(go_type, e, n, w, s):
    offset = 0 | e | (n << 1) | (w << 2) | (s << 3)
    table = GO_SPRITE_LOCS[go_type]
    return table[0] + offset, table[1]
