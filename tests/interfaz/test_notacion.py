"""Notación matemática en pantalla (visualizacion/notacion.py).

Comprueba que los textos del núcleo se muestran sin sintaxis de programación
(«a_11», «d_7», «F2», códigos como TOLERANCIA_CAMBIO) y que la conversión nunca
altera un número.
"""

import re
import unittest

from interfaz.compartido.estilo import _e
from visualizacion import interactivas, notacion
from visualizacion.notacion import ecuacion, md, unicode


class TestConversion(unittest.TestCase):

    def test_subindices_del_nucleo(self):
        self.assertEqual(md("a_11 = 0 en la fila 1"), "$a_{11}$ = 0 en la fila 1")
        self.assertEqual(unicode("a_11 = 0"), "a₁₁ = 0")
        self.assertEqual(md("no se puede usar x_i(0) = b_i / a_ii."),
                         "no se puede usar $x_i^{(0)}$ = $b_i$ / $a_{ii}$.")
        self.assertEqual(md("Criterio satisfecho: d_7 = 0.000378 < ε"),
                         "Criterio satisfecho: $d_{7}$ = 0.000378 < ε")
        self.assertEqual(md("μ = 1 − λ(T_J)"), "μ = 1 − λ($T_J$)")

    def test_filas_e_incognitas(self):
        self.assertEqual(md("F2 → F2 − (2)·F1"), "F₂ → F₂ − (2)·F₁")
        self.assertEqual(md("x3 = (5 − (0)) / 2 = 5/2"), "x₃ = (5 − (0)) / 2 = 5/2")
        self.assertEqual(md("det(M_1)"), "det(M₁)")

    def test_no_toca_numeros_ni_palabras(self):
        for texto in ("1e-3", "2x2", "ε = 0.001", "matriz A", "Paso 10", "A·A⁻¹ = I", "x⁽ᵏ⁾"):
            self.assertEqual(md(texto), texto)
        mensaje = "ρ(T) = 1.17436 ≥ 1: el método Jacobi no converge"
        self.assertEqual(re.findall(r"\d+(?:\.\d+)?", md(mensaje)), re.findall(r"\d+(?:\.\d+)?", mensaje))

    def test_codigos_internos_en_palabras(self):
        self.assertEqual(md("12 iteraciones (TOLERANCIA_CAMBIO)"), "12 iteraciones (criterio A cumplido)")
        for codigo, texto in notacion.MOTIVOS.items():
            self.assertEqual(notacion.motivo(codigo), texto)
            self.assertNotIn("_", texto)

    def test_ecuacion_con_signos_correctos(self):
        self.assertEqual(ecuacion([1, -2, 0.5], "xyz", -3), "x − 2y + 0.5z = −3")
        self.assertEqual(ecuacion([-1, 1], "xy", 0), "−x + y = 0")
        self.assertEqual(ecuacion([0, 3], "xy", 6), "3y = 6")


class TestFormas(unittest.TestCase):

    def test_tres_formas_sin_guion_bajo_visible(self):
        for simbolo in (notacion.D_K, notacion.R_K, notacion.E_K, notacion.K_MAX, notacion.X_K):
            self.assertNotIn("_", simbolo.texto)
            self.assertNotIn("_", re.sub(r"<[^>]+>", "", simbolo.html))
            self.assertTrue(simbolo.md().startswith("$") and simbolo.md().endswith("$"))

    def test_estado_final_html_y_texto(self):
        self.assertEqual(interactivas.estado_final("MAXIMO_ITERACIONES", 50),
                         "Se alcanzó k<sub>máx</sub> = 50 sin cumplir el criterio")
        self.assertEqual(interactivas.estado_final("TOLERANCIA_CAMBIO", 7, forma="texto"),
                         "Criterio A cumplido en k = 7: dₖ < ε")
        self.assertIsNone(interactivas.estado_final("DIAGONAL_CERO", 0))

    def test_html_propio_solo_admite_sub_y_sup(self):
        self.assertEqual(_e("T<sub>J</sub> y x<sup>(k)</sup>"), "T<sub>J</sub> y x<sup>(k)</sup>")
        self.assertEqual(_e("<script>alert(1)</script>"), "&lt;script&gt;alert(1)&lt;/script&gt;")
        self.assertEqual(_e("a < b & c"), "a &lt; b &amp; c")


if __name__ == "__main__":
    unittest.main()
