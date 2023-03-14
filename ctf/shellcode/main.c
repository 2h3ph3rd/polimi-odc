// gcc main.c; ./a.out
// https://stackoverflow.com/questions/7684359/how-to-use-nanosleep-in-c-what-are-tim-tv-sec-and-tim-tv-nsec

// initial tests on nanosleep

#include <stdio.h>
#include <time.h> /* Needed for struct timespec */

int mssleep(long miliseconds)
{
    struct timespec rem;
    struct timespec req = {
        (int)(miliseconds / 1000),     /* secs (Must be Non-Negative) */
        (miliseconds % 1000) * 1000000 /* nano (Must be in range of 0 to 999999999) */
    };

    return nanosleep(&req, &rem);
}

int main()
{
    int ret = mssleep(500);

    if (ret < 0)
    {
        printf("Nano sleep system call failed \n");
        return -1;
    }

    printf("Nano sleep successfull \n");
    return 0;
}