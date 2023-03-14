#!/usr/bin/env python3

#

from pwn import *

import angr
import claripy
import z3

import logging
logging.getLogger('angr').setLevel('INFO')

param_1 = [z3.BitVec('c%d' % i, 8) for i in range(23)]


flag = [claripy.BVS('c%d' % i, 8) for i in range(23)]
input_str = claripy.Concat(*flag + [claripy.BVV(b'\n')])
stdin = angr.SimFileStream(name='stdin', content=input_str, has_end=False)

# the string is the name of the executable
proj = angr.Project('cracksymb')
initial_state = proj.factory.entry_state(stdin=stdin)

initial_state.solver.add(flag[0] == ord('f'))
initial_state.solver.add(flag[1] == ord('l'))
initial_state.solver.add(flag[2] == ord('a'))
initial_state.solver.add(flag[3] == ord('g'))
initial_state.solver.add(flag[4] == ord('{'))
initial_state.solver.add(flag[22] == ord('}'))

for c in flag:  # make sure all chars are printable
    initial_state.solver.add(c >= 0x20, c <= 0x7e)

sm = proj.factory.simulation_manager(initial_state)

# find = [0x4033c2]
# avoid = [0x4033d0]
find = [0x4033d0]
avoid = [0x4033c2]
sm.explore(find=find, avoid=avoid)

if len(sm.found) == 0:
    print("Failure!")
    exit()

print("Success!")
found = sm.found[0]
flag = found.posix.dumps(0)
print("%s" % flag)
