import pygame
from typing import List

from Graphics.constants import SPRITE_WIDTH, WOBBLE_COUNT
from Graphics.spritesheet import SpriteSheet

sprite_sheet = None


def load_sprite_triple(xy) -> List[pygame.Surface]:
    """
    Returns a list containing the animation images for that sprite.
    :param xy: the xy coordinates of the sprite to load in columns and rows not pixels
    :return:
    """
    global sprite_sheet
    if sprite_sheet is None:
        sprite_sheet = SpriteSheet("Graphics/sprites.png")

    rectangles = [pygame.Rect(xy[0] * SPRITE_WIDTH,
                              xy[1] * SPRITE_WIDTH * WOBBLE_COUNT + rect_num * SPRITE_WIDTH,
                              SPRITE_WIDTH,
                              SPRITE_WIDTH)
                  for rect_num in range(WOBBLE_COUNT)]
    images = [sprite_sheet.image_at(rect) for rect in rectangles]
    return images
