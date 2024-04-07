#include <stdio.h>
#include <stdlib.h>

int* calculator(float arr[], int size)
{
	
	int* arrInt = malloc(size * sizeof(int));
	if (arrInt == NULL) {
		printf("Error: No se pudo asignar memoria.\n");
		return NULL;
	}

	for (int i = 0; i < size; i++)
	{
		arrInt[i] = (int)arr[i] +1;
	}

	return arrInt;
}