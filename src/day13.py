from enum import Enum, auto
from typing import List, Tuple, Set
import sys


class Direction(Enum):
    UP = auto(),
    DOWN = auto(),
    LEFT = auto(),
    RIGHT = auto()


class Cart:
    def __init__(self, current_direction: "Direction", position: Tuple[int, int]):
        self.direction: "Direction" = current_direction
        self.last_move = -1
        self.next_turn = 0  # 0: left. 1: straight. 2: right
        self.position = position

    def __repr__(self):
        direction = ""
        if self.direction == Direction.DOWN:
            direction = "v"
        if self.direction == Direction.UP:
            direction = "^"
        if self.direction == Direction.LEFT:
            direction = "<"
        if self.direction == Direction.RIGHT:
            direction = ">"
        return direction + str(self.position)

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
        if self.__cart is not None and c is not None:
            self.__cart = Crash(c.direction, self.__cart.position)
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

    def sort_carts(self):
        self.carts.sort(key=lambda x: x.position[1] * self.height + x.position[0])

    def remove_carts(self, position):
        self.carts = [cart for cart in self.carts if cart.position != position]

    def tick(self, stop_at_crash=True):
        self.t += 1
        self.sort_carts()
        i = 0
        while i < len(self.carts):
            cart = self.carts[i]
            if i > 0 and self.carts[i-1].last_move < self.t:
                cart = self.carts[i-1]
            if cart.last_move == self.t:
                i += 1
                continue
            if isinstance(cart, Crash):
                raise Exception("Shouldn't happen")
                # self.carts.remove(cart)
            target = (0, 0)
            x, y = cart.position
            tile = self.get_tile(x, y)
            if cart.direction == Direction.UP:
                target = (x, y-1)
            elif cart.direction == Direction.RIGHT:
                target = (x+1, y)
            elif cart.direction == Direction.DOWN:
                target = (x, y+1)
            elif cart.direction == Direction.LEFT:
                target = (x-1, y)
            target_tile = self.get_tile(*target)
            target_tile.cart = cart
            cart.position = target
            cart.set_direction(target_tile)
            cart.last_move = self.t
            tile.cart = None
            if isinstance(target_tile.cart, Crash):
                print(target)
                if stop_at_crash:
                    print(self)
                    print(target)
                    self.remove_carts(target)
                    print(list(c.position for c in self.carts))
                    sys.exit(-1)
                self.remove_carts(target)
                target_tile.cart = None
        if len(self.carts) == 1:
            print("Highlander:", self.carts[0].position)
            sys.exit(0)

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
                        if x != 0 and (isinstance(m.get_tile(x-1, y), LeftRight)
                                       or isinstance(m.get_tile(x-1, y), Intersection)):  # left-up curve
                            m.set_tile(x, y, Curve({Direction.LEFT, Direction.UP}))
                        else:
                            m.set_tile(x, y, Curve({Direction.RIGHT, Direction.DOWN}))
                    elif tile == "\\":
                        if x != 0 and (isinstance(m.get_tile(x-1, y), LeftRight)
                                       or isinstance(m.get_tile(x-1, y), Intersection)):  # up-right curve
                            m.set_tile(x, y, Curve({Direction.DOWN, Direction.LEFT}))
                        else:
                            m.set_tile(x, y, Curve({Direction.UP, Direction.RIGHT}))
                    elif tile == "^":
                        c = Cart(Direction.UP, (x, y))
                        m.carts.append(c)
                        m.set_tile(x, y, UpDown())
                        m.get_tile(x, y).cart = c
                    elif tile == "v":
                        m.set_tile(x, y, UpDown())
                        c = Cart(Direction.DOWN, (x, y))
                        m.carts.append(c)
                        m.get_tile(x, y).cart = c
                    elif tile == ">":
                        m.set_tile(x, y, LeftRight())
                        c = Cart(Direction.RIGHT, (x, y))
                        m.carts.append(c)
                        m.get_tile(x, y).cart = c
                    elif tile == "<":
                        m.set_tile(x, y, LeftRight())
                        c = Cart(Direction.LEFT, (x, y))
                        m.carts.append(c)
                        m.get_tile(x, y).cart = c
            return m


m = Map.from_file()

while True:
    m.tick(stop_at_crash=False)


