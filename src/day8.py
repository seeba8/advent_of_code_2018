from typing import List, Tuple


class Node:
    def __init__(self):
        self.metadata: List[int] = []
        self.children: List["Node"] = []

    def iter_metadata(self):
        for m in self.metadata:
            yield m
        for x in self.children:
            for a in x.iter_metadata():
                yield a

    def get_value(self):
        if len(self.children) == 0:
            return sum(self.metadata)
        # else:
        value = 0
        for m in self.metadata:
            if m-1 < len(self.children):
                value += self.children[m-1].get_value()
        return value


def parse_input(values: List[int]) -> Tuple[Node, int]:
    """
    :param values:
    :return: Tuple [Node, position where node ends
    """
    this_node = Node()
    child_nodes = values[0]
    metadata_entries = values[1]
    if child_nodes == 0:
        this_node.metadata = values[2:(2+metadata_entries)]
        return this_node, 2+metadata_entries
    else:
        childnode_start = 2
        for c in range(child_nodes):
            child_node, next_child = parse_input(values[childnode_start:])
            this_node.children.append(child_node)
            childnode_start += next_child
        this_node.metadata = values[childnode_start:childnode_start+metadata_entries]
    return this_node, childnode_start + metadata_entries


def part1():
    text = ""
    with open("../input/2018/day8.txt", "r") as file:
        text = file.readlines()[0]
    if len(text) == 0:
        return
    values = [int(x) for x in text.split(" ")]
    rootnode,_ = parse_input(values)
    print(sum(x for x in rootnode.iter_metadata()))
    return rootnode

def part2(rootnode):
    print(rootnode.get_value())


#rootnode, _ = parse_input([2,3,0,3,10,11,12,1,1,0,1,99,2,1,1,2])
#print(sum(x for x in rootnode.iter_metadata()))
#print(rootnode.get_value())

rootnode = part1()
part2(rootnode)