import string
from math import floor
import pygame
from Graphics.constants import FPS, WOBBLE_COUNT, SPRITE_WIDTH, TEXT_SQUISH, TEXT_WOBBLE_TIME
from Graphics.load_sprite_triple import load_sprite_triple


class TextSprite(pygame.sprite.Sprite):
    def __init__(self, text: string, scale: int):
        super(TextSprite, self).__init__()

        self.text = text
        self.set_text(text)
        self.scale = scale

        self.images = [get_letter_triple(c) for c in text]
        self.set_scale(scale)

        self.wobble_index = 0

    def update(self) -> None:
        self.wobble_index += 1 / (FPS * TEXT_WOBBLE_TIME) * WOBBLE_COUNT
        if self.wobble_index >= len(self.images[0]):
            self.wobble_index = 0

    def set_scale(self, size: int) -> None:
        self.scale = size
        for (index, image) in enumerate(self.images):
            self.images[index][0] = pygame.transform.scale(image[0], (SPRITE_WIDTH * size, SPRITE_WIDTH * size))
            self.images[index][1] = pygame.transform.scale(image[1], (SPRITE_WIDTH * size, SPRITE_WIDTH * size))
            self.images[index][2] = pygame.transform.scale(image[2], (SPRITE_WIDTH * size, SPRITE_WIDTH * size))

    def set_text(self, text: string):
        self.text = text
        self.images = [get_letter_triple(c) for c in text]

    def draw_centered(self, onto: pygame.Surface, where: pygame.Rect):
        rect = self.get_rect()
        rect.center = where.center
        self.draw_onto(onto, rect)

    def draw_onto(self, onto: pygame.Surface, where: pygame.Rect) -> None:
        y = where.top
        x = where.left
        step = SPRITE_WIDTH * TEXT_SQUISH * self.scale
        for image in self.images:
            onto.blit(image[floor(self.wobble_index)], pygame.Rect(x, y, step, step))
            x += step

    def width(self):
        return SPRITE_WIDTH * TEXT_SQUISH * self.scale * len(self.text)

    def get_rect(self):
        return pygame.Rect(
            0,
            0,
            self.width(),
            SPRITE_WIDTH * self.scale
        )


def get_letter_triple(letter: string):
    return load_sprite_triple(LETTER_SPRITE_LOCS[letter.upper()], (255, 255, 255))


LETTER_SPRITE_LOCS = {
    "A": (0, 12),
    "B": (1, 12),
    "C": (2, 12),
    "D": (3, 12),
    "E": (4, 12),
    "F": (5, 12),
    "G": (6, 12),
    "H": (7, 12),
    "I": (8, 12),
    "L": (9, 12),
    "M": (10, 12),
    "N": (11, 12),
    "O": (12, 12),
    "R": (13, 12),
    "S": (14, 12),
    "T": (15, 12),
    "U": (16, 12),
    "V": (17, 12),
    "W": (18, 12),
    "X": (19, 12),
    "Y": (23, 8),
    " ": (16, 4),
    "?": (3, 8)
}
