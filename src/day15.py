from typing import List, Generator, Tuple, Optional, Dict
from sortedcontainers import SortedListWithKey
import heapq
from math import inf
import sys


class Cavern:
    def __init__(self, w, h):
        self.width = w
        self.height = h
        self.entities: List[Entity] = [Air(x, y) for x in range(w) for y in range(h)]

    def set_entity(self, entity: "Entity"):
        self.entities[entity.position[1] * self.width + entity.position[0]] = entity

    def get_entity_at(self, position):
        return self.entities[position[1] * self.width + position[0]]

    def get_entity_at_offset(self, entity: "Entity", x=0, y=0) -> "Entity":
        return self.get_entity_at((entity.position[0]+x, entity.position[1]+y))

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
    def calculate_distance(cls, e1: Tuple[int, int], e2: Tuple[int, int]):
        return abs(e1[0] - e2[0]) + abs(e1[1] - e2[1])

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
        self.__position = (x, y)

    @property
    def position(self):
        return self.__position

    @position.setter
    def position(self, new_position):
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
        return "{0}: ({1[0]:>2}, {1[1]:>2}) ({2:>3} HP)".format(self, self.position, self.hit_points)

    def die(self):
        print(repr(self), "died!")
        game.cavern.set_entity(Air(self.position[0], self.position[1]))
        game.check_is_game_over()

    def iter_free_neighbours(self):
        blocked_spots = [e.position for e in game.cavern.iter_obstacles()]
        if (self.position[0] - 1, self.position[1]) not in blocked_spots:
            yield (self.position[0] - 1, self.position[1])
        if (self.position[0] + 1, self.position[1]) not in blocked_spots:
            yield (self.position[0] + 1, self.position[1])
        if (self.position[0], self.position[1] - 1) not in blocked_spots:
            yield (self.position[0], self.position[1] - 1)
        if (self.position[0], self.position[1] + 1) not in blocked_spots:
            yield (self.position[0], self.position[1] + 1)

    def find_target(self, distances: Dict[Tuple[int, int], Tuple[Tuple[int, int], int]]):
        prime, prime_dist = None, inf
        for potential in game.cavern.iter_characters():
            if potential.__class__ == self.__class__:
                continue
            for t in potential.iter_free_neighbours():
                    # closest spot is last step in shortest path to the potential target
                    if t not in distances:
                        continue
                    if distances[t][1] < prime_dist:
                        prime = t
                        prime_dist = distances[t][1]
                    elif distances[t][1] == prime_dist and (t[1] < prime[1] or (t[1] == prime[1] and t[0] < prime[0])):
                        prime = t
        return prime

    def dijkstra(self):
        def get_neighbours(coords: Tuple[int, int]):
            _neighbours = []
            for delta in [-1, 1]:
                if (coords[0] - delta, coords[1]) in distances:
                    _neighbours.append((coords[0] - delta, coords[1]))
                if (coords[0], coords[1] - delta) in distances:
                    _neighbours.append((coords[0], coords[1] - delta))
            return _neighbours

        def initialise_queue():  # -> List[Tuple[int, int]]:
            # returns a list of tuples [priority, coordinates = (x, y)]
            for y in range(game.cavern.height):
                for x in range(game.cavern.width):
                    if (x, y) not in blocked_spots or (x, y) == self.position:
                        if (x, y) == self.position:
                            distances[(x, y)] = 0
                        else:
                            distances[(x, y)] = inf
                        not_visited.add((x, y))

        def set_as_closer():
            not_visited.remove(neighbour)  # to update the distance, gets re-added a few lines below
            distances[neighbour] = alternative
            not_visited.add(neighbour)
            nodes[neighbour] = (u, alternative)

        blocked_spots = [e.position for e in game.cavern.iter_obstacles()]
        nodes: Dict[Tuple[int, int], Tuple[Tuple[int, int], int]] = {}
        distances = {}
        not_visited: SortedListWithKey[Tuple[int, int]] = SortedListWithKey(key=lambda x: -distances[x])
        initialise_queue()
        while len(not_visited) > 0:
            u = not_visited.pop()
            if distances[u] == inf:
                continue
            for neighbour in get_neighbours(u):
                alternative = distances[u] + 1
                if alternative < distances[neighbour]:
                    set_as_closer()
                elif alternative == distances[neighbour]:  # equal
                    if u[1] < nodes[neighbour][0][1]:  # more up
                        set_as_closer()
                    elif u[1] == nodes[neighbour][0][1] and u[0] < nodes[neighbour][0][0]:  # more left
                        set_as_closer()
        return nodes

    def move(self):
        distances = self.dijkstra()
        target = self.find_target(distances)
        if target is None:
            # print(repr(self), "not moving")
            return
        # print(distances)
        x = target
        while self.position != distances[x][0]:
            x = distances[x][0]
        # print(self.position, "Target", target, "Step:", x)
        self.position = x

    def try_get_enemy_in_range(self) -> Optional[Entity]:
        offsets = [(0, -1), (-1, 0), (1, 0), (0, 1)]
        enemy_class = Elf if isinstance(self, Goblin) else Goblin
        enemies: List[Character] = []
        for offset in offsets:
            if isinstance(game.cavern.get_entity_at_offset(self, *offset), enemy_class):
                enemies.append(game.cavern.get_entity_at_offset(self, *offset))
        if len(enemies) == 0:
            return None
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
            print("Game over! Round {}, Outcome {}".format(self.round_number,
                                                           self.round_number *
                                                           sum(c.hit_points for c in self.cavern.iter_characters())))
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

