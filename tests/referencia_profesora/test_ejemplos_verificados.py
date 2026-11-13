"""Pruebas de referencia con ejemplos resueltos de la profesora.

Cada prueba indica el PDF y la página donde está el ejemplo, y solo incluye valores que se
han leído en la imagen de esa página (revisión visual, no OCR).  Los valores que la lámina
no muestra o que no se pudieron leer no se usan como referencia.

Cuando la lámina contiene una errata, la prueba fija el valor correcto y lo indica.
Los ejercicios sintéticos de otros archivos de tests/ no pertenecen a este grupo.

Índice: docs/auditoria/pruebas_ejemplos_profesora.md
"""

import unittest
from fractions import Fraction as F

from algebra.compartido.matriz import sumas_absolutas_por_fila
from algebra.modulo_I_sistemas.directos import resolver_gauss, solucion_unica
from algebra.modulo_II_condicionamiento.condicion import numero_condicion_infinito
from algebra.modulo_IV_iterativos.espectral import radio_espectral
from algebra.modulo_IV_iterativos.ejecucion import CRITERIO_ITERACIONES, ConfiguracionIterativa, ejecutar
from algebra.modulo_IV_iterativos.matriz_iteracion import matriz_iteracion
from algebra.modulo_IV_iterativos.metodos import GAUSS_SEIDEL, JACOBI
from algebra.modulo_IV_iterativos.polinomio_raices import polinomio_caracteristico


def fr(valores):
    return [F(v) for v in valores]


def cerca(valores, esperados, tol=1e-12):
    """Compara iteraciones (punto flotante) con valores exactos de la lámina."""
    return all(abs(float(v) - float(e)) < tol for v, e in zip(valores, esperados))


def fm(matriz):
    return [[F(v) for v in fila] for fila in matriz]


class TestS616Gauss(unittest.TestCase):
    """S6-16/09 p. 29 (imagen revisada): sistema x+y+z=6, 2x+y−z=3, −x+y+2z=7."""

    A = [[1, 1, 1], [2, 1, -1], [-1, 1, 2]]
    b = [6, 3, 7]

    def test_operaciones_de_fila_del_ejemplo(self):
        # Lámina: −2F₁+F₂ ; F₁+F₃ ; −F₂ ; −2F₂+F₃ ; (−1/3)F₃.
        # Ax omite el paso −F₂ (normalizar el pivote): simplificación equivalente, documentada.
        r = resolver_gauss(self.A, self.b)
        notas = [p.notacion for p in r.pasos[1:]]
        self.assertEqual(notas, ["−2F₁ + F₂", "F₁ + F₃", "2F₂ + F₃"])

    def test_matrices_intermedias(self):
        # Lámina: [[1,1,1|6],[0,−1,−3|−9],[0,2,3|13]] tras −2F₁+F₂ y F₁+F₃.
        r = resolver_gauss(self.A, self.b)
        self.assertEqual(r.pasos[2].matriz[1], [0, -1, -3, -9])
        self.assertEqual(r.pasos[2].matriz[2], [0, 2, 3, 13])

    def test_fila_final_z_igual_a_menos_cinco_tercios_y_solucion(self):
        r = resolver_gauss(self.A, self.b)
        self.assertEqual(r.pasos[-1].matriz[2], [0, 0, -3, -5])      # −3z = −5 (lámina: escalonada tras −2F₂+F₃)
        self.assertEqual(r.solucion, fr([F(1, 3), 4, F(5, 3)]))      # Sol = {(1/3, 4, 5/3)}


class TestS616SustitucionHaciaAtras(unittest.TestCase):
    """S6-16/09 p. 29 (imagen revisada): x1 − x2 + x3 = 4 ; x2 + x3 = 3 ; x3 = 1 ⇒ Sol = {(5, 2, 1)}."""

    def test_sustitucion_hacia_atras(self):
        A = [[1, -1, 1], [0, 1, 1], [0, 0, 1]]
        self.assertEqual(solucion_unica(A, [4, 3, 1]), fr([5, 2, 1]))


