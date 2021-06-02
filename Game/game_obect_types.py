from enum import Enum
from typing import Optional


class GOCategory(Enum):
    OBJECT = 0
    NOUN = 1
    VERB = 2
    PROPERTY = 3

    def is_text(self) -> bool:
        return self == GOCategory.NOUN or self == GOCategory.VERB or self == GOCategory.PROPERTY


class GameObjectType(Enum):
    BABA = 0
    T_BABA = 1
    T_IS = 2
    T_YOU = 3
    WALL = 4
    T_WALL = 5
    ROCK = 6
    T_ROCK = 7
    TILE = 8
    T_TILE = 9
    FLAG = 10
    T_FLAG = 11
    T_WIN = 12
    T_PUSH = 13
    T_STOP = 14
    GRASS = 15
    WATER = 16
    T_WATER = 17
    T_SINK = 18
    SKULL = 19
    T_SKULL = 20
    T_DEFEAT = 21
    LAVA = 22
    T_LAVA = 23
    T_HOT = 24
    T_MELT = 25

    def get_category(self) -> GOCategory:
        return _GO_CATEGORIES[self.value]

    def object_referral(self):
        return _TEXT_REFERRALS.get(self, None)

    def is_tiled(self) -> bool:
        return self in _TILED_OBJECTS


def type_from_string(name: str) -> Optional[GameObjectType]:
    try:
        return eval(f"GameObjectType.{name}")
    except AttributeError:
        return None


_GO_CATEGORIES = [
    GOCategory.OBJECT,  # BABA
    GOCategory.NOUN,  # T_BABA
    GOCategory.VERB,  # T_IS
    GOCategory.PROPERTY,  # T_YOU
    GOCategory.OBJECT,  # WALL
    GOCategory.NOUN,  # T_WALL
    GOCategory.OBJECT,  # ROCK
    GOCategory.NOUN,  # T_ROCK
    GOCategory.OBJECT,  # TILE
    GOCategory.NOUN,  # T_TILE
    GOCategory.OBJECT,  # FLAG
    GOCategory.NOUN,  # T_FLAG
    GOCategory.PROPERTY,  # T_WIN
    GOCategory.PROPERTY,  # T_PUSH
    GOCategory.PROPERTY,  # T_STOP
    GOCategory.OBJECT,  # GRASS
    GOCategory.OBJECT,  # WATER
    GOCategory.NOUN,  # T_WATER
    GOCategory.PROPERTY,  # T_SINK
    GOCategory.OBJECT,  # SKULL
    GOCategory.NOUN,  # T_SKULL
    GOCategory.PROPERTY,  # T_DEFEAT
    GOCategory.OBJECT,  # LAVA
    GOCategory.NOUN,  # T_LAVA
    GOCategory.PROPERTY,  # T_HOT
    GOCategory.PROPERTY,  # T_MELT
]

_TEXT_REFERRALS = {
    GameObjectType.T_BABA: GameObjectType.BABA,
    GameObjectType.T_WALL: GameObjectType.WALL,
    GameObjectType.T_ROCK: GameObjectType.ROCK,
    GameObjectType.T_FLAG: GameObjectType.FLAG,
    GameObjectType.T_WATER: GameObjectType.WATER,
    GameObjectType.T_SKULL: GameObjectType.SKULL,
    GameObjectType.T_LAVA: GameObjectType.LAVA,
}

_TILED_OBJECTS = {
    GameObjectType.WALL,
    GameObjectType.GRASS,
    GameObjectType.WATER,
    GameObjectType.LAVA,
}
