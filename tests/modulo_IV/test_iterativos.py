"""Pruebas de algebra/modulo_IV_iterativos/ — casos de aceptación P1–P21 de la especificación.

Oráculos: los valores esperados se obtuvieron el 27-oct-2026 con un programa
independiente (escrito aparte, no con este módulo) y se contrastaron con:
  * la solución exacta de S, (217/208, 59/26, -225/208), comprobada por sustitución;
  * las iteraciones 1-3 de SOR del manuscrito S8-30/09 pp. 32-33 / S9-05/10 pp. 2-4;
  * la solución estudiantil de la Tarea II #2 (ZIP), que usa la norma infinito.
Los valores impresos en las láminas de S8 para el sistema S son incorrectos y
NO se usan como referencia.
"""

import unittest
from fractions import Fraction as F

from algebra.modulo_IV_iterativos.comparacion import (
    comparar_metodos,
    configuraciones_homogeneas,
)
from algebra.modulo_IV_iterativos.convergencia import dominancia_diagonal
from algebra.modulo_IV_iterativos.ejecucion import (
    CRITERIO_CAMBIO,
    CRITERIO_ITERACIONES,
    CRITERIO_RESIDUO,
    ConfiguracionIterativa,
    DIAGONAL_CERO,
    ENTRADA_INVALIDA,
    ERROR_NO_FINITO,
    K_TOPE,
    MAXIMO_ITERACIONES,
    N_COMPLETADAS,
    TOLERANCIA_CAMBIO,
    TOLERANCIA_RESIDUO,
    ejecutar,
    vector_diagonal,
)
from algebra.modulo_IV_iterativos.metodos import (
    GAUSS_SEIDEL,
    JACOBI,
    SOR,
)

# Sistema S (S8-30/09 pp. 17-18, 23, 29; Tarea II #2 reordenada)
S_A = [[10, -1, 2], [-1, 11, -1], [2, -1, 10]]
S_b = [6, 25, -11]
# M2 (S8-30/09 p. 32)
M2_A = [[10, 2, 1], [2, 10, 2], [1, 2, 10]]
M2_b = [9, 13, 14]
# M3 (S8-30/09 p. 19), solución (2, 3, 4)
M3_A = [[6, 2, 1], [-1, 8, 2], [1, -1, 6]]
M3_b = [22, 30, 23]
# Dv (S9-07/10): ρ(T_J) ≈ 1.174 > 1, ρ(T_GS) ≈ 0.935 < 1
Dv_A = [[3, 3, 3], [3, 3, 2], [-3, -2, 3]]
Dv_b = [9, 9, -2]

TOL = 5e-7   # los valores de referencia están redondeados a 6 decimales


def config(metodo=JACOBI, criterio=CRITERIO_CAMBIO, **kw):
    return ConfiguracionIterativa(metodo=metodo, criterio=criterio, **kw)


class Ayudas(unittest.TestCase):

    def assertVector(self, obtenido, esperado, tol=TOL):
        self.assertEqual(len(obtenido), len(esperado))
        for a, e in zip(obtenido, esperado):
            self.assertAlmostEqual(a, e, delta=tol)

    def assertRelativo(self, obtenido, esperado, cifras=6):
        self.assertAlmostEqual(obtenido / esperado, 1.0, delta=10 ** (-cifras + 1) / 2)


