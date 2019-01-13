from typing import List, Generator, Tuple, Optional, Dict, Union
from sortedcontainers import SortedListWithKey
from math import inf
import sys


class Point:
    def __init__(self, x: Union[Tuple[int, int], int], y: Optional[int]=None):
        if isinstance(x, int):
            self.x = x
            self.y = y
        else:
            (self.x, self.y) = x[0], x[1]

    def __eq__(self, other: "Point"):
        return self.x == other.x and self.y == other.y

    def __cmp__(self, other: "Point"):
        if self == other:
            return 0
        if self.y < other.y:
            return -1
        if self.y == other.y and self.x < other.x:
            return -1
        return 1

    def __lt__(self, other: "Point"):
        return self.y < other.y or (self.y == other.y and self.x < other.x)

    def __repr__(self):
        return "Point ({}, {})".format(self.x, self.y)

    def __iter__(self):
        yield self.x
        yield self.y

    def __hash__(self):
        return self.y * game.cavern.width + self.x

    def offset(self, x=0, y=0):
        return Point(self.x+x, self.y+y)

    def iter_neighbours(self):
        for i in [(0, -1), (-1, 0), (1, 0), (0, 1)]:
            yield self.offset(*i)


class Cavern:
    def __init__(self, w, h):
        self.width = w
        self.height = h
        self.entities: List[Entity] = [Air(x, y) for x in range(w) for y in range(h)]

    def set_entity(self, entity: "Entity"):
        self.entities[entity.position.y * self.width + entity.position.x] = entity

    def get_entity_at(self, position: Point) -> "Entity":
        return self.entities[position.y * self.width + position.x]

    def iter_characters(self) -> Generator["Character", None, None]:
        for unit in self.entities:
            if isinstance(unit, Wall) or isinstance(unit, Air):
                continue
            yield unit

    def iter_obstacles(self) -> Generator["Entity", None, None]:
        for unit in self.entities:
            if isinstance(unit, Air):
                continue
            yield unit

    @classmethod
    def create_from_string(cls, maplines: List[str]):
        cavern = Cavern(len(maplines[0].strip()), len(maplines))
        print("test")
        for y, line in enumerate(maplines):
            for x, item in enumerate(line.strip()):
                if item == "#":
                    cavern.set_entity(Wall(x, y))
                elif item == "G":
                    cavern.set_entity(Goblin(x, y))
                elif item == "E":
                    cavern.set_entity(Elf(x, y))
        return cavern

    def __str__(self):
        s = ""
        for i, entity in enumerate(self.entities):
            if i % self.width == 0:
                s += "\n"
            s += str(entity)
        return s

    def __repr__(self):
        s = ""
        for unit in self.iter_characters():
            s += repr(unit) + "\n"
        return s


class Entity:
    def __init__(self, x, y):
        self.__position = Point(x, y)

    @property
    def position(self):
        return self.__position

    @position.setter
    def position(self, new_position: Point):
        game.cavern.set_entity(Air(*self.position))
        self.__position = new_position
        game.cavern.set_entity(self)

    def __repr__(self):
        return "{}: {}".format(self, self.position)


