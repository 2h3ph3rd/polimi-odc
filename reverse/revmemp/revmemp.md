# revmemp

flag{this_was_a_bit_more_complex}

There is a ptrace that avoid gdb or ltrace like utility.

### 1st way (Advanced debugging)

It is possible to use gdb to catch the ptrace and edited it to continue debugging.
Then avoid calling the function that search in the code for the byte 0xcc.

### 2nd way (Patch)

Patch the binary
Use Ghex and patch at least the ptrace to use gdb.

### 3rd way (LD_PRELOAD trick)

Create a fake strncmp to print out the flag.

```
gcc -shared -fPIC -o inject.so inject.c
LD_PRELOAD=$PWD/inject.so ./revmemp aaa
```