class TestCriterioA(Ayudas):

    def test_P1_jacobi(self):
        r = ejecutar(S_A, S_b, config(JACOBI))
        self.assertEqual((r.codigo, r.k_final, r.criterio_cumplido), (TOLERANCIA_CAMBIO, 7, True))
        self.assertVector(r.x_final, [1.043187, 2.269277, -1.081786])
        self.assertRelativo(r.d_final, 3.78139e-4)
        self.assertRelativo(r.r_final, 9.76218e-4)

    def test_P2_gauss_seidel(self):
        r = ejecutar(S_A, S_b, config(GAUSS_SEIDEL))
        self.assertEqual((r.codigo, r.k_final), (TOLERANCIA_CAMBIO, 4))
        self.assertVector(r.x_final, [1.043297, 2.269235, -1.081736])
        self.assertRelativo(r.d_final, 3.07307e-4)
        self.assertRelativo(r.r_final, 2.62104e-4)

    def test_P3_sor(self):
        r = ejecutar(S_A, S_b, config(SOR, omega=1.2))
        self.assertEqual((r.codigo, r.k_final), (TOLERANCIA_CAMBIO, 6))
        self.assertVector(r.x_final, [1.043010, 2.269367, -1.081809])
        self.assertRelativo(r.d_final, 8.62517e-4)
        self.assertRelativo(r.r_final, 2.88132e-3)

    def test_P5_sor_manuscrito(self):
        r = ejecutar(M2_A, M2_b, config(SOR, omega=1.2))
        # iteraciones 1-3 coinciden con el manuscrito S8-30/09 pp. 32-33
        self.assertVector(r.historial[1].x, [1.08, 1.3008, 1.2382], tol=5e-5)
        self.assertVector(r.historial[2].x, [0.4032, 0.9059, 1.1666], tol=5e-5)
        self.assertVector(r.historial[3].x, [0.6420, 0.9448, 1.1429], tol=5e-5)
        self.assertEqual((r.codigo, r.k_final), (TOLERANCIA_CAMBIO, 7))
        self.assertVector(r.x_final, [0.594685, 0.950986, 1.150353])
        self.assertRelativo(r.d_final, 3.56697e-4)

    def test_P6_norma_infinito_no_suma(self):
        # El manuscrito S8-30/09 p. 20 suma las diferencias (2.4028) y lo rotula ∞.
        # La norma infinito correcta de x(1) - x(0) es 1.8889.
        x0 = vector_diagonal(M3_A, M3_b)
        r = ejecutar(M3_A, M3_b, config(JACOBI, tolerancia=0.01, x0=x0))
        d = [fila.d for fila in r.historial[1:]]
        self.assertAlmostEqual(d[0], 1.8889, delta=5e-5)
        self.assertNotAlmostEqual(d[0], 2.4028, delta=1e-3)
        self.assertVector(d, [1.8889, 0.2396, 0.0673, 0.0237, 0.0062], tol=5e-5)
        self.assertEqual((r.codigo, r.k_final), (TOLERANCIA_CAMBIO, 5))

    def test_P7_tarea2_item2(self):
        r = ejecutar(S_A, S_b, config(GAUSS_SEIDEL))
        self.assertEqual(r.k_final, 4)
        self.assertVector(r.x_final, [1.0433, 2.2692, -1.0817], tol=5e-5)

    def test_P10_criterio_A_no_se_evalua_en_k0(self):
        r = ejecutar(M3_A, M3_b, config(GAUSS_SEIDEL, x0=[2, 3, 4]))
        self.assertEqual((r.codigo, r.k_final, r.d_final), (TOLERANCIA_CAMBIO, 1, 0.0))
        self.assertIsNone(r.historial[0].d)


class TestCriterioB(Ayudas):

    def test_P4_residuo(self):
        esperado = {JACOBI: (7, 9.76218e-4), GAUSS_SEIDEL: (4, 2.62104e-4), SOR: (7, 8.78688e-4)}
        for metodo, (k, residuo) in esperado.items():
            r = ejecutar(S_A, S_b, config(metodo, CRITERIO_RESIDUO, omega=1.2))
            self.assertEqual((r.codigo, r.k_final), (TOLERANCIA_RESIDUO, k), metodo)
            self.assertRelativo(r.r_final, residuo)
        # Con SOR el criterio B necesita una iteración más que el A (7 frente a 6)
        self.assertEqual(ejecutar(S_A, S_b, config(SOR, omega=1.2)).k_final, 6)

    def test_P9_vector_inicial_ya_es_solucion(self):
        r = ejecutar(M3_A, M3_b, config(GAUSS_SEIDEL, CRITERIO_RESIDUO, x0=[2, 3, 4]))
        self.assertEqual((r.codigo, r.k_final, r.r_final), (TOLERANCIA_RESIDUO, 0, 0.0))
        self.assertIn("no se realizaron iteraciones", r.mensaje)

    def test_residuo_con_sistema_original(self):
        # r_k se recalcula aquí, de forma independiente, con A y b originales
        r = ejecutar(S_A, S_b, config(JACOBI, CRITERIO_RESIDUO))
        for fila in r.historial:
            ax = [sum(S_A[i][j] * fila.x[j] for j in range(3)) for i in range(3)]
            self.assertAlmostEqual(fila.r, max(abs(S_b[i] - ax[i]) for i in range(3)), places=12)


