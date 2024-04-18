import ctypes

# Cargamos la libreria 
libfactorial = ctypes.CDLL('./libIntConverter.so')

# Definimos los tipos de los argumentos de la función factorial
libfactorial.calculator_C.argtypes = (ctypes.POINTER(ctypes.c_float),ctypes.c_int,)

# Definimos el tipo del retorno de la función factorial
libfactorial.calculator_C.restype = ctypes.POINTER(ctypes.c_int)

# Creamos nuestra función factorial en Python
# hace de Wrapper para llamar a la función de C
def calculator(arr):
    size = len(arr)
    arr_ptr = (ctypes.c_float * size)(*arr)
    result_ptr = libfactorial.calculator_C(arr_ptr, size)
    result = [result_ptr[i] for i in range(size)]
    return result
