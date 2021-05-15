from typing import Optional, List

from Game.directions import Direction
from Game.game_obect_types import GameObjectType, GOCategory, GO_CATEGORIES
from Graphics.game_object_sprite import GameObjectSprite


class GameObject:
    def __init__(self, playing_level, x: int, y: int, object_type: GameObjectType, direction: Direction):
        self.playing_level = playing_level
        self.x = x
        self.y = y
        self.object_type = object_type
        self._sprite: Optional[GameObjectSprite] = None
        self.direction = direction

    def get_sprite(self) -> GameObjectSprite:
        if self._sprite is None:
            self._sprite = GameObjectSprite(self.playing_level.get_tile_grid(), self.x, self.y, self.object_type,
                                            self.direction)
        return self._sprite

    def copy(self):
        go = GameObject(self.playing_level, self.x, self.y, self.object_type, self.direction)
        go._sprite = None
        return go

    def set_x(self, x):
        self.x = x
        self.get_sprite().set_x(x)

    def set_y(self, y):
        self.y = y
        self.get_sprite().set_y(y)

    def set_direction(self, d: Direction):
        self.direction = d
        self.get_sprite().set_direction(d)

    def has_prop(self, prop: GameObjectType, rules) -> bool:
        for rule in rules:
            if rule.targets_object(self) and rule.gives_prop(prop):
                return True
        return False

    def is_push(self, rules) -> bool:
        return ((GO_CATEGORIES[self.object_type.value] in [GOCategory.NOUN, GOCategory.PROPERTY, GOCategory.VERB]) or
                self.has_prop(GameObjectType.T_PUSH, rules))
