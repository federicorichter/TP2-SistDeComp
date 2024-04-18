#include <stdio.h>
#include <stdlib.h>

int* calculator_C(float arr[], int size)
{
    int* arrInt = malloc(size * sizeof(int));
    if (arrInt == NULL) {
        printf("Error: No se pudo asignar memoria.\n");
        return NULL;
    }

    // Inline assembly to convert float array to int array
    __asm__ (
        "xorl %%ecx, %%ecx\n\t"             // Initialize loop counter
        "loop_start:\n\t"
        "movss (%[arr], %%rcx, 4), %%xmm0\n\t"  // Load float value into XMM0
        "cvttss2si %%xmm0, %%eax\n\t"      // Convert float to int and store in EAX
        "addl $1, %%eax\n\t"                // Increment the integer value
        "movl %%eax, (%[arrInt], %%rcx, 4)\n\t"  // Store the result in arrInt
        "addl $1, %%ecx\n\t"                // Increment loop counter
        "cmpl %[size], %%ecx\n\t"           // Compare loop counter with size
        "jl loop_start"                     // Jump to loop_start if less than size
        :
        : [arr] "r" (arr), [arrInt] "r" (arrInt), [size] "r" (size)
        : "eax", "ecx", "xmm0"              // List of registers used in assembly code
    );

    return arrInt;
}