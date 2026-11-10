"""Pruebas de algebra/dispersas.py (incentivo «matrices dispersas»)."""

import time
import unittest

from algebra.modulo_IV_iterativos.dispersas import (
    a_csr,
    a_densa,
    paso_gauss_seidel_csr,
    producto_csr_vector,
    tridiagonal,
)
from algebra.modulo_IV_iterativos.iterativos import (
    CRITERIO_CAMBIO,
    CRITERIO_RESIDUO,
    ConfiguracionIterativa,
    GAUSS_SEIDEL,
    JACOBI,
    METODOS,
    SOR,
    TOLERANCIA_CAMBIO,
    ejecutar,
    paso_gauss_seidel,
)

S_A = [[10, -1, 2], [-1, 11, -1], [2, -1, 10]]
S_b = [6, 25, -11]


class TestFormatoCSR(unittest.TestCase):

    def test_ejemplo_tridiagonal_3x3(self):
        # Ejemplo del docstring, construido a mano
        M = a_csr([[4, -1, 0], [-1, 4, -1], [0, -1, 4]])
        self.assertEqual(M.valores, [4, -1, -1, 4, -1, -1, 4])
        self.assertEqual(M.columnas, [0, 1, 0, 1, 2, 1, 2])
        self.assertEqual(M.inicio, [0, 2, 5, 7])
        self.assertEqual(M.diagonal(), [4, 4, 4])

    def test_nnz_lamina(self):
        # S9-05/10 p. 8: tridiagonal 5x5 -> 5 + 4 + 4 = 13 no nulos
        M = a_csr(tridiagonal(5))
        self.assertEqual(M.nnz, 13)
        self.assertAlmostEqual(M.densidad, 13 / 25)

    def test_ida_y_vuelta(self):
        A = [[1, 0, 2], [0, 0, 3], [4, 5, 0]]
        self.assertEqual(a_densa(a_csr(A)), [[1, 0, 2], [0, 0, 3], [4, 5, 0]])

    def test_producto(self):
        # [[1,0,2],[0,0,3],[4,5,0]] · (1,2,3) = (7, 9, 14)
        self.assertEqual(producto_csr_vector(a_csr([[1, 0, 2], [0, 0, 3], [4, 5, 0]]), [1, 2, 3]),
                         [7, 9, 14])

    def test_memoria(self):
        M = a_csr(tridiagonal(100))
        # nnz = 100 + 99 + 99 = 298 ; CSR = 2·298 + 101 = 697 números frente a 10 000
        self.assertEqual(M.memoria(), {"csr": 697, "densa": 10000})


class TestIteracionesIdenticas(unittest.TestCase):

    def test_mismas_iteraciones_que_denso(self):
        for A, b in ((S_A, S_b), (tridiagonal(6), [1, 0, 0, 0, 0, 1])):
            for metodo in METODOS:
                for criterio in (CRITERIO_CAMBIO, CRITERIO_RESIDUO):
                    densa = ejecutar(A, b, ConfiguracionIterativa(metodo=metodo, criterio=criterio))
                    csr = ejecutar(A, b, ConfiguracionIterativa(metodo=metodo, criterio=criterio,
                                                               formato="csr"))
                    self.assertEqual([(f.x, f.d, f.r) for f in densa.historial],
                                     [(f.x, f.d, f.r) for f in csr.historial], (metodo, criterio))
                    self.assertEqual(densa.codigo, csr.codigo)

    def test_diagonal_cero_y_formato_invalido(self):
        r = ejecutar([[0, 1], [1, 0]], [1, 1], ConfiguracionIterativa(formato="csr"))
        self.assertEqual(r.codigo, "DIAGONAL_CERO")
        r = ejecutar(S_A, S_b, ConfiguracionIterativa(formato="xyz"))
        self.assertEqual(r.codigo, "ENTRADA_INVALIDA")

    def test_paso_csr_mas_rapido(self):
        # Tridiagonal 400x400: un paso CSR hace ~1 200 productos; el denso, 160 000.
        # Se mide solo el paso (coste por iteración), no la conversión de la entrada.
        n = 400
        A = tridiagonal(n)
        M = a_csr(A)
        b = [1.0] + [0.0] * (n - 2) + [1.0]
        x = [0.0] * n
        inicio = time.perf_counter()
        for _ in range(5):
            paso_gauss_seidel(A, b, x)
        t_densa = time.perf_counter() - inicio
        inicio = time.perf_counter()
        for _ in range(5):
            paso_gauss_seidel_csr(M, b, x)
        t_csr = time.perf_counter() - inicio
        self.assertLess(t_csr * 10, t_densa)   # al menos 10 veces más rápido
        r = ejecutar(A, b, ConfiguracionIterativa(metodo=GAUSS_SEIDEL, formato="csr", tolerancia=1e-8))
        self.assertEqual(r.codigo, TOLERANCIA_CAMBIO)


if __name__ == "__main__":
    unittest.main()
