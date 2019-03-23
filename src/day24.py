from typing import List
import re
from math import floor


class Group:
    def __init__(self,
                 units: int,
                 hp: int,
                 ap: int,
                 at: str,
                 initiative: int,
                 weaknesses: List[str],
                 immunities: List[str]):
        self.units = units
        self.health = hp
        self.attack = ap
        self.attack_type = at
        self.initiative = initiative
        self.weaknesses = weaknesses
        self.immunities = immunities
        self.is_target = False
        self.target: "Group" = None

    def effective_power(self):
        return self.units * self.attack

    def incoming_attack(self, ap: int, type: str, simulate=False):
        if type in self.immunities:
            return 0
        modifier = 1
        if type in self.weaknesses:
            modifier = 2
        if not simulate:
            self.units =max(0,self.units - floor((modifier * ap) / self.health))
        return modifier * ap

    def __str__(self):
        return "Units: {}, HP: {}, AP: {} ({}), Initiative: {}, Weaknesses: {}, Immunities: {} => {}".format(
            self.units, self.health, self.attack, self.attack_type, self.initiative, self.weaknesses, self.immunities,
            self.effective_power()
        )

    @staticmethod
    def __parse_features(line: str):
        weaknesses = []
        immunities = []
        current = weaknesses
        for word in line.split(" "):
            word = word.strip(" ,;()")
            if len(word) == 0:
                continue
            if word == "weak":
                current = weaknesses
            elif word == "immune":
                current = immunities
            elif word == "to":
                continue
            else:
                current.append(word)
        return weaknesses, immunities

    @staticmethod
    def from_line(line: str, boost: int = 0):
        regex = re.compile(r"^(\d+) units each with (\d+) hit points (\(.*\))?\s?with an attack that does " +
                           "(\d+) (\w+) damage at initiative (\d+)$")
        res = regex.findall(line)[0]
        group = Group(int(res[0]), int(res[1]), int(res[3]) + boost, res[4], int(res[5]), *Group.__parse_features(res[2]))
        return group


class Fight:
    def __init__(self, boost=0):
        self.boost = boost
        self.immune_system: List[Group] = []
        self.infection: List[Group] = []
        with open("../input/2018/day24.txt", "r") as f:
            lines = f.readlines()
        current = self.immune_system
        for current_line in lines[1:]:
            if len(current_line.strip()) == 0:
                continue
            if current_line.strip() == "Infection:":
                current = self.infection
                continue
            current.append(Group.from_line(current_line, boost if current == self.immune_system else 0))

    def sort_groups(self):
        self.immune_system.sort(key=lambda x: x.effective_power() + (1 / x.initiative), reverse=True)
        self.infection.sort(key=lambda x: x.effective_power() + (1 / x.initiative), reverse=True)

    def get_target(self, current: Group, opponents: List[Group]):
        best_attack = 0
        final_opponent: Group = None
        for opponent in opponents:
            if opponent.is_target or opponent.units == 0:
                continue
            att = opponent.incoming_attack(current.effective_power(), current.attack_type, True)
            if att == 0:
                continue
            if (
                    best_attack < att
            ) or (
                    best_attack == att and final_opponent.effective_power() < opponent.effective_power()
            ) or (
                    best_attack == att and final_opponent.effective_power() == opponent.effective_power() and
                    final_opponent.initiative < opponent.initiative
            ):
                best_attack, final_opponent = att, opponent
        return final_opponent

    def target_selection(self):
        self.sort_groups()
        for x in self.infection:
            x.is_target = False
            x.target = None
        for x in self.immune_system:
            x.is_target = False
            x.target = None
        all_groups = self.immune_system + self.infection
        all_groups.sort(key=lambda x: x.effective_power() + (1 / x.initiative), reverse=True)
        while all_groups:
            current = all_groups.pop(0)
            if current.units == 0:
                continue
            if current in self.infection:
                target = self.get_target(current, self.immune_system)
            else:
                target = self.get_target(current, self.infection)
            if target is not None:
                current.target = target
                target.is_target = True

    def attacking_phase(self):
        all_groups = self.immune_system + self.infection
        all_groups.sort(key=lambda x: x.initiative, reverse=True)
        for g in all_groups:
            if g.units == 0 or g.target is None:
                continue
            if self.boost == 58:
                print("Group ({}U) => Group ({}U)".format(g.units, g.target.units))
                if g.units == 874:
                    print("debug")
            g.target.incoming_attack(g.effective_power(), g.attack_type)

    def next_round(self):
        # self.print_groups()
        self.target_selection()
        self.attacking_phase()

    def fight(self):
        while sum(x.units for x in self.infection) > 0 and sum(x.units for x in self.immune_system) > 0:
            f.next_round()
        # self.print_groups()
        # print(sum(x.units for x in self.infection + self.immune_system))
        return sum(x.units for x in self.infection) == 0

    def print_groups(self):
        print()
        print("Immune System:")
        for x in self.immune_system:
            if x.units > 0:
                print(x)
        print("Infection:")
        for x in self.infection:
            if x.units > 0:
                print(x)

f = Fight()
f.fight()

# Part 2
i = 59  # 58 runs in an endless circle because immune system and viruses are in a stalemate and can't hurt each other
f = Fight(i)
while not f.fight():
    i += 1
    f = Fight(i)
    print(i)
print(sum(x.units for x in f.immune_system))