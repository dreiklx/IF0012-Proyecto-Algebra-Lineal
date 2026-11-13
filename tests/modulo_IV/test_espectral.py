"""Pruebas del radio espectral con los procedimientos de clase (Sarrus y fórmula cuadrática).

Los valores de referencia son los de S9-07/10 pp. 5-7 (imágenes revisadas) y se calculan
también a mano en cada caso. ρ solo se calcula cuando el curso lo permite (OFICIAL p. 2).
"""

import unittest
from fractions import Fraction as F

from algebra.modulo_IV_iterativos.espectral import (
    CONVERGE,
    INDETERMINADO,
    NO_CALCULADO,
    NO_CONVERGE,
    analizar_matriz,
    concluir,
    radio_espectral,
)
from algebra.modulo_IV_iterativos.metodos import GAUSS_SEIDEL, JACOBI, SOR
from algebra.modulo_IV_iterativos.polinomio_raices import (
    polinomio_caracteristico,
    raices,
    texto_polinomio_curso,
)

A_LAMINA = [[3, 3, 3], [3, 3, 2], [-3, -2, 3]]
B_LAMINA = [9, 9, -2]


class TestPolinomioCaracteristico(unittest.TestCase):
    def test_sarrus_3x3_de_jacobi(self):
        # T_J de S9-07/10 p. 4: det(T − λI) = −λ³ − (4/9)λ + 4/3 (la lámina omite +4/3).
        T = [[0, -1, -1], [-1, 0, F(-2, 3)], [1, F(2, 3), 0]]
        self.assertEqual(polinomio_caracteristico(T), [1, 0, F(4, 9), F(-4, 3)])
        self.assertEqual(texto_polinomio_curso(polinomio_caracteristico(T)),
                         "det(T − λI) = −λ³ − 4/9λ + 4/3")

    def test_sarrus_3x3_de_gauss_seidel(self):
        # T_GS de S9-07/10 p. 6: el polinomio sale con factor λ (raíz 0).
        T = [[0, -1, -1], [0, 1, F(1, 3)], [0, F(-1, 3), F(-7, 9)]]
        self.assertEqual(polinomio_caracteristico(T), [1, F(-2, 9), F(-2, 3), 0])

    def test_2x2(self):
        self.assertEqual(polinomio_caracteristico([[2, 1], [1, 2]]), [1, -4, 3])   # (λ−1)(λ−3)

    def test_mas_de_3x3_no_se_calcula(self):
        with self.assertRaises(ValueError):
            polinomio_caracteristico([[1] * 4 for _ in range(4)])


class TestRaices(unittest.TestCase):
    def test_gauss_seidel_raices_de_la_lamina(self):
        # S9-07/10 p. 7: λ₁ = 0,9351; λ₂ = −0,7129; λ₃ = 0.
        autovalores, ceros = raices([1, F(-2, 9), F(-2, 3), 0])
        self.assertEqual(ceros, 1)
        reales = sorted(round(z.real, 4) for z in autovalores)
        self.assertEqual(reales, [-0.7129, 0.0, 0.9351])

    def test_grado_tres_sin_factor_lambda_no_se_resuelve(self):
        autovalores, ceros = raices([1, 0, F(4, 9), F(-4, 3)])
        self.assertIsNone(autovalores)

    def test_raices_complejas_de_grado_dos(self):
        autovalores, _ = raices([1, 0, 1])                  # λ² + 1
        self.assertEqual(sorted(z.imag for z in autovalores), [-1.0, 1.0])


class TestRadioEspectral(unittest.TestCase):
    def test_gauss_seidel_converge_con_rho_de_la_lamina(self):
        r = radio_espectral(A_LAMINA, B_LAMINA, GAUSS_SEIDEL)
        self.assertEqual(r.conclusion, CONVERGE)
        self.assertAlmostEqual(r.rho, 0.9351, places=4)
        self.assertTrue(r.fiable)
        self.assertEqual(r.multiplicidad_cero, 1)

    def test_jacobi_no_se_calcula_con_el_curso(self):
        # ρ(T_J) = 1,1744 requiere raíces de un cúbico sin factor λ: no es procedimiento de clase.
        r = radio_espectral(A_LAMINA, B_LAMINA, JACOBI)
        self.assertEqual(r.conclusion, NO_CALCULADO)
        self.assertIsNone(r.rho)
        self.assertIn("−λ³", r.polinomio_curso)

    def test_sor_no_se_calcula(self):
        r = radio_espectral(A_LAMINA, B_LAMINA, SOR, 1.2)
        self.assertEqual(r.conclusion, NO_CALCULADO)
        self.assertIsNone(r.rho)
        self.assertIn("SOR", r.mensaje)

    def test_n_mayor_que_3_no_se_calcula(self):
        A4 = [[4, -1, 0, 0], [-1, 4, -1, 0], [0, -1, 4, -1], [0, 0, -1, 4]]
        r = radio_espectral(A4, [1, 0, 0, 1], GAUSS_SEIDEL)
        self.assertEqual(r.conclusion, NO_CALCULADO)
        self.assertIn("n > 3", r.mensaje)

    def test_matriz_con_autovalor_uno_es_indeterminada(self):
        # T = [[1, 0], [0, 0]] tiene λ = 1: ρ = 1 y la conclusión no es decidible.
        a = analizar_matriz([[1, 0], [0, 0]])
        self.assertEqual(a.rho, 1)
        self.assertEqual(concluir(a.rho, a.fiable), INDETERMINADO)


class TestConclusion(unittest.TestCase):
    def test_teorema_del_curso(self):
        self.assertEqual(concluir(0.5, True), CONVERGE)
        self.assertEqual(concluir(1.2, True), NO_CONVERGE)
        self.assertEqual(concluir(0.5, False), INDETERMINADO)


if __name__ == "__main__":
    unittest.main()
