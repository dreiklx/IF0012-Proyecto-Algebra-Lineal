"""Pruebas de integración de la interfaz con streamlit.testing (AppTest).

Ejecutan app.py sin navegador, pulsan botones y comprueban los mensajes que
se muestran.  Se omiten si Streamlit no está instalado (por ejemplo al usar
un Python sin el entorno virtual del proyecto).
"""

import os
import unittest

try:
    from streamlit.testing.v1 import AppTest
except ImportError:  # pragma: no cover
    AppTest = None

RUTA_APP = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "app.py")


def textos(elementos):
    return " | ".join(str(e.value) for e in elementos)


@unittest.skipIf(AppTest is None, "Streamlit no está instalado en este intérprete")
class TestAplicacion(unittest.TestCase):

    def abrir(self, pagina):
        at = AppTest.from_file(RUTA_APP, default_timeout=60)
        at.run()
        self.assertFalse(at.exception, at.exception)
        if pagina:
            at.sidebar.radio(key="navegacion").set_value(pagina)
            at.run()
            self.assertFalse(at.exception, at.exception)
        return at

    def test_inicio(self):
        at = self.abrir(None)
        self.assertIn("Álgebra Lineal", at.title[0].value)

    def test_modulo_I_unica_infinitas_inconsistente(self):
        at = self.abrir("I · Sistemas lineales (Gauss)")
        at.button(key="dir_resolver").click()
        at.run()
        self.assertFalse(at.exception)
        self.assertIn("Solución única", textos(at.success))
        for ejemplo, esperado, tipo in (
                ("Infinitas soluciones (una variable libre)", "Infinitas soluciones", "warning"),
                ("Sistema inconsistente (planos sin punto común)", "inconsistente", "error")):
            at.selectbox(key="dir_ejemplo").set_value(ejemplo)
            at.run()
            at.button(key="dir_resolver").click()
            at.run()
            self.assertFalse(at.exception)
            self.assertIn(esperado, textos(getattr(at, tipo)))

    def test_modulo_I_entrada_invalida(self):
        at = self.abrir("I · Sistemas lineales (Gauss)")
        nombre = at.selectbox(key="dir_ejemplo").value
        at.text_area(key=f"dir_A_{nombre}").input("1 2\n3 x")
        at.button(key="dir_resolver").click()
        at.run()
        self.assertFalse(at.exception)
        self.assertIn("(2, 2)", textos(at.error))

    def test_modulo_II(self):
        at = self.abrir("II · Condicionamiento")
        at.button(key="cond_calcular").click()
        at.run()
        self.assertFalse(at.exception)
        self.assertIn("Sensibilidad baja", textos(at.success))
        self.assertIn("la cota se cumple", textos(at.info))

    def test_modulo_II_singular(self):
        at = self.abrir("II · Condicionamiento")
        nombre = at.selectbox(key="cond_ejemplo").value
        at.text_area(key=f"cond_A_{nombre}").input("1 2\n2 4")
        at.button(key="cond_calcular").click()
        at.run()
        self.assertFalse(at.exception)
        self.assertIn("singular", textos(at.error))

    def test_modulo_III(self):
        at = self.abrir("III · Mínimos cuadrados")
        at.button(key="mc_resolver").click()
        at.button(key="aj_calcular").click()
        at.run()
        self.assertFalse(at.exception)
        self.assertIn("y = 3/4 x + 6/5", textos(at.success))

    def test_modulo_IV_ejecutar_y_comparar(self):
        at = self.abrir("IV · Métodos iterativos")
        at.button(key="it_ejecutar").click()
        at.run()
        self.assertFalse(at.exception)
        self.assertIn("Criterio satisfecho: d_7", textos(at.success))
        at.button(key="it_comparar").click()
        at.run()
        self.assertFalse(at.exception)
        self.assertIn("Experimento homogéneo", textos(at.success))
        at.button(key="it_conv").click()
        at.run()
        self.assertFalse(at.exception)
        self.assertIn("converge para cualquier vector inicial", textos(at.success))

    def test_modulo_IV_criterio_C_y_validacion(self):
        at = self.abrir("IV · Métodos iterativos")
        at.radio(key="it_criterio").set_value("C")
        at.run()
        at.button(key="it_ejecutar").click()
        at.run()
        self.assertFalse(at.exception)
        self.assertIn("no demuestra convergencia", textos(at.info))
        at.radio(key="it_criterio").set_value("A")
        at.run()
        at.text_input(key="it_eps").input("0")
        at.button(key="it_ejecutar").click()
        at.run()
        self.assertFalse(at.exception)
        self.assertIn("mayor que 0", textos(at.error))

    def test_modulo_IV_jacobi_no_converge(self):
        at = self.abrir("IV · Métodos iterativos")
        at.selectbox(key="it_ejemplo").set_value("S9-07/10 — Jacobi no converge (ρ ≈ 1.174)")
        at.run()
        at.button(key="it_conv").click()
        at.run()
        self.assertFalse(at.exception)
        self.assertIn("no converge", textos(at.error))
        at.button(key="it_ejecutar").click()
        at.run()
        self.assertIn("máximo de iteraciones sin satisfacer", textos(at.warning))


if __name__ == "__main__":
    unittest.main()
