import pygame
from collections import OrderedDict
from typing import List, Optional, Tuple
from Game.directions import Direction, moved_in_direction
from Game.game_obect_types import GameObjectType, GOCategory
from Game.game_object import GameObject
from Game.sentence import is_valid_sentence, Sentence, parse_sentence
from Graphics.color_palette import get_palette, PaletteGroups
from Graphics.tile_grid import TileGrid


class RestoreState:
    def __init__(self, gos: List[GameObject]):
        self.gos = gos


class PlayingLevel:

    def __init__(self, level_name: str, theme: str, width: int, height: int):
        self.level_name = level_name
        self.theme = theme
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
            self.tile_grid = TileGrid(self.theme, self.width, self.height)
            for go in self.gos:
                self.tile_grid.add_go(go.get_sprite())
            self.find_sentences(True)
        return self.tile_grid

    def get_ng_bk_color(self):
        return get_palette(self.theme)[PaletteGroups.NON_GRID_BK_COLOR]

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
        self.find_sentences(True)

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
        elif key == pygame.K_r:
            if self.restore_states:
                self.set_gos(self.restore_states[0].gos)
                self.restore_states = []

    def tick(self, key: Optional[Direction]):

        self.push_restore_state()
        self.find_sentences()
        self.tick_movement(key)
        self.find_sentences(True)
        self.tick_is_transformations()
        self.tick_check_block()

    def tick_movement(self, key: Optional[Direction]):
        movers: OrderedDict[GameObject: (Direction, int)] = OrderedDict()

        def sort_movers():
            def get_sort_order_val(item: Tuple[GameObject, Tuple[Direction, int]]) -> int:
                if item[1][0] == Direction.EAST:
                    return item[0].playing_level.width - item[0].x
                elif item[1][0] == Direction.WEST:
                    return item[0].x
                elif item[1][0] == Direction.NORTH:
                    return item[0].y
                elif item[1][0] == Direction.SOUTH:
                    return item[0].playing_level.height - item[0].y

            mover_tuples = [(k, v) for k, v in movers.items()]
            mover_tuples = sorted(mover_tuples, key=get_sort_order_val)
            return OrderedDict(mover_tuples)

        def run_movements():
            sorted_movers = sort_movers()

            for mover in sorted_movers:
                self.increase_go_draw_priority(mover)

            while len(sorted_movers):
                to_delete = []
                for (mover, movement) in sorted_movers.items():
                    d, mag = movement
                    run_move(mover, d)
                    if mag == 1:
                        to_delete.append(mover)
                    else:
                        sorted_movers[mover] = (d, mag - 1)
                for mover in to_delete:
                    del sorted_movers[mover]

        def run_move(pusher: GameObject, d: Direction):
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
                        is_push = being_pushed.is_push()
                        is_stop = being_pushed.has_prop(GameObjectType.T_STOP)
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
                nx, ny = moved_in_direction(moving.x, moving.y, d)
                moving.set_x(nx)
                moving.set_y(ny)
                moving.set_direction(d)
                self.increase_go_draw_priority(moving)

        def move_go(mover: GameObject, d: Direction):
            if mover not in movers:
                movers[mover] = (d, 1)
            elif movers[mover][0] == d:
                movers[mover] = (d, movers[mover][1] + 1)
            else:
                raise Exception("Moving in multiple directions")

        # YOU movement
        if key:
            for go in self.gos:
                if go.has_prop(GameObjectType.T_YOU):
                    move_go(go, key)
        run_movements()

    def tick_is_transformations(self):
        protected_objects = []
        for sentence in self.sentences:
            protected_objects += sentence.get_protected_objects()

        to_add = []
        to_remove = []
        for go in self.gos:
            go.get_sprite().xed = False
            if go.object_type not in protected_objects:
                transforms: List[GameObjectType] = []
                for sentence in self.sentences:
                    if sentence.is_transformation() and sentence.targets_object(go):
                        transforms += sentence.transformation_types()
                if transforms:
                    x, y, d = go.x, go.y, go.direction
                    to_add += [GameObject(self, x, y, t.object_referral(), d) for t in transforms]
                    to_remove.append(go)

        # find disabled sentences from protected objects
        for go in protected_objects:
            for sentence in self.sentences:
                if sentence.is_transformation() and sentence.targets_type(go):
                    for o in sentence.objects:
                        o.get_sprite().xed = True

        for r in to_remove:
            self.remove_go(r)
        for a in to_add:
            self.add_go(a)

    def tick_check_block(self):

        def check_for_win() -> bool:
            for go in self.gos:
                if go.has_prop(GameObjectType.T_YOU):
                    if go.has_prop(GameObjectType.T_WIN):
                        return True
                    for other in self.gos_at(go.x, go.y):
                        if other.has_prop(GameObjectType.T_WIN):
                            return True
            return False

        def do_sink():
            for go in self.gos:
                if go.has_prop(GameObjectType.T_SINK):
                    at = self.gos_at(go.x, go.y)
                    if len(at) > 1:
                        for r in at:
                            self.remove_go(r)

        def do_defeat():
            for go in self.gos:
                if go.has_prop(GameObjectType.T_DEFEAT):
                    at = self.gos_at(go.x, go.y)
                    for r in at:
                        if r.has_prop(GameObjectType.T_YOU):
                            self.remove_go(r)

        def do_melt():
            for go in self.gos:
                if go.has_prop(GameObjectType.T_HOT):
                    at = self.gos_at(go.x, go.y)
                    for r in at:
                        if r.has_prop(GameObjectType.T_MELT):
                            self.remove_go(r)

        if check_for_win():
            self.won = True

        do_sink()
        do_defeat()
        do_melt()

    def push_restore_state(self) -> None:
        rs = RestoreState([go.copy() for go in self.gos])
        self.restore_states.append(rs)

    def pop_restore_state(self) -> None:
        rs = self.restore_states.pop().gos
        self.set_gos(rs)

    def find_sentences(self, set_muted=False):
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

        if set_muted:
            not_muted = []
            for s in found_sentences:
                for go in s:
                    not_muted.append(go)
                    go.get_sprite().set_muted(False)
            for go in self.gos:
                if go.object_type.get_category() != GOCategory.OBJECT and go not in not_muted:
                    go.get_sprite().set_muted(True)

        self.sentences = [parse_sentence(s) for s in found_sentences]

    def out_of_bounds(self, x, y) -> bool:
        return x < 0 or x >= self.width or y < 0 or y >= self.height
