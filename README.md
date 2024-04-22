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

## Parte 2 usando assembler
En esta segunda parte embeberemos código assembler en nuestra función escrita en C para convertir los elementos del array de flotantes en enteros y guardarlos en un nuevo array sumándoles 1 a cada uno de los valores, utilizando la sentencia _ _ asm_ _:
```C
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
```

- Paso 1
  
  En este primer paso se ven inicializados los valores ECX en 0 además de toda la ejecución previa de instrucciones de guardado de contexto y guardado de memoria en la pila. Luego vemos que el puntero de instrucción nos indica el uso de la instrucción movss para mover desde rdx (registro donde se guarda el primer parámetro pasado a la función en C que en nuestro caso es el array de flotantes) el elemento apuntado por ECX (el elemento 0 en la primera iteración) a xmm0 (registro del coprocesador matemático).   
  ![image](https://github.com/federicorichter/TP2-SistDeComp/assets/82000054/9b1e869e-7493-48f0-b5e2-8ed745fde4e1)

- Paso 2
  
  Luego con la instrucción cvttsi convertimos a entero de 4 bytes el valor que se encuentra en xmm0 y se guarda en EAX
  ![image](https://github.com/federicorichter/TP2-SistDeComp/assets/82000054/b2273902-9144-4eb2-bc80-c9afc15c986c)

- Paso 3
  
  En este tercer paso se le suma 1 al valor de EAX con el uso de la instrucción add
  ![image](https://github.com/federicorichter/TP2-SistDeComp/assets/82000054/720f6464-e442-4554-a414-9067b7251b53)

- Paso 4
  
  Luego de esto se guarda el valor de EAX en el arreglo al que apunta rsi accediendo al elemento apuntado por rcx, multiplicando este valor por 4 (ya que asumimos enteros de y flotantes de 4 bytes).
  ![image](https://github.com/federicorichter/TP2-SistDeComp/assets/82000054/e01b3b17-461e-4d28-84cb-88b2bed3ddf9)

- Paso 5
  
    En este paso se suma 1 al valor del registro utilizado como contador e índice ecx
    ![image](https://github.com/federicorichter/TP2-SistDeComp/assets/82000054/3f470f81-dad2-4287-9d04-a34c16e1992f)

- Paso 6
  
    Se ejecuta la instrucción cmp (compare) que ejecuta una resta sin guardar el resultado entre el registro edi (size del array y segundo parámetro pasado a la función) y el valor de nuestro contador ecx. Como edi > ecx, la resta nos da negativa, haciendo que se ejcute la instrucción siguiente y se levante la flag de Sign en el registro eflags (en el siguiente paso ya se ve).
    ![image](https://github.com/federicorichter/TP2-SistDeComp/assets/82000054/92507f6c-aff6-454e-a7b7-a2d36c6907de)

- Paso 7
  
    Como la instrucción cmp nos indica que se ejecutará la instrucción siguiente, realizamos esta, la cual consiste en saltar a la primera línea del loop que se esta ejecutando cambiando el puntero de instrucción.
    ![image](https://github.com/federicorichter/TP2-SistDeComp/assets/82000054/dfa6b622-30d0-4be1-83d9-a7884b0d6b47)


 - Paso 8
   
    Vemos que se reinicia el loop con el valor incrementado de rcx
    ![image](https://github.com/federicorichter/TP2-SistDeComp/assets/82000054/bec7506e-73d3-4e56-850a-c35d2731a929)

 - Paso 9 (finalización del loop)
   
     Luego de 10 iteraciones vemos que el valor de rcx es 10, por lo que ahora la instrucción cmp indica al procesador que saltee la siguiente instrucción y vaya directo a las instrucciones de leave y ret, las cuales se encargan de liberar espacio en la pila (vemos que el stack pointer que es rsp aumenta)

     ![image](https://github.com/federicorichter/TP2-SistDeComp/assets/82000054/09a78bbc-37d9-4a22-82c5-3b88a32b5d8a)
     ![image](https://github.com/federicorichter/TP2-SistDeComp/assets/82000054/15ed83e4-d9ad-45cc-90da-3fb476ee8267)
     ![image](https://github.com/federicorichter/TP2-SistDeComp/assets/82000054/cd8fbf08-fbaf-4246-9b16-3aae7da45929)
     Ya en la última imagen vemos el contexto de ejecución que se tenía previo a la llamada de la función.

### Tiempo total con las dos formas

Luego de realizar las conversiones de flotantes a enteros con distintos modos (1000 pruebas), estos son los resultados :
 - Python: 0.34739 [s]
 - C : 0.35356 [s]
 - Usando ASM : 0.332 [s] 







