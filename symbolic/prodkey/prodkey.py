#!/usr/bin/env python3

# flag{nice_keygen!now_it_only_needs_some_music!_notleakedflag}

import angr

import sys
from pwn import *


def sendline(p, line):
    p.sendline(line)


# the string is the name of the executable
proj = angr.Project('prodkey')
sm = proj.factory.simulation_manager()

find = [0x400deb]
avoid = [0x400df2]
sm.explore(find=find, avoid=avoid)

if len(sm.found) == 0:
    print("Failure!")
    exit()

print("Success!")
found = sm.found[0]
print("%s" % found.posix.dumps(0))

prodkey = found.posix.dumps(0)

p = remote("bin.training.jinblack.it", 2021)
p.recvuntil(b"\nPlease Enter a product key to continue: \n")
sendline(p, prodkey)
print(p.recvall())
