from typing import List, Tuple, Dict
import json
import math

def print_areas(areas: Dict[Tuple[int, int], int]):
    xmin, xmax = min([k for (k, _) in areas.keys()]), max([k for (k, _) in areas.keys()])
    ymin, ymax = min([k for (_, k) in areas.keys()]), max([k for (_, k) in areas.keys()])
    plot = list()
    for y in range(ymin, ymax + 1):
        plot.append(list())
        for x in range(xmin, xmax + 1):
        #    print("| " + str(areas[(x, y)] if (x, y) in areas else " ") + " ", end="")
            plot[y-ymin].append(areas[(x, y)] if (x, y) in areas else None)
        #print()
    sizes = [0]*(max(areas.values())+1)
    for (x,y), i in areas.items():
            if not sizes[areas[(x,y)]] == math.inf:
                if (x-1,y) not in areas or (x+1, y) not in areas or (x,y-1) not in areas or (x,y+1) not in areas:
                    sizes[areas[(x,y)]] = math.inf
                else:
                    sizes[areas[(x,y)]] += 1
    print(sizes)


def handle_field(x, y, i, old, areas):
    if (x, y) not in old:
        if (x, y) in areas and areas[(x,y)] != i:
            areas[(x, y)] = -1
        else:
            areas[(x, y)] = i
            return i


def own_area(coords: List[Tuple[int, int]]) -> List[int]:
    areas: Dict[Tuple[int, int], int] = {}
    for i, (x, y) in enumerate(coords):
        areas[(x, y)] = i
    prev_vals = set()
    c = 0
    while c < 100:
        c += 1
        added_vals = set()
        new_fields: List[Tuple[int, int]] = []
        old = areas.copy()
        for (x, y), i in old.items():
            added_vals.add(handle_field(x-1, y, i, old, areas))
            added_vals.add(handle_field(x+1, y, i, old, areas))
            added_vals.add(handle_field(x, y-1, i, old, areas))
            added_vals.add(handle_field(x, y+1, i, old, areas))
        #if prev_vals == added_vals:
        #    break
        prev_vals = added_vals
    print_areas(areas)
    print(c)


def part1():
    coords: List[Tuple[int, int]] = []
    with open("../input/2018/day6.txt", "r") as file:
        lines = file.readlines()
        for l in lines:
            (a, b) = l.strip().split(",")
            coords.append((int(a), int(b)))
    print(coords)
    own_area(coords)

def calculate_region(coords: List[Tuple[int, int]], maxdist):
    xmin, xmax = min([k for (k, _) in coords]), max([k for (k, _) in coords])
    ymin, ymax = min([k for (_, k) in coords]), max([k for (_, k) in coords])
    xdelta = xmax-xmin
    ydelta = ymax-ymin
    middlex, middley = sum(x for x, _ in coords) / len(coords), sum(y for _, y in coords) / len(coords)
    region_size = 0
    for x in range(xmin, xmax):
        print(x)
        for y in range(ymin, ymax):
                if sum(abs(x-px)+abs(y-py) for px,py in coords) < maxdist:
                    region_size += 1
    print(region_size)

def part2():
    maxdist = 10000
    coords: List[Tuple[int, int]] = []
    with open("../input/2018/day6.txt", "r") as file:
        lines = file.readlines()
        for l in lines:
            (a, b) = l.strip().split(",")
            coords.append((int(a), int(b)))

    #print(xmin, xmax, ymin, ymax)
    calculate_region(coords, maxdist)


#part1()
#own_area([(1, 1), (1, 6), (8, 3), (3, 4), (5, 5), (8, 9)])

part2()