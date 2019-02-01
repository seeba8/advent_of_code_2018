import sys


class Assembly:
    def __init__(self, a=0, b=0, c=0, d=0, e=0):
        self.a = a
        self.b = b
        self.c = c
        self.d = d
        self.e = e
        self.i16()

    def __str__(self):
        return "{}, {}, {}, {}, {}".format(self.a, self.b, self.c, self.d, self.e)
        
    def i0(self):
        self.c = 1
        self.i1()

    def i1(self):
        self.e = 1
        self.i2()

    def i2(self):
        print("before the loop:", str(self))
        not_run = True
        while not_run or self.c <= self.b:
            while not_run or self.e <= self.b:
                not_run = False
                self.d = self.c * self.e
                if self.d == self.b:
                    self.a += self.c
                self.e += 1

            self.c += 1
            if self.c > self.b:
                print(self)
                sys.exit(0)
            self.e = 1
            # not_run = True

    def i16(self):
        self.b += 2
        self.b *= 2
        self.b *= 19
        self.b *= 11  # 836
        self.d += 7
        self.d *= 22
        self.d += 13  # 167
        self.b += self.d  # 1003
        if self.a == 0:
            self.i0()
        else:
            self.d = 27
            self.d *= 28
            self.d += 29
            self.d *= 30
            self.d *= 14
            self.d *= 32
            self.b += self.d
            self.a = 0
            print(self.b)
            self.i0()


# self.a= self.b= self.c= self.d = self.e = 0
print("start")
ass = Assembly(a=1)
print(ass)
