# leakers

flag{canary_may_not_die!}

bss is not executable, only writable.

stack is writable and executable but there is aslr and a canary.

To find the address it requires some brute forcing.
The stack is not the same between the local and the remote version.
Once found a possible address the delta is a multiple of eight.
Locally, all addresses have delta between 0x100 and 0x200.
Probably, also remotely so test 0x100, 0x108, 0x110, 0x118, and so on.
