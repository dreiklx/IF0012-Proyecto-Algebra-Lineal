"""El panel de control gestual aparece en el Módulo I, pero la cámara no se enciende sola.

No se pulsa «Activar»: estas pruebas nunca encienden la cámara del equipo.
"""

import unittest

from interfaz import navegacion as nav
from tests.rutas import RUTA_APP

try:
    from streamlit.testing.v1 import AppTest
except ImportError:  # pragma: no cover
    AppTest = None


@unittest.skipIf(AppTest is None, "Streamlit no está instalado en este intérprete")
class TestPanelGestual(unittest.TestCase):

    def test_panel_visible_y_camara_apagada(self):
        at = AppTest.from_file(RUTA_APP, default_timeout=60)
        at.run()
        at.switch_page(nav.SISTEMAS).run()
        at.button(key="dir_resolver").click().run()
        self.assertFalse(at.exception, at.exception)
        claves = [b.key for b in at.button]
        import gestos
        if gestos.disponible()[0]:
            self.assertIn("gest_activar", claves)
            self.assertFalse(at.button(key="gest_activar").disabled)
            self.assertTrue(at.button(key="gest_detener").disabled)   # nada encendido
            from interfaz.compartido import control_gestual
            self.assertFalse(control_gestual.control().activo)
        else:
            self.assertNotIn("gest_activar", claves)
            self.assertIn("no disponible", " ".join(str(i.value) for i in at.info))


if __name__ == "__main__":
    unittest.main()
