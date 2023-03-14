# emptyspaces

### Notes

- In rdx and rsi there is already the address of the buffer

### ropper

```sh
ropper --inst-count 3 --nocolor --type rop --file emptyspaces > small_gadgets.txt
```

### Gadgets found

```py
0x474dc5 # syscall; ret;

0x47e6db # mov rax, rcx; ret;
0x412903 # mov rax, rdi; ret;
0x41a720 # mov rax, rdx; ret;
0x41dc10 # mov rax, rsi; ret;

0x48d656 # mov rsp, rcx; ret;
0x400b84 # mov rsp, rsi; ret;

0x42b128 # add rax, rcx; ret;
0x42b353 # add rax, rdi; ret;

0x444b00 # xor rax, rax; ret;

0x488505 # push rax; pop rbx; ret;

0x481b76 # pop rax; pop rdx; pop rbx; ret;

0x450a83 # push rax; push rsp; ret;

0x4155a4  # pop rax; ret;
0x400696  # pop rdi; ret;
0x410133  # pop rsi; ret;
0x44bd36  # pop rdx; ret;
0x400de8  # pop rbx; ret;


bss = 0x6bb2e0
main = 0x400b95
```
