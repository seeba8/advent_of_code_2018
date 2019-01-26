class STATES:
    OPEN = "."
    TREES = "|"
    LUMBERYARD = "#"
    VOID = "X"


class Area:
    def __init__(self, w, h):
        self.w = w
        self.h = h
        self.area = ""

    def neighbours(self, i):
        n = []
        if i >= self.w:
            if i % self.w != 0:
                n.append(i - self.w - 1)
            if (i + 1) % self.w != 0:
                n.append(i + 1 - self.w)
            n.append(i - self.w)
        if i % self.w > 0:
            n.append(i - 1)
        if (i + 1) % self.w != 0:
            n.append(i + 1)
        if i + self.w < len(self.area):
            if i % self.w != 0:
                n.append(i + self.w - 1)
            if (i + 1) % self.w != 0:
                n.append(i + 1 + self.w)
            n.append(i + self.w)
        return n

    def __str__(self):
        s = ""
        for i, v in enumerate(self.area):
            if i % self.w == 0 and i > 0:
                s += "\n"
            s += v
        return s

    def tick(self):
        new: str = self.area
        for i, v in enumerate(self.area):
            neighbours = self.neighbours(i)
            if v == STATES.OPEN:
                if sum(1 for n in neighbours if self.area[n] == STATES.TREES) >= 3:
                    new = new[:i] + STATES.TREES + new[i + 1:]
            elif v == STATES.TREES:
                if sum(1 for n in neighbours if self.area[n] == STATES.LUMBERYARD) >= 3:
                    new = new[:i] + STATES.LUMBERYARD + new[i + 1:]
            elif v == STATES.LUMBERYARD:
                if not (sum(1 for n in neighbours if self.area[n] == STATES.TREES) and
                        sum(1 for n in neighbours if self.area[n] == STATES.LUMBERYARD)):
                    new = new[:i] + STATES.OPEN + new[i + 1:]
        self.area = new

    def resource_value(self):
        return sum(1 for x in self.area if x == STATES.LUMBERYARD) * sum(1 for x in self.area if x == STATES.TREES)

    @staticmethod
    def from_file(path="../input/2018/day18.txt"):
        with open(path, "r") as f:
            lines = f.readlines()
        _area = Area(len(lines[0].strip()), len(lines))
        for y, line in enumerate(lines):
            line = line.strip()
            for x, c in enumerate(line):
                _area.area += c
        return _area


area = Area.from_file()
known_states = [area.area]
print(area)
limit = 1000000000
for i in range(1, limit + 1):
    area.tick()
    if i == 10:
        print("Part 1:", area.resource_value())
    if area.area in known_states:
        first = known_states.index(area.area)
        val = first + ((limit - first) % (i - first))  # (i-first) is the period. (limit-first) the remaining steps
        print(val)
        area.area = known_states[val]
        break
    else:
        known_states.append(area.area)
print()
print(area)
print("Part 2:", area.resource_value())