class TestS721Condicionamiento(unittest.TestCase):
    """S7-21/09 p. 19 (imagen revisada): B = [[1,2],[3,1]], norma ∞, κ∞ = 16/5."""

    def test_pasos_de_la_norma_y_del_numero_de_condicion(self):
        B = fm([[1, 2], [3, 1]])
        c = numero_condicion_infinito(B)
        self.assertEqual(sumas_absolutas_por_fila(B), [3, 4])                  # Fila 1: 3 · Fila 2: 4
        self.assertEqual(c.norma_A, 4)                                         # ‖B‖∞ = 4
        self.assertEqual(c.inversa, fm([[F(-1, 5), F(2, 5)], [F(3, 5), F(-1, 5)]]))
        self.assertEqual(sumas_absolutas_por_fila(c.inversa), [F(3, 5), F(4, 5)])   # Fila 1: 3/5 · Fila 2: 4/5
        self.assertEqual(c.norma_inversa, F(4, 5))                             # ‖B⁻¹‖∞ = 4/5
        self.assertEqual(c.kappa, F(16, 5))                                    # κ∞ = 4 · 4/5 = 16/5


class TestS907Jacobi(unittest.TestCase):
    """S9-07/10 pp. 3-5 (imágenes revisadas): A = [[3,3,3],[3,3,2],[−3,−2,3]], b = (9, 9, −2)."""

    A = fm([[3, 3, 3], [3, 3, 2], [-3, -2, 3]])
    b = fr([9, 9, -2])

    def test_matriz_de_iteracion_y_constante_de_jacobi(self):
        m = matriz_iteracion(self.A, self.b, JACOBI)
        self.assertEqual(m.T, fm([[0, -1, -1], [-1, 0, F(-2, 3)], [1, F(2, 3), 0]]))
        self.assertEqual(m.c, fr([3, 3, F(-2, 3)]))                             # c_J = D⁻¹b

    def test_primeras_iteraciones_desde_cero(self):
        # x(1) = (3, 3, −2/3) se lee en p. 4; x(2) = (2/3, 4/9, …) en p. 5.
        r = ejecutar(self.A, self.b, ConfiguracionIterativa(metodo=JACOBI, criterio=CRITERIO_ITERACIONES,
                                                          x0=[0, 0, 0], n_iteraciones=2))
        self.assertTrue(cerca(r.historial[1].x, fr([3, 3, F(-2, 3)])))
        self.assertTrue(cerca(r.historial[2].x[:2], fr([F(2, 3), F(4, 9)])))

    def test_polinomio_caracteristico_con_el_termino_4_3(self):
        # Errata: la lámina (p. 5) escribe −λ³ − (4/9)λ = 0 y deduce ρ = 0. El término +4/3 es necesario.
        T = fm([[0, -1, -1], [-1, 0, F(-2, 3)], [1, F(2, 3), 0]])
        self.assertEqual(polinomio_caracteristico(T), fr([1, 0, F(4, 9), F(-4, 3)]))

    def test_radio_espectral_de_jacobi_no_converge(self):
        r = radio_espectral(self.A, [9, 9, -2], JACOBI)
        self.assertAlmostEqual(r.rho, 1.1743642528889138, places=9)   # no 0 como en la lámina
        self.assertGreaterEqual(r.rho, 1)


class TestS907GaussSeidel(unittest.TestCase):
    """S9-07/10 pp. 6-7 (imágenes revisadas): mismo sistema."""

    A = fm([[3, 3, 3], [3, 3, 2], [-3, -2, 3]])
    b = fr([9, 9, -2])

    def test_matriz_de_gauss_seidel(self):
        m = matriz_iteracion(self.A, self.b, GAUSS_SEIDEL)
        self.assertEqual(m.T, fm([[0, -1, -1], [0, 1, F(1, 3)], [0, F(-1, 3), F(-7, 9)]]))   # T_GS = −(D+L)⁻¹U

    def test_constante_de_gauss_seidel_corrige_la_errata(self):
        # Errata (p. 7): la lámina escribe C_GS = −(D+L)⁻¹b pero calcula T_GS·b = (−7, 25/3, −13/9).
        # El valor correcto es (D+L)⁻¹b, sin signo negativo.
        m = matriz_iteracion(self.A, self.b, GAUSS_SEIDEL)
        self.assertEqual(m.c, fr([3, 0, F(7, 3)]))

    def test_primera_iteracion_de_gauss_seidel(self):
        r = ejecutar(self.A, self.b, ConfiguracionIterativa(metodo=GAUSS_SEIDEL, criterio=CRITERIO_ITERACIONES,
                                                          x0=[0, 0, 0], n_iteraciones=1))
        self.assertTrue(cerca(r.historial[1].x, fr([3, 0, F(7, 3)])))

    def test_radio_espectral_de_gauss_seidel(self):
        r = radio_espectral(self.A, self.b, GAUSS_SEIDEL)
        self.assertAlmostEqual(r.rho, 0.9351, places=4)              # lámina p. 7: λ₁ = 0,9351
        self.assertLess(r.rho, 1)


if __name__ == "__main__":
    unittest.main()
