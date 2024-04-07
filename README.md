# TP2 Sistemas de computación

Grupo : Santiago Recalde - Joaquín Otalora - Federico Richter

## Request a API

Comenzamos generando una request a la API del Banco Mundial donde se encuentran los índices de GINI medidos en los países desde el año 2011 hasta el 2019. Haciendo uso del módulo requests de python, hacemos una petición GET para obtener todos los datos en forma de JSON y guardarlos en la variable llamada data. Luego iremos iterando sobre todos los elementos del objeto JSON y si vemos que los datos pertenecen a Argentina los agregamos a un arreglo llamado index_argentina. Todo esto envuelto en try-except, el cual sirve como except handler en caso de, como dice el nombre, ocurra una excepción a la hora de requerir los datos a la API  : 

```python
import requests
import numpy as np
from calculator import calculator


api_url = "https://api.worldbank.org/v2/en/country/all/indicator/SI.POV.GINI?format=json&date=2011:2020&per_page=32500&page=1&country=%22Argentina%22"

try:
    response = requests.get(api_url) #get request from api
    response.raise_for_status()  # Check for any errors

    data = response.json()
    count = 0
    index_argentina = []

    for item in data[1]:  
    	country_name = item["country"]["value"]
    	if (country_name == "Argentina") :
    		if item["value"] == None:
    			index_argentina.append(0.0)
    		else:
    			index_argentina.append(item["value"])
    		count = count + 1
    	indicator_value = item["value"]
    	year = item["date"]

except requests.RequestException as e:
    print(f"Error fetching data: {e}")
```

## Libreria en C para conversion de datos:
Se crea una libreria calculator.c, la cual recibe un array de flotantes y el tamaño del array.
Castea todos los flotantes del array a int, les suma 1 y los guarda en un array de enteros y
finalmente devuelve un puntero al array de enteros. 

```C
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
```
## Script de linkeo entre Python y C:
Utilizando ctypes, se linkea la libreria de C calculator.c con el script de python.
Se buildea la libreria calculator.c utilizando:
```bash
gcc -c calculator.c
gcc -shared -W -o libIntConverter.so calculator.o
```
Luego se carga el shared object de la libreria de C, se define el tipo de los argumentos que recibira la funcion
calculator, y se define el tipo de los valores que retornara la funcion calculator.
Por ultimo se define la funcion de python calculator que hara de wrapper de nuestra funcion de C.

```python
import ctypes
libfactorial = ctypes.CDLL('./libIntConverter.so')

libfactorial.calculator.argtypes = (ctypes.POINTER(ctypes.c_float),ctypes.c_int,)

libfactorial.calculator.restype = ctypes.POINTER(ctypes.c_int)

def calculator(arr):
    size = len(arr)
    arr_ptr = (ctypes.c_float * size)(*arr)
    result_ptr = libfactorial.calculator(arr_ptr, size)
    result = [result_ptr[i] for i in range(size)]
    return result
```
## Impresion de los datos convertidos y forma final del script de python:
Finalmente se crea la funcion fetch_data, la cual utilizando la funcion calculator, convierte los datos recibidos de la API, imprime los datos originales y luego los convertidos con calculator. Finalmente los grafica y sale de la funcion.

```python
import requests
from calculator import calculator

import matplotlib.pyplot as plt

def fetch_data():
    api_url = "https://api.worldbank.org/v2/en/country/all/indicator/SI.POV.GINI?format=json&date=2011:2020&per_page=32500&page=1&country=%22Argentina%22"

    try:
        response = requests.get(api_url)  # get request from api
        response.raise_for_status()  # Check for any errors

        data = response.json()
        count = 0
        index_argentina = []

        for item in data[1]:
            country_name = item["country"]["value"]
            if country_name == "Argentina":
                if item["value"] == None:
                    index_argentina.append(0.0)
                else:
                    index_argentina.append(item["value"])
                    count = count + 1
            indicator_value = item["value"]
            year = item["date"]

        print(f"Argentina GINI Index antes del calculo en C:")
        print(index_argentina)
        res = calculator(index_argentina)
        print(f"Argentina GINI Index luego del calculo en C: ")
        print(res)
        plt.plot(res)
        plt.xlabel('Year')
        plt.ylabel('GINI Index')
        plt.title('Argentina GINI Index over Time')
        plt.show()

    except requests.RequestException as e:
        print(f"Error fetching data: {e}")

fetch_data()
```
## Test unitario de calculator:
Se procedio a realizar un sencillo test unitario de la funcion calculator, este test lo que hace es generar un array con 10 numeros aleatorios flotantes y guardar en otro array estos mismos numeros pero casteados a entero y sumandole uno. Esto se hace de forma local en python ya que nos permite tener un resultado con el que comparar la funcion calculator.
A continuacion se guarda en un arreglo nuevo el resultado de llamar a la funcion calculator con el arreglo de los numeros flotantes y su tamaño como argumentos.
Finalmente se hace un assertEqual entre el arreglo con los resultados de la funcion y el arreglo con los valores casteados localmente

```python
import unittest
from calculator import calculator
import random

class TestFunciones(unittest.TestCase):
    def test_calculator(self):
        arr = []
        arr_truncated = []
        for _ in range(10):
            num = random.uniform(0.0, 1000.0)
            arr.append(num)
            arr_truncated.append(int(num) + 1)
        compare = arr_truncated
        resultado = calculator(arr)
        print(f"Generado: {arr}")
        print(f"Resultado: {resultado}")
        self.assertEqual(compare, resultado)
```

