import re
from typing import List, Tuple, Dict


def get_graph(steps: List[Tuple[str, str]]) -> Dict[str, List[str]]:
    graph: Dict[str, List[str]] = {}
    for l,r in steps:
        if l not in graph:
            graph[l] = []
        graph[l].append(r)
    return graph


def get_next(graph: Dict[str, List[str]], past: List[str], all_elems):
    options = set(all_elems).difference(past)
    for k, lst in graph.items():
        if k not in past:
            options = options.difference(lst)
    return sorted(options)[0]


def part1():
    steps: List[Tuple[str, str]] = []
    regex = re.compile(r"Step\s(.)\smust be finished before step\s(.)\scan begin\.")
    with open("../input/2018/day7.txt", "r") as file:
        text = file.readlines()
        for line in text:
            steps.append(regex.findall(line)[0])
    graph = get_graph(steps)
    all_elems = set(graph.keys()).union(v for sublist in graph.values() for v in sublist)
    path = []
    while len(path) < len(all_elems):
        path.append(get_next(graph, path, all_elems))
    print("".join(path))


part1()
