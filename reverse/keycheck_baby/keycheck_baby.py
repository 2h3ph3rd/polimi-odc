#!/bin/python3

xor_str = b"babuzz"
magic0 = b"\x1b\x51\x17\x2a\x1e\x4e\x3d\x10\x17\x46\x49\x14\x3d"
magic1 = b"\xeb\x51\xb0\x13\x85\xb9\x1c\x87\xb8\x26\x8d\x07"

assert len(magic0) == 13
assert len(magic1) == 12

flag = "flag{"
for i, c in enumerate(magic0):
    flag += chr(xor_str[i % 6] ^ magic0[i])

offset = 187
# 81 -  -21 =    f (102)
for i, c in enumerate(magic1):
    b = c - offset
    if b > 256:
        b -= 256
    flag += chr(b)
    if c > 128:
        offset = -1 * (256 - c)
    else:
        offset = c

flag += "}"
print(flag)
