#include <stdio.h>
#include <stdlib.h>

extern int float_to_int_asm(float value);

int* calculator_C(float arr[], int size)
{
    int* arrInt = malloc(size * sizeof(int));

    if (arrInt == NULL) {
        printf("Error: No se pudo asignar memoria.\n");
        return NULL;
    }

    for(int i = 0;i < size; i++)
    {
        int convertedValue ;
        convertedValue = float_to_int_asm(arr[i]);
        arrInt[i] = convertedValue;
        printf("arrInt = %d \n", arrInt[i]);
        printf("arr = %.2f \n", arr[i]);
    }

    return arrInt;
}

int main()
{
    float arr[5] = {10.1, 5.2, 98.2, 45.5, 12.7};
    int *res = calculator_C(arr, 5);
    //printf("res = %d", res[0]);
    free(res);

    return 0;


}
