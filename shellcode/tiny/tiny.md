# tiny

flag{F3llS_l1k3_sh3llc0d1NG_1n_4rm_THumb}

read -> write shellcode

the pointer of the buffer is in rdx.

### 2 byte operations

Be careful, working with 32 bit registers leads to lose the high part of them.

For example, the instruction `inc esp` removes the sixth and fifth byte of the address or more if it is bigger.


```as
push rax
pop rax

mov eax, esp

xor eax, eax
or eax, eax
and eax, eax

inc eax
dec eax
shl eax
shr eax

add al, 0x01
sub al, 0x01

xor al, al
or al, al
and al, al

inc al
dec al
shl al
shr al
```