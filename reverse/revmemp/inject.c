#include <string.h>

int strncmp(const char *s1, const char *s2, size_t n)
{
  printf("Hijacked puts: %s %s\n", s1, s2);
  return 0;
}
