from collections import OrderedDict
from typing import List, Optional

import pygame

from Game.directions import Direction, moved_in_direction
from Game.game_obect_types import GameObjectType, GOCategory, TEXT_REFERRALS
from Game.game_object import GameObject
from Game.sentence import is_valid_sentence, Sentence, parse_sentence
from Graphics.tile_grid import TileGrid


class RestoreState:
    def __init__(self, gos: List[GameObject]):
        self.gos = gos


class PlayingLevel:

    def __init__(self, level_name: str, width: int, height: int):
        self.level_name = level_name
        self.width = width
        self.height = height

        self.tile_grid: Optional[TileGrid] = None
        self.gos: List[GameObject] = []
        self.restore_states: List[RestoreState] = []

        self.sentences: List[Sentence] = []

        self.won = False

        self.find_sentences()

    def get_tile_grid(self) -> TileGrid:
        if self.tile_grid is None:
            self.tile_grid = TileGrid(self.width, self.height)
            for go in self.gos:
                self.tile_grid.add_go(go.get_sprite())

        return self.tile_grid

    def add_go(self, go: GameObject) -> None:
        self.gos.append(go)
        if self.tile_grid is not None:
            self.tile_grid.add_go(go.get_sprite())

    def remove_go(self, go: GameObject):
        self.gos.remove(go)
        self.tile_grid.remove_go(go.get_sprite())

    def set_gos(self, gos: List[GameObject]) -> None:
        self.gos = gos
        self.tile_grid.set_gos([go.get_sprite() for go in gos])

    def increase_go_draw_priority(self, go: GameObject):
        self.gos.remove(go)
        self.gos.append(go)
        self.tile_grid.increase_go_draw_priority(go.get_sprite())

    def gos_at(self, x: int, y: int) -> List[GameObject]:
        ret = []
        for go in self.gos:
            if go.x == x and go.y == y:
                ret.append(go)
        return ret

    def receive_input(self, key: int) -> None:
        if self.won: return

        if key in [pygame.K_UP, pygame.K_RIGHT, pygame.K_DOWN, pygame.K_LEFT, pygame.K_w, pygame.K_d, pygame.K_s,
                   pygame.K_a]:
            self.tick({
                pygame.K_UP: Direction.NORTH,
                pygame.K_RIGHT: Direction.EAST,
                pygame.K_DOWN: Direction.SOUTH,
                pygame.K_LEFT: Direction.WEST,
                pygame.K_w: Direction.NORTH,
                pygame.K_d: Direction.EAST,
                pygame.K_s: Direction.SOUTH,
                pygame.K_a: Direction.WEST
            }[key])
        elif key == pygame.K_SPACE:
            self.tick(None)
        elif key == pygame.K_x:
            if self.restore_states:
                self.pop_restore_state()

    def tick(self, key: Optional[Direction]):

        self.push_restore_state()
        self.find_sentences()
        self.tick_movement(key)
        self.find_sentences()
        self.tick_is_transformations()
        self.tick_check_block()

    def tick_movement(self, key: Optional[Direction]):
        movers: OrderedDict[GameObject: (Direction, int)] = OrderedDict()

        def run_movements():
            for mover in movers:
                self.increase_go_draw_priority(mover)

            while len(movers):
                to_delete = []
                for (mover, movement) in movers.items():
                    d, mag = movement
                    nx, ny = moved_in_direction(mover.x, mover.y, d)
                    mover.set_x(nx)
                    mover.set_y(ny)
                    if mag == 1:
                        to_delete.append(mover)
                    else:
                        movers[mover] = mag - 1
                for mover in to_delete:
                    del movers[mover]

        def find_movement_for_pusher(pusher: GameObject, d: Direction):
            if pusher.has_prop(GameObjectType.T_STOP, self.sentences):
                return

            gos_moving = [pusher]
            nx, ny = moved_in_direction(pusher.x, pusher.y, d)
            while True:
                at_tile = self.gos_at(nx, ny)
                stop_found = False
                tile_found = False
                if self.out_of_bounds(nx, ny):
                    stop_found = True
                else:
                    for being_pushed in at_tile:
                        is_push = being_pushed.is_push(self.sentences)
                        is_stop = being_pushed.has_prop(GameObjectType.T_STOP, self.sentences)
                        if is_stop and (not is_push):
                            tile_found = True
                            stop_found = True
                        elif is_push:
                            tile_found = True
                            gos_moving.append(being_pushed)
                if stop_found:
                    gos_moving = []
                    break
                elif not tile_found:
                    break
                else:
                    nx, ny = moved_in_direction(nx, ny, d)
            for moving in gos_moving:
                move_go(moving, d)

        def move_go(mover: GameObject, d: Direction):
            if movers.get(mover, None) is None:
                movers[mover] = (d, 1)
            elif movers[mover][0] == d:
                movers[mover] = (d, movers[mover] + 1)
            else:
                raise Exception("Moving in multiple directions")

        # YOU movement
        if key:
            for go in self.gos:
                if go.has_prop(GameObjectType.T_YOU, self.sentences):
                    find_movement_for_pusher(go, key)
                    go.set_direction(key)

        run_movements()

    def tick_is_transformations(self):
        protected_objects = []
        for sentence in self.sentences:
            protected_objects += sentence.get_protected_objects()

        to_add = []
        to_remove = []
        for go in self.gos:
            if go.object_type not in protected_objects:
                transforms = []
                for sentence in self.sentences:
                    if sentence.is_transformation() and sentence.targets_object(go):
                        transforms += sentence.transformation_types()
                if transforms:
                    x, y, d = go.x, go.y, go.direction
                    to_add += [GameObject(self, x, y, TEXT_REFERRALS[t], d) for t in transforms]
                    to_remove.append(go)

        for r in to_remove:
            self.remove_go(r)
        for a in to_add:
            self.add_go(a)

    def tick_check_block(self):

        def check_for_win() -> bool:
            for go in self.gos:
                if go.has_prop(GameObjectType.T_YOU, self.sentences):
                    if go.has_prop(GameObjectType.T_WIN, self.sentences):
                        return True

                    for other in self.gos_at(go.x, go.y):
                        if other.has_prop(GameObjectType.T_WIN, self.sentences):
                            return True
            return False

        if check_for_win():
            self.won = True

    def push_restore_state(self) -> None:
        rs = RestoreState([go.copy() for go in self.gos])
        self.restore_states.append(rs)

    def pop_restore_state(self) -> None:
        rs = self.restore_states.pop().gos
        self.set_gos(rs)

    def find_sentences(self):
        found_sentences: List[List[GameObject]] = []

        def find_continuations(current: List[GameObject], direction: Direction):
            if is_valid_sentence(current):
                found_sentences.append(current)
            last = current[-1]
            nx, ny = moved_in_direction(last.x, last.y, direction)
            for word in self.gos_at(nx, ny):
                if word.object_type.get_category() in [GOCategory.NOUN, GOCategory.PROPERTY, GOCategory.VERB]:
                    nl = current = current.copy()
                    nl.append(word)
                    find_continuations(nl, direction)

        for go in self.gos:
            find_continuations([go], Direction.EAST)
            find_continuations([go], Direction.SOUTH)

        self.sentences = [parse_sentence(s) for s in found_sentences]

    def out_of_bounds(self, x, y) -> bool:
        return x < 0 or x >= self.width or y < 0 or y >= self.height
