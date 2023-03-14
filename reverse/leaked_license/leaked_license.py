#!/bin/python3

# 726cfc2d26c6defedb06562199f5c7d0da4f4930
license = b"\x72\x6c\xfc\x2d\x26\xc6\xde\xfe\xdb\x06\x56\x21\x99\xf5\xc7\xd0\xda\x4f\x49\x30"

# f3ed47e26e4de24a414981945c7da2db1ac93d5
my_license = b"\xf3\xed\x47\xe2\x6e\x4d\xe2\x4a\x41\x49\x81\x94\x5c\x7d\xa2\xdb\x1a\xc9\x3d\x50"

for i in range(0, len(my_license), 5):
    code = int.from_bytes(my_license[i: i+5], byteorder='big')
    print(code)
    