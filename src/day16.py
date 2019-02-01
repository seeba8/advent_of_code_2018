import re
import sys
from typing import List, Tuple, Set


class CPU:
    def __init__(self, num_registers=4, instruction_register=None):
        self.reg = [0] * num_registers
        self.opcodes = [""] * 16
        self.instruction_register = instruction_register

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
            "eqir": self.eqir,
            "eqri": self.eqri,
            "eqrr": self.eqrr,
        }
        if str(instruction).isnumeric():
            instruction = self.opcodes[instruction]
        s = "{}({},{},{}): {}".format(instruction, a, b, c, self.reg)
        options[instruction](a, b, c)
        s += " => " + str(self.reg)
        print(s)

    def possible_instructions(self, before: [], after: [], instruction):
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


def parse_file_part2(path="../input/2018/day16.txt"):
    instruction = []
    regex_instr = re.compile(r"(\d+) (\d+) (\d+) (\d+)")
    with open(path, "r") as file:
        lines = file.readlines()
        num_empty_lines = 0
        start_part_two = False
        for i, line in enumerate(lines):
            line = line.strip()
            if line == "":
                num_empty_lines += 1
            else:
                num_empty_lines = 0
            if num_empty_lines > 2:
                start_part_two = True
            if start_part_two and len(line) > 0:
                instruction.append([int(x) for x in regex_instr.findall(line)[0]])
    return instruction


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
results: List[Set[str]] = []
opcodes_rows: List[int] = []
for i in range(len(before)):
    opcode = instr[i][0]
    res = cpu.possible_instructions(before[i], after[i], instr[i])
    if len(res) > 2:
        three_or_more += 1
    if len(res) == 1:
        cpu.opcodes[opcode] = res[0]
    results.append(set(res))
    opcodes_rows.append(opcode)
print("Part 1:", three_or_more)
print()
while any([opc == "" for opc in cpu.opcodes]):
    for i in range(len(results)):
        results[i].difference_update(cpu.opcodes)
        if len(results[i]) == 1:
            cpu.opcodes[opcodes_rows[i]] = results[i].pop()
print(cpu.opcodes)
assert len(set(cpu.opcodes)) == 16
cpu.reg = [0] * 4
instructions = parse_file_part2()
print(instructions)
for instr in instructions:
    assert len(instr) == 4
    assert 0 <= instr[0] < 16
    cpu.callmethod(*instr)
print(cpu.reg)
