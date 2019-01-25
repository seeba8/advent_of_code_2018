import re


class STATES:
    SAND = 0
    CLAY = 1
    STILL_WATER = 2
    FLOWING_WATER = 3
    SPRING = 4
    OUT_OF_BOUNDS = -1


class Arctic:
    def __init__(self, w, h, spring_x, spring_y):
        self.ground = [STATES.SAND] * w * h
        self.w = w
        self.h = h
        self.moving = set()
        self.set(STATES.SPRING, spring_x, spring_y)

    def set(self, state,  x, y=None):
        if y is not None:
            self.ground[y * self.w + x] = state
            if state in (STATES.SPRING, STATES.FLOWING_WATER):
                self.moving.add(y * self.w + x)
        else:
            self.ground[x] = state
            if state in (STATES.SPRING, STATES.FLOWING_WATER):
                self.moving.add(x)

    def get(self, x, y=None):
        if y is not None:
            return self.ground[y * self.w + x] if y * self.w + x < self.w * self.h else STATES.OUT_OF_BOUNDS
        return self.ground[x] if x < self.w * self.h else STATES.OUT_OF_BOUNDS

    def amount_of_water(self):
        return sum(1 for x in self.ground if x in (STATES.STILL_WATER, STATES.FLOWING_WATER))

    def count_still_water(self):
        return sum(1 for x in self.ground if x == STATES.STILL_WATER)

    def fill_row_if_full(self, i):
        min_x = max_x = i
        can_fill = True
        while can_fill:
            min_x -= 1
            if self.get(min_x) == STATES.SAND:
                can_fill = False
                break
            if self.get(min_x) == STATES.CLAY:
                min_x += 1
                break
        while can_fill:
            max_x += 1
            if self.get(max_x) == STATES.SAND:
                can_fill = False
                break
            if self.get(max_x) == STATES.CLAY:
                max_x -= 1
                break
        if can_fill:
            for x in range(min_x, max_x+1):
                self.set(STATES.STILL_WATER, x)
                if self.get(x-self.w) == STATES.FLOWING_WATER:
                    self.moving.add(x-self.w)

    def flow(self):
        while self.moving:
            i = self.moving.pop()
            if self.get(i + self.w) == STATES.SAND:
                self.set(STATES.FLOWING_WATER, i+self.w)
            else:
                if self.get(i + self.w) == STATES.CLAY and self.get(i + 1) == STATES.SAND:
                    self.set(STATES.FLOWING_WATER, i + 1)  # Cliff
                if self.get(i + self.w) == STATES.CLAY and self.get(i - 1) == STATES.SAND:
                    self.set(STATES.FLOWING_WATER, i - 1)  # Cliff
                if self.get(i + self.w) in (STATES.STILL_WATER, STATES.CLAY):
                    if self.get(i - 1) == STATES.SAND and self.get(i - 1 + self.w) in (STATES.CLAY, STATES.STILL_WATER):
                        self.set(STATES.FLOWING_WATER, i - 1)
                    if self.get(i + 1) == STATES.SAND and self.get(i + 1 + self.w) in (STATES.CLAY, STATES.STILL_WATER):
                        self.set(STATES.FLOWING_WATER, i + 1)
                self.fill_row_if_full(i)

    def __str__(self):
        s = ""
        reprs = {STATES.SPRING: "+", STATES.CLAY: "#", STATES.SAND: ".", STATES.FLOWING_WATER: "|",
                 STATES.STILL_WATER: "~"}
        for i, v in enumerate(self.ground):
            if i % self.w == 0 and i != 0:
                s += "\n"
            s += reprs[v]
        return s

    @staticmethod
    def from_file(path="../input/2018/day17.txt"):
        regex = re.compile(r"(\w)=(\d+), (\w)=(\d+)\.\.(\d+)")
        values = set()
        with open(path, "r") as file:
            lines = file.readlines()
        for line in lines:
            reg_result = regex.findall(line)[0]
            if reg_result[0] == "x":
                values.update((int(reg_result[1]), y) for y in range(int(reg_result[3]), int(reg_result[4]) + 1))
            else:
                values.update((x, int(reg_result[1])) for x in range(int(reg_result[3]), int(reg_result[4]) + 1))
        print(values)
        xmin, xmax = min(a[0] for a in values), max(a[0] for a in values)
        ymin, ymax = min(a[1] for a in values), max(a[1] for a in values)
        print(xmin, xmax, ymin, ymax)
        _arctic = Arctic(w=xmax - xmin + 3, h=ymax - ymin + 2, spring_x=500-xmin + 3, spring_y=0)
        for x_val, y_val in values:
            _arctic.set(STATES.CLAY, x_val - xmin + 1, y_val - ymin + 1)
        return _arctic

    @staticmethod
    def from_solution(path="../input/2018/day17_2.txt"):
        with open(path, "r") as file:
            lines = file.readlines()
        _arctic = Arctic(w=len(lines[0].strip()), h=len(lines)+1, spring_x=153, spring_y=0)
        for y, line in enumerate(lines):
            line = line.strip()
            for x, c in enumerate(line):
                if c == "#":
                    _arctic.set(STATES.CLAY, x, y+1)
        return _arctic


arctic = Arctic.from_file()
arctic.flow()
print(arctic.amount_of_water())
print(arctic)
print(arctic.count_still_water())
