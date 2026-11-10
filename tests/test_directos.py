"""Pruebas de algebra/directos.py (Módulo I).

Oráculos: las soluciones esperadas se comprobaron a mano por sustitución en
las ecuaciones originales (el cálculo figura en cada comentario).  Varios
ejemplos provienen de las láminas; cuando la lámina tiene un error, se usa el
valor correcto y se indica.
"""

import unittest
from fractions import Fraction as F

from algebra.compartido.matriz import ErrorDimension, ErrorMatriz
from algebra.directos import (
    ErrorSistema,
    INCONSISTENTE,
    INFINITAS,
    PIVOTEO_PARCIAL,
    UNICA,
    determinante,
    inversa_gauss_jordan,
    resolver_gauss,
    resolver_gauss_jordan,
    solucion_unica,
)


def evaluar(A, x):
    """A x calculado con ciclos simples, para comprobar soluciones."""
    return [sum(F(A[i][j]) * x[j] for j in range(len(x))) for i in range(len(A))]


class TestSolucionUnica(unittest.TestCase):

    def comprobar_ambos_metodos(self, A, b, esperado):
        for resolver in (resolver_gauss, resolver_gauss_jordan):
            r = resolver(A, b)
            self.assertEqual(r.clasificacion, UNICA, r.metodo)
            self.assertEqual(r.solucion, esperado, r.metodo)
            self.assertEqual(evaluar(A, r.solucion), [F(v) for v in b])

    def test_manuscrito_s6_16_09_p29(self):
        # x+y+z=6, 2x+y-z=3, -x+y+2z=7 -> (1/3, 4, 5/3)
        # 1/3+4+5/3 = 6;  2/3+4-5/3 = 3;  -1/3+4+10/3 = 7
        self.comprobar_ambos_metodos([[1, 1, 1], [2, 1, -1], [-1, 1, 2]], [6, 3, 7],
                                     [F(1, 3), F(4), F(5, 3)])

    def test_lamina_gauss_corregida(self):
        # S6-14/09 p. 29: la lámina da (1/2, -1, -1), que NO satisface el sistema.
        # Correcto: (19/20, -5/4, -7/20):  38/20 - 25/20 + 7/20 = 1;
        #   19/20 + 75/20 - 14/20 = 4;  57/20 - 50/20 - 7/20 = 0
        self.comprobar_ambos_metodos([[2, 1, -1], [1, -3, 2], [3, 2, 1]], [1, 4, 0],
                                     [F(19, 20), F(-5, 4), F(-7, 20)])

    def test_lamina_oef_corregida(self):
        # S3-24/08 p. 3: la lámina da (2, 1, -1) (incorrecto). Correcto: (16/5, 1, -3/5)
        #   32/5+1+3/5 = 8;  16/5-1-6/5 = 1;  48/5+2-3/5 = 11
        self.comprobar_ambos_metodos([[2, 1, -1], [1, -1, 2], [3, 2, 1]], [8, 1, 11],
                                     [F(16, 5), F(1), F(-3, 5)])

    def test_ejemplo_lu(self):
        # S6-16/09 p. 35 -> (1, 1, 2), verificado: (5, -2, 9)
        self.comprobar_ambos_metodos([[2, 1, 1], [4, -6, 0], [-2, 7, 2]], [5, -2, 9],
                                     [F(1), F(1), F(2)])

    def test_pivote_cero_requiere_intercambio(self):
        # y = 2, x + y = 3 -> (1, 2); a11 = 0 obliga a F1 <-> F2
        r = resolver_gauss([[0, 1], [1, 1]], [2, 3])
        self.assertEqual(r.solucion, [F(1), F(2)])
        self.assertTrue(any("↔" in p.descripcion for p in r.pasos))

    def test_pivote_cero_en_medio(self):
        # Tras eliminar la columna 1 aparece un 0 en (2,2): x+y+z=3, x+y+2z=4, x+2y+z=4
        # Solución (1, 1, 1): 3, 4, 4
        r = resolver_gauss([[1, 1, 1], [1, 1, 2], [1, 2, 1]], [3, 4, 4])
        self.assertEqual(r.solucion, [1, 1, 1])
        self.assertTrue(any("F2 ↔ F3" in p.descripcion for p in r.pasos))

    def test_pivoteo_parcial_misma_solucion(self):
        A, b = [[1, 1, 1], [2, 1, -1], [-1, 1, 2]], [6, 3, 7]
        r = resolver_gauss(A, b, pivoteo=PIVOTEO_PARCIAL)
        self.assertEqual(r.solucion, [F(1, 3), F(4), F(5, 3)])
        # |2| > |1| en la columna 1 -> el pivoteo parcial intercambia F1 y F2
        self.assertIn("F1 ↔ F2", r.pasos[1].descripcion)

    def test_sobredeterminado_compatible(self):
        # x+y=2, x-y=0, 2x=2 -> (1, 1)
        r = resolver_gauss([[1, 1], [1, -1], [2, 0]], [2, 0, 2])
        self.assertEqual((r.clasificacion, r.solucion), (UNICA, [1, 1]))

    def test_entrada_float(self):
        # 2.5 x = 5 -> x = 2 ; los float se convierten al decimal escrito
        self.assertEqual(resolver_gauss([[2.5]], [5]).solucion, [2])
        self.assertEqual(resolver_gauss([[0.1]], [0.3]).solucion, [3])

    def test_solucion_unica_helper(self):
        self.assertEqual(solucion_unica([[2, 0], [0, 4]], [2, 8]), [1, 2])
        with self.assertRaises(ErrorSistema) as ctx:
            solucion_unica([[1, 1], [1, 1]], [1, 2])
        self.assertEqual(ctx.exception.resultado.clasificacion, INCONSISTENTE)


