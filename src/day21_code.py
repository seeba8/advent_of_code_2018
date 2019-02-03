a = b = c = ip = e = f = 0
b = 123  # start:
b = b & 456
b = int(b == 72)
if b != 1:
    raise Exception("b is not a number!")
b = 0
c = b | 65536  # 5:
b = 10605201
f = c & 255  # 7:
b += f
b &= 16777215
b *= 65899
b &= 16777215
f = int(256 > c)
if f == 1:
    ip = 27  # goto 27
else:
    f = 0
    e = f + 1  # 17:
    e *= 256
    e = int(e > c)
    if e == 1:
        ip = 25  # goto 25
    else:
        f += 1
        ip = 17  # goto 17
    c = f  # 25:
    ip = 7  # goto 7
    f = int(a == b)  # 27:
    if f == 1:
        sys.exit(-1)
    ip = 5  # goto 5