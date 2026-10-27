"""Pruebas de algebra/espectral.py (matrices de iteración y radio espectral).

Oráculos independientes del código probado:
  * coeficientes del polinomio característico calculados a mano con
    traza, suma de menores principales y determinante (regla de Sarrus);
  * fórmulas cerradas (cuadrática) para los radios de Gauss-Seidel;
  * bisección escrita en esta prueba y relaciones de Vieta para cúbicas;
  * resultados teóricos para la matriz tridiagonal [-1, 4, -1]
    (autovalores de Jacobi (1/2)cos(kπ/5); ρ_GS = ρ_J²; ρ_SOR = ω - 1 si ω ≥ ω_opt).
"""

import math
import unittest
from fractions import Fraction as F

from algebra.espectral import (
    CONVERGE,
    INDETERMINADO,
    NO_CONVERGE,
    descomponer,
    durand_kerner,
    matriz_iteracion,
    polinomio_caracteristico,
    radio_espectral,
    texto_polinomio_curso,
)
from algebra.iterativos import GAUSS_SEIDEL, JACOBI, SOR, ConfiguracionIterativa, ejecutar
from algebra.validacion import ErrorEntrada


def biseccion(f, a, b, iteraciones=200):
    """Raíz de f en [a, b] (f(a) y f(b) de signos distintos)."""
    fa = f(a)
    for _ in range(iteraciones):
        m = (a + b) / 2
        if (f(m) > 0) == (fa > 0):
            a, fa = m, f(m)
        else:
            b = m
    return (a + b) / 2


TAREA_4 = [[4, -1, 1], [-2, 6, 1], [1, 1, 5]]     # Tarea II #4 y #5
Dv = [[3, 3, 3], [3, 3, 2], [-3, -2, 3]]           # S9-07/10
LAMINA_38 = [[4, 1, 1], [1, 3, 1], [2, 1, 5]]      # S8-30/09 p. 38
TRIDIAG = [[4, -1, 0, 0], [-1, 4, -1, 0], [0, -1, 4, -1], [0, 0, -1, 4]]


class TestMatricesIteracion(unittest.TestCase):

    def test_descomposicion(self):
        D, L, U = descomponer([[3, 3, 3], [3, 3, 2], [-3, -2, 3]])
        self.assertEqual(D, [[3, 0, 0], [0, 3, 0], [0, 0, 3]])
        self.assertEqual(L, [[0, 0, 0], [3, 0, 0], [-3, -2, 0]])
        self.assertEqual(U, [[0, 3, 3], [0, 0, 2], [0, 0, 0]])

    def test_jacobi_manuscrito(self):
        # S9-07/10 p. 3: T_J = [[0,-1,-1],[-1,0,-2/3],[1,2/3,0]], c_J = (3, 3, -2/3)
        it = matriz_iteracion(Dv, [9, 9, -2], JACOBI)
        self.assertEqual(it.T, [[0, -1, -1], [-1, 0, F(-2, 3)], [1, F(2, 3), 0]])
        self.assertEqual(it.c, [3, 3, F(-2, 3)])

    def test_gauss_seidel_manuscrito(self):
        # S9-07/10 p. 6: T_GS = [[0,-1,-1],[0,1,1/3],[0,-1/3,-7/9]] (correcto en la hoja);
        # c_GS = (D+L)^-1 b = (3, 0, 7/3)  (la hoja da (-7, 25/3, -13/9): error)
        it = matriz_iteracion(Dv, [9, 9, -2], GAUSS_SEIDEL)
        self.assertEqual(it.T, [[0, -1, -1], [0, 1, F(1, 3)], [0, F(-1, 3), F(-7, 9)]])
        self.assertEqual(it.c, [3, 0, F(7, 3)])

    def test_iteracion_coincide_con_paso_del_metodo(self):
        # x(1) = T x(0) + c debe coincidir con una iteración de los métodos (x0 = 0 -> c)
        for metodo, omega in ((JACOBI, None), (GAUSS_SEIDEL, None), (SOR, F(6, 5))):
            it = matriz_iteracion(TAREA_4, [7, 9, -6], metodo, omega)
            r = ejecutar(TAREA_4, [7, 9, -6], ConfiguracionIterativa(
                metodo=metodo, criterio="C", n_iteraciones=1, omega=1.2))
            for a, e in zip(r.historial[1].x, it.c):
                self.assertAlmostEqual(a, float(e), places=12)

    def test_sor_omega_uno_es_gauss_seidel(self):
        self.assertEqual(matriz_iteracion(TAREA_4, [7, 9, -6], SOR, 1).T,
                         matriz_iteracion(TAREA_4, [7, 9, -6], GAUSS_SEIDEL).T)

    def test_diagonal_cero(self):
        with self.assertRaises(ErrorEntrada):
            matriz_iteracion([[0, 1], [1, 0]], [1, 1], JACOBI)


