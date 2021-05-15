from math import ceil

import pygame

from Graphics.constants import NON_GRID_BK_COLOR, SPRITE_WIDTH, FPS, WIN_TEXT_LEN, FRAMES_PER_WIN_LETTER, \
    WIN_LETTER_APPEARS, WIN_LETTER_FRAMES, SCREEN_WASH_FRAMES, WIN_TEXT, WIN_END_WAIT, LEVEL_NAME_WAIT, SMALL_WAIT
from Graphics.text_sprite import TextSprite
from Graphics.tile_grid import TileGrid


class MainWindow:
    def __init__(self):
        self.screen = pygame.display.set_mode((160 * 6, 90 * 6), pygame.RESIZABLE)
        pygame.display.set_caption("Baba Is Clone")
        self.playing_level = None
        self.win_counter = -1
        self.fade_in_counter = -1
        self.win_text = None

    SCREEN_WASH_CIRCLES = [
        # top triple
        lambda w, h: ((w * .5, -w * .3), (w * .5, h * .55 - w * .15), w * .3),
        lambda w, h: ((w * .35, -w * .17), (w * .4, h * .5 - w * .1), w * .1),
        lambda w, h: ((w * .65, -w * .17), (w * .6, h * .5 - w * .1), w * .1),

        # bottom triple
        lambda w, h: ((w * .5, h + w * .3), (w * .5, h * .45 + w * .15), w * .3),
        lambda w, h: ((w * .35, h + w * .17), (w * .4, h * .5 + w * .1), w * .1),
        lambda w, h: ((w * .65, h + w * .17), (w * .6, h * .5 + w * .1), w * .1),

        # left pair
        lambda w, h: ((-h * .8, h * (.5 - .18)), (w * .4, h * .45), h * .25),
        lambda w, h: ((-h * .8, h * (.5 + .18)), (w * .4, h * .55), h * .25),

        # right pair
        lambda w, h: ((w + h * .8, h * (.5 - .18)), (w * .6, h * .45), h * .25),
        lambda w, h: ((w + h * .8, h * (.5 + .18)), (w * .6, h * .55), h * .25),

        # top left
        lambda w, h: ((w * .2, -h * .6), (w * .3, h * .4), h * .25),
        lambda w, h: ((w * .1, -h * .6), (w * .2, h * .4), h * .25),
        lambda w, h: ((w * -.25, -h * .05), (w * .3, h * .3), h * .25),

        # top right
        lambda w, h: ((w - w * .2, -h * .6), (w * .7, h * .4), h * .25),
        lambda w, h: ((w - w * .1, -h * .6), (w * .8, h * .4), h * .25),
        lambda w, h: ((w + w * .25, -h * .05), (w * .7, h * .3), h * .25),

        # bottom left
        lambda w, h: ((w * .2, h + h * .6), (w * .3, h * .6), h * .25),
        lambda w, h: ((w * .1, h + h * .6), (w * .2, h * .6), h * .25),
        lambda w, h: ((w * -.25, h + h * .05), (w * .3, h * .7), h * .25),

        # bottom right
        lambda w, h: ((w - w * .2, h + h * .6), (w * .7, h * .6), h * .25),
        lambda w, h: ((w - w * .1, h + h * .6), (w * .8, h * .6), h * .25),
        lambda w, h: ((w + w * .25, h + h * .05), (w * .7, h * .7), h * .25),
    ]

    def draw_grid(self) -> None:
        self.screen.fill(NON_GRID_BK_COLOR)
        if self.playing_level is not None:
            self.playing_level.get_tile_grid().set_scale_factor(self.find_max_resize())
            draw_rect = self.playing_level.get_tile_grid().get_rect()
            draw_rect.center = self.screen.get_rect().center
            self.playing_level.get_tile_grid().draw_onto(self.screen, draw_rect)
            self.draw_win_animation()
            self.draw_fade_in()

    def draw_win_animation(self):
        if self.win_counter >= 0:
            if self.win_counter == 0: self.win_text = TextSprite(" ", self.find_max_resize())

            # screen wash
            if self.win_counter > WIN_LETTER_FRAMES:
                wash_count = self.win_counter - WIN_LETTER_FRAMES
                percent = wash_count / SCREEN_WASH_FRAMES
                self.draw_screen_wash(percent)

            # open congratulations
            if self.win_counter < WIN_LETTER_FRAMES:
                letters_appeared = self.win_counter // FRAMES_PER_WIN_LETTER
                center_letter = WIN_LETTER_APPEARS - 1
                win_text = WIN_TEXT[center_letter-letters_appeared:center_letter+letters_appeared+1]
                self.win_text.set_text(win_text)
            elif WIN_LETTER_FRAMES + SCREEN_WASH_FRAMES < self.win_counter:
                frame_count = self.win_counter - (WIN_LETTER_FRAMES + SCREEN_WASH_FRAMES)
                letters_appeared = (WIN_LETTER_FRAMES - frame_count) // FRAMES_PER_WIN_LETTER
                center_letter = WIN_LETTER_APPEARS - 1
                win_text = WIN_TEXT[center_letter-letters_appeared:center_letter+letters_appeared+1]
                self.win_text.set_text(f" {win_text} ")

            self.win_text.set_scale(self.find_max_resize())
            self.win_text.draw_centered(self.screen, self.screen.get_rect())
            self.win_text.update()

            if self.win_counter < WIN_LETTER_FRAMES + SCREEN_WASH_FRAMES + WIN_LETTER_FRAMES + WIN_END_WAIT:
                self.win_counter += 1
            else:
                self.win_counter = -2

    def draw_fade_in(self):
        if self.fade_in_counter >= 0:
            if self.fade_in_counter == 0: self.win_text = TextSprite(" ", self.find_max_resize())

            LEVEL_NAME = self.playing_level.level_name
            NAME_TEXT_LEN = len(LEVEL_NAME)
            NAME_LETTER_APPEARS = int(ceil(NAME_TEXT_LEN / 2))
            NAME_LETTER_FRAMES = int(FRAMES_PER_WIN_LETTER * NAME_LETTER_APPEARS)

            if self.fade_in_counter > NAME_LETTER_FRAMES * 2 + LEVEL_NAME_WAIT + SMALL_WAIT:
                percent = 1 - ((self.fade_in_counter - NAME_LETTER_FRAMES * 2 - LEVEL_NAME_WAIT - SMALL_WAIT) / SCREEN_WASH_FRAMES)
                self.draw_screen_wash(percent)
            else:
                self.screen.fill(NON_GRID_BK_COLOR)

            if self.fade_in_counter < NAME_LETTER_FRAMES:
                letters_appeared = self.fade_in_counter // FRAMES_PER_WIN_LETTER
                center_letter = NAME_LETTER_APPEARS - 1
                name_text = LEVEL_NAME[center_letter-letters_appeared:center_letter+letters_appeared+1]
                self.win_text.set_text(name_text)
            elif (NAME_LETTER_FRAMES + LEVEL_NAME_WAIT <= self.fade_in_counter
                  < NAME_LETTER_FRAMES * 2 + LEVEL_NAME_WAIT):
                frame_count = self.fade_in_counter - NAME_LETTER_FRAMES - LEVEL_NAME_WAIT
                letters_appeared = (NAME_LETTER_FRAMES - 1 - frame_count) // FRAMES_PER_WIN_LETTER
                center_letter = NAME_LETTER_APPEARS - 1
                name_text = LEVEL_NAME[center_letter-letters_appeared:center_letter+letters_appeared+1]
                self.win_text.set_text(name_text)
            elif self.fade_in_counter > NAME_LETTER_FRAMES * 2 + LEVEL_NAME_WAIT:
                self.win_text.set_text(" ")

            self.win_text.set_scale(self.find_max_resize())
            self.win_text.draw_centered(self.screen, self.screen.get_rect())
            self.win_text.update()

            if self.fade_in_counter < SCREEN_WASH_FRAMES + NAME_LETTER_FRAMES * 2 + LEVEL_NAME_WAIT + SMALL_WAIT:
                self.fade_in_counter += 1
            else:
                self.fade_in_counter = -1

    def draw_screen_wash(self, percent: float):
        w = self.screen.get_width()
        h = self.screen.get_height()
        for circle in self.SCREEN_WASH_CIRCLES:
            ((x, y), (cx, cy), s) = circle(w, h)
            dx = lerp(x, cx, percent)
            dy = lerp(y, cy, percent)
            pygame.draw.line(self.screen, NON_GRID_BK_COLOR, (int(x), int(y)), (int(dx), int(dy)), int(s))
            pygame.draw.circle(self.screen, NON_GRID_BK_COLOR, (int(dx), int(dy)), int(s) / 2)

    def set_playing_level(self, playing_level) -> None:
        self.fade_in_counter = 0
        self.win_counter = -1
        self.playing_level = playing_level

    def init_win_animation(self):
        self.win_counter = 0

    def find_max_resize(self):
        """
        :return: the maximum scale factor the current window size can accommodate for the tile_grid
        """
        effective_width = (self.playing_level.get_tile_grid().tiles_wide + 1) * SPRITE_WIDTH
        effective_height = (self.playing_level.get_tile_grid().tiles_high + 1) * SPRITE_WIDTH

        max_width_scale_factor = self.screen.get_width() // effective_width
        max_height_scale_factor = self.screen.get_height() // effective_height

        return min(max_width_scale_factor, max_height_scale_factor)


def lerp(s, e, p):
    return s + (e - s) * p
