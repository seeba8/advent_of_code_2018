import re
import sys


class CPU:
    def __init__(self):
        self.reg = [0] * 4

    def addr(self, a, b, c):
        self.reg[c] = self.reg[a] + self.reg[b]

    def addi(self, a, b, c):
        self.reg[c] = self.reg[a] + b

    def mulr(self, a, b, c):
        self.reg[c] = self.reg[a] * self.reg[b]

    def muli(self, a, b, c):
        self.reg[c] = self.reg[a] * b

    def banr(self, a, b, c):
        self.reg[c] = self.reg[a] & self.reg[b]

    def bani(self, a, b, c):
        self.reg[c] = self.reg[a] & b

    def borr(self, a, b, c):
        self.reg[c] = self.reg[a] | self.reg[b]

    def bori(self, a, b, c):
        self.reg[c] = self.reg[a] | b

    def setr(self, a, b, c):
        self.reg[c] = self.reg[a]

    def seti(self, a, b, c):
        self.reg[c] = a

    def gtir(self, a, b, c):
        self.reg[c] = int(a > self.reg[b])

    def gtri(self, a, b, c):
        self.reg[c] = int(self.reg[a] > b)

    def gtrr(self, a, b, c):
        self.reg[c] = int(self.reg[a] > self.reg[b])

    def eqir(self, a, b, c):
        self.reg[c] = int(a == self.reg[b])

    def eqri(self, a, b, c):
        self.reg[c] = int(self.reg[a] == b)

    def eqrr(self, a, b, c):
        self.reg[c] = int(self.reg[a] == self.reg[b])

    def callmethod(self, instruction, a, b, c):
        options = {
            "addr": self.addr,
            "addi": self.addi,
            "mulr": self.mulr,
            "muli": self.muli,
            "banr": self.banr,
            "bani": self.bani,
            "borr": self.borr,
            "bori": self.bori,
            "setr": self.setr,
            "seti": self.seti,
            "gtir": self.gtir,
            "gtri": self.gtri,
            "gtrr": self.gtrr,
            "eqir": self.eqri,
            "eqri": self.eqri,
            "eqrr": self.eqrr,
        }
        options[instruction](a, b, c)

    def possible_instructions(self, before: [], after: [], instruction):
        print(before, after, instruction)
        options = {
            "addr": self.addr,
            "addi": self.addi,
            "mulr": self.mulr,
            "muli": self.muli,
            "banr": self.banr,
            "bani": self.bani,
            "borr": self.borr,
            "bori": self.bori,
            "setr": self.setr,
            "seti": self.seti,
            "gtir": self.gtir,
            "gtri": self.gtri,
            "gtrr": self.gtrr,
            "eqir": self.eqir,
            "eqri": self.eqri,
            "eqrr": self.eqrr,
        }
        possible_instructions = []
        for k, instr in options.items():
            self.reg = before.copy()
            instr(*instruction[1:])
            if self.reg == after:
                possible_instructions.append(k)
        return possible_instructions


def parse_file_part1(path="../input/2018/day16.txt"):
    before = []
    after = []
    instruction = []
    regex = re.compile(r"(\d+), (\d+), (\d+), (\d+)")
    regex_instr = re.compile(r"(\d+) (\d+) (\d+) (\d+)")
    with open(path, "r") as file:
        lines = file.readlines()
        for i, line in enumerate(lines):
            if i % 4 == 0 and len(line.strip()) == 0:
                return before, after, instruction
            if i % 4 == 0:
                before.append([int(x) for x in regex.findall(line)[0]])
            if i % 4 == 1:
                instruction.append([int(x) for x in regex_instr.findall(line)[0]])
            if i % 4 == 2:
                after.append([int(x) for x in regex.findall(line)[0]])


def parse_example(str):
    before = []
    after = []
    instruction = []
    regex = re.compile(r"(\d+), (\d+), (\d+), (\d+)")
    regex_instr = re.compile(r"(\d+) (\d+) (\d+) (\d+)")
    for i, line in enumerate(str.split("\n")):
        if i % 4 == 0:
            before = list([int(x) for x in regex.findall(line)[0]])
        if i % 4 == 1:
            instruction = list([int(x) for x in regex_instr.findall(line)[0]])
        if i % 4 == 2:
            after = list([int(x) for x in regex.findall(line)[0]])
    return before, after, instruction


three_or_more = 0
cpu = CPU()

before, after, instr = parse_file_part1()
for i in range(len(before)):
    res = cpu.possible_instructions(before[i], after[i], instr[i])
    print(res)
    if len(res) > 2:
        three_or_more += 1
print(three_or_more)
print()