class TestPolinomio(unittest.TestCase):

    def test_faddeev_coincide_con_sarrus_3x3(self):
        # Tarea II #4: T_J = [[0,1/4,-1/4],[1/3,0,-1/6],[-1/5,-1/5,0]]
        # tr = 0; menores principales: -1/12 - 1/20 - 1/30 = -1/6; det = 1/40
        # p(λ) = λ³ - tr λ² + (Σ menores) λ - det = λ³ - (1/6) λ - 1/40
        T = matriz_iteracion(TAREA_4, [7, 9, -6], JACOBI).T
        self.assertEqual(T, [[0, F(1, 4), F(-1, 4)], [F(1, 3), 0, F(-1, 6)], [F(-1, 5), F(-1, 5), 0]])
        self.assertEqual(polinomio_caracteristico(T), [1, 0, F(-1, 6), F(-1, 40)])

    def test_texto_como_en_clase(self):
        # S9-07/10: det(T - λI) correcto = -λ³ - (4/9)λ + 4/3  (la hoja omite el 4/3)
        T = matriz_iteracion(Dv, [9, 9, -2], JACOBI).T
        coef = polinomio_caracteristico(T)
        self.assertEqual(coef, [1, 0, F(4, 9), F(-4, 3)])
        self.assertEqual(texto_polinomio_curso(coef), "det(T − λI) = −λ³ − 4/9λ + 4/3")

    def test_triangular(self):
        # Autovalores de una triangular = diagonal: (λ-2)(λ-3) = λ² - 5λ + 6
        self.assertEqual(polinomio_caracteristico([[2, 7], [0, 3]]), [1, -5, 6])


