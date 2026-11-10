"""Pruebas de algebra/matriz.py.

Los valores esperados se calcularon a mano (el desarrollo está en los
comentarios) o provienen de ejemplos del curso cuyo resultado se verificó por
sustitución.  Se indica la fuente cuando corresponde.
"""

import unittest
from fractions import Fraction

from algebra.compartido.matriz import (
    ErrorDimension,
    ErrorMatriz,
    copiar_matriz,
    dimensiones,
    es_cuadrada,
    es_numero,
    identidad,
    multiplicar_matrices,
    multiplicar_matriz_vector,
    norma_2_cuadrado_vector,
    norma_2_vector,
    norma_infinito_matriz,
    norma_infinito_vector,
    norma_residuo_infinito,
    producto_escalar,
    residuo,
    restar_matrices,
    restar_vectores,
    sumar_matrices,
    sumar_vectores,
    transpuesta,
    validar_cuadrada,
    validar_matriz,
    validar_sistema,
    validar_vector,
)


class TestValidacion(unittest.TestCase):

    def test_numeros_aceptados(self):
        for valor in (0, -3, 2.5, Fraction(1, 3)):
            self.assertTrue(es_numero(valor), valor)

    def test_numeros_rechazados(self):
        for valor in (True, False, None, "3", float("nan"), float("inf"),
                      float("-inf"), [1], 1 + 2j):
            self.assertFalse(es_numero(valor), valor)

    def test_matriz_valida_devuelve_dimensiones(self):
        self.assertEqual(validar_matriz([[1, 2, 3], [4, 5, 6]]), (2, 3))
        self.assertEqual(validar_matriz([[7]]), (1, 1))
        self.assertEqual(dimensiones([[1], [2]]), (2, 1))

    def test_matriz_vacia(self):
        with self.assertRaises(ErrorMatriz):
            validar_matriz([])
        with self.assertRaises(ErrorMatriz):
            validar_matriz([[]])

    def test_matriz_no_lista(self):
        for dato in (None, 5, "[[1]]", ([1, 2],), [(1, 2)]):
            with self.assertRaises(ErrorMatriz):
                validar_matriz(dato)

    def test_filas_de_distinto_tamano(self):
        with self.assertRaises(ErrorDimension):
            validar_matriz([[1, 2], [3]])

    def test_elemento_invalido_indica_posicion(self):
        with self.assertRaises(ErrorMatriz) as ctx:
            validar_matriz([[1, 2], [3, "x"]])
        self.assertIn("(2, 2)", str(ctx.exception))
        for malo in (None, True, float("nan"), float("inf")):
            with self.assertRaises(ErrorMatriz):
                validar_matriz([[1, malo]])

    def test_vector(self):
        self.assertEqual(validar_vector([1, 2.5, Fraction(1, 2)]), 3)
        with self.assertRaises(ErrorMatriz):
            validar_vector([])
        with self.assertRaises(ErrorMatriz):
            validar_vector([[1, 2]])  # una matriz no es un vector
        with self.assertRaises(ErrorMatriz):
            validar_vector((1, 2))
        with self.assertRaises(ErrorMatriz) as ctx:
            validar_vector([1, "a"])
        self.assertIn("componente 2", str(ctx.exception))

    def test_cuadrada(self):
        self.assertTrue(es_cuadrada([[1, 2], [3, 4]]))
        self.assertFalse(es_cuadrada([[1, 2, 3], [4, 5, 6]]))
        self.assertEqual(validar_cuadrada([[1, 2], [3, 4]]), 2)
        with self.assertRaises(ErrorDimension):
            validar_cuadrada([[1, 2, 3], [4, 5, 6]])

    def test_sistema_compatible(self):
        self.assertEqual(validar_sistema([[1, 2], [3, 4], [5, 6]], [1, 2, 3]), (3, 2))
        with self.assertRaises(ErrorDimension):
            validar_sistema([[1, 2], [3, 4]], [1, 2, 3])


