"""Pruebas de las visualizaciones complementarias del Módulo II: normas y sensibilidad.

Comprueban que las figuras usan los cálculos reales del núcleo. No prueban la interfaz
(la renderización en Brave se comprueba aparte) ni ningún gesto.
"""

import unittest
from fractions import Fraction as F

import plotly.io as pio

from algebra.compartido.matriz import norma_infinito_matriz, sumas_absolutas_por_columna, sumas_absolutas_por_fila
from algebra.modulo_II_condicionamiento.condicion import analizar_perturbacion, numero_condicion_infinito
from visualizacion import geometria_modulo_II as gm


class TestNormas(unittest.TestCase):
    def test_sumas_por_columna_y_por_fila(self):
        A = [[1, -2], [3, 1]]
        self.assertEqual(sumas_absolutas_por_columna(A), [4, 3])
        self.assertEqual(sumas_absolutas_por_fila(A), [3, 4])

    def test_la_barra_destacada_de_filas_es_la_norma_infinito(self):
        A = [[1, 2], [3, 1]]
        figura = gm.normas_filas(sumas_absolutas_por_fila(A))
        colores = list(figura.data[0].marker.color)
        self.assertEqual(colores.index(gm.COLOR_MAXIMO), 1)                 # fila 2: 3 + 1 = 4
        self.assertEqual(max(figura.data[0].y), norma_infinito_matriz(A))    # 4

    def test_filas_de_A_inverso_con_su_propio_maximo(self):
        A = [[1, 2], [3, 1]]
        inv = [[F(-1, 5), F(2, 5)], [F(3, 5), F(-1, 5)]]                   # S7-21/09 p. 19
        figura = gm.normas_filas(sumas_absolutas_por_fila(A), sumas_absolutas_por_fila(inv))
        self.assertEqual(len(figura.data), 2)
        self.assertEqual(list(figura.data[1].y), [0.6, 0.8])               # 3/5 y 4/5

    def test_columnas_son_referencia_de_la_norma_1(self):
        figura = gm.normas_columnas([4, 3])
        self.assertEqual(max(figura.data[0].y), 4)
        self.assertIn("norma 1", figura.layout.title.text)

    def test_rango_inicial_cubre_las_barras(self):
        x0, x1, y0, y1 = gm.rango_normas_inicial([3, 4], [F(3, 5), F(4, 5)])
        self.assertEqual((x0, x1), (-0.5, 1.5))
        self.assertGreaterEqual(y1, 4)

    def test_se_serializa_con_fracciones(self):
        pio.to_json(gm.normas_filas([F(4, 3), 4], [F(1, 2), F(3, 2)]))
        pio.to_json(gm.normas_columnas([F(5, 3), 2]))


class TestSensibilidad(unittest.TestCase):
    def test_barras_coinciden_con_la_perturbacion_real(self):
        A = [[1, 2], [3, 1]]
        b = [3, 4]
        condicion = numero_condicion_infinito([[F(v) for v in fila] for fila in A])
        p = analizar_perturbacion(A, b, [F(0), F(1, 10)])
        figura = gm.sensibilidad_barras(p.error_relativo_b, p.error_relativo_x, p.cota)
        valores = list(figura.data[0].y)
        self.assertAlmostEqual(valores[0], float(p.error_relativo_b) * 100)
        self.assertAlmostEqual(valores[1], float(p.error_relativo_x) * 100)
        self.assertAlmostEqual(valores[2], float(condicion.kappa * p.error_relativo_b) * 100)
        self.assertLessEqual(valores[1], valores[2] + 1e-12)                 # S7-21/09 p. 18

    def test_se_serializa_con_fracciones(self):
        pio.to_json(gm.sensibilidad_barras(F(1, 100), F(2, 100), F(3, 100)))


if __name__ == "__main__":
    unittest.main()
