from enum import Enum
from typing import Dict
from Game.game_obect_types import GameObjectType
from Graphics.load_sprite_triple import load_palette


class PaletteGroups(Enum):
    BABA = 0
    VERB = 1
    WIN = 2
    YOU = 3
    ROCK = 4
    WALL = 5
    PUSH = 6
    STOP = 7
    WALL_T = 8
    TILE = 9
    BK_COLOR = 10
    NON_GRID_BK_COLOR = 11
    MUTED_YOU = 12
    MUTED_STOP = 13
    MUTED_PUSH = 14
    XS = 15
    GRASS = 16
    WATER = 17
    MUTED_WATER = 18
    SKULL = 19
    MUTED_SKULL = 20
    LAVA = 21
    MUTED_LAVA = 22

    def get_location(self) -> (int, int):
        return PALETTE_COLOR_LOCATIONS[self]


PALETTE_GROUP_MEMBERSHIP = {
    GameObjectType.BABA:   PaletteGroups.BABA,
    GameObjectType.T_BABA: PaletteGroups.YOU,
    GameObjectType.T_IS:   PaletteGroups.VERB,
    GameObjectType.T_YOU:  PaletteGroups.YOU,
    GameObjectType.WALL:   PaletteGroups.WALL,
    GameObjectType.T_WALL: PaletteGroups.WALL_T,
    GameObjectType.ROCK:   PaletteGroups.ROCK,
    GameObjectType.T_ROCK: PaletteGroups.PUSH,
    GameObjectType.TILE:   PaletteGroups.TILE,
    GameObjectType.T_TILE: PaletteGroups.TILE,
    GameObjectType.FLAG:   PaletteGroups.WIN,
    GameObjectType.T_FLAG: PaletteGroups.WIN,
    GameObjectType.T_WIN:  PaletteGroups.WIN,
    GameObjectType.T_PUSH: PaletteGroups.PUSH,
    GameObjectType.T_STOP: PaletteGroups.STOP,
    GameObjectType.GRASS:  PaletteGroups.GRASS,
    GameObjectType.WATER:  PaletteGroups.WATER,
    GameObjectType.T_WATER: PaletteGroups.WATER,
    GameObjectType.T_SINK: PaletteGroups.WATER,
    GameObjectType.SKULL:  PaletteGroups.SKULL,
    GameObjectType.T_SKULL: PaletteGroups.SKULL,
    GameObjectType.T_DEFEAT: PaletteGroups.SKULL,
    GameObjectType.LAVA: PaletteGroups.LAVA,
    GameObjectType.T_LAVA: PaletteGroups.LAVA,
    GameObjectType.T_HOT: PaletteGroups.LAVA,
    GameObjectType.T_MELT: PaletteGroups.WATER,
}

MUTED_LOCATIONS = {
    PaletteGroups.YOU: PaletteGroups.MUTED_YOU,
    PaletteGroups.VERB: PaletteGroups.WALL_T,
    PaletteGroups.WALL_T: PaletteGroups.WALL,
    PaletteGroups.WIN: PaletteGroups.PUSH,
    PaletteGroups.STOP: PaletteGroups.MUTED_STOP,
    PaletteGroups.PUSH: PaletteGroups.MUTED_PUSH,
    PaletteGroups.WATER: PaletteGroups.MUTED_WATER,
    PaletteGroups.SKULL: PaletteGroups.MUTED_SKULL,
    PaletteGroups.LAVA: PaletteGroups.MUTED_LAVA,
}

PALETTE_COLOR_LOCATIONS = {
    PaletteGroups.BABA:   (0, 3),
    PaletteGroups.VERB:   (0, 3),
    PaletteGroups.WIN:    (2, 4),
    PaletteGroups.YOU:    (4, 1),
    PaletteGroups.ROCK:   (6, 2),
    PaletteGroups.WALL:   (1, 1),
    PaletteGroups.PUSH:   (6, 1),
    PaletteGroups.STOP:   (5, 1),
    PaletteGroups.WALL_T: (0, 1),
    PaletteGroups.TILE:   (0, 0),
    PaletteGroups.BK_COLOR: (0, 4),
    PaletteGroups.NON_GRID_BK_COLOR: (1, 0),
    PaletteGroups.MUTED_YOU: (4, 0),
    PaletteGroups.MUTED_STOP: (5, 0),
    PaletteGroups.MUTED_PUSH: (6, 3),
    PaletteGroups.XS:   (2, 2),
    PaletteGroups.GRASS:  (5, 0),
    PaletteGroups.WATER: (1, 3),
    PaletteGroups.MUTED_WATER: (1, 2),
    PaletteGroups.SKULL: (2, 1),
    PaletteGroups.MUTED_SKULL: (2, 0),
    PaletteGroups.LAVA: (2, 3),
    PaletteGroups.MUTED_LAVA: (2, 2),
}

PALETTES: Dict[str, any] = {}


def init_palettes():
    global PALETTES
    PALETTES = {
        "DEFAULT": load_palette(0, 0),
        "ABSTRACT": load_palette(1, 0),
        "AUTUMN": load_palette(2, 0),
        "CONTRAST": load_palette(3, 0),
        "FACTORY": load_palette(0, 1),
        "GARDEN": load_palette(1, 1),
        "MARSHMALLOW": load_palette(2, 1),
        "MONO": load_palette(3, 1),
        "MOUNTAIN": load_palette(0, 2),
        "OCEAN": load_palette(1, 2),
        "RUINS": load_palette(1, 2),
        "SPACE": load_palette(3, 2),
        "SWAMP": load_palette(0, 3),
        "TEST": load_palette(1, 3),
        "VARIANT": load_palette(2, 3),
        "VOLCANO": load_palette(3, 3),
    }


def get_palette(name="DEFAULT"):
    global PALETTES
    return PALETTES[name]