class TestCriterioCyLimites(Ayudas):

    def test_P8_iteraciones_fijas(self):
        r = ejecutar(S_A, S_b, config(JACOBI, CRITERIO_ITERACIONES, n_iteraciones=5))
        self.assertEqual((r.codigo, r.k_final, len(r.historial)), (N_COMPLETADAS, 5, 6))
        self.assertRelativo(r.d_final, 5.85917e-3)
        self.assertRelativo(r.r_final, 1.48168e-2)
        self.assertIn("no demuestra convergencia", r.mensaje)

    def test_P11_maximo_sin_afirmar_divergencia(self):
        r = ejecutar(Dv_A, Dv_b, config(JACOBI, k_max=30))
        self.assertEqual((r.codigo, r.k_final, r.criterio_cumplido), (MAXIMO_ITERACIONES, 30, False))
        self.assertVector(r.x_final, [121.842635, 75.937765, 182.564325], tol=5e-6)
        self.assertNotIn("diverg", r.mensaje.lower())

    def test_P12_maximo_en_metodo_convergente(self):
        r = ejecutar(Dv_A, Dv_b, config(GAUSS_SEIDEL, k_max=10))
        self.assertEqual((r.codigo, r.k_final), (MAXIMO_ITERACIONES, 10))
        self.assertAlmostEqual(r.d_final, 0.3526, delta=5e-5)

    def test_P13_valores_no_finitos(self):
        r = ejecutar([[1, 1e200], [1e200, 1]], [1, 1], config(JACOBI))
        self.assertEqual((r.codigo, r.k_error, r.k_final), (ERROR_NO_FINITO, 2, 1))
        self.assertVector(r.x_final, [1.0, 1.0])
        self.assertIn("no constituye", r.mensaje)

    def test_P14_diagonal_cero(self):
        for metodo in (JACOBI, GAUSS_SEIDEL, SOR):
            r = ejecutar([[0, 1], [1, 0]], [1, 1], config(metodo))
            self.assertEqual((r.codigo, r.historial), (DIAGONAL_CERO, []), metodo)

    def test_P15_sor_omega_uno_igual_gauss_seidel(self):
        gs = ejecutar(S_A, S_b, config(GAUSS_SEIDEL))
        sor = ejecutar(S_A, S_b, config(SOR, omega=1))
        self.assertEqual([f.x for f in gs.historial], [f.x for f in sor.historial])

    def test_P16_tolerancia_justo_en_kmax(self):
        r = ejecutar(S_A, S_b, config(JACOBI, k_max=7))
        self.assertEqual((r.codigo, r.k_final, r.criterio_cumplido), (TOLERANCIA_CAMBIO, 7, True))
        r = ejecutar(S_A, S_b, config(JACOBI, k_max=6))
        self.assertEqual((r.codigo, r.k_final), (MAXIMO_ITERACIONES, 6))
        self.assertRelativo(r.d_final, 1.48168e-3)

    def test_P17_desigualdad_estricta(self):
        # 2x = 2, x0 = 0, ε = 1:  d1 = 1 (no < 1) -> sigue; d2 = 0 -> para en k = 2
        r = ejecutar([[2]], [2], config(JACOBI, tolerancia=1))
        self.assertEqual((r.codigo, r.k_final), (TOLERANCIA_CAMBIO, 2))
        # Criterio B: r0 = 2, r1 = 0 < 1 -> para en k = 1
        r = ejecutar([[2]], [2], config(JACOBI, CRITERIO_RESIDUO, tolerancia=1))
        self.assertEqual((r.codigo, r.k_final), (TOLERANCIA_RESIDUO, 1))

    def test_P21_tolerancia_inalcanzable_avisa(self):
        r = ejecutar(S_A, S_b, config(JACOBI, tolerancia=1e-18))
        self.assertTrue(any("inalcanzable" in a for a in r.advertencias))
        # d_k se estanca en el redondeo (~2.2e-16 > 1e-18): se alcanza el máximo.
        self.assertEqual((r.codigo, r.k_final), (MAXIMO_ITERACIONES, 50))
        self.assertGreater(r.d_final, 1e-18)

    def test_no_modifica_configuracion(self):
        c = config(JACOBI)
        ejecutar(S_A, S_b, c)
        self.assertIsNone(c.x0)


