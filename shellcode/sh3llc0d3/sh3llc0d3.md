# Sh3llc0d3

There is a buffer overflow but with some conditions on input
At least 1000 chars, but the buffer is long 208 + 8 (sEBP) -> return address
Also no "\0" is accepted.

arg     0xffffcc88 —▸ 0xffffccc8
buffer  0x804c060


To put "\0" at the end of "/bin/sh"  it is possible to use this instruction.

```
xor eax, eax            ; eax is zero
mov ebx, 0x804c060      ; ebx is the address of the string
mov [ebx + 7], al       ; move zero in the byte pointed by ebx + 7 
```

flag{really_good_sh3llc0der!!!}
