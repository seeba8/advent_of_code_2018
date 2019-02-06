import sys


class Program:
    end_values = set()

    def __init__(self):
        self.a = self.b = self.c = self.ip = self.e = self.f = 0
        self.num_instructions = 0

    def start(self):
        self.b = 123
        self.b &= 456
        if self.b != 72:
            raise Exception("param not a number")
        self.b = 0
        self.num_instructions += 5
        self.goto5()  # flow, no instruction

    def goto5(self):  # goto5
        self.c = self.b | 65536
        self.b = 10605201
        self.num_instructions += 2
        while True:
            self.f = self.c & 255  # 7:
            self.b += self.f
            self.b &= 16777215
            self.b *= 65899
            self.b &= 16777215
            self.f = int(256 > self.c)
            if self.f == 1:
                self.num_instructions += 8
                # goto27:
                # debug this value here to see what b is
                if self.b not in Program.end_values:
                    print(self.b)
                    Program.end_values.add(self.b)
                else:
                    print("ALREADY SEEN")
                    sys.exit(-1)
                self.f = int(self.a == self.b)  # 27:
                if self.f == 1:
                    self.num_instructions += 2
                    print("#instructions:", self.num_instructions)
                    sys.exit(-1)
                else:
                    self.num_instructions += 3
                    self.c = self.b | 65536
                    self.b = 10605201
                    self.num_instructions += 2
                    continue
            else:
                self.f = 0
                self.num_instructions += 9
                first_run = True
                self.f -= 1
                while first_run or self.e != 1:
                    self.f += 1
                    first_run = False
                    self.e = self.f + 1
                    self.e *= 256
                    self.e = int(self.e > self.c)
                self.c = self.f  # goto25
                self.num_instructions += 2


# p = Program()
# p.a = 11592302
# p.start()
p = Program()
p.start()
