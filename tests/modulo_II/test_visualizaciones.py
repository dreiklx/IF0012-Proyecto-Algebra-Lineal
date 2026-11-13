"""Pruebas de las visualizaciones complementarias del Módulo II (geometría, normas, sensibilidad).

Comprueban que las figuras usan los cálculos reales del núcleo y que la geometría del
determinante es coherente con det(A).  No prueban la interfaz; la renderización en Brave se
comprueba aparte (ver docs/auditoria/decision_graficas.md).
"""

import unittest
from fractions import Fraction as F

from algebra.compartido.matriz import sumas_absolutas_por_columna, sumas_absolutas_por_fila, norma_infinito_matriz
from algebra.modulo_I_sistemas.directos import determinante
from algebra.modulo_II_condicionamiento.condicion import analizar_perturbacion, numero_condicion_infinito
from visualizacion import geometria_modulo_II as gm


def _vertices_imagen(A):
    _, imagen = gm._puntos_transformados(A)
    return imagen


class TestDeterminanteGeometrico(unittest.TestCase):
    def test_area_del_paralelogramo_coincide_con_valor_absoluto_del_determinante(self):
        for A in ([[1, 2], [3, 1]], [[2, -1], [0, 3]], [[F(1, 2), 4], [-3, F(5, 3)]], [[0, 1], [1, 0]]):
            A = [[F(v) for v in fila] for fila in A]
            det = determinante(A)
            area = gm.area_shoelace(_vertices_imagen(A))
            self.assertAlmostEqual(area, abs(float(det)), places=9, msg=str(A))

    def test_los_vertices_son_A_por_los_puntos_del_cuadrado(self):
        A = [[1, 2], [3, 1]]
        self.assertEqual(_vertices_imagen(A), [(0, 0), (1, 3), (3, 4), (2, 1)])

    def test_determinante_cero_colapsa_el_area(self):
        A = [[1, 2], [2, 4]]
        det = determinante([[F(v) for v in fila] for fila in A])
        self.assertEqual(det, 0)
        figura, area = gm.transformacion_2x2([[F(v) for v in fila] for fila in A], det)
        self.assertEqual(area, 0)
        self.assertIn("det(A) = 0", figura.layout.annotations[0].text)

    def test_la_figura_se_serializa_con_fracciones(self):
        import plotly.io as pio
        figura, _ = gm.transformacion_2x2([[F(1, 3), F(2)], [F(3), F(1, 7)]], F(1, 3) * F(1, 7) - 6)
        pio.to_json(figura)                       # falla si queda algún Fraction
        figura_n, _ = gm.normas_barras([F(4, 3), 4], [F(1, 2), F(3, 2)], [F(5, 3), 2]), None
        pio.to_json(figura_n)
        pio.to_json(gm.sensibilidad_barras(F(1, 100), F(2, 100), F(3, 100)))

    def test_la_figura_depende_de_la_matriz_introducida(self):
        f1, a1 = gm.transformacion_2x2([[F(1), F(2)], [F(3), F(1)]], F(-5))
        f2, a2 = gm.transformacion_2x2([[F(2), F(0)], [F(0), F(2)]], F(4))
        self.assertNotEqual(a1, a2)
        self.assertAlmostEqual(a1, 5.0)
        self.assertAlmostEqual(a2, 4.0)

    def test_la_figura_tiene_cuadricula_original_y_transformada(self):
        figura, _ = gm.transformacion_2x2([[F(1), F(2)], [F(3), F(1)]], F(-5))
        nombres = [t.name for t in figura.data if t.name]
        self.assertIn("Cuadrado unitario", nombres)
        self.assertTrue(any("paralelogramo" in n for n in nombres))
        # 7 líneas originales (x = k, y = k para k = -3…3) + 7 transformadas, por eje, en pares.
        self.assertGreaterEqual(len(figura.data), 2 * 2 * 7)


class TestNormas(unittest.TestCase):
    def test_sumas_por_columna(self):
        A = [[1, -2], [3, 1]]
        self.assertEqual(sumas_absolutas_por_columna(A), [4, 3])
        self.assertEqual(sumas_absolutas_por_fila(A), [3, 4])

    def test_la_barra_destacada_es_la_norma_infinito(self):
        A = [[1, 2], [3, 1]]
        figura = gm.normas_barras(sumas_absolutas_por_fila(A))
        colores = list(figura.data[0].marker.color)
        self.assertEqual(colores.index(gm.COLOR_MAXIMO), 1)                 # fila 2: 3 + 1 = 4
        self.assertEqual(max(figura.data[0].y), norma_infinito_matriz(A))    # 4

    def test_panel_de_columnas_se_rotula_como_referencia(self):
        figura = gm.normas_barras([3, 4], [F(4, 5), F(3, 5)], [4, 3])
        titulos = [a.text for a in figura.layout.annotations]
        self.assertTrue(any("complementaria" in t for t in titulos))
        self.assertEqual(len(figura.data), 3)


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
        self.assertLessEqual(valores[1], valores[2] + 1e-12)                 # la cota se cumple


if __name__ == "__main__":
    unittest.main()