class TestInfinitasEInconsistentes(unittest.TestCase):

    def test_infinitas_una_libre(self):
        # x+y+z=1, 2x+2y+2z=2, x-y=0: la 2a ecuación es el doble de la 1a.
        A, b = [[1, 1, 1], [2, 2, 2], [1, -1, 0]], [1, 2, 0]
        for resolver in (resolver_gauss, resolver_gauss_jordan):
            r = resolver(A, b)
            self.assertEqual(r.clasificacion, INFINITAS)
            self.assertEqual((r.rango_A, r.rango_aumentada), (2, 2))
            self.assertEqual(len(r.variables_libres), 1)
            # Toda x = xp + t v debe cumplir A x = b (comprobado para varios t)
            for t in (F(0), F(1), F(-3), F(5, 2)):
                x = [r.solucion_particular[i] + t * r.direcciones[0][i] for i in range(3)]
                self.assertEqual(evaluar(A, x), [1, 2, 0])
            self.assertEqual(evaluar(A, r.direcciones[0]), [0, 0, 0])

    def test_infinitas_subdeterminado(self):
        # Una ecuación, tres incógnitas: x + y + z = 3 -> 2 variables libres
        r = resolver_gauss([[1, 1, 1]], [3])
        self.assertEqual(r.clasificacion, INFINITAS)
        self.assertEqual(r.variables_libres, [1, 2])
        self.assertEqual(r.solucion_particular, [3, 0, 0])
        self.assertEqual(r.direcciones, [[-1, 1, 0], [-1, 0, 1]])

    def test_inconsistente(self):
        # x + y = 1, x + y = 2 -> 0 = 1
        r = resolver_gauss([[1, 1], [1, 1]], [1, 2])
        self.assertEqual(r.clasificacion, INCONSISTENTE)
        self.assertEqual((r.rango_A, r.rango_aumentada), (1, 2))
        self.assertIsNone(r.solucion)
        self.assertIn("0 = 1", r.mensaje)

    def test_inconsistente_tarea2_item1(self):
        # Tarea II #1: x+y=2, 2x+y=2, x+2y=3 no tiene solución exacta
        # (de las dos primeras x=0, y=2, pero 0+4 = 4 != 3) -> requiere mínimos cuadrados
        r = resolver_gauss([[1, 1], [2, 1], [1, 2]], [2, 2, 3])
        self.assertEqual(r.clasificacion, INCONSISTENTE)

    def test_matriz_nula(self):
        r = resolver_gauss([[0, 0], [0, 0]], [0, 0])
        self.assertEqual((r.clasificacion, r.rango_A), (INFINITAS, 0))
        r = resolver_gauss([[0, 0], [0, 0]], [0, 1])
        self.assertEqual(r.clasificacion, INCONSISTENTE)


