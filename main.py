import sys
from typing import Optional
import pygame

from Game.directions import Direction
from Game.game_obect_types import GameObjectType
from Game.game_object import GameObject
from Graphics.color_palette import init_palettes
from Graphics.constants import FPS, SPRITE_WIDTH
from Graphics.load_level_from_file import load_level
from Graphics.main_window import MainWindow

w: Optional[MainWindow] = None


def main():
    global w

    pygame.init()
    pygame.key.set_repeat(200, 200)

    w = MainWindow()
    init_palettes()

    level_num = 0
    level = load_level(f"level{level_num}.txt")
    # level = load_level("levelmake.txt")
    w.set_playing_level(level)

    clock = pygame.time.Clock()

    # adding_go = GameObject(level, 0, 0, GameObjectType.ROCK, Direction.NORTH)
    # level.add_go(adding_go)

    while True:
        event = pygame.event.poll()
        if event.type == pygame.QUIT:
            # for go in level.gos:
            #     print(f"{go.object_type},{go.x},{go.y}")

            pygame.quit()
            sys.exit(0)
        elif event.type == pygame.KEYDOWN:
            # if event.key == 61:
            #     if adding_go.object_type.value != 25:
            #         adding_go.object_type = GameObjectType(adding_go.object_type.value + 1)
            #         adding_go.get_sprite().object_type = GameObjectType(adding_go.object_type.value)
            #         adding_go.get_sprite()._update_images()
            # elif event.key == 45:
                # if adding_go.object_type.value != 0:
                #     adding_go.object_type = GameObjectType(adding_go.object_type.value - 1)
                #     adding_go.get_sprite().object_type = GameObjectType(adding_go.object_type.value)
                #     adding_go.get_sprite()._update_images()

            level.receive_input(event.key)
        # elif event.type == pygame.MOUSEBUTTONUP:
        #     adding_go = GameObject(level, adding_go.x, adding_go.y, adding_go.object_type, Direction.NORTH)
        #     level.add_go(adding_go)

        # mx, my = pygame.mouse.get_pos()
        # draw_rect = level.get_tile_grid().get_rect()
        # draw_rect.center = w.screen.get_rect().center
        # gx = (mx - draw_rect.left) // (level.get_tile_grid().scale_factor * SPRITE_WIDTH)
        # gy = (my - draw_rect.top) // (level.get_tile_grid().scale_factor * SPRITE_WIDTH)
        # adding_go.set_x(gx)
        # adding_go.set_y(gy)

        level.get_tile_grid().update()
        w.draw_grid()
        pygame.display.flip()

        clock.tick(FPS)

        if level.won and w.win_counter == -1:
            w.init_win_animation()
        if w.win_counter == -2:
            level_num += 1
            if level_num >= 5:
                break
            level = load_level(f"level{level_num}.txt")
            w.set_playing_level(level)


if __name__ == '__main__':
    main()
