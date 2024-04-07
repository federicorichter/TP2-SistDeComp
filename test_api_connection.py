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
