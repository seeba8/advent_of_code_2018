# from math import inf, isinf
from typing import List, Tuple, Union


WALL = 500
ELF = 200
GOBLIN = -200
G_ATTACK_POWER = 3
E_ATTACK_POWER = 3
AIR = 0
INF = 2**16 - 1


class Game:
    def __init__(self, w, h):
        self.cavern = [0]*w*h
        self.last_move = [0]*w*h
        self.width = w
        self.height = h
        self.is_game_over = False
        self.round_number = 0
        self.elf_died = False

    @staticmethod
    def from_file(path="../input/2018/day15.txt"):
        with open(path, "r") as file:
            map_lines = file.readlines()
        _game = Game(len(map_lines[0].strip()), len(map_lines))
        i = 0
        value = {"#": WALL, "G": GOBLIN, "E": ELF, ".": AIR}
        for line in map_lines:
            for c in line.strip():
                _game.cavern[i] = value[c]
                i += 1
        return _game

    def __str__(self):
        s = ""
        lives = []
        for i, c in enumerate(self.cavern):
            if i != 0 and i % self.width == 0:
                s += " "*5 + ", ".join(["G({})".format(abs(x[1])) if x[1] < 0
                                        else "E({})".format(x[1]) for x in lives])
                lives = []
                s += "\n"
            if c == WALL:
                s += "#"
            elif c > 0:
                s += "E"
                lives.append((i, c))
            elif c < 0:
                s += "G"
                lives.append((i, c))
            else:
                s += "."
        s += "\n"
        return s

    def next_round(self, elves_must_live=False):
        self.round_number += 1
        for i, c in enumerate(self.cavern):
            if c in (0, WALL):
                continue
            if self.elf_died and elves_must_live:
                print("Elf died :-(")
                break
            if self.is_game_over:
                self.round_number -= 1
                break
            if not self.last_move[i] == self.round_number:
                enemy = self.enemy_to_attack(i)
                if enemy is not None:
                    self.attack(enemy)
                else:
                    new_i = self.move(i)
                    if new_i is None:  # did not move, therefore nothing there to attack now
                        continue
                    enemy = self.enemy_to_attack(new_i)
                    if enemy is not None:
                        self.attack(enemy)
        if self.is_game_over:
            sum_health = sum(abs(i) for i in self.cavern if i != WALL)
            print("Game over! Round {}, Sum {},  Outcome {}{}"
                  .format(self.round_number,  sum_health, self.round_number * sum_health,
                          ", Elf died :-(" if elves_must_live and self.elf_died else ""))

    def _print_distances(self, distances, i):
        s = ""
        for x, d in enumerate(distances):
            if x % self.width == 0:
                s += "\n"
            if x == i:
                s += "X"
            elif self.is_elf(x):
                s += "E"
            elif self.is_goblin(x):
                s += "G"
            elif x == 154:
                s += "A"
            elif d == INF:
                s += "."
            else:
                s += str(d % 10)
        print(s)

    def find_target(self, i, distances):
        best_so_far = None
        is_elf = self.is_elf(i)
        for index, val in enumerate(self.cavern):
            if val in (AIR, WALL):
                continue
            if is_elf ^ self.is_elf(index):
                for n in self.get_neighbours(index):
                    if distances[n] == INF:
                        continue
                    if self.cavern[n] == AIR and (best_so_far is None or distances[n] < distances[best_so_far] or
                                                  (distances[n] == distances[best_so_far] and n < best_so_far)):
                        best_so_far = n
        return best_so_far

    def move(self, i):
        predecessors, distances = self.dijkstra(i)
        target = self.find_target(i, distances)
        if target is None:
            return
        # Backtrack to the first step towards the goal
        while predecessors[target] != i:
            target = predecessors[target]
        self.cavern[target] = self.cavern[i]
        self.cavern[i] = AIR
        self.last_move[target] = self.round_number
        return target

    def dijkstra(self, i):
        predecessor = [INF] * len(self.cavern)  # the predecessor of index x is y
        distances = [INF for _ in self.cavern]  # distance from the character to the target
        distances[i] = 0  # distance to itself
        not_visited = [x for x, v in enumerate(self.cavern) if v == AIR or x == i]
        while len(not_visited) > 0:
            not_visited.sort(key=lambda x: distances[x])
            u = not_visited.pop(0)
            if distances[u] == INF:
                continue
            for neighbour in self.get_neighbours(u):
                if self.cavern[neighbour] != AIR:
                    continue
                alternative = distances[u] + 1
                if alternative < distances[neighbour]:
                    distances[neighbour] = alternative
                    predecessor[neighbour] = u
                elif alternative == distances[neighbour]:
                    prev_path = Game.get_steps_in_order(i, neighbour, predecessor)
                    former_predecessor = predecessor[neighbour]
                    predecessor[neighbour] = u
                    alternative_path = Game.get_steps_in_order(i, neighbour, predecessor)
                    if Game.first_step_smaller(prev_path, alternative_path):
                        # undo setting the new predecessor, back to the old one
                        predecessor[neighbour] = former_predecessor
        return predecessor, distances

    @staticmethod
    def first_step_smaller(a, b):
        assert len(a) == len(b)
        for i in range(len(a)):
            if a[i] == b[i]:
                continue
            return a[i] < b[i]
        assert False

    @staticmethod
    def get_steps_in_order(start: int, end: int, predecessor: List[int]):
        path = [end]
        while predecessor[end] != start:
            end = predecessor[end]
            path.append(end)
        path.append(start)
        return list(reversed(path))

    def get_neighbours(self, i):
        return restrict([i - self.width,   # above
                         i - 1,            # left
                         i + 1,            # right
                         i + self.width],  # below
                        0, self.width * self.height)

    def is_elf(self, i):
        return AIR < self.cavern[i] < WALL

    def is_goblin(self, i):
        return self.cavern[i] < AIR

    def enemy_to_attack(self, i):
        i_is_elf = self.is_elf(i)
        enemies: List[Tuple[int, int]] = []  # position, health
        for n in self.get_neighbours(i):

            if self.cavern[n] in (AIR, WALL):
                continue
            if self.is_elf(n) ^ i_is_elf:  # XOR
                enemies.append((n, abs(self.cavern[n])))
        if len(enemies) == 0:
            return None
        buffer = len(self.cavern) + 100  # whatever happens, the health is more important than position
        # Return the position (second [0]) of the best (first [0]) enemy
        return sorted(enemies, key=lambda x: buffer * x[1] + x[0], reverse=False)[0][0]

    def attack(self, enemy):
        attack = (E_ATTACK_POWER if self.is_goblin(enemy) else G_ATTACK_POWER)
        if abs(self.cavern[enemy]) - attack <= 0:  # died
            if self.is_elf(enemy):  # was elf:
                self.elf_died = True
            self.cavern[enemy] = AIR
            self.last_move[enemy] = 0
            self.check_is_game_over()
        else:
            self.cavern[enemy] += E_ATTACK_POWER if self.is_goblin(enemy) else -G_ATTACK_POWER

    def check_is_game_over(self):
        has_goblin = has_elf = False
        for i in range(len(self.cavern)):
            if self.is_goblin(i):
                has_goblin = True
            elif self.is_elf(i):
                has_elf = True
            if has_elf and has_goblin:
                return
        if not (has_goblin and has_elf):
            self.is_game_over = True


