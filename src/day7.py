import re
from typing import List, Tuple, Dict


def get_graph(steps: List[Tuple[str, str]]) -> Dict[str, List[str]]:
    graph: Dict[str, List[str]] = {}
    for l,r in steps:
        if l not in graph:
            graph[l] = []
        graph[l].append(r)
    return graph


def get_next(graph: Dict[str, List[str]], past: List[str], current: List[str], all_elems):
    options = set(all_elems).difference(past).difference(current)
    for k, lst in graph.items():
        if k not in past:
            options = options.difference(lst)
    return sorted(options)[0] if len(options) > 0 else None


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
        path.append(get_next(graph, path, [], all_elems))
    print("".join(path))


def part2(testdata: Dict[str, List[str]] = None, num_workers = 5, default_effort = 60):
    steps: List[Tuple[str, str]] = []
    regex = re.compile(r"Step\s(.)\smust be finished before step\s(.)\scan begin\.")
    with open("../input/2018/day7.txt", "r") as file:
        text = file.readlines()
        for line in text:
            steps.append(regex.findall(line)[0])
    graph = get_graph(steps)
    if testdata is not None:
        graph = testdata
    busy_until = [0]*num_workers
    working_on = [""]*num_workers
    all_elems = set(graph.keys()).union(v for sublist in graph.values() for v in sublist)
    path = []
    current_time = 0
    while len(path) < len(all_elems):
        for i in range(num_workers):
            if busy_until[i] <= current_time:
                if working_on[i] != "":
                    path.append(working_on[i])
                next_task = get_next(graph, path, working_on, all_elems)
                working_on[i] = ""
                if next_task is not None:
                    working_on[i] = next_task
                    busy_until[i] = current_time + (ord(working_on[i]) - 64) + default_effort
                    print("Second {}. Worker {} starts on {}, duration {}".format(current_time, i, working_on[i],
                                                                                  ord(working_on[i]) - 64))
        current_time += 1
    print("".join(path))
    print(max(busy_until))



#part1()
part2({
    "A": ["B", "D"],
    "B": ["E"],
    "C": ["A", "F"],
    "D": ["E"],
    "E": [],
    "F": ["E"]
}, 2, 0)
part2()
