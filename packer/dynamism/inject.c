#include <sys/ptrace.h>
#include <sys/types.h>

extern long int ptrace(enum __ptrace_request __request, ...)
{
    return 0;
}
