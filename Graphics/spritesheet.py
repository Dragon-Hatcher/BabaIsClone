from typing import Tuple, List, Optional
import pygame


class SpriteSheet:

    def __init__(self, filename):
        """Load the sheet."""
        try:
            self.sheet = pygame.image.load(filename).convert_alpha()
        except pygame.error as e:
            print(f"Unable to load spritesheet image: {filename}")
            raise SystemExit(e)

    def image_at(self, rectangle: pygame.Rect) -> pygame.Surface:
        """Load a specific image from a specific rectangle."""
        rect = pygame.Rect(rectangle)
        image = pygame.Surface(rect.size, pygame.SRCALPHA).convert_alpha()
        image.blit(self.sheet, (0, 0), rect)
        return image

    PALLETS_START = (488, 24)
    SWATCH_SIZE = 8
    PALETTE_SIZE = (7, 5)
    GAP_SIZE = (16, 26)

    def get_palette_colors(self, x, y) -> List[List[Tuple[int, int, int]]]:
        loc = (self.PALLETS_START[0] + x * (self.PALETTE_SIZE[0] * self.SWATCH_SIZE + self.GAP_SIZE[0]),
               self.PALLETS_START[1] + y * (self.PALETTE_SIZE[1] * self.SWATCH_SIZE + self.GAP_SIZE[1]))

        ret: List[List[Optional[Tuple[int, int, int]]]] \
            = [[None for _ in range(self.PALETTE_SIZE[0])] for _ in range(self.PALETTE_SIZE[0])]
        for sx in range(self.PALETTE_SIZE[0]):
            for sy in range(self.PALETTE_SIZE[1]):
                pix_loc = (loc[0] + sx * self.SWATCH_SIZE + self.SWATCH_SIZE - 1,
                           loc[1] + sy * self.SWATCH_SIZE + self.SWATCH_SIZE - 1)
                col = self.sheet.get_at(pix_loc)
                ret[sx][sy] = col[0], col[1], col[2]
        return ret
