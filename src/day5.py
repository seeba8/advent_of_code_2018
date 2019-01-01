def react(polymer: str) -> str:
    before = ""
    while before != polymer:
        before = polymer
        for i in range(26):
            polymer = polymer.replace(chr(65 + i) + chr(97 + i), "").replace(chr(97 + i) + chr(65 + i), "")
    return polymer

def part1():
    print("PART 1")
    polymer: str = ""
    with open("../input/2018/day5.txt", "r") as file:
        polymer = file.read().strip()
    print("Len before:", len(polymer))
    polymer = react(polymer)
    print("Len after:", len(polymer))

def part2():
    print("PART 2")
    polymer: str = ""
    with open("../input/2018/day5.txt", "r") as file:
        polymer = file.read().strip()
    optimised = []
    for i in range(26):
        new_polymer = polymer.replace(chr(65+i), "").replace(chr(97+i), "")
        optimised.append(len(react(new_polymer)))
    print(min(optimised))


part1()
part2()