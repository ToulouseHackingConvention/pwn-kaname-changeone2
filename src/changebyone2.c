#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <unistd.h>

#define LENBUFF 4096

int main() {
    char buff[LENBUFF] = {0};

    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 0);
    
    printf("Welcome in complaints center.\n\n"
           "Please enter your message [4096 bytes] : ");

    read(STDIN_FILENO, buff, 4096);

    printf("\nThanks for taping your complaints.\n"
           "An operator may read your message or just ignore it.\n\n"
           "Have a good day");


    return 0;
}

