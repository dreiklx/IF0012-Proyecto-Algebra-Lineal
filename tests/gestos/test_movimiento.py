"""Pruebas de gestos/movimiento.py: suavizado y cámara orbital."""

import math
import unittest

from gestos import movimiento as mv


def eye(c):
    e = c.a_plotly()["eye"]
    return e["x"], e["y"], e["z"]


class TestSuavizador(unittest.TestCase):
    def test_media_exponencial(self):
        s = mv.Suavizador(0.5)
        self.assertEqual(s.actualizar(0, 0), (0, 0))
        self.assertEqual(s.actualizar(1, 2), (0.5, 1.0))
        self.assertEqual(s.actualizar(1, 2), (0.75, 1.5))

    def test_alfa_invalido(self):
        with self.assertRaises(ValueError):
            mv.Suavizador(0)


class TestCamaraOrbital(unittest.TestCase):
    def test_vista_inicial_igual_a_la_de_la_figura(self):
        for a, b in zip(eye(mv.CamaraOrbital()), mv.EYE_INICIAL):
            self.assertAlmostEqual(a, b, places=4)

    def test_girar_conserva_la_distancia(self):
        c = mv.CamaraOrbital()
        r0 = c.r
        c.girar(0.1, -0.05)
        self.assertAlmostEqual(math.dist((0, 0, 0), eye(c)), r0, places=4)

    def test_zona_muerta(self):
        c = mv.CamaraOrbital()
        self.assertFalse(c.girar(0.001, 0.001))
        self.assertTrue(c.girar(0.05, 0))

    def test_movimiento_lento_sostenido_si_llega(self):
        c = mv.CamaraOrbital()
        cambios = [c.girar(0.001, 0) for _ in range(10)]     # cada paso < zona muerta
        self.assertTrue(any(cambios))
        # nada se pierde: lo aplicado más lo pendiente (< zona muerta) suma los 10 × 0,001
        aplicado = (mv.esfericas(mv.EYE_INICIAL)[0] - c.theta) / c.sensibilidad
        self.assertAlmostEqual(aplicado + c._pendiente[0], 0.010, places=9)
        self.assertLess(c._pendiente[0], c.zona_muerta)

    def test_temblor_no_mueve(self):
        c = mv.CamaraOrbital()
        self.assertFalse(any(c.girar(0.003 * (-1) ** k, 0) for k in range(50)))

    def test_limites_de_elevacion_y_distancia(self):
        c = mv.CamaraOrbital()
        c.girar(0, -10)           # mano muy arriba
        self.assertAlmostEqual(c.phi, mv.ELEVACION_MAX)
        c.girar(0, 20)
        self.assertAlmostEqual(c.phi, mv.ELEVACION_MIN)
        for _ in range(50):
            c.zoom(2)
        self.assertAlmostEqual(c.r, mv.DISTANCIA_MIN)
        for _ in range(50):
            c.zoom(0.5)
        self.assertAlmostEqual(c.r, mv.DISTANCIA_MAX)

    def test_up_fijo(self):
        c = mv.CamaraOrbital()
        c.girar(0.3, 0.2)
        self.assertEqual(c.a_plotly()["up"], {"x": 0, "y": 0, "z": 1})

    def test_restablecer(self):
        c = mv.CamaraOrbital()
        c.girar(0.4, 0.1)
        c.zoom(1.5)
        c.restablecer()
        for a, b in zip(eye(c), mv.EYE_INICIAL):
            self.assertAlmostEqual(a, b, places=4)

    def test_continua_desde_la_vista_del_raton(self):
        c = mv.CamaraOrbital()
        self.assertTrue(c.desde_plotly({"eye": {"x": 0, "y": 2, "z": 0}}))
        self.assertAlmostEqual(c.theta, math.pi / 2)
        self.assertAlmostEqual(c.r, 2)
        self.assertFalse(c.desde_plotly({"sin": "eye"}))


if __name__ == "__main__":
    unittest.main()
