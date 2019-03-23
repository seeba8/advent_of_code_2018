import re
from typing import List, Set


class Nanobot:
    def __init__(self, x, y, z, r):
        self.x = x
        self.y = y
        self.z = z
        self.r = r

    def __str__(self):
        return f'pos=<{self.x},{self.y},{self.z}>, r={self.r}'

    @staticmethod
    def get_best_bot(bots: List["Nanobot"]):
        best_so_far: Nanobot = None
        for bot in bots:
            if best_so_far is None or bot.r > best_so_far.r:
                best_so_far = bot
        return best_so_far

    def distance(self, bot: "Nanobot"):
        return abs(self.x - bot.x) + abs(self.y - bot.y) + abs(self.z - bot.z)

    def get_bots_in_range(self, bots: List["Nanobot"], exclude_self=False):
        in_range = []
        for bot in bots:
            if self.distance(bot) <= self.r and (bot != self or not exclude_self):
                in_range.append(bot)
        return in_range

    @staticmethod
    def bron_kerbosch1(r: Set["Nanobot"], p: Set["Nanobot"], x: Set["Nanobot"], all_bots: Set["Nanobot"],
                      cliques: List[Set["Nanobot"]]):
        if len(p) == 0 and len(x) == 0:
            cliques.append(r)
        while p:
            v = p.pop()
            p.add(v)
            Nanobot.bron_kerbosch1(r.union([v]),
                                  p.intersection(v.get_bots_in_range(all_bots, True)),
                                  x.intersection(v.get_bots_in_range(all_bots, True)),
                                  all_bots, cliques)
            p.difference_update([v])
            x.update([v])
        return cliques

    @staticmethod
    def bron_kerbosch2(r: Set["Nanobot"], p: Set["Nanobot"], x: Set["Nanobot"], all_bots: Set["Nanobot"],
                       cliques: List[Set["Nanobot"]]):
        if len(p) == 0 and len(x) == 0:
            cliques.append(r)
        u = None
        if p:
            u = p.pop()

        u_neighbours = u.get_bots_in_range(all_bots, True) if u is not None else None
        while p.difference(u_neighbours):
            v = p.difference(u_neighbours).pop()
            p.add(v)
            v_neighbours = v.get_bots_in_range(all_bots, True)
            Nanobot.bron_kerbosch2(r.union([v]),
                                  p.intersection(v_neighbours),
                                  x.intersection(v_neighbours),
                                  all_bots, cliques)
            p.difference_update([v])
            x.update([v])
        return cliques

    @staticmethod
    def get_graph(r: set["Nanobot"]):
        #for bot in r:
        pass


with open("../input/2018/day23.txt", "r") as file:
    bot_text = file.readlines()
bots = []
regex = re.compile(r"pos=<(-?\d+),(-?\d+),(-?\d+)>, r=(\d+)")
for line in bot_text:
    if len(line) > 0:
        x, y, z, r = (int(x) for x in regex.findall(line)[0])
        bots.append(Nanobot(x, y, z, r))
        print(bots[-1])

best_bot = Nanobot.get_best_bot(bots)
print(len(best_bot.get_bots_in_range(bots)))

print(best_bot)
print(max(bot.x for bot in bots), min(bot.x for bot in bots))
print(max(bot.y for bot in bots), min(bot.y for bot in bots))
print(max(bot.z for bot in bots), min(bot.z for bot in bots))
q = Nanobot.bron_kerbosch2(set(), set(bots), set(), set(bots.copy()), list())
print(q)
