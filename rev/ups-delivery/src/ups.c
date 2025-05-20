#include <stdio.h>

// Define global strings
char str[] = "Can't strings this, can you? ;)";
char str1[] = "Trojan{00pS_MAy53_1t_wA5_UPX}";

int main() {
    // Use the str1 variable to prevent warnings
    (void)str1;

    // Print the string
    printf("%s\n", str);

    return 0;
}
