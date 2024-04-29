#include <stdio.h>
#include <stdlib.h>

extern int float_to_int_asm(float value1,float value2,float value3,float value4,float value5,float value6,float value7,float value8,float value);

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
        float aux = arr[i];
        convertedValue = float_to_int_asm(7.3,8.5,4.5,9.6,55.6,4.8,123.5,4.6,aux);
        arrInt[i] = convertedValue;
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
