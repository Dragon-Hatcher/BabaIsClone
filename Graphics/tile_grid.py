from math import floor
from typing import List, Optional
import pygame
from Game.game_obect_types import GameObjectType
from Graphics.color_palette import get_palette, PaletteGroups
from Graphics.constants import SPRITE_WIDTH, FPS, WOBBLE_COUNT
from Graphics.game_object_sprite import GameObjectSprite
from Graphics.go_sprite_loc import X_LOC
from Graphics.load_sprite_triple import load_sprite_triple


class TileGrid(pygame.sprite.Sprite):

    def __init__(self, theme: str, tiles_wide: int, tiles_high: int):
        super(TileGrid, self).__init__()
        self.theme = theme
        self.tiles_wide = tiles_wide
        self.tiles_high = tiles_high
        self.gos: List[GameObjectSprite] = []
        self.gosGroup = pygame.sprite.Group()
        self.scale_factor: Optional[int] = None
        self.xs = load_sprite_triple(X_LOC, get_palette(theme)[PaletteGroups.XS])
        self.x_image = None
        self.wobble_index = 0
        self.set_scale_factor(1)

    def update(self) -> None:
        self.wobble_index += 1 / FPS * WOBBLE_COUNT
        if self.wobble_index >= len(self.xs):
            self.wobble_index = 0
        self.x_image = self.xs[floor(self.wobble_index)]
        self.gosGroup.update()

    def set_scale_factor(self, scale_factor: int) -> None:
        if self.scale_factor != scale_factor:
            self.scale_factor = scale_factor
            self.rect = self.get_rect()
            for go in self.gos:
                go.set_scale(scale_factor)
            for (index, x) in enumerate(self.xs):
                self.xs[index] = pygame.transform.scale(x, (SPRITE_WIDTH * scale_factor, SPRITE_WIDTH * scale_factor))

    def draw_onto(self, onto: pygame.Surface, where: pygame.Rect) -> None:
        self.rect.center = where.center
        pygame.draw.rect(onto, get_palette(self.theme)[PaletteGroups.BK_COLOR], self.rect)
        for go in self.gos:
            if go.object_type.is_tiled():
                go.update_tiled()
            go.draw_onto(onto, where)

    def get_rect(self) -> pygame.Rect:
        adjusted_sprite_width = SPRITE_WIDTH * self.scale_factor
        return pygame.Rect(0,
                           0,
                           self.tiles_wide * adjusted_sprite_width,
                           self.tiles_high * adjusted_sprite_width)

    def add_go(self, go: GameObjectSprite) -> None:
        self.gos.append(go)
        self.gosGroup.add(go)

    def remove_go(self, go: GameObjectSprite) -> None:
        self.gos.remove(go)
        self.gosGroup.remove(go)
        go.kill()

    def set_gos(self, gos: List[GameObjectSprite]) -> None:
        for go in self.gosGroup:
            go.kill()
        self.gos = gos
        self.gosGroup = pygame.sprite.Group(gos)

    def increase_go_draw_priority(self, go: GameObjectSprite):
        self.gos.remove(go)
        self.gos.append(go)

    def type_at(self, x, y, t: GameObjectType) -> bool:
        for go in self.gos:
            if go.grid_x == x and go.grid_y == y and go.object_type == t:
                return True
        return False
