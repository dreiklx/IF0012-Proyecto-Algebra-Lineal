"""Pruebas del precondicionador diagonal M = D (incentivo, OFICIAL p. 5).

Procedimiento de clase: S9-05/10 pp. 19-23 (M = D, B = M⁻¹A, b̃ = M⁻¹b) y κ∞ del Módulo II.
Se comprueba que T y c no cambian con M = D para Jacobi y Gauss-Seidel (exacto), y que
las iteraciones coinciden. Richardson se retiró por no aparecer en los materiales del curso.
"""

import unittest
from fractions import Fraction as F

from algebra.modulo_IV_iterativos.ejecucion import ConfiguracionIterativa
from algebra.modulo_IV_iterativos.metodos import GAUSS_SEIDEL, JACOBI, SOR
from algebra.modulo_IV_iterativos.precondicionamiento import analizar_precondicionador, precondicionar_diagonal

TRIDIAGONAL = [[4, -1, 0, 0], [-1, 4, -1, 0], [0, -1, 4, -1], [0, 0, -1, 4]]
B_TRI = [1, 0, 0, 1]


class TestPrecondicionarDiagonal(unittest.TestCase):
    def test_b_tilde_y_B_son_D_inverso_por_A_y_b(self):
        A = [[3, 3, 3], [3, 3, 2], [-3, -2, 3]]
        M, M_inv, B, b_tilde = precondicionar_diagonal(A, [9, 9, -2])
        self.assertEqual(M, [[3, 0, 0], [0, 3, 0], [0, 0, 3]])
        self.assertEqual(B[0], [1, 1, 1])                       # fila 1 de D⁻¹A = (1, 1, 1)
        self.assertEqual(b_tilde, [3, 3, F(-2, 3)])

    def test_diagonal_nula_se_rechaza(self):
        from algebra.compartido.validacion import ErrorEntrada
        with self.assertRaises(ErrorEntrada):
            precondicionar_diagonal([[0, 1], [1, 2]], [1, 1])


class TestAnalisisPrecondicionador(unittest.TestCase):
    def setUp(self):
        self.r = analizar_precondicionador(TRIDIAGONAL, B_TRI, ConfiguracionIterativa(tolerancia=1e-4, k_max=60))

    def test_metodos_comparados_sin_richardson(self):
        self.assertEqual([f.metodo for f in self.r.comparaciones], [JACOBI, GAUSS_SEIDEL, SOR])

    def test_jacobi_y_gauss_seidel_tienen_T_y_c_identicas(self):
        # Verificado con fracciones: en B = D⁻¹A la diagonal es I y T no cambia.
        por_metodo = {f.metodo: f for f in self.r.comparaciones}
        self.assertTrue(por_metodo[JACOBI].T_identicas)
        self.assertTrue(por_metodo[GAUSS_SEIDEL].T_identicas)
        self.assertIsNone(por_metodo[SOR].T_identicas)

    def test_mismas_iteraciones_con_y_sin_precondicionador(self):
        por_metodo = {f.metodo: f for f in self.r.comparaciones}
        self.assertTrue(por_metodo[JACOBI].mismas_iteraciones)
        self.assertTrue(por_metodo[GAUSS_SEIDEL].mismas_iteraciones)

    def test_kappa_de_A_y_de_B_son_numeros_exactos(self):
        self.assertIsNotNone(self.r.kappa_A)
        self.assertIsNotNone(self.r.kappa_B)
        self.assertIsInstance(self.r.kappa_B, F)

    def test_n_mayor_que_3_no_calcula_rho(self):
        for f in self.r.comparaciones:
            self.assertIsNone(f.rho_original)
            self.assertIsNone(f.rho_precondicionado)


if __name__ == "__main__":
    unittest.main()
