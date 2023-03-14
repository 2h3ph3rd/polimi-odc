# syscall

flag{nice_job!_self_modifying_shellcode?}

buffer -> 00404080

The char `\x0f` and `\x05` are not allowed

Syscall code is `\x0f\x05`

To make the execve is possible to change the memory and put the two bytes somewhere in the nop sled.