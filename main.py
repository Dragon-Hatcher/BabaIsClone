import sys
from typing import Optional

import pygame

from Game.game_obect_types import type_from_string
from Game.playing_level import PlayingLevel
from Graphics.constants import FPS
from Graphics.load_level_from_file import load_level
from Graphics.main_window import MainWindow

w: Optional[MainWindow] = None


def main():
    global w

    pygame.init()

    level = load_level("level0.txt")
    w = MainWindow()

    w.set_playing_level(level)

    clock = pygame.time.Clock()

    while True:
        event = pygame.event.poll()
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit(0)
        elif event.type == pygame.KEYDOWN:
            level.receive_input(event.key)

        level.get_tile_grid().update()
        w.draw_grid()
        pygame.display.flip()
        clock.tick(FPS)

        if level.won and w.win_counter == -1:
            w.init_win_animation()
        if w.win_counter == -2:
            level = load_level("level0.txt")
            w.set_playing_level(level)


if __name__ == '__main__':
    main()