class Character(Entity):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.last_turn = 0
        self.attack_power = 3
        self.hit_points = 200

    def __repr__(self):
        return "{0}: ({1}) ({2:>3} HP)".format(self, self.position, self.hit_points)

    def die(self):
        print(repr(self), "died!")
        game.cavern.set_entity(Air(self.position.x, self.position.y))
        game.check_is_game_over()

    def iter_free_neighbours(self):
        blocked_spots = [e.position for e in game.cavern.iter_obstacles()]
        for neighbour in self.position.iter_neighbours():
            if neighbour not in blocked_spots:
                yield neighbour

    def find_target(self, targets: Dict[Point, Point], distances: Dict[Point, int]):
        prime, prime_dist = None, inf
        for potential in game.cavern.iter_characters():
            if potential.__class__ == self.__class__:
                continue
            for t in potential.iter_free_neighbours():
                # closest spot is last step in shortest path to the potential target
                if t not in targets:
                    continue
                if distances[t] < prime_dist:
                    prime = t
                    prime_dist = distances[t]
                elif distances[t] == prime_dist and (t < prime):
                    prime = t
        return prime

    def dijkstra(self):
        def get_neighbours(coords: Point):
            return [n for n in coords.iter_neighbours() if n in distances]

        def initialise_queue():  # -> List[Tuple[int, int]]:
            # returns a list of tuples [priority, coordinates = (x, y)]
            for y in range(game.cavern.height):
                for x in range(game.cavern.width):
                    if Point(x, y) not in blocked_spots or Point(x, y) == self.position:
                        if Point(x, y) == self.position:
                            distances[Point(x, y)] = 0
                        else:
                            distances[Point(x, y)] = inf
                        not_visited.add(Point(x, y))

        def set_as_closer():
            not_visited.remove(neighbour)  # to update the distance, gets re-added a few lines below
            distances[neighbour] = alternative
            not_visited.add(neighbour)
            predecessor[neighbour] = u

        blocked_spots = [e.position for e in game.cavern.iter_obstacles()]
        # what is the predecessor of a point. E.g., predecessor[A] = B means
        # that the predecessor of A is B
        predecessor: Dict[Point, Point] = {}
        distances: Dict[Point, int] = {}  # what is the distance from the character to the target
        not_visited: SortedListWithKey[Point] = SortedListWithKey(key=lambda x: -distances[x])
        initialise_queue()
        while len(not_visited) > 0:
            u: Point = not_visited.pop()
            if distances[u] == inf:
                continue
            for neighbour in get_neighbours(u):
                alternative = distances[u] + 1
                if alternative < distances[neighbour]:
                    set_as_closer()
                elif alternative == distances[neighbour]:  # equal
                    if u < predecessor[neighbour]:
                        set_as_closer()
        return predecessor, distances

    def move(self):
        predecessors, distances = self.dijkstra()
        target = self.find_target(predecessors, distances)
        if target is None:
            # print(repr(self), "not moving")
            return
        # print(distances)
        x = target
        while self.position != predecessors[x]:
            x = predecessors[x]
        # print(self.position, "Target", target, "Step:", x)
        self.position = x
        # sys.exit(-1)

    def try_get_enemy_in_range(self) -> Optional["Character"]:
        enemy_class: Character.__class__ = Elf if isinstance(self, Goblin) else Goblin
        enemies: List[Character] = []
        for n in self.position.iter_neighbours():
            if isinstance(game.cavern.get_entity_at(n), enemy_class):
                enemies.append(game.cavern.get_entity_at(n))

        if len(enemies) == 0:
            return None
        enemies.sort(key=lambda x: x.position)
        best_i, best_hp = 0, enemies[0].hit_points
        for i, enemy in enumerate(enemies):
            if enemy.hit_points < best_hp or (enemy.hit_points == best_hp and i < best_i):
                best_i = i
                best_hp = enemy.hit_points
        return enemies[best_i]

    def attack(self, enemy: "Character"):
        # print(repr(self), "attacks", repr(enemy))
        enemy.hit_points -= self.attack_power
        if enemy.hit_points <= 0:
            enemy.die()


class Elf(Character):
    def __str__(self):
        return "E"


class Goblin(Character):
    def __str__(self):
        return "G"


class Wall(Entity):
    def __str__(self):
        return "#"


class Air(Entity):
    def __str__(self):
        return "."


class Game:
    def __init__(self, maplines):
        self.cavern = Cavern.create_from_string(maplines)
        self.round_number = 0
        self.is_game_over = False

    def next_round(self):
        self.round_number += 1
        for unit in self.cavern.iter_characters():
            if unit.last_turn == self.round_number:
                continue
            if self.is_game_over:
                self.round_number -= 1
                break
            enemy = unit.try_get_enemy_in_range()
            if enemy is None:
                unit.move()
            enemy = unit.try_get_enemy_in_range()
            if enemy is not None:
                unit.attack(enemy)
            unit.last_turn = self.round_number
        if self.is_game_over:
            for c in game.cavern.iter_characters():
                print(repr(c))
            print("Game over! Round {}, Sum {},  Outcome {}".format(self.round_number,
                                                                    sum(c.hit_points for c in
                                                                        self.cavern.iter_characters()),
                                                                    self.round_number *
                                                                    sum(c.hit_points for c in
                                                                        self.cavern.iter_characters())))
            # It's not 220320

    def check_is_game_over(self):
        has_goblin = has_elf = False
        for character in self.cavern.iter_characters():
                if isinstance(character, Goblin):
                    has_goblin = True
                elif isinstance(character, Elf):
                    has_elf = True
        if not (has_goblin and has_elf):
            self.is_game_over = True


game: Game = None
with open("../input/2018/day15.txt", "r") as file:
    game = Game(file.readlines())
    print(game.cavern)
    print(repr(game.cavern))
    while not game.is_game_over:
        game.next_round()
        #print(game.cavern)
    print(game.cavern)

