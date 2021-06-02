import pygame
from typing import List, Optional, Dict, Tuple
from Graphics.constants import SPRITE_WIDTH, WOBBLE_COUNT
from Graphics.spritesheet import SpriteSheet


sprite_sheet: Optional[SpriteSheet] = None


LOADED_TRIPLES: Dict[Tuple[Tuple[int, int], Tuple[int, int, int]], List[pygame.Surface]] = {}


def load_sprite_triple(xy: (int, int), primary: (int, int, int)) -> List[pygame.Surface]:
    global sprite_sheet
    global LOADED_TRIPLES

    key = (xy, primary)

    if key in LOADED_TRIPLES:
        return LOADED_TRIPLES[key]
    else:
        if sprite_sheet is None:
            sprite_sheet = SpriteSheet("Graphics/sprites.png")

        rectangles = [pygame.Rect(xy[0] * SPRITE_WIDTH,
                                  xy[1] * SPRITE_WIDTH * WOBBLE_COUNT + rect_num * SPRITE_WIDTH,
                                  SPRITE_WIDTH,
                                  SPRITE_WIDTH)
                      for rect_num in range(WOBBLE_COUNT)]
        images = [recolor_image(sprite_sheet.image_at(rect), primary) for rect in rectangles]
        LOADED_TRIPLES[key] = images
        return images


def recolor_image(image: pygame.Surface, primary: (int, int, int)) -> pygame.Surface:
    for x in range(image.get_width()):
        for y in range(image.get_height()):
            color = image.get_at((x, y))
            if color[3] == 255:
                percent = color[0] / 255
                result = (primary[0] * percent, primary[1] * percent, primary[2] * percent)
                image.set_at((x, y), result)
    return image


def load_palette(x, y):
    global sprite_sheet
    if sprite_sheet is None:
        sprite_sheet = SpriteSheet("Graphics/sprites.png")
    colors = sprite_sheet.get_palette_colors(x, y)
    ret = {}
    import Graphics.color_palette as cp
    for g, loc in cp.PALETTE_COLOR_LOCATIONS.items():
        ret[g] = colors[loc[0]][loc[1]]
    return ret