class TestTranspuesta(unittest.TestCase):

    def test_rectangular(self):
        A = [[1, 2, 3], [4, 5, 6]]
        self.assertEqual(transpuesta(A), [[1, 4], [2, 5], [3, 6]])

    def test_doble_transpuesta(self):
        A = [[1, -2], [0, 5], [7, 3]]
        self.assertEqual(transpuesta(transpuesta(A)), A)

    def test_vector_fila_y_columna(self):
        self.assertEqual(transpuesta([[1, 2, 3]]), [[1], [2], [3]])

    def test_no_modifica_argumento(self):
        A = [[1, 2], [3, 4]]
        transpuesta(A)
        self.assertEqual(A, [[1, 2], [3, 4]])


class TestSumaResta(unittest.TestCase):

    def test_suma(self):
        self.assertEqual(sumar_matrices([[1, 2], [3, 4]], [[5, -6], [0, 1]]),
                         [[6, -4], [3, 5]])

    def test_resta(self):
        self.assertEqual(restar_matrices([[1, 2], [3, 4]], [[5, -6], [0, 1]]),
                         [[-4, 8], [3, 3]])

    def test_resta_consigo_misma_da_cero(self):
        A = [[2, -1, 0], [1, 3, 2]]
        self.assertEqual(restar_matrices(A, A), [[0, 0, 0], [0, 0, 0]])

    def test_fracciones_exactas(self):
        # 1/3 + 1/6 = 1/2 exactamente
        C = sumar_matrices([[Fraction(1, 3)]], [[Fraction(1, 6)]])
        self.assertEqual(C, [[Fraction(1, 2)]])
        self.assertIsInstance(C[0][0], Fraction)

    def test_dimensiones_distintas(self):
        with self.assertRaises(ErrorDimension):
            sumar_matrices([[1, 2]], [[1], [2]])
        with self.assertRaises(ErrorDimension):
            restar_matrices([[1, 2], [3, 4]], [[1, 2, 3], [4, 5, 6]])

    def test_operando_invalido(self):
        with self.assertRaises(ErrorMatriz):
            sumar_matrices([[1, 2]], [])


class TestProducto(unittest.TestCase):

    def test_producto_2x2(self):
        # [1 2][5 6]   [1*5+2*7  1*6+2*8]   [19 22]
        # [3 4][7 8] = [3*5+4*7  3*6+4*8] = [43 50]
        self.assertEqual(multiplicar_matrices([[1, 2], [3, 4]], [[5, 6], [7, 8]]),
                         [[19, 22], [43, 50]])

    def test_producto_no_conmutativo(self):
        # [5 6][1 2]   [5+18  10+24]   [23 34]
        # [7 8][3 4] = [7+24  14+32] = [31 46]
        self.assertEqual(multiplicar_matrices([[5, 6], [7, 8]], [[1, 2], [3, 4]]),
                         [[23, 34], [31, 46]])

    def test_producto_rectangular(self):
        # (2x3)(3x2) = 2x2:  1*7+2*9+3*11 = 58,  1*8+2*10+3*12 = 64,
        #                    4*7+5*9+6*11 = 139, 4*8+5*10+6*12 = 154
        A = [[1, 2, 3], [4, 5, 6]]
        B = [[7, 8], [9, 10], [11, 12]]
        self.assertEqual(multiplicar_matrices(A, B), [[58, 64], [139, 154]])

    def test_identidad(self):
        A = [[2, -1, 0], [1, 3, 2], [0, -2, 1]]
        I = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
        self.assertEqual(multiplicar_matrices(A, I), A)
        self.assertEqual(multiplicar_matrices(I, A), A)

    def test_transpuesta_del_producto(self):
        # Propiedad (AB)^T = B^T A^T
        A = [[1, 2, 3], [4, 5, 6]]
        B = [[7, 8], [9, 10], [11, 12]]
        self.assertEqual(transpuesta(multiplicar_matrices(A, B)),
                         multiplicar_matrices(transpuesta(B), transpuesta(A)))

    def test_dimensiones_incompatibles(self):
        with self.assertRaises(ErrorDimension) as ctx:
            multiplicar_matrices([[1, 2, 3]], [[1, 2, 3]])
        self.assertIn("1x3", str(ctx.exception))

    def test_no_modifica_argumentos(self):
        A = [[1, 2], [3, 4]]
        B = [[5, 6], [7, 8]]
        multiplicar_matrices(A, B)
        self.assertEqual((A, B), ([[1, 2], [3, 4]], [[5, 6], [7, 8]]))


