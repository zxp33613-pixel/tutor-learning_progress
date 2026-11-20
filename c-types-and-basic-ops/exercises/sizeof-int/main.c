#include <stdio.h>
int main(void) {
    printf("%d\n", (int)(sizeof(char) <= sizeof(int)));
    return 0;
}
