from typing import Dict, Tuple, List


class Garden:
    def __init__(self):
        self.pots: List[bool] = []
        self.growing_rules: List[List[bool, bool, bool, bool, bool]] = []
        self.zero = 0

    def load_file(self):
        with open("../input/2018/day12.txt", "r") as file:
            lines = file.readlines()
            initial_state = lines[0].strip()
            for i, c in enumerate(initial_state[len("initial state: "):]):
                self.pots.append(c == "#")
            for rule in lines[2:]:
                rule = rule.strip()
                if len(rule) == 0 or rule[-1] == ".":
                    continue
                # it is a growing rule:
                self.growing_rules.append(list(c == "#" for c in rule[:5]))

    def grow(self):
        buff = [False] * 5 + self.pots + [False] * 5
        new_pots = []
        for i in range(len(buff) - 5):
            new_pots.append(buff[i:i+5] in self.growing_rules)
        new_idx = new_pots.index(True)
        self.pots = new_pots[new_idx:Garden.find_last_plant(new_pots) + 1]
        # self.pots = new_pots
        self.zero += 3 - new_idx

    def print_pots(self):
        print("".join("#" if b else "." for b in self.pots))

    def get_sum(self):
        return sum(k-self.zero for k, v in enumerate(self.pots) if v)

    @staticmethod
    def find_last_plant(l):
        for k, v in enumerate(reversed(l)):
            if v:
                return len(l) - 1 - k


def calc_score(x):
    return 34*x + 11

import time, os
start_time = time.time()
garden = Garden()
garden.load_file()
garden.print_pots()
previous_garden = []
for i in range(1, 50000000001):
    if i % 10000 == 0:
        print("--- %s seconds ---" % (time.time() - start_time))
        print("Garden size: {}".format(len(garden.pots)))
        garden.print_pots()
    garden.grow()
    previous_garden = garden.pots

    garden.print_pots()
    print(i, garden.get_sum())

# Schema: +1 iteration = score + 34
# so its 34x + c. what is c?
# 80353 = 34*2363 + c
# c = 80353 - 34*2363
# c = 11
# => 34*50000000000+11
print(garden.get_sum())

