from typing import Optional, List

from Game.directions import Direction
from Game.game_obect_types import GameObjectType, GOCategory
from Graphics.game_object_sprite import GameObjectSprite


class GameObject:
    def __init__(self, playing_level, x: int, y: int, object_type: GameObjectType, direction: Direction):
        self.playing_level = playing_level

        self.x = x
        self.y = y
        self.direction = direction
        self.object_type = object_type

        self._sprite: GameObjectSprite = GameObjectSprite(playing_level.get_tile_grid(), x, y, object_type, direction)

    def get_sprite(self) -> GameObjectSprite:
        return self._sprite

    def copy(self):
        return GameObject(self.playing_level, self.x, self.y, self.object_type, self.direction)

    def set_x(self, x: int):
        self.x = x
        self._sprite.set_x(x)

    def set_y(self, y: int):
        self.y = y
        self._sprite.set_y(y)

    def set_direction(self, d: Direction):
        self.direction = d
        self._sprite.set_direction(d)

    def has_prop(self, prop: GameObjectType) -> bool:
        for rule in self.playing_level.sentences:
            if rule.targets_object(self) and rule.gives_prop(prop):
                return True
        return False

    def get_category(self) -> GOCategory:
        return self.object_type.get_category()

    def is_push(self) -> bool:
        return self.object_type.get_category().is_text() or self.has_prop(GameObjectType.T_PUSH)
