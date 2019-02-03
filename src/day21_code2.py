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
        self.goto7()  # flow, no instruction

    def goto7(self):  # goto7
        self.f = self.c & 255  # 7:
        self.b += self.f
        self.b &= 16777215
        self.b *= 65899
        self.b &= 16777215
        self.f = int(256 > self.c)
        if self.f == 1:
            self.num_instructions += 8
            self.goto27()  # goto 27
        else:
            self.f = 0
            self.num_instructions += 9
            self.goto17()  # flow, no instruction

    def goto17(self):  # goto17
        self.e = self.f + 1
        self.e *= 256
        self.e = int(self.e > self.c)
        if self.e == 1:
            self.num_instructions += 5
            self.goto25()  # goto 25
        else:
            self.f += 1
            self.num_instructions += 7
            self.goto17()  # goto 17

    def goto25(self):  # goto25
        self.c = self.f
        self.num_instructions += 2
        self.goto7()

    def goto27(self):  # goto27
        # debug this value here to see what b is
        if self.b not in Program.end_values:
            print(self.b)
            Program.end_values.add(self.b)
        self.f = int(self.a == self.b)  # 27:
        if self.f == 1:
            self.num_instructions += 2
            print("#instructions:", self.num_instructions)
            sys.exit(-1)
        else:
            self.num_instructions += 3
            self.goto5()


#p = Program()
#p.a = 11592302
#p.start()

i = 1
while True:
    i += 1
    if i % 1000 == 0:
        print(i)
    p = Program()
    p.a = i
    try:
        p.start()
    except RecursionError:
        pass
print("finished")
