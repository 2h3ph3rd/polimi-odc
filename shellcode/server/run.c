#include <stdio.h>

int main()
{
    unsigned char code[1000];
    read(0, code, 1000);
    int (*ret)() = (int (*)())code;
    ret();
    return 0;
}