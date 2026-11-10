"""Pruebas de algebra/modulo_II_condicionamiento/condicion.py (Módulo II).

Los valores de κ∞ se derivaron a mano con la fórmula de la inversa 2x2
(A⁻¹ = (1/det)[[d,-b],[-c,a]]) o con la estructura A = I + 10J (ver comentarios).
"""

import unittest
from fractions import Fraction as F

from algebra.compartido.matriz import ErrorDimension
from algebra.modulo_II_condicionamiento.condicion import (
    MATRIZ_SINGULAR,
    PERTURBACION_ABSOLUTA,
    PERTURBACION_PORCENTAJE,
    SENSIBILIDAD_ALTA,
    SENSIBILIDAD_BAJA,
    SENSIBILIDAD_MODERADA,
    analizar_perturbacion,
    clasificar_kappa,
    construir_delta_b,
    numero_condicion_infinito,
)
from algebra.modulo_I_sistemas.directos import ErrorSistema


class TestNumeroCondicion(unittest.TestCase):

    def test_bien_condicionada(self):
        # [[2,1],[1,2]]: ||A|| = 3; A^-1 = (1/3)[[2,-1],[-1,2]] -> ||A^-1|| = 1 -> κ = 3
        r = numero_condicion_infinito([[2, 1], [1, 2]])
        self.assertEqual((r.norma_A, r.norma_inversa, r.kappa), (3, 1, 3))
        self.assertEqual(r.clasificacion, SENSIBILIDAD_BAJA)

    def test_ejemplo_lamina_norma_inf(self):
        # S7-21/09 p. 19: B = [[1,2],[3,1]], det = -5, ||B|| = 4,
        # B^-1 = (-1/5)[[1,-2],[-3,1]] -> filas 3/5 y 4/5 -> ||B^-1|| = 4/5 -> κ = 16/5
        r = numero_condicion_infinito([[1, 2], [3, 1]])
        self.assertEqual(r.kappa, F(16, 5))

    def test_mal_condicionada(self):
        # S7-21/09 p. 15: [[1,1],[1,1.0001]]; det = 0.0001
        # ||A|| = 2.0001; A^-1 = 10000·[[1.0001,-1],[-1,1]] -> ||A^-1|| = 20001
        # κ = 2.0001 · 20001 = 40004.0001
        r = numero_condicion_infinito([[1, 1], [1, F("1.0001")]])
        self.assertEqual(r.kappa, F("40004.0001"))
        self.assertEqual(r.clasificacion, SENSIBILIDAD_ALTA)

    def test_moderada_estructura_I_mas_10J(self):
        # A = [[11,10,10],[10,11,10],[10,10,11]] = I + 10 J (J = matriz de unos 3x3).
        # (I + 10J)^-1 = I - (10/31) J  -> diagonal 21/31, fuera -10/31
        # ||A|| = 31; ||A^-1|| = 21/31 + 20/31 = 41/31 -> κ∞ = 41 (κ2 = 31 en S8-28/09 p. 13)
        r = numero_condicion_infinito([[11, 10, 10], [10, 11, 10], [10, 10, 11]])
        self.assertEqual(r.inversa[0], [F(21, 31), F(-10, 31), F(-10, 31)])
        self.assertEqual(r.kappa, 41)
        self.assertEqual(r.clasificacion, SENSIBILIDAD_MODERADA)

    def test_singular_distinta_de_mal_condicionada(self):
        r = numero_condicion_infinito([[1, 2], [2, 4]])
        self.assertEqual(r.clasificacion, MATRIZ_SINGULAR)
        self.assertIsNone(r.kappa)
        self.assertIn("singular", r.interpretacion)

    def test_umbrales(self):
        self.assertEqual(clasificar_kappa(F(99999, 10000)), SENSIBILIDAD_BAJA)
        self.assertEqual(clasificar_kappa(10), SENSIBILIDAD_MODERADA)
        self.assertEqual(clasificar_kappa(F(9999, 100)), SENSIBILIDAD_MODERADA)
        self.assertEqual(clasificar_kappa(100), SENSIBILIDAD_ALTA)

    def test_identidad_kappa_uno(self):
        self.assertEqual(numero_condicion_infinito([[1, 0], [0, 1]]).kappa, 1)