class TestRadioEspectral(unittest.TestCase):

    def test_tarea2_jacobi(self):
        # ρ = raíz positiva de λ³ - λ/6 - 1/40 (las otras dos son reales negativas menores)
        esperado = biseccion(lambda t: t ** 3 - t / 6 - 1 / 40, 0.4, 0.5)
        r = radio_espectral(TAREA_4, [7, 9, -6], JACOBI)
        self.assertAlmostEqual(r.rho, esperado, places=10)
        self.assertAlmostEqual(r.rho, 0.4690, places=4)
        self.assertEqual(r.conclusion, CONVERGE)
        self.assertTrue(r.fiable)

    def test_tarea2_gauss_seidel_forma_cerrada(self):
        # T_GS tiene λ = 0 y las raíces de λ² - (11/60)λ - 1/120 -> ρ = (11 + √241)/120
        r = radio_espectral(TAREA_4, [7, 9, -6], GAUSS_SEIDEL)
        self.assertEqual(r.multiplicidad_cero, 1)
        self.assertAlmostEqual(r.rho, (11 + math.sqrt(241)) / 120, places=12)
        self.assertTrue(r.decision_exacta)
        self.assertEqual(r.conclusion, CONVERGE)

    def test_jacobi_no_converge_raices_complejas(self):
        # S9-07/10: la hoja concluye ρ = 0 (error).  p(λ) = λ³ + (4/9)λ - 4/3:
        # raíz real por bisección; por Vieta, |λ_complejas|² = (4/3)/λ_real.
        real = biseccion(lambda t: t ** 3 + 4 * t / 9 - 4 / 3, 0.5, 1.5)
        modulo = math.sqrt((4 / 3) / real)
        r = radio_espectral(Dv, [9, 9, -2], JACOBI)
        self.assertAlmostEqual(r.rho, modulo, places=10)
        self.assertAlmostEqual(r.rho, 1.1744, places=4)
        self.assertEqual(r.conclusion, NO_CONVERGE)
        complejas = [z for z in r.autovalores if z.imag != 0]
        self.assertEqual(len(complejas), 2)

    def test_gauss_seidel_lento_forma_cerrada(self):
        # Bloque [[1,1/3],[-1/3,-7/9]]: λ² - (2/9)λ - 2/3 -> ρ = (2 + √220)/18 ≈ 0.9351
        r = radio_espectral(Dv, [9, 9, -2], GAUSS_SEIDEL)
        self.assertAlmostEqual(r.rho, (2 + math.sqrt(220)) / 18, places=12)
        self.assertEqual(r.conclusion, CONVERGE)

    def test_lamina_38_corregida(self):
        # S8-30/09 p. 38: la lámina da 0.52, -0.31, 0.16.  p(λ) = λ³ - λ/4 + 1/20:
        # raíz real negativa por bisección; complejas con |λ|² = (1/20)/|λ_real| (menor)
        real = biseccion(lambda t: t ** 3 - t / 4 + 1 / 20, -1.0, -0.4)
        r = radio_espectral(LAMINA_38, [6, 5, 7], JACOBI)
        self.assertEqual(r.coeficientes, [1, 0, F(-1, 4), F(1, 20)])
        self.assertAlmostEqual(r.rho, abs(real), places=10)
        self.assertAlmostEqual(r.rho, 0.57985, places=5)
        self.assertEqual(sum(1 for z in r.autovalores if z.imag != 0), 2)

    def test_tridiagonal_resultados_teoricos(self):
        b = [1, 0, 0, 1]
        rho_j = math.cos(math.pi / 5) / 2
        self.assertAlmostEqual(radio_espectral(TRIDIAG, b, JACOBI).rho, rho_j, places=10)
        self.assertAlmostEqual(radio_espectral(TRIDIAG, b, GAUSS_SEIDEL).rho, rho_j ** 2, places=10)
        # ω = 1.25 >= ω_opt ≈ 1.0446  ->  todos los autovalores tienen |λ| = ω - 1 = 0.25
        r = radio_espectral(TRIDIAG, b, SOR, F(5, 4))
        self.assertAlmostEqual(r.rho, 0.25, places=6)

    def test_matriz_diagonal_rho_cero(self):
        r = radio_espectral([[2, 0], [0, 5]], [1, 1], JACOBI)
        self.assertEqual((r.rho, r.multiplicidad_cero, r.conclusion), (0.0, 2, CONVERGE))

    def test_rho_igual_a_uno_decision_exacta(self):
        # A = [[1,1],[-1,1]]: T_J = [[0,-1],[1,0]], autovalores ±i, ρ = 1 -> no converge
        r = radio_espectral([[1, 1], [-1, 1]], [1, 1], JACOBI)
        self.assertAlmostEqual(r.rho, 1.0, places=14)
        self.assertTrue(r.decision_exacta)
        self.assertEqual(r.conclusion, NO_CONVERGE)

    def test_consistencia_con_iteraciones(self):
        # ρ < 1 y converge; ρ > 1 y las iteraciones no se estabilizan (P11)
        self.assertEqual(radio_espectral([[10, -1, 2], [-1, 11, -1], [2, -1, 10]],
                                         [6, 25, -11], JACOBI).conclusion, CONVERGE)


