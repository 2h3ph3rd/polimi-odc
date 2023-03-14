#include <stdio.h>

void print(int m1, int m2)
{
    printf("%4d - %4d = %4c (%d)\n", m1, m2, m1 - m2, m1 - m2);
}

int main()
{
    char c = -0x45;
    char m1 = 0xeb; // 1110 1011 -> 00010101 = 1 + 4 + 16 = 21 -> -21
    char m2 = 0x51;
    printf("Sum in ca2 8 byte\n");
    print(m1, c);
    print(m2, m1);
    return 0;
}