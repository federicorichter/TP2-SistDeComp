import ctypes

# Cargamos la libreria 
libfactorial = ctypes.CDLL('./libfactorial.so')

# Definimos los tipos de los argumentos de la función factorial
libfactorial.calculator.argtypes = (ctypes.POINTER(ctypes.c_float),ctypes.c_int,)

# Definimos el tipo del retorno de la función factorial
libfactorial.calculator.restype = ctypes.c_ulonglong

# Creamos nuestra función factorial en Python
# hace de Wrapper para llamar a la función de C
def calculator(arr):
    size = len(arr)
    arr_ptr = (ctypes.c_float * size)(*arr)
    return libfactorial.calculator(arr_ptr, size)