class TestMatrizVector(unittest.TestCase):

    def test_ejemplo_lu_del_curso(self):
        # S6-16/09 p. 35: A x con x = (1, 1, 2) da b = (5, -2, 9)
        #   2+1+2 = 5,  4-6+0 = -2,  -2+7+4 = 9
        A = [[2, 1, 1], [4, -6, 0], [-2, 7, 2]]
        self.assertEqual(multiplicar_matriz_vector(A, [1, 1, 2]), [5, -2, 9])

    def test_matriz_rectangular(self):
        # (3x2) por x = (1, 1):  1+3 = 4,  3-2 = 1,  -2+5 = 3
        A = [[1, 3], [3, -2], [-2, 5]]
        self.assertEqual(multiplicar_matriz_vector(A, [1, 1]), [4, 1, 3])

    def test_dimension_incompatible(self):
        with self.assertRaises(ErrorDimension):
            multiplicar_matriz_vector([[1, 2], [3, 4]], [1, 2, 3])

    def test_vector_invalido(self):
        with self.assertRaises(ErrorMatriz):
            multiplicar_matriz_vector([[1, 2]], [1, None])


class TestNormaInfinito(unittest.TestCase):

    def test_ejemplos_del_curso(self):
        # S3-26/08 p. 25: u = (-2, 1, 7)  -> 7
        # S3-26/08 p. 26: (3, -4) -> 4 ;  (-1, 2, -3) -> 3
        self.assertEqual(norma_infinito_vector([-2, 1, 7]), 7)
        self.assertEqual(norma_infinito_vector([3, -4]), 4)
        self.assertEqual(norma_infinito_vector([-1, 2, -3]), 3)

    def test_negativo_dominante_y_un_elemento(self):
        self.assertEqual(norma_infinito_vector([-5]), 5)
        self.assertEqual(norma_infinito_vector([0, 0, 0]), 0)

    def test_no_es_la_suma(self):
        # La norma infinito es el máximo |v_i| = 1, no la suma
        # |1| + |-1| + |1| = 3 (eso sería la norma 1).
        self.assertEqual(norma_infinito_vector([1, -1, 1]), 1)

    def test_fraccion(self):
        self.assertEqual(norma_infinito_vector([Fraction(-7, 3), Fraction(1, 2)]),
                         Fraction(7, 3))

    def test_vacio(self):
        with self.assertRaises(ErrorMatriz):
            norma_infinito_vector([])


