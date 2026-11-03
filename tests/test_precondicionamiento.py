"""Pruebas de las funciones añadidas en la revisión del 03-nov-2026:
precondicionador diagonal, Richardson, reordenamiento dominante, desarrollo
de Sarrus y verificación de mínimos cuadrados por Cramer.

Oráculos independientes del código probado:
  * lámina S9-05/10 diapositiva 18 (M⁻¹A = A/4 en la tridiagonal [-1, 4, -1]),
    revisada a mano;
  * inversas 2x2 por la fórmula de la adjunta, calculadas a mano;
  * autovalores teóricos de la tridiagonal: λ_k = 4 - 2cos(kπ/5);
  * manuscrito S8-30/09 pp. 6-7 (det([A|b]) = -11; Cramer 363, 715, -319),
    recalculado a mano;
  * menores principales y Sarrus de T_J de S9-07/10, calculados a mano.
"""

import math
import unittest
from fractions import Fraction as F

from algebra.espectral import desarrollo_sarrus, matriz_iteracion
from algebra.iterativos import (
    CRITERIO_CAMBIO,
    GAUSS_SEIDEL,
    JACOBI,
    METODOS,
    RICHARDSON,
    SOR,
    ConfiguracionIterativa,
    ejecutar,
    paso_richardson,
    reordenamiento_dominante,
)
from algebra.minimos import minimos_cuadrados
from algebra.precondicionamiento import analizar_precondicionador, precondicionar_diagonal
from algebra.validacion import ErrorEntrada

TRIDIAGONAL = [[4, -1, 0, 0], [-1, 4, -1, 0], [0, -1, 4, -1], [0, 0, -1, 4]]


class TestPrecondicionadorDiagonal(unittest.TestCase):

    def test_construccion_como_en_la_lamina(self):
        M, M_inv, B, b_t = precondicionar_diagonal(TRIDIAGONAL, [1, 0, 0, 1])
        self.assertEqual([M[i][i] for i in range(4)], [4, 4, 4, 4])
        self.assertEqual(B, [[F(v, 4) for v in fila] for fila in TRIDIAGONAL])
        self.assertEqual(b_t, [F(1, 4), 0, 0, F(1, 4)])
        self.assertEqual(M_inv[0][0], F(1, 4))

    def test_diagonal_cero(self):
        with self.assertRaises(ErrorEntrada):
            precondicionar_diagonal([[0, 1], [1, 0]], [1, 1])

    def test_T_identicas_en_jacobi_gs_sor(self):
        # Teorema: T y c no cambian con M = D (ver docstring del módulo).
        A = [[5, 2, -1], [1, -7, 3], [2, 1, 9]]
        b = [3, -1, 4]
        _, _, B, b_t = precondicionar_diagonal(A, b)
        for metodo, w in ((JACOBI, None), (GAUSS_SEIDEL, None), (SOR, F(3, 2))):
            original = matriz_iteracion(A, b, metodo, w)
            nueva = matriz_iteracion(B, b_t, metodo, w)
            self.assertEqual(original.T, nueva.T, metodo)
            self.assertEqual(original.c, nueva.c, metodo)

    def test_comparacion_tridiagonal(self):
        r = analizar_precondicionador(TRIDIAGONAL, [1, 0, 0, 1],
                                      ConfiguracionIterativa(tolerancia=1e-4, k_max=200), F(5, 4))
        # Diagonal uniforme: D⁻¹A = A/4 y κ no cambia (κ(cA) = κ(A)).
        self.assertEqual(r.kappa_A, r.kappa_B)
        por_metodo = {f.metodo: f for f in r.comparaciones}
        for metodo in METODOS:
            self.assertTrue(por_metodo[metodo].T_identicas)
            self.assertTrue(por_metodo[metodo].mismas_iteraciones)
        rich = por_metodo[RICHARDSON]
        # ρ(I - A) = máx |1 - λ_k| con λ_k = 4 - 2cos(kπ/5)  -> 3 + 2cos(π/5)
        self.assertAlmostEqual(rich.rho_original, 3 + 2 * math.cos(math.pi / 5), places=10)
        # ρ(I - D⁻¹A) = ρ(T_J) = cos(π/5)/2
        self.assertAlmostEqual(rich.rho_precondicionado, math.cos(math.pi / 5) / 2, places=10)
        self.assertEqual(rich.precondicionado.codigo, "TOLERANCIA_CAMBIO")
        self.assertNotEqual(rich.original.codigo, "TOLERANCIA_CAMBIO")
        # Richardson precondicionado con M = D es Jacobi: mismas iteraciones.
        self.assertEqual([fila.x for fila in rich.precondicionado.historial],
                         [fila.x for fila in por_metodo[JACOBI].original.historial])

    def test_kappa_cambia_con_diagonal_no_uniforme(self):
        # A = [[100, 1], [1, 1/50]]: det = 1, A⁻¹ = [[1/50, -1], [-1, 100]] -> κ = 101·101.
        # B = D⁻¹A = [[1, 1/100], [50, 1]]: det = 1/2, B⁻¹ = [[2, -1/50], [-100, 2]]
        #   -> κ = 51 · 102 = 5202.
        r = analizar_precondicionador([[100, 1], [1, F(1, 50)]], [1, 1])
        self.assertEqual(r.kappa_A, 10201)
        self.assertEqual(r.kappa_B, 5202)
        self.assertTrue(any("mejora" in t for t in r.conclusiones))


