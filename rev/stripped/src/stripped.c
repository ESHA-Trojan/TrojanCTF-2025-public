#include <stdio.h>
#include <string.h>
#include <stdlib.h>

int pass[] = {89, 120, 118, 114, 106, 120, 134, 96, 78, 121, 66, 111, 126, 73, 114, 124, 86, 132, 91, 119, 124, 74, 136, 79, 124, 128, 128, 99, 108, 129, 151, 84, 132, 154, 143, 91, 136, 118, 140, 154, 145, 171};

void fail() {
    printf("\nLet me hear you make decisions without your television\nhttps://www.youtube.com/watch?v=qU8UfYdKHvs\n");
    exit(1);
}

void (*fail_ptr)() = NULL;
void init_fail() { fail_ptr = fail; }

void transform(int* str) {
    for (int i = 5; str[i - 5] != 0; i++) {
        str[i - 5] += i;
    }
}

int main() {
    char input1[50] = { 0 };
    int input2[50] = { 0 };
    init_fail();

    printf("Let me hear you speaking just for me:\n");
    if (scanf("%49[^\n]", input1) != 1) {
        printf("Error reading input\n");
        return 1;
    }

    for (int i = 0; i < 50; i++) {
        input2[i] = (int)input1[i];
    }

    transform(input2);

    for (int i = 0; i < 35; i++) {
        if (pass[i] != input2[i]) {
            fail_ptr();
        }
    }

    printf("\nMetropolis has nothing on this!\n");
    return 0;
}
