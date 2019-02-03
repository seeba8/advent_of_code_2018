from day16 import CPU
import re


with open("../input/2018/day21.txt", "r") as file:
    lines = file.readlines()

cpu = CPU(num_registers=6, instruction_register=int(lines[0][4]))
cpu.reg[0] = 0  # Part 2
regex = re.compile(r"(\w{4})\s(\d+)\s(\d+)\s(\d+)")
instructions = []
for line in lines[1:]:
    instructions.append(tuple(int(x) if i > 0 else x for i, x in enumerate(regex.findall(line)[0])))
while cpu.reg[cpu.instruction_register] < len(instructions):
    cpu.callmethod(*instructions[cpu.reg[cpu.instruction_register]])
    if cpu.reg[cpu.instruction_register] + 1 < len(instructions):
        cpu.reg[cpu.instruction_register] += 1
    else:
        break
