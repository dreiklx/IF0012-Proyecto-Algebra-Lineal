"""Pruebas de la tabla y de la gráfica de ajuste del Módulo III.

Comprueban que los residuos son yᵢ − ŷᵢ con los datos introducidos, que la recta corresponde
al cálculo de mínimos cuadrados y que la figura cambia al cambiar los datos.
"""

import unittest
from fractions import Fraction as F

from algebra.modulo_III_minimos.minimos import ajuste_lineal
from interfaz.modulos.modulo_III_minimos import tabla_ajuste
from visualizacion.interactivas import ajuste as grafica_ajuste


class TestResiduosDelAjuste(unittest.TestCase):
    def setUp(self):
        self.xs = [0, 1, 2, 3]
        self.ys = [1, 2, 2, 4]
        self.r = ajuste_lineal(self.xs, self.ys)

    def test_residuos_son_observado_menos_estimado(self):
        for x, y, est in zip(self.r.xs, self.r.ys, self.r.minimos.estimados):
            self.assertEqual(y - est, y - (self.r.pendiente * x + self.r.intercepto))

    def test_la_suma_de_residuos_es_cero_con_intercepto(self):
        # Propiedad de las ecuaciones normales con columna de unos: Aᵀr = 0 ⇒ Σ rᵢ = 0.
        self.assertEqual(sum(self.ys[i] - self.r.minimos.estimados[i] for i in range(4)), 0)

    def test_tabla_tiene_una_fila_por_punto_y_columnas_correctas(self):
        filas = tabla_ajuste(self.r)
        self.assertEqual(len(filas), 4)
        self.assertEqual(set(filas[0]), {"i", "xᵢ", "yᵢ (observado)", "ŷᵢ = m·xᵢ + c (estimado)", "rᵢ = yᵢ − ŷᵢ"})
        self.assertEqual(filas[0]["i"], 1)

    def test_recta_corresponde_al_calculo_de_minimos_cuadrados(self):
        # Ecuaciones normales a mano: AᵀA = [[14, 6], [6, 4]], Aᵀb = (18, 9); det = 20 ⇒ m = c = 9/10.
        self.assertEqual(self.r.pendiente, F(9, 10))
        self.assertEqual(self.r.intercepto, F(9, 10))


class TestGraficaSeActualiza(unittest.TestCase):
    def _segmentos(self, figura):
        return figura.data[0]

    def test_residuos_dibujados_como_segmentos_verticales(self):
        r = ajuste_lineal([0, 1, 2, 3], [1, 2, 2, 4])
        figura = grafica_ajuste(r.xs, r.ys, r.pendiente, r.intercepto, r.minimos.estimados)
        residuos = figura.data[0]
        # Cada punto aporta (x, y), (x, ŷ) y un hueco: 3 valores por punto.
        self.assertEqual(len(residuos.x), 3 * len(r.xs))
        for i in range(len(r.xs)):
            self.assertEqual(residuos.x[3 * i], residuos.x[3 * i + 1])              # vertical
            self.assertEqual(residuos.y[3 * i], float(r.ys[i]))
            self.assertAlmostEqual(residuos.y[3 * i + 1], float(r.minimos.estimados[i]))

    def test_cambiar_los_datos_cambia_la_figura(self):
        r1 = ajuste_lineal([0, 1, 2], [0, 1, 2])
        r2 = ajuste_lineal([0, 1, 2], [0, 3, 2])
        f1 = grafica_ajuste(r1.xs, r1.ys, r1.pendiente, r1.intercepto, r1.minimos.estimados)
        f2 = grafica_ajuste(r2.xs, r2.ys, r2.pendiente, r2.intercepto, r2.minimos.estimados)
        self.assertNotEqual(list(f1.data[1].y), list(f2.data[1].y))


if __name__ == "__main__":
    unittest.main()