class TestRegresionAuditoria(unittest.TestCase):
    """Defectos encontrados en la auditoría final (27-oct-2026)."""

    def test_raices_simples_no_deben_marcarse_no_fiables(self):
        # SOR ω = 1/2 sobre esta matriz: autovalores simples y separados
        # (par complejo dominante de módulo ≈ 0.5951).  Antes, la tolerancia de
        # parada de Durand-Kerner (1e-15) era inalcanzable por redondeo y el
        # resultado salía «no fiable» / INDETERMINADO.
        A = [[-4, -1, 3, -1], [2, 5, 1, 0], [1, -3, 5, 0], [2, 2, 2, 5]]
        r = radio_espectral(A, [1, 1, 1, 1], SOR, F(1, 2))
        self.assertTrue(r.fiable, r.advertencias)
        self.assertEqual(r.conclusion, CONVERGE)
        self.assertAlmostEqual(r.rho, 0.5950974, places=6)
        # Comprobación independiente: las iteraciones de SOR efectivamente convergen
        corrida = ejecutar(A, [1, 1, 1, 1], ConfiguracionIterativa(
            metodo=SOR, omega=0.5, tolerancia=1e-10, k_max=500))
        self.assertEqual(corrida.codigo, "TOLERANCIA_CAMBIO")

    def test_autovalor_uno_exacto_decide_no_convergencia(self):
        # A singular  <=>  T = I - M^-1 A tiene el autovalor λ = 1, luego ρ(T) >= 1.
        # A = [[2,1,1],[1,2,1],[3,3,2]] es singular (fila 3 = fila 1 + fila 2).
        # Con SOR (ω = 1/2) el polinomio reducido es de grado 3 y λ = 1 es raíz exacta.
        A = [[2, 1, 1], [1, 2, 1], [3, 3, 2]]
        r = radio_espectral(A, [1, 1, 1], SOR, F(1, 2))
        self.assertEqual(len(r.coeficientes) - 1 - r.multiplicidad_cero, 3)
        self.assertTrue(r.decision_exacta)
        self.assertEqual(r.conclusion, NO_CONVERGE)

    def test_raiz_multiple_se_declara_indeterminada_no_garantizada(self):
        # T triangular con el autovalor 1/2 triple (bloque de Jordan): ρ = 1/2 < 1,
        # pero Durand-Kerner pierde precisión con raíces múltiples: la aplicación
        # no debe presentar como fiable un ρ impreciso.
        from algebra.espectral import raices
        av, ceros, fiable, avisos, decision = raices(polinomio_caracteristico(
            [[F(1, 2), 1, 0], [0, F(1, 2), 1], [0, 0, F(1, 2)]]))
        self.assertFalse(fiable)
        self.assertTrue(any("múltiple" in a for a in avisos))
        for z in av:
            self.assertAlmostEqual(abs(z), 0.5, places=3)


class TestConclusion(unittest.TestCase):

    def test_bandas(self):
        from algebra.espectral import concluir
        self.assertEqual(concluir(0.5, True), CONVERGE)
        self.assertEqual(concluir(1.5, True), NO_CONVERGE)
        self.assertEqual(concluir(1 - 1e-10, True), INDETERMINADO)
        self.assertEqual(concluir(1 - 1e-7, True), CONVERGE)
        # con raíces casi repetidas la banda es 1e-6
        self.assertEqual(concluir(1 - 1e-7, True, casi_repetidas=True), INDETERMINADO)
        self.assertEqual(concluir(0.5, False), INDETERMINADO)
        # la decisión exacta prevalece
        self.assertEqual(concluir(1.0, True, decision_exacta=False), NO_CONVERGE)
        self.assertEqual(concluir(0.99999999999, False, decision_exacta=True), CONVERGE)

    def test_raiz_doble_cerca_de_uno_no_da_conclusion_falsa(self):
        # (λ - a)²(λ - 1/10) con a = 1 ± 1e-7: el ρ verdadero está a 1e-7 de 1.
        from algebra.espectral import AVISO_CASI_REPETIDOS, concluir, raices
        for a, verdadero in ((1 - F(1, 10**7), CONVERGE), (1 + F(1, 10**7), NO_CONVERGE)):
            coef = [F(1), -(2 * a + F(1, 10)), a * a + 2 * a / 10, -a * a / 10]
            av, _, fiable, avisos, decision = raices(coef)
            c = concluir(max(abs(z) for z in av), fiable, decision, AVISO_CASI_REPETIDOS in avisos)
            self.assertIn(c, (verdadero, INDETERMINADO))


class TestDurandKerner(unittest.TestCase):

    def test_raices_conocidas(self):
        # (λ-1)(λ-2)(λ-3) = λ³ - 6λ² + 11λ - 6
        z, ok = durand_kerner([1, -6, 11, -6])
        self.assertTrue(ok)
        self.assertEqual(sorted(round(v.real, 10) for v in z), [1, 2, 3])
        # λ⁴ + 1: raíces e^{iπ/4 + k iπ/2}, todas de módulo 1
        z, ok = durand_kerner([1, 0, 0, 0, 1])
        self.assertTrue(ok)
        for v in z:
            self.assertAlmostEqual(abs(v), 1.0, places=12)


if __name__ == "__main__":
    unittest.main()
