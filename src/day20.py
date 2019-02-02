from collections import namedtuple
from typing import Dict, Tuple, List, Set


Point = namedtuple("Point", ["x", "y"])


class Labyrinth:
    def __init__(self):
        self.doors = set()
        self.regex = ""
        self.min_x = self.max_x = self.min_y = self.max_y = 0

    def __str__(self):
        s = ""
        # s += "x({}-{}), y({}-{})\n".format(self.min_x, self.max_x, self.min_y, self.max_y)
        # s += str(self.doors) + "\n"
        for y in range(self.min_y - 1, self.max_y + 2):
            for x in range(self.min_x - 1, self.max_x + 2):
                if Point(x, y) in self.doors:
                    s += "|" if y % 2 == 0 else "-"
                elif y % 2 == 0 and x % 2 == 0:
                    s += "." if x != 0 or y != 0 else "X"
                else:
                    s += "#"
            s += "\n"
        return s

    @staticmethod
    def from_file(path="../input/2018/day20.txt"):
        _l = Labyrinth()
        with open(path, "r") as file:
            regex = file.readlines()[0]
        print(regex)
        _l.regex = regex
        return _l

    def build(self, i=0, start=Point(0, 0)):
        positions = [Point(start.x, start.y)]
        endpoints = set()
        r = self.regex
        while i < len(r):
            # c = r[i]
            new_pos = []
            while positions:
                pos = positions.pop()
                if r[i] == "N":
                    self.doors.add(Point(pos.x, pos.y - 1))
                    new_pos = [pos._replace(y=pos.y - 2)]
                elif r[i] == "E":
                    self.doors.add(Point(pos.x + 1, pos.y))
                    new_pos = [pos._replace(x=pos.x + 2)]
                elif r[i] == "S":
                    self.doors.add(Point(pos.x, pos.y + 1))
                    new_pos = [pos._replace(y=pos.y + 2)]
                elif r[i] == "W":
                    self.doors.add(Point(pos.x - 1, pos.y))
                    new_pos = [pos._replace(x=pos.x - 2)]
                elif r[i] == "(":
                    # old_i = i
                    i, new_pos = self.build(i+1, pos)
                    # print("{}: {}".format(old_i, i))
                elif r[i] == "|":
                    endpoints.add(pos)
                    new_pos = [Point(start.x, start.y)]
                elif r[i] == ")":
                    endpoints.add(pos)
                    return i, endpoints
                else:
                    new_pos = [pos]
            positions.extend(new_pos)
            self.min_x = min([self.min_x] + [pos.x for pos in positions])
            self.max_x = max([self.max_x] + [pos.x for pos in positions])
            self.min_y = min([self.min_y] + [pos.y for pos in positions])
            self.max_y = max([self.max_y] + [pos.y for pos in positions])
            i += 1

    def get_graph(self) -> Dict[Point, Set[Point]]:
        graph = {}
        visited = set()
        positions = {Point(0, 0)}
        while positions:
            pos = positions.pop()
            if pos in visited:
                continue
            visited.add(pos)
            if pos not in graph:
                graph[pos] = set()
            if Point(pos.x - 1, pos.y) in self.doors:
                new_room = Point(pos.x - 2, pos.y)
                graph[pos].add(new_room)
                positions.add(new_room)
            if Point(pos.x + 1, pos.y) in self.doors:
                new_room = Point(pos.x + 2, pos.y)
                graph[pos].add(new_room)
                positions.add(new_room)
            if Point(pos.x, pos.y - 1) in self.doors:
                new_room = Point(pos.x, pos.y - 2)
                graph[pos].add(new_room)
                positions.add(new_room)
            if Point(pos.x, pos.y + 1) in self.doors:
                new_room = Point(pos.x, pos.y + 2)
                graph[pos].add(new_room)
                positions.add(new_room)
        return graph

    def most_doors(self):
        graph = self.get_graph()
        print(graph)
        predecessors, distances = Labyrinth.dijkstra(graph)
        print(distances)
        print("Part 1:", max(distances.values()))
        print("Part 2:", len([x for x in distances.values() if x >= 1000]))

    @staticmethod
    def dijkstra(graph: Dict[Point, Set[Point]], start=Point(0, 0)):
        predecessor = {}  # the predecessor of index x is y
        distances = {}  # distance from the source to the target
        for g in graph:
            predecessor[g] = None
            distances[g] = float("inf")
        distances[start] = 0  # distance to itself
        not_visited = list(graph.keys())
        while not_visited:
            not_visited.sort(key=lambda x: distances[x])
            u = not_visited.pop(0)
            if distances[u] == float("inf"):
                continue
            for neighbour in graph[u]:
                alternative = distances[u] + 1
                if alternative < distances[neighbour]:
                    distances[neighbour] = alternative
                    predecessor[neighbour] = u
        return predecessor, distances

    def disentangle_brackets(self):
        stack = []
        s = ""
        for i, c in enumerate(self.regex):
            if c == "(":
                stack.append(i)
            elif c == ")":
                s += "{}: {}\n".format(stack.pop(), i)
        return s


labyrinth = Labyrinth.from_file()
# labyrinth.disentangle_brackets()
labyrinth.build()
print(labyrinth)
labyrinth.most_doors()

