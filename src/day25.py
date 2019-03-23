import re
from typing import Set, List


class Point:
    def __init__(self, x: int, y: int, z: int, t: int):
        self.x = x
        self.y = y
        self.z = z
        self.t = t

    def manhattan(self, other: "Point"):
        return abs(self.x-other.x)+abs(self.y-other.y)+abs(self.z-other.z)+abs(self.t-other.t)

    def __repr__(self):
        return "{},{},{},{}".format(self.x,self.y,self.z,self.t)


def find_constellations(stars: Set[Point]):
    constellations: List[Set[Point]] = []
    for s1 in stars:
        for s2 in stars.difference([s1]):
            if s1.manhattan(s2) <= 3:
                added = False
                for const in constellations:
                    if s1 in const or s2 in const:
                        const.update([s1, s2])
                        added = True
                if not added:
                    constellations.append({s1, s2})
    # merge constellations containing the same star:
    for s in stars:
        new_const = []
        while constellations:
            c1 = constellations.pop()
            if s in c1:
                for c2 in constellations.copy():
                    if s in c2:
                        c1.update(c2)
                        constellations.remove(c2)
            new_const.append(c1)
        constellations = new_const


    # add missing stars as their own constellations
    for s in stars:
        exists = False
        for const in constellations:
            if s in const:
                exists = True
        if not exists:
            constellations.append({s})
    return constellations


stars = set()
with open("../input/2018/day25.txt", "r") as input:
    lines = input.readlines()
regex = re.compile(r"^(-?\d+),(-?\d+),(-?\d+),(-?\d+)$")
for line in lines:
    if len(line.strip()) == 0:
        continue
    res = regex.findall(line.strip())[0]
    stars.add(Point(int(res[0]), int(res[1]), int(res[2]), int(res[3])))
for s in stars:
    print(s)
constellations = find_constellations(stars)
print(constellations)
print(len(constellations))