class TestEntradasInvalidas(unittest.TestCase):

    def assertInvalida(self, A, b, c):
        r = ejecutar(A, b, c)
        self.assertEqual(r.codigo, ENTRADA_INVALIDA, c)
        self.assertTrue(r.mensaje)

    def test_P20_parametros(self):
        for tol in (0, -1, "abc", "", float("nan"), float("inf"), None, True):
            self.assertInvalida(S_A, S_b, config(tolerancia=tol))
        for kmax in (0, -3, 2.5, K_TOPE + 1, None, True):
            self.assertInvalida(S_A, S_b, config(k_max=kmax))
        self.assertInvalida(S_A, S_b, config(criterio=CRITERIO_ITERACIONES, n_iteraciones=0))
        for omega in (0, 2, 2.5, -1, None):
            self.assertInvalida(S_A, S_b, config(SOR, omega=omega))

    def test_tolerancias_extremas_mensajes(self):
        r = ejecutar(S_A, S_b, config(tolerancia=F(1, 10**400)))
        self.assertEqual(r.codigo, ENTRADA_INVALIDA)
        self.assertIn("vale 0", r.mensaje)
        r = ejecutar(S_A, S_b, config(tolerancia=F(10**400)))
        self.assertEqual(r.codigo, ENTRADA_INVALIDA)
        self.assertIn("demasiado grande", r.mensaje)
        self.assertNotIn("El tolerancia", r.mensaje)

    def test_P20_omega_se_ignora_fuera_de_sor(self):
        r = ejecutar(S_A, S_b, config(JACOBI, omega=7))
        self.assertEqual(r.codigo, TOLERANCIA_CAMBIO)

    def test_P20_dimensiones_y_datos(self):
        self.assertInvalida(S_A, S_b, config(x0=[0, 0]))
        self.assertInvalida([[1, 2, 3], [4, 5, 6]], [1, 2], config())
        self.assertInvalida(S_A, [1, 2], config())
        self.assertInvalida([[1, "x"], [1, 1]], [1, 1], config())
        self.assertInvalida(S_A, S_b, config(metodo="Newton"))
        self.assertInvalida(S_A, S_b, config(criterio="Z"))

    def test_fracciones_aceptadas(self):
        r = ejecutar(S_A, S_b, config(JACOBI, tolerancia=F(1, 1000)))
        self.assertEqual(r.k_final, 7)


class TestComparacion(unittest.TestCase):

    def test_P18_homogenea(self):
        comp = comparar_metodos(S_A, S_b, configuraciones_homogeneas(omega=1.2))
        self.assertTrue(comp.homogeneo)
        self.assertEqual([r.k_final for r in comp.resultados], [7, 4, 6])
        self.assertTrue(all(r.codigo == TOLERANCIA_CAMBIO for r in comp.resultados))
        # referencia = solución exacta del método directo
        for a, e in zip(comp.referencia, (217 / 208, 59 / 26, -225 / 208)):
            self.assertAlmostEqual(a, e, places=12)
        self.assertTrue(all(e < 1e-3 for e in comp.errores_finales))

    def test_P19_no_homogenea(self):
        configs = configuraciones_homogeneas()
        configs[1].k_max = 10
        comp = comparar_metodos(S_A, S_b, configs)
        self.assertFalse(comp.homogeneo)
        self.assertEqual(comp.diferencias, ["k_max"])

    def test_sin_referencia_si_singular(self):
        comp = comparar_metodos([[1, 1], [1, 1]], [2, 2], configuraciones_homogeneas(k_max=5))
        self.assertIsNone(comp.referencia)
        self.assertEqual(comp.errores_finales, [None, None, None])


class TestDominancia(unittest.TestCase):

    def test_dominante(self):
        # S8-30/09 p. 37: |10| > 3, |11| > 2, |10| > 3
        r = dominancia_diagonal(S_A)
        self.assertTrue(r.estricta)
        self.assertEqual([(f[1], f[2]) for f in r.filas], [(10, 3), (11, 2), (10, 3)])

    def test_no_dominante_tarea2_orden_original(self):
        # Tarea II #2 en el orden dado: -x+11y-z ... fila 1 |-1| > 12 falla
        r = dominancia_diagonal([[-1, 11, -1], [10, -1, 2], [2, -1, 10]])
        self.assertFalse(r.estricta)
        self.assertIn("NO implica", r.mensaje)

    def test_no_estricta_igualdad(self):
        self.assertFalse(dominancia_diagonal([[2, 2], [1, 3]]).estricta)


if __name__ == "__main__":
    unittest.main()
