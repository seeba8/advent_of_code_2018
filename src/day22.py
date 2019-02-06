from typing import Dict, Optional


class Tool:
    Neither = "n"
    Climbing = "c"
    Torch = "t"


class Cave:
    def __init__(self, depth, target_x, target_y):
        self.depth = depth
        self.mouth = 0
        self.w = (target_x + 1) + 50
        self.h = (target_y + 1) + 50
        self.target = target_y * self.w + target_x
        self.geologic_index = [0] * (self.w*self.h)
        self.calculate_geologic_index()
        self.current_tool = Tool.Neither
        self.paths: Dict[str, Dict[str, int]] = {}  # location to location with cost

    def calculate_geologic_index(self):
        for y in range(self.h):
            for x in range(self.w):
                if x == 0 and y == 0:
                    self.geologic_index[y*self.w+x] = 0
                elif y*self.w+x == self.target:
                    self.geologic_index[y*self.w+x] = 0
                elif x == 0:
                    self.geologic_index[y*self.w+x] = y * 48271
                elif y == 0:
                    self.geologic_index[y*self.w+x] = x * 16807
                else:
                    self.geologic_index[y*self.w+x] = (self.get_erosion_level((y-1)*self.w+x) *
                                                       self.get_erosion_level(y*self.w+(x-1)))

    def get_erosion_level(self, i):
        return (self.geologic_index[i] + self.depth) % 20183

    def get_region_type(self, i):
        types = ["rocky", "wet", "narrow"]
        return types[self.get_risk_level(i)]

    def get_risk_level(self, i):
        return self.get_erosion_level(i) % 3

    def __str__(self):
        s = ""
        visuals = [".", "=", "|"]
        for y in range(self.h):
            for x in range(self.w):
                s += visuals[self.get_risk_level(y*self.w+x)]
            s += "\n"
        return s

    def part1(self):
        s = 0
        for y in range((self.target // self.w)+1):
            for x in range((self.target % self.w) + 1):
                s += cave.get_risk_level(y*self.w+x)
        return s

    def is_valid_tool(self, i, tool):
        if tool == Tool.Neither:
            return self.get_region_type(i) in ("wet", "narrow")
        if tool == Tool.Climbing:
            return self.get_region_type(i) in ("rocky", "wet")
        # if tool == Tool.Torch:  # last option
        return self.get_region_type(i) in ("rocky", "narrow")

    def get_neighbours(self, i):
        n = []
        if i % self.w != 0:
            n.append(i-1)
        if (i+1) % self.w != 0:
            n.append(i+1)
        if i >= self.w:
            n.append(i-self.w)
        if i + self.w < len(self.geologic_index):
            n.append(i+self.w)
        return n

    def get_paths(self):
        for i in range(len(self.geologic_index)):
            for tool in ["c", "t", "n"]:
                if not self.is_valid_tool(i, tool):
                    continue
                loc = str(i) + tool
                if loc not in self.paths:
                    self.paths[loc] = dict()

                # change tool:
                for other_tool in [x for x in ["c", "n", "t"] if x != tool]:
                    if self.is_valid_tool(i, other_tool):
                        self.paths[loc][str(i)+other_tool] = 7

                neighbours = self.get_neighbours(i)
                for n in neighbours:
                    if self.is_valid_tool(n, tool):
                        self.paths[loc][str(n)+tool] = 1

    @staticmethod
    def weighed_dijkstra(graph: Dict[str, Dict[str, int]], start: str, target: Optional[str] = None):
        predecessor = {}  # the predecessor of index x is y
        distances = {}  # distance from the source to the target
        for g in graph:
            predecessor[g] = None
            distances[g] = float("inf")
        distances[start] = 0  # distance to itself
        not_visited = [start]
        visited = set()
        while not_visited:
            not_visited.sort(key=lambda x: distances[x])
            u = not_visited.pop(0)
            visited.add(u)
            for neighbour, distance_to_neighbour in graph[u].items():
                if neighbour in visited:
                    continue
                if neighbour not in not_visited:
                    not_visited.append(neighbour)
                alternative = distances[u] + distance_to_neighbour
                if alternative < distances[neighbour]:
                    distances[neighbour] = alternative
                    predecessor[neighbour] = u
            if target is not None and u == target:
                return predecessor, distances

        return predecessor, distances


cave = Cave(10647, 7, 770)
print(cave)
# print(sum(cave.get_risk_level(i) for i in range(cave.w*cave.h)))
print(cave.part1())
cave.get_paths()
predecessor, distances = cave.weighed_dijkstra(cave.paths, "0t", str(cave.target)+"t" )
print(distances[str(cave.target)+"t"])