class TestPerturbacion(unittest.TestCase):

    def test_ejemplo_lamina_corregido(self):
        # S7-21/09 p. 20: A = [[4,1],[1,3]], b = (1,2) -> x = (1/11, 7/11)
        # Δb = (0.01, -0.01); A^-1 = (1/11)[[3,-1],[-1,4]]
        # Δx = (1/11)(0.03+0.01, -0.01-0.04) = (1/275, -1/220)
        # x̃ = (26/275, 139/220) ≈ (0.0945, 0.6318)  (la lámina dice 0.6309: error)
        r = analizar_perturbacion([[4, 1], [1, 3]], [1, 2], [F("0.01"), F("-0.01")])
        self.assertEqual(r.x, [F(1, 11), F(7, 11)])
        self.assertEqual(r.x_perturbada, [F(26, 275), F(139, 220)])
        self.assertEqual(r.error_relativo_b, F(1, 200))        # 0.01 / 2
        self.assertEqual(r.error_relativo_x, F(1, 140))        # (1/220)/(7/11)
        self.assertEqual(r.condicion.kappa, F(25, 11))
        self.assertEqual(r.cota, F(25, 11) * F(1, 200))
        self.assertTrue(r.cumple_cota)

    def test_porcentaje_escala_la_solucion(self):
        # Si b se multiplica por 1.1 (p = 10 %), x también: x̃ = 1.1 x.
        A = [[11, 10, 10], [10, 11, 10], [10, 10, 11]]
        b = [31, 31, 31]   # x = (1, 1, 1)
        db = construir_delta_b(b, PERTURBACION_PORCENTAJE, 10)
        self.assertEqual(db, [F(31, 10)] * 3)
        r = analizar_perturbacion(A, b, db)
        self.assertEqual(r.x_perturbada, [F(11, 10)] * 3)
        self.assertEqual(r.error_relativo_x, F(1, 10))
        self.assertEqual(r.amplificacion, 1)

    def test_amplificacion_direccion_desfavorable(self):
        # Mismo A, b = (31,31,31), Δb = (1,-1,1): x̃ = (52/31, -10/31, 52/31)
        # (comprobado por sustitución: 11·52/31 - 100/31 + 520/31 = 32, etc.)
        r = analizar_perturbacion([[11, 10, 10], [10, 11, 10], [10, 10, 11]],
                                  [31, 31, 31], [1, -1, 1])
        self.assertEqual(r.x_perturbada, [F(52, 31), F(-10, 31), F(52, 31)])
        # ||Δx|| = 41/31, ||x|| = 1, ||Δb||/||b|| = 1/31 -> amplificación 41 = κ∞ (caso peor)
        self.assertEqual(r.amplificacion, 41)
        self.assertTrue(r.cumple_cota)

    def test_construir_absoluta(self):
        self.assertEqual(construir_delta_b([1, 2], PERTURBACION_ABSOLUTA, F(1, 10)),
                         [F(1, 10), F(1, 10)])
        self.assertEqual(construir_delta_b([1, 2], PERTURBACION_ABSOLUTA, [1, -1]), [1, -1])
        with self.assertRaises(ErrorDimension):
            construir_delta_b([1, 2], PERTURBACION_ABSOLUTA, [1, 2, 3])

    def test_denominador_cero(self):
        # b = 0 -> x = 0: ningún error relativo está definido
        r = analizar_perturbacion([[1, 0], [0, 1]], [0, 0], [1, 0])
        self.assertIsNone(r.error_relativo_b)
        self.assertIsNone(r.error_relativo_x)
        self.assertEqual(len(r.avisos), 2)

    def test_singular_no_se_puede_perturbar(self):
        with self.assertRaises(ErrorSistema):
            analizar_perturbacion([[1, 2], [2, 4]], [1, 2], [0, 1])


if __name__ == "__main__":
    unittest.main()