class TestResiduo(unittest.TestCase):

    def test_residuo_cero_en_solucion_entera(self):
        # S8-30/09 p. 19: 6x1+2x2+x3=22, -x1+8x2+2x3=30, x1-x2+6x3=23; sol (2,3,4)
        #   12+6+4 = 22,  -2+24+8 = 30,  2-3+24 = 23
        A = [[6, 2, 1], [-1, 8, 2], [1, -1, 6]]
        b = [22, 30, 23]
        self.assertEqual(residuo(A, [2, 3, 4], b), [0, 0, 0])
        self.assertEqual(norma_residuo_infinito(A, [2, 3, 4], b), 0)

    def test_residuo_cero_exacto_con_fracciones(self):
        # Sistema S (S8-30/09 pp. 17-18): solución exacta (217/208, 59/26, -225/208),
        # verificada por sustitución: 10*217/208 - 59/26 + 2*(-225/208) = 1248/208 = 6, etc.
        A = [[10, -1, 2], [-1, 11, -1], [2, -1, 10]]
        b = [6, 25, -11]
        x = [Fraction(217, 208), Fraction(59, 26), Fraction(-225, 208)]
        self.assertEqual(residuo(A, x, b), [0, 0, 0])

    def test_residuo_no_nulo(self):
        # A x = (2+1, 1+3) = (3, 4);  r = (4-3, 6-4) = (1, 2);  ||r||_inf = 2
        A = [[2, 1], [1, 3]]
        self.assertEqual(residuo(A, [1, 1], [4, 6]), [1, 2])
        self.assertEqual(norma_residuo_infinito(A, [1, 1], [4, 6]), 2)

    def test_signo_b_menos_Ax(self):
        # r = b - A x (no A x - b): con A=[[1]], x=[3], b=[1] -> r = [-2]
        self.assertEqual(residuo([[1]], [3], [1]), [-2])

    def test_sistema_rectangular(self):
        # Mínimos cuadrados (S8-30/09 p. 6): A 3x2, b de 3 componentes.
        # A x con x=(1,1): (4, 1, 3);  b=(-1, 8, -8);  r = (-5, 7, -11)
        A = [[1, 3], [3, -2], [-2, 5]]
        self.assertEqual(residuo(A, [1, 1], [-1, 8, -8]), [-5, 7, -11])

    def test_dimensiones_incompatibles(self):
        A = [[1, 2], [3, 4]]
        with self.assertRaises(ErrorDimension):
            residuo(A, [1, 2], [1, 2, 3])   # b demasiado largo
        with self.assertRaises(ErrorDimension):
            residuo(A, [1, 2, 3], [1, 2])   # x demasiado largo


class TestOperacionesAuxiliares(unittest.TestCase):

    def test_norma_infinito_matriz(self):
        # S7-21/09 p. 19: B = [[1, 2], [3, 1]] -> filas 3 y 4 -> ||B||_inf = 4
        self.assertEqual(norma_infinito_matriz([[1, 2], [3, 1]]), 4)
        # Con negativos: filas |2|+|-1|+|0| = 3, |1|+|3|+|2| = 6, |0|+|-2|+|1| = 3
        self.assertEqual(norma_infinito_matriz([[2, -1, 0], [1, 3, 2], [0, -2, 1]]), 6)
        self.assertEqual(norma_infinito_matriz([[Fraction(-1, 2), Fraction(1, 3)]]),
                         Fraction(5, 6))

    def test_producto_escalar(self):
        self.assertEqual(producto_escalar([1, 2, 3], [4, 5, 6]), 32)  # 4+10+18
        with self.assertRaises(ErrorDimension):
            producto_escalar([1, 2], [1, 2, 3])

    def test_suma_resta_vectores(self):
        self.assertEqual(sumar_vectores([1, 2], [3, -5]), [4, -3])
        self.assertEqual(restar_vectores([1, 2], [3, -5]), [-2, 7])
        with self.assertRaises(ErrorDimension):
            restar_vectores([1], [1, 2])

    def test_norma_2(self):
        # S3-26/08: ||(3,-4)||_2 = 5 ;  S3-26/08 p. 22: ||(2,3,-1)||_2^2 = 14
        self.assertEqual(norma_2_vector([3, -4]), 5.0)
        self.assertEqual(norma_2_cuadrado_vector([2, 3, -1]), 14)

    def test_identidad_y_copia(self):
        self.assertEqual(identidad(2), [[1, 0], [0, 1]])
        for malo in (0, -1, 2.0, True):
            with self.assertRaises(ErrorMatriz):
                identidad(malo)
        A = [[1, 2], [3, 4]]
        C = copiar_matriz(A)
        C[0][0] = 99
        self.assertEqual(A[0][0], 1)


if __name__ == "__main__":
    unittest.main()
