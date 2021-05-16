from math import floor

import pygame

from Game.directions import Direction
from Game.game_obect_types import GameObjectType, TILED_OBJECTS
from Graphics.color_palette import get_palette
from Graphics.go_sprite_loc import get_sprites_for, get_sprites_for_tiled
from Graphics.constants import SPRITE_WIDTH, FPS, WOBBLE_COUNT, SLIDE_FRAMES


class GameObjectSprite(pygame.sprite.Sprite):
    def __init__(self, grid, grid_x: int, grid_y: int, go_type: GameObjectType, direction: Direction):
        super(GameObjectSprite, self).__init__()

        self.grid = grid
        self.grid_x = grid_x
        self.grid_y = grid_y

        self.go_type = go_type
        self.direction = direction

        self.old_x = grid_x
        self.old_y = grid_y
        self.slide_time = 0
        self.muted = False

        self.object_type = go_type

        self.images = get_sprites_for(go_type, direction, 0, get_palette(self.grid.theme))
        self.set_scale(grid.scale_factor)

        if self.object_type in TILED_OBJECTS:
            self.update_tiled()

        self.wobble_index = 0
        self.image = self.images[self.wobble_index]

    def _update_images(self):
        self.images = get_sprites_for(self.go_type, self.direction, 0, get_palette(self.grid.theme), self.muted)
        self.set_scale(self.grid.scale_factor)

    def set_muted(self, muted):
        if muted != self.muted:
            self.muted = muted
            self._update_images()

    def update_tiled(self):
        e = self.grid.type_at(self.grid_x + 1, self.grid_y - 0, self.object_type)
        n = self.grid.type_at(self.grid_x + 0, self.grid_y - 1, self.object_type)
        w = self.grid.type_at(self.grid_x - 1, self.grid_y + 0, self.object_type)
        s = self.grid.type_at(self.grid_x - 0, self.grid_y + 1, self.object_type)
        self.images = get_sprites_for_tiled(self.object_type, e, n, w, s, get_palette(self.grid.theme))
        self.set_scale(self.grid.scale_factor)

    def update(self) -> None:
        self.wobble_index += 1 / FPS * WOBBLE_COUNT
        if self.wobble_index >= len(self.images):
            self.wobble_index = 0
        self.image = self.images[floor(self.wobble_index)]
        if self.slide_time > 1:
            self.slide_time -= 1
        else:
            self.slide_time = 0

    def set_scale(self, size: int) -> None:
        for (index, image) in enumerate(self.images):
            self.images[index] = pygame.transform.scale(image, (SPRITE_WIDTH * size, SPRITE_WIDTH * size))

    def draw_onto(self, onto: pygame.Surface, where: pygame.Rect) -> None:
        sprite_size = SPRITE_WIDTH * self.grid.scale_factor
        slide_percent = self.slide_time / SLIDE_FRAMES
        rect = pygame.Rect(where.left + lerp(self.old_x, self.grid_x, slide_percent) * sprite_size,
                           where.top + lerp(self.old_y, self.grid_y, slide_percent) * sprite_size,
                           sprite_size, sprite_size)
        onto.blit(self.image, rect)

    def set_direction(self, d: Direction):
        self.direction = d
        self._update_images()

    def set_x(self, x: int):
        self.old_x = self.grid_x
        self.grid_x = x
        self.slide_time = SLIDE_FRAMES

    def set_y(self, y: int):
        self.old_y = self.grid_y
        self.grid_y = y
        self.slide_time = SLIDE_FRAMES


def lerp(old, new, slide_time) -> float:
    return old + (new - old) * (1 - slide_time)