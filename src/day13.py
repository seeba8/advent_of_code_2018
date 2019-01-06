from enum import Enum, auto
from typing import List, Tuple, Set
import sys


class Direction(Enum):
    UP = auto(),
    DOWN = auto(),
    LEFT = auto(),
    RIGHT = auto()


class Cart:
    def __init__(self, current_direction: "Direction"):
        self.direction: "Direction" = current_direction
        self.last_move = -1
        self.next_turn = 0  # 0: left. 1: straight. 2: right

    def __repr__(self):
        if self.direction == Direction.DOWN:
            return "v"
        if self.direction == Direction.UP:
            return "^"
        if self.direction == Direction.LEFT:
            return "<"
        if self.direction == Direction.RIGHT:
            return ">"
        raise Exception("Shouldn't happen")

    def set_direction(self, tile: "Tile"):
        if isinstance(tile, UpDown) or isinstance(tile, LeftRight):
            return
        if isinstance(tile, Curve):
            if self.direction in (Direction.UP, Direction.DOWN):
                self.direction = Direction.LEFT if Direction.LEFT in tile.directions else Direction.RIGHT
            else:
                self.direction = Direction.UP if Direction.UP in tile.directions else Direction.DOWN
            return
        if isinstance(tile, Intersection):
            if self.next_turn % 3 == 0:
                self.turn_left()
            elif self.next_turn % 3 == 2:
                self.turn_right()
            self.next_turn += 1

    def turn_left(self):
        turns = {
            Direction.LEFT: Direction.DOWN,
            Direction.DOWN: Direction.RIGHT,
            Direction.RIGHT: Direction.UP,
            Direction.UP: Direction.LEFT
        }
        self.direction = turns[self.direction]

    def turn_right(self):
        turns = {
            Direction.LEFT: Direction.UP,
            Direction.DOWN: Direction.LEFT,
            Direction.RIGHT: Direction.DOWN,
            Direction.UP: Direction.RIGHT
        }
        self.direction = turns[self.direction]


class Crash(Cart):
    def __repr__(self):
        return "X"


class Tile:
    def __init__(self):
        self.directions: Set[Direction] = set()
        self.__cart: Cart = None

    def __repr__(self):
        return "O"

    @property
    def cart(self):
        return self.__cart

    @cart.setter
    def cart(self, c: Cart):
        if self.cart is not None and c is not None:
            self.__cart = Crash(c.direction)
        else:
            self.__cart = c


class Empty(Tile):
    def __init__(self):
        super().__init__()

    def __repr__(self):
        return " "


class UpDown(Tile):
    def __init__(self):
        super().__init__()
        self.directions = {Direction.UP, Direction.DOWN}

    def __repr__(self):
        if self.cart is not None:
            return str(self.cart)
        return "|"


class LeftRight(Tile):
    def __init__(self):
        super().__init__()
        self.directions = {Direction.LEFT, Direction.RIGHT}

    def __repr__(self):
        if self.cart is not None:
            return str(self.cart)
        return "-"


class Intersection(Tile):
    def __init__(self):
        super().__init__()
        self.directions = {Direction.LEFT, Direction.RIGHT, Direction.UP, Direction.DOWN}

    def __repr__(self):
        if self.cart is not None:
            return str(self.cart)
        return "+"


class Curve(Tile):
    def __init__(self, directions: Set[Direction]):
        super().__init__()
        if len(directions) != 2:
            raise Exception("Not a valid curve")
        self.directions = directions

    def __repr__(self):
        if self.cart is not None:
            return str(self.cart)
        if ((Direction.DOWN in self.directions and Direction.RIGHT in self.directions)
                or (Direction.UP in self.directions and Direction.LEFT in self.directions)):
            return "/"
        return "\\"


class Map:
    def __init__(self, w, h):
        self.width = w
        self.height = h
        self.__tiles: List[Tile] = [Empty()] * w * h
        self.carts: List[Cart] = []
        self.t = -1

    def get_tile(self, x, y):
        return self.__tiles[self.width * y + x]

    def set_tile(self, x, y, tile: Tile):
        self.__tiles[self.width * y + x] = tile

    def __repr__(self):
        map = ""
        for y in range(self.height):
            for x in range(self.width):
                tile = self.get_tile(x, y)
                map += str(tile)
            map += "\n"
        return map

    def tick(self):
        self.t += 1
        for y in range(self.height):
            for x in range(self.width):
                target = (0,0)
                tile = self.get_tile(x, y)
                if tile.cart is None or tile.cart.last_move == self.t:
                    continue
                if tile.cart.direction == Direction.UP:
                    target = (x, y-1)
                    self.get_tile(*target).cart = tile.cart
                    tile.cart.set_direction(self.get_tile(*target))
                    tile.cart.last_move = self.t
                    tile.cart = None
                elif tile.cart.direction == Direction.RIGHT:
                    target = (x+1, y)
                    self.get_tile(*target).cart = tile.cart
                    tile.cart.set_direction(self.get_tile(*target))
                    tile.cart.last_move = self.t
                    tile.cart = None
                elif tile.cart.direction == Direction.DOWN:
                    target = (x, y+1)
                    self.get_tile(*target).cart = tile.cart
                    tile.cart.set_direction(self.get_tile(*target))
                    tile.cart.last_move = self.t
                    tile.cart = None
                elif tile.cart.direction == Direction.LEFT:
                    target = (x-1, y)
                    self.get_tile(*target).cart = tile.cart
                    tile.cart.set_direction(self.get_tile(*target))
                    tile.cart.last_move = self.t
                    tile.cart = None
                if isinstance(self.get_tile(*target).cart, Crash):
                    print(target)
                    print(self)
                    sys.exit(-1)

    @staticmethod
    def from_file(path="../input/2018/day13.txt"):
        with open(path, "r") as file:
            lines = file.readlines()
            lines = [line.strip("\r").strip("\n") for line in lines]
            max_width = max(len(l) for l in lines)
            m = Map(max_width, len(lines))
            for y, line in enumerate(lines):

                for x, tile in enumerate(line):
                    # Curves:
                    # /-  |
                    # |  -/
                    if tile == "|":
                        m.set_tile(x,y, UpDown())
                    elif tile == "-":
                        m.set_tile(x, y, LeftRight())
                    elif tile == "+":
                        m.set_tile(x, y, Intersection())
                    elif tile == "/":
                        if x != 0 and isinstance(m.get_tile(x-1, y), LeftRight):  # left-up curve
                            m.set_tile(x, y, Curve({Direction.LEFT, Direction.UP}))
                        else:
                            m.set_tile(x, y, Curve({Direction.RIGHT, Direction.DOWN}))
                    elif tile == "\\":
                        if x != 0 and isinstance(m.get_tile(x-1, y), LeftRight):  # up-right curve
                            m.set_tile(x, y, Curve({Direction.DOWN, Direction.LEFT}))
                        else:
                            m.set_tile(x, y, Curve({Direction.UP, Direction.RIGHT}))
                    elif tile == "^":
                        c = Cart(Direction.UP)
                        m.carts.append(c)
                        m.set_tile(x, y, UpDown())
                        m.get_tile(x, y).cart = c

                    elif tile == "v":
                        m.set_tile(x, y, UpDown())
                        c = Cart(Direction.DOWN)
                        m.carts.append(c)
                        m.get_tile(x, y).cart = c
                    elif tile == ">":
                        m.set_tile(x, y, LeftRight())
                        c = Cart(Direction.RIGHT)
                        m.carts.append(c)
                        m.get_tile(x, y).cart = c
                    elif tile == "<":
                        m.set_tile(x, y, LeftRight())
                        c = Cart(Direction.LEFT)
                        m.carts.append(c)
                        m.get_tile(x, y).cart = c
            return m


m = Map.from_file()

while True:
    m.tick()