class TestInversaYDeterminante(unittest.TestCase):

    def test_inversa_2x2_del_curso(self):
        # S3-24/08 p. 6: [[2,1],[1,1]]^-1 = [[1,-1],[-1,2]]
        r = inversa_gauss_jordan([[2, 1], [1, 1]])
        self.assertTrue(r.invertible)
        self.assertEqual(r.inversa, [[1, -1], [-1, 2]])
        self.assertTrue(r.verificacion_identidad)
        self.assertEqual(r.determinante, 1)

    def test_inversa_3x3_manuscrito_corregido(self):
        # S3-24/08 p. 8: el manuscrito tiene error en la 1a columna.
        # Correcto (comprobado: A·A^-1 = I):
        esperado = [[F(1, 8), F(1, 4), F(1, 8)],
                    [F(-1, 8), F(-5, 4), F(7, 8)],
                    [F(3, 8), F(3, 4), F(-5, 8)]]
        r = inversa_gauss_jordan([[1, 2, 3], [2, -1, -1], [3, 0, -1]])
        self.assertEqual(r.inversa, esperado)
        self.assertTrue(r.verificacion_identidad)

    def test_inversa_por_adjunta_como_oraculo(self):
        # A = [[2,-1,0],[1,3,2],[0,-2,1]]: cofactores (calculados a mano)
        # C = [[7,-1,-2],[1,2,4],[-2,-4,7]], det = 2·7 + (-1)(-1) = 15,
        # A^-1 = C^T / 15.  (La lámina S3-24/08 p. 25-27 tiene det = 42: incorrecto.)
        Ct = [[7, 1, -2], [-1, 2, -4], [-2, 4, 7]]
        esperado = [[F(v, 15) for v in fila] for fila in Ct]
        r = inversa_gauss_jordan([[2, -1, 0], [1, 3, 2], [0, -2, 1]])
        self.assertEqual(r.inversa, esperado)
        self.assertEqual(r.determinante, 15)

    def test_inversa_con_intercambio(self):
        r = inversa_gauss_jordan([[0, 1], [1, 0]])
        self.assertEqual(r.inversa, [[0, 1], [1, 0]])
        self.assertEqual(r.determinante, -1)

    def test_singular(self):
        r = inversa_gauss_jordan([[1, 2], [2, 4]])
        self.assertFalse(r.invertible)
        self.assertIsNone(r.inversa)
        self.assertEqual(r.determinante, 0)
        self.assertIn("singular", r.mensaje)

    def test_no_cuadrada(self):
        with self.assertRaises(ErrorDimension):
            inversa_gauss_jordan([[1, 2, 3], [4, 5, 6]])

    def test_determinantes(self):
        # S3-24/08 p. 11: |[[2,1],[3,2]]| = 1;  |[[-7,3],[1,2]]| = -14-3 = -17
        self.assertEqual(determinante([[2, 1], [3, 2]]), 1)
        self.assertEqual(determinante([[-7, 3], [1, 2]]), -17)
        self.assertEqual(determinante([[2, -1, 0], [1, 3, 2], [0, -2, 1]]), 15)
        self.assertEqual(determinante([[1, 2], [2, 4]]), 0)
        # determinante del sistema en la resolución de Gauss
        self.assertEqual(resolver_gauss([[2, 1], [3, 2]], [1, 1]).determinante, 1)


class TestAdvertenciasYErrores(unittest.TestCase):

    def test_pivote_pequeno_advierte(self):
        r = resolver_gauss([[F(1, 10**12), 1], [1, 1]], [1, 2])
        self.assertEqual(r.clasificacion, UNICA)
        self.assertTrue(any("problemático" in a for a in r.advertencias))
        # la solución exacta sigue siendo correcta
        self.assertEqual(evaluar([[F(1, 10**12), 1], [1, 1]], r.solucion), [1, 2])

    def test_pasos_registrados(self):
        r = resolver_gauss([[2, 1], [4, 3]], [3, 7])
        self.assertEqual(r.pasos[0].descripcion, "Matriz aumentada inicial [A | b]")
        self.assertIn("F2 → F2 − (2)·F1", [p.descripcion for p in r.pasos])
        self.assertEqual(r.solucion, [1, 1])

    def test_entradas_invalidas(self):
        with self.assertRaises(ErrorDimension):
            resolver_gauss([[1, 2], [3, 4]], [1, 2, 3])
        with self.assertRaises(ErrorMatriz):
            resolver_gauss([[1, "a"], [3, 4]], [1, 2])
        with self.assertRaises(ErrorMatriz):
            resolver_gauss([], [])

    def test_no_modifica_entrada(self):
        A, b = [[0, 1], [1, 1]], [2, 3]
        resolver_gauss_jordan(A, b)
        self.assertEqual((A, b), ([[0, 1], [1, 1]], [2, 3]))


if __name__ == "__main__":
    unittest.main()
