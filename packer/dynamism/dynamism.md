# dynamism

`flag{congratulationz_!_you_got_the_flag_from_dyn!_was_it_hard_?}`

In this challenge the dynamic code is taken by calling an external service unaccessible by us.
One of the possible solutions is to use gdb to obtain the code.
It could be possible also to mock the remote call in some way.

In this case, I implemented the first solution.
But in the official executable there is a ptrace that must be avoided (LD_PRELOAD trick).

By using gdb you can find the three dynamic executions with relative remote call: data, prepareinput, and check.
The first does not depends on the flag that we give, while other two work on the flag by doing xors.
In prepare input a single value is used 8 times -> 0x4827c3baaa35c7cc.
Instead, in check there are 8 different values.

By doing the xors between these value it is possible to obtain the flag.
Be careful with endianess and hex values.

## GDB

Use LD_PRELOAD with custom library to avoid ptrace

```
set environment LD_PRELOAD=/home/fra/Documents/university/odc/dynamism/inject.so
```

Set command line argument

```
set args flag{fake_flag_fake_flag}
```

### Special addresses

0x555555555190 -> main
0x5555555551cd -> first do_something call
0x5555555551f1 -> second do_something call
0x555555555207 -> third do_something call
0x555555555574 -> call data/prepareinput/check

## Dynamic parts

### data

```
0x7ffff7fb9000:	mov    rdi,QWORD PTR [rdi]
0x7ffff7fb9003:	jmp    0x7ffff7fb9027
0x7ffff7fb9005:	pop    rsi
0x7ffff7fb9006:	mov    r12,0x9
0x7ffff7fb900d:	cmp    r12,0x0
0x7ffff7fb9011:	je     0x7ffff7fb9026
0x7ffff7fb9013:	mov    r13,QWORD PTR [rsi]
0x7ffff7fb9016:	mov    QWORD PTR [rdi],r13
0x7ffff7fb9019:	add    rsi,0x8
0x7ffff7fb901d:	add    rdi,0x8
0x7ffff7fb9021:	dec    r12
0x7ffff7fb9024:	jmp    0x7ffff7fb900d
0x7ffff7fb9026:	ret
```

### prepareinput

```
0x7ffff7fb9000:	mov    rsi,QWORD PTR [rdi+0x8]
0x7ffff7fb9004:	mov    rdi,QWORD PTR [rdi]
0x7ffff7fb9007:	mov    rdx,rsi
0x7ffff7fb900a:	add    rdx,0x100
0x7ffff7fb9011:	mov    rsi,QWORD PTR [rsi]
0x7ffff7fb9014:	mov    r12,0x8
0x7ffff7fb901b:	cmp    r12,0x0
0x7ffff7fb901f:	je     0x7ffff7fb9037
0x7ffff7fb9021:	mov    rcx,QWORD PTR [rdi]
0x7ffff7fb9024:	xor    rcx,rsi
0x7ffff7fb9027:	mov    QWORD PTR [rdx],rcx
0x7ffff7fb902a:	add    rdx,0x8
0x7ffff7fb902e:	add    rdi,0x8
0x7ffff7fb9032:	dec    r12
0x7ffff7fb9035:	jmp    0x7ffff7fb901b
0x7ffff7fb9037:	ret
```

Value used for xor

```
0x4827c3baaa35c7cc
```

### check

```
0x7ffff7fb9000:	mov    rdi,QWORD PTR [rdi]
0x7ffff7fb9003:	mov    rsi,rdi
0x7ffff7fb9006:	add    rsi,0x100
0x7ffff7fb900d:	add    rdi,0x8
0x7ffff7fb9011:	mov    rcx,0x9
0x7ffff7fb9018:	cmp    rcx,0x0
0x7ffff7fb901c:	je     0x7ffff7fb903e
0x7ffff7fb901e:	mov    r10,QWORD PTR [rdi]
0x7ffff7fb9021:	mov    r11,QWORD PTR [rsi]
0x7ffff7fb9024:	add    rdi,0x8
0x7ffff7fb9028:	add    rsi,0x8
0x7ffff7fb902c:	cmp    r10,r11
0x7ffff7fb902f:	jne    0x7ffff7fb9036
0x7ffff7fb9031:	dec    rcx
0x7ffff7fb9034:	jmp    0x7ffff7fb9018
0x7ffff7fb9036:	mov    rax,0x0
0x7ffff7fb903d:	ret
0x7ffff7fb903e:	mov    rax,0x1
0x7ffff7fb9045:	ret
```

To continue execution

```
set $r10=$r11
```

Values used for xor

```
0x2648a0c1cd54abaa
0x3c46afcfde54b5ab
0x3178e2e5d05ba8a5
0x3c78b7d5cd6ab2a3
0x1740a2d6cc6aa2a4
0x265ea7e5c75ab5aa
0x3c4e9cc9cb4298ed
0x35189cded854af93
0
```