class TestRichardson(unittest.TestCase):

    def test_paso(self):
        # x1 = x0 + b - A x0 con x0 = (1, 2): A x0 = (4, 5) -> x1 = (1+1-4, 2+3-5) = (-2, 0)
        self.assertEqual(paso_richardson([[2, 1], [1, 2]], [1, 3], [1.0, 2.0]), [-2.0, 0.0])

    def test_no_exige_diagonal_no_nula(self):
        # A = [[0, 1/2], [1/2, 0]]: T = I - A tiene ρ = 3/2; no debe dar DIAGONAL_CERO.
        r = ejecutar([[0, 0.5], [0.5, 0]], [1, 1], ConfiguracionIterativa(metodo=RICHARDSON))
        self.assertNotEqual(r.codigo, "DIAGONAL_CERO")


class TestReordenamientoDominante(unittest.TestCase):

    def test_tarea2_item3_desordenada(self):
        # Ecuaciones de la Tarea II #3 en otro orden; el orden dominante es (E3, E1, E2).
        A = [[-1, 4, -1], [0, -1, 3], [4, -1, 0]]
        A_r, b_r, orden = reordenamiento_dominante(A, [10, 10, 15])
        self.assertEqual(A_r, [[4, -1, 0], [-1, 4, -1], [0, -1, 3]])
        self.assertEqual(b_r, [15, 10, 10])
        self.assertEqual(orden, [2, 0, 1])

    def test_sin_reordenamiento_posible(self):
        self.assertIsNone(reordenamiento_dominante([[1, 1], [1, 1]], [1, 1]))
        # S9-07/10: ninguna fila tiene un elemento mayor que la suma del resto.
        self.assertIsNone(reordenamiento_dominante([[3, 3, 3], [3, 3, 2], [-3, -2, 3]], [9, 9, -2]))

    def test_ya_dominante_conserva_orden(self):
        A = [[10, -1, 2], [-1, 11, -1], [2, -1, 10]]
        self.assertEqual(reordenamiento_dominante(A, [6, 25, -11])[2], [0, 1, 2])


class TestProcedimientosDeClase(unittest.TestCase):

    def test_sarrus_S9_jacobi(self):
        # T_J = [[0,-1,-1],[-1,0,-2/3],[1,2/3,0]]
        # menores: (0 - 1) + (0 + 1) + (0 + 4/9) = 4/9
        # det (Sarrus): 0 + (-1)(-2/3)(1) + (-1)(-1)(2/3) - [(-1)(0)(1) + 0 + (-1)(-1)(0)] = 4/3
        T = [[0, -1, -1], [-1, 0, F(-2, 3)], [1, F(2, 3), 0]]
        self.assertEqual(desarrollo_sarrus(T), (0, F(4, 9), F(4, 3)))

    def test_sarrus_solo_3x3(self):
        with self.assertRaises(ErrorEntrada):
            desarrollo_sarrus([[1, 0], [0, 1]])

    def test_minimos_como_el_manuscrito(self):
        r = minimos_cuadrados([[1, 3], [3, -2], [-2, 5]], [-1, 8, -8])
        self.assertEqual(r.det_aumentada, -11)
        self.assertEqual(r.cramer["det"], 363)
        self.assertEqual(r.cramer["dets"], [715, -319])
        self.assertEqual(r.cramer["solucion"], [F(65, 33), F(-29, 33)])
        self.assertEqual(r.cramer["solucion"], r.solucion)

    def test_minimos_sin_det_aumentada_si_m_distinto_de_n_mas_1(self):
        r = minimos_cuadrados([[1, 1], [2, 1], [3, 1], [4, 1]], [2, 2.5, 3.7, 4.1])
        self.assertIsNone(r.det_aumentada)
        self.assertEqual(r.cramer["solucion"], [F(3, 4), F(6, 5)])


if __name__ == "__main__":
    unittest.main()
