from collections import namedtuple
import numpy as np
LargestSquare = namedtuple("LargestSquare", "x y power_level size")


class Grid:
    def __init__(self, width=300, height=300, serial_number=7400):
        self.width = width
        self.height = height
        # self.__power_levels = [0] * (self.width * self.height)
        self.__power_levels = np.zeros((self.width, self.height))
        self.serial_number = serial_number

    def __get_index(self, x, y):
        return (y - 1) * self.width + (x - 1)

    def __calculate_power_level(self, x, y):
        rack_id = x + 10
        power_level = rack_id * y
        power_level += self.serial_number
        power_level *= rack_id
        power_level = Grid.hundreds_digit(power_level)
        power_level -= 5
        return power_level

    def calculate_power_levels(self):
        for x in range(1, self.width + 1):
            for y in range(1, self.width + 1):
                # self.__power_levels[self.__get_index(x, y)] = self.__calculate_power_level(x, y)
                self.__power_levels[x-1, y-1] = self.__calculate_power_level(x, y)

    def get_power_level(self, x, y):
        return self.__power_levels[self.__get_index(x, y)]

    # def get_largest_square(self, size):
    #     largest = LargestSquare(1, 1, 0)
    #     for left in range(1, self.width + 1 - size):
    #         for top in range(1, self.height + 1 - size):
    #             power_level = 0
    #             for x in range(size):
    #                 for y in range(size):
    #                     power_level += self.get_power_level(left + x, top + y)
    #             if power_level > largest.size:
    #                 largest = LargestSquare(left, top, power_level)
    #     return largest

    def get_largest_square2(self, size):
        largest = LargestSquare(1, 1, 0, size)
        for left in range(self.width - size):
            for top in range(self.height - size):
                power_level = self.__power_levels[left:left+size, top:top+size].sum()
                if power_level > largest.power_level:
                    largest = LargestSquare(left+1, top+1, power_level, size)
        return largest

    def hundreds_digit(n):
        return max(0, int((abs(n) % 1000 - abs(n) % 100) / 100))

    def get_absolute_largest(self):
        largest = LargestSquare(0, 0, 0, 0)
        for size in range(1, self.width + 1):
            print(size)
            s = self.get_largest_square2(size)
            if s.power_level > largest.power_level:
                largest = s
        return largest


grid = Grid()
grid.calculate_power_levels()
print(grid.get_largest_square2(3))
print(grid.get_absolute_largest())
