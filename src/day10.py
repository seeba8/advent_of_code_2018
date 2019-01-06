import matplotlib.pyplot as plt
import re
from typing import List


class Sky:
    def __init__(self):
        self.stars: List[Star] = []
        self.stepsize = 1
        self.time = 0

    def positions(self):
        while True:
            x, y = [], []
            for star in self.stars:
                x.append(star.position[0])
                y.append(star.position[1])
                star.move(self.stepsize)
            self.time += self.stepsize
            yield x, y

    def animate(self):
        plt.ion()
        pause = .0005
        for x,y in self.positions():

            if min(y) >= 160 and max(y) <= 197: #min(x) > -100:
                print(self.time-self.stepsize)
                pause = 100
                self.stepsize = 1
            else:
                pause = .00005
                self.stepsize = 5
            y = [-i for i in y]
            plt.plot(x, y, marker='.', color='r', ls='')
            plt.draw()
            plt.pause(pause)
            plt.clf()


class Star:
    def __init__(self, position, velocity):
        self.position = position
        self.velocity = velocity

    def move(self, factor=1):
        self.position = (self.position[0] + factor * self.velocity[0],
                         self.position[1] + factor * self.velocity[1])


def parse_input(data: List[str]):
    sky = Sky()
    regex = re.compile(r"position=<\s*(-?\d+),\s*(-?\d+)> velocity=<\s*(-?\d+),\s*(-?\d+)>")
    for line in data:
        line = line.strip()
        x, y, vx, vy = regex.findall(line)[0]
        sky.stars.append(Star((int(x), int(y)), (int(vx), int(vy))))
    return sky


def test_part1():
    data = """position=< 9,  1> velocity=< 0,  2>
position=< 7,  0> velocity=<-1,  0>
position=< 3, -2> velocity=<-1,  1>
position=< 6, 10> velocity=<-2, -1>
position=< 2, -4> velocity=< 2,  2>
position=<-6, 10> velocity=< 2, -2>
position=< 1,  8> velocity=< 1, -1>
position=< 1,  7> velocity=< 1,  0>
position=<-3, 11> velocity=< 1, -2>
position=< 7,  6> velocity=<-1, -1>
position=<-2,  3> velocity=< 1,  0>
position=<-4,  3> velocity=< 2,  0>
position=<10, -3> velocity=<-1,  1>
position=< 5, 11> velocity=< 1, -2>
position=< 4,  7> velocity=< 0, -1>
position=< 8, -2> velocity=< 0,  1>
position=<15,  0> velocity=<-2,  0>
position=< 1,  6> velocity=< 1,  0>
position=< 8,  9> velocity=< 0, -1>
position=< 3,  3> velocity=<-1,  1>
position=< 0,  5> velocity=< 0, -1>
position=<-2,  2> velocity=< 2,  0>
position=< 5, -2> velocity=< 1,  2>
position=< 1,  4> velocity=< 2,  1>
position=<-2,  7> velocity=< 2, -2>
position=< 3,  6> velocity=<-1, -1>
position=< 5,  0> velocity=< 1,  0>
position=<-6,  0> velocity=< 2,  0>
position=< 5,  9> velocity=< 1, -2>
position=<14,  7> velocity=<-2,  0>
position=<-3,  6> velocity=< 2, -1>"""
    sky = parse_input(data.split("\n"))
    sky.animate()


def part1():
    with open("../input/2018/day10.txt", "r") as file:
        input = file.readlines()
        sky = parse_input(input)
        for star in sky.stars:
            star.move(10000)
        sky.time = 10000
        sky.animate()

# test_part1()
part1()
