from enum import Enum
from typing import Optional


class GOCategory(Enum):
    OBJECT = 0
    NOUN = 1
    VERB = 2
    PROPERTY = 3


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

    def get_category(self) -> GOCategory:
        v = self.value
        return GO_CATEGORIES[v]


def type_from_string(name: str) -> Optional[GameObjectType]:
    try:
        return eval(f"GameObjectType.{name}")
    except AttributeError:
        return None


GO_CATEGORIES = [
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
]

TEXT_REFERRALS = {
    GameObjectType.T_BABA: GameObjectType.BABA,
    GameObjectType.T_WALL: GameObjectType.WALL,
    GameObjectType.T_ROCK: GameObjectType.ROCK,
    GameObjectType.T_FLAG: GameObjectType.FLAG,
}

TILED_OBJECTS = {
    GameObjectType.WALL
}