def restrict(array, min_val, max_val):
    """removes any value where min_val <= v < max_val"""
    return [x for x in array if min_val <= x < max_val]


def part1():
    game = Game.from_file()
    print(game)
    while not game.is_game_over:
        game.next_round()
        print(game.round_number)
        # print(game)
    print(game)
    print(game.elf_died)


def part2():
    elves_victories: List[Union[bool, None]] = [False] * 4
    global E_ATTACK_POWER
    E_ATTACK_POWER = 4
    while True:
        print("trying {} attack".format(E_ATTACK_POWER))
        if len(elves_victories) - 1 < E_ATTACK_POWER:
            elves_victories.extend([None] * (E_ATTACK_POWER - len(elves_victories) + 1))

        game = Game.from_file()
        while not game.elf_died and not game.is_game_over:
            game.next_round(elves_must_live=True)

        if not game.elf_died:
            elves_victories[E_ATTACK_POWER] = True
            print("Elf won at {} attack".format(E_ATTACK_POWER))
            if elves_victories[E_ATTACK_POWER - 1] is not None and not elves_victories[E_ATTACK_POWER - 1]:
                break
            max_lose = max(i for i, v in enumerate(elves_victories) if v is not None and not v)
            E_ATTACK_POWER = round((E_ATTACK_POWER+max_lose)/2)
        else:
            elves_victories[E_ATTACK_POWER] = False
            if any(victory for victory in elves_victories):
                min_vic = min(i for i, v in enumerate(elves_victories) if v)
                E_ATTACK_POWER = round((E_ATTACK_POWER+min_vic)/2)
            else:
                E_ATTACK_POWER *= 2


def part2b():
    global E_ATTACK_POWER
    E_ATTACK_POWER = 4
    while True:
        game = Game.from_file()
        while not game.elf_died and not game.is_game_over:
            game.next_round(elves_must_live=True)
        if game.elf_died:
            E_ATTACK_POWER += 1
        else:
            break


# binary search tree not working according to
# https://www.reddit.com/r/adventofcode/comments/a6chwa/2018_day_15_solutions/ebtyjs0
part2b()
