#!/usr/bin/env python3

expected_xor = [
    0x2648a0c1cd54abaa,
    0x3c46afcfde54b5ab,
    0x3178e2e5d05ba8a5,
    0x3c78b7d5cd6ab2a3,
    0x1740a2d6cc6aa2a4,
    0x265ea7e5c75ab5aa,
    0x3c4e9cc9cb4298ed,
    0x35189cded854af93,
    0
]

seed = 0x4827c3baaa35c7cc

flag = ""

for i in range(len(expected_xor)):
    temp = expected_xor[i] ^ seed
    temp = hex(temp)
    for i in range(16, 1, -2):
        flag += chr(int(temp[i:i+2], base=16))

print(flag)
