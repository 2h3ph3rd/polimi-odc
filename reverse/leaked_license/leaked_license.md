# leaked_license

### Leaked license

```
726cfc2d26c6defedb06562199f5c7d0da4f4930

726cfc2d
26c6defe
db065621
99f5c7d0
da4f4930
```

### My license

```
f3ed47e26e4de24a414981945c7da2db1ac93d5

f3ed47e2
6e4de24a
41498194
05c7da2d
b1ac93d5
```

### GDB commands used

Using the call to printf it is possible to find the address of the code.

```bash
info address printf
break 0x...
c
finish
```

Then, delete the breakpoints and by looking to the instructions find where the code is stored.

Each iteration change the value with the leaked license.

```bash
delete 2
c 5
b $rip + 66 # 0x5555555552a6 - 0x555555555240
set *0x7fffffffde88=0xda4f4930
```
