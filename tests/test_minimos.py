"""Pruebas de algebra/minimos.py (Módulo III).

Oráculos calculados a mano (desarrollo en los comentarios).  Además se
comprueba la propiedad independiente Aᵀ r = 0 de toda solución de mínimos
cuadrados.
"""

import math
import unittest
from fractions import Fraction as F

from algebra.compartido.matriz import ErrorDimension
from algebra.directos import INFINITAS
from algebra.minimos import (
    CUADRADO,
    ErrorAjuste,
    SOBREDETERMINADO,
    SUBDETERMINADO,
    ajuste_lineal,
    clasificar_forma,
    minimos_cuadrados,
)


class TestMinimosCuadrados(unittest.TestCase):

    def test_ejemplo_clase_s8_30_09(self):
        # S8-30/09 pp. 6-7: x+3y=-1, 3x-2y=8, -2x+5y=-8
        # AᵀA = [[14,-13],[-13,38]], Aᵀb = (39,-59)
        # Cramer: det = 532-169 = 363; x = (39·38 - 13·59)/363 = 715/363 = 65/33,
        #         y = (14·(-59) + 13·39)/363 = -319/363 = -29/33
        r = minimos_cuadrados([[1, 3], [3, -2], [-2, 5]], [-1, 8, -8])
        self.assertEqual(r.tipo, SOBREDETERMINADO)
        self.assertFalse(r.b_en_espacio_columna)
        self.assertEqual(r.AtA, [[14, -13], [-13, 38]])
        self.assertEqual(r.Atb, [39, -59])
        self.assertEqual(r.solucion, [F(65, 33), F(-29, 33)])
        # A x̂ = (-2/3, 23/3, -25/3)  ->  r = (-1/3, 1/3, 1/3),  ||r||2² = 1/3
        self.assertEqual(r.residuo, [F(-1, 3), F(1, 3), F(1, 3)])
        self.assertEqual(r.norma_residuo_2_cuadrado, F(1, 3))
        self.assertAlmostEqual(r.norma_residuo_2, math.sqrt(1 / 3), places=14)
        self.assertEqual(r.ortogonalidad, [0, 0])

    def test_tarea2_item1(self):
        # Tarea II #1: x+y=2, 2x+y=2, x+2y=3
        # AᵀA = [[6,5],[5,6]], Aᵀb = (9,10), det = 11 -> x̂ = (4/11, 15/11)
        # r = (3/11, -1/11, -1/11), ||r||2² = 11/121 = 1/11
        r = minimos_cuadrados([[1, 1], [2, 1], [1, 2]], [2, 2, 3])
        self.assertEqual(r.AtA, [[6, 5], [5, 6]])
        self.assertEqual(r.Atb, [9, 10])
        self.assertEqual(r.solucion, [F(4, 11), F(15, 11)])
        self.assertEqual(r.residuo, [F(3, 11), F(-1, 11), F(-1, 11)])
        self.assertEqual(r.norma_residuo_2_cuadrado, F(1, 11))
        self.assertEqual(r.ortogonalidad, [0, 0])

    def test_b_en_espacio_columna(self):
        # x+y=2, x-y=0, 2x=2 tiene solución exacta (1,1): residuo cero
        r = minimos_cuadrados([[1, 1], [1, -1], [2, 0]], [2, 0, 2])
        self.assertTrue(r.b_en_espacio_columna)
        self.assertEqual(r.solucion, [1, 1])
        self.assertEqual(r.residuo, [0, 0, 0])

    def test_columnas_dependientes(self):
        # 2a columna = 2 · 1a columna -> AᵀA singular
        r = minimos_cuadrados([[1, 2], [2, 4], [3, 6]], [1, 2, 4])
        self.assertIsNone(r.solucion)
        self.assertEqual(r.ecuaciones_normales.clasificacion, INFINITAS)
        self.assertTrue(r.advertencias)

    def test_clasificar_forma(self):
        self.assertEqual(clasificar_forma(3, 2)[0], SOBREDETERMINADO)
        self.assertEqual(clasificar_forma(2, 2)[0], CUADRADO)
        self.assertEqual(clasificar_forma(1, 2)[0], SUBDETERMINADO)

    def test_dimensiones(self):
        with self.assertRaises(ErrorDimension):
            minimos_cuadrados([[1, 2], [3, 4], [5, 6]], [1, 2])


class TestAjusteLineal(unittest.TestCase):

    def test_ejercicio_s8_30_09_p8(self):
        # Puntos (1,2), (2,2.5), (3,3.7), (4,4.1).  Fórmula cerrada (independiente):
        #   n=4, Σx=10, Σx²=30, Σy=12.3, Σxy=2+5+11.1+16.4=34.5
        #   m = (nΣxy - ΣxΣy)/(nΣx² - (Σx)²) = (138 - 123)/(120 - 100) = 3/4
        #   c = (Σy - mΣx)/n = (12.3 - 7.5)/4 = 6/5
        r = ajuste_lineal([1, 2, 3, 4], [2, F("2.5"), F("3.7"), F("4.1")])
        self.assertEqual((r.pendiente, r.intercepto), (F(3, 4), F(6, 5)))
        self.assertEqual(r.ecuacion, "y = 3/4 x + 6/5")
        # ŷ = 1.95, 2.7, 3.45, 4.2 ; r = 0.05, -0.2, 0.25, -0.1 ; Σr = 0 ; ||r||2² = 0.115
        self.assertEqual(r.minimos.estimados, [F("1.95"), F("2.7"), F("3.45"), F("4.2")])
        self.assertEqual(r.minimos.residuo, [F("0.05"), F("-0.2"), F("0.25"), F("-0.1")])
        self.assertEqual(r.minimos.norma_residuo_2_cuadrado, F(23, 200))

    def test_puntos_alineados(self):
        # (0,1), (1,3), (2,5) están sobre y = 2x + 1
        r = ajuste_lineal([0, 1, 2], [1, 3, 5])
        self.assertEqual((r.pendiente, r.intercepto), (2, 1))
        self.assertEqual(r.minimos.residuo, [0, 0, 0])

    def test_pendiente_negativa_ecuacion(self):
        r = ajuste_lineal([0, 1], [1, -1])   # y = -2x + 1
        self.assertEqual(r.ecuacion, "y = -2 x + 1")
        r = ajuste_lineal([0, 1], [-1, 1])   # y = 2x - 1
        self.assertEqual(r.ecuacion, "y = 2 x − 1")

    def test_datos_invalidos(self):
        with self.assertRaises(ErrorAjuste):
            ajuste_lineal([1, 2, 3], [1, 2])
        with self.assertRaises(ErrorAjuste):
            ajuste_lineal([1], [1])
        with self.assertRaises(ErrorAjuste):
            ajuste_lineal([2, 2, 2], [1, 2, 3])


if __name__ == "__main__":
    unittest.main()
