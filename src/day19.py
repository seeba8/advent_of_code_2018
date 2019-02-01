from day16 import CPU
import re


with open("../input/2018/day19.txt", "r") as file:
    lines = file.readlines()

cpu = CPU(num_registers=6, instruction_register=int(lines[0][4]))
cpu.reg[0] = 1  # Part 2
regex = re.compile(r"(\w{4})\s(\d+)\s(\d+)\s(\d+)")
instructions = []
for line in lines[1:]:
    instructions.append(tuple(int(x) if i > 0 else x for i, x in enumerate(regex.findall(line)[0])))
#cpu.reg = [0,4,1551403,1,1551403,1551403]
#cpu.reg = [0,5,1551403,1,1,1551403]
#cpu.reg = [1,10,1551403,2,1,1551404]
#cpu.reg = [1,10,1551403,6,1,1551404]
#cpu.reg = [1,4,1551403,7,1551403,221629]
#cpu.reg = [8,9,1551403,7,0,1551404]
#cpu.reg = [8,9,1551403,8,0,1551404]
#cpu.reg = [8,4,1551403,17,1551403,91259]
#cpu.reg = [25,4,1551403,119,1551403,13037]
#cpu.reg = [144,4,1551403,13037,1551403,119]
#cpu.reg = [13181,4,1551403,91259,1551403,17]
#cpu.reg = [104440,4,1551403,221629,1551403,7]
#cpu.reg = [326069,9,1551403,221629,0,1551404]
#cpu.reg = [326069,4,1551403,1551403,1551403,1]
#cpu.reg = [1877472,9,1551403,1551403,0,1551402]
# all those are missing a zero, code sums prime factors

while cpu.reg[cpu.instruction_register] < len(instructions):
    cpu.callmethod(*instructions[cpu.reg[cpu.instruction_register]])
    if cpu.reg[cpu.instruction_register] + 1 < len(instructions):
        cpu.reg[cpu.instruction_register] += 1
    else:
        break
    if 1 == 0:
        print("debug start")

print("Day 19:", cpu.reg)
# 11106760
