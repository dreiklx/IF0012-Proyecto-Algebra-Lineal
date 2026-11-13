"""Pruebas de la navegación 2D (gestos/vista2d.py) con datos y manos SINTÉTICOS.

No prueban ningún gesto con una mano real: la validación física la hace el equipo con su
cámara (ver docs/mediapipe_2d.md).  Tampoco tocan algebra/: solo rangos de ejes.
"""

import time
import unittest

from gestos import control as gc
from gestos import interpretacion as gi
from gestos.vista2d import ESCALA_MAX, ESCALA_MIN, VistaPlano2D, rango_inicial
from tests.gestos import manos_sinteticas as ms
from tests.gestos.test_control import CamaraFalsa, DetectorFalso, esperar
from tests.gestos.test_interpretacion import correr


def vista():
    return VistaPlano2D(-0.5, 9.5, -4.0, 1.0)     # 10 iteraciones, valores de 1e-4 a 10


class TestDesplazamiento(unittest.TestCase):
    def test_mano_a_la_derecha_desplaza_el_contenido_a_la_derecha(self):
        v = vista()
        x0 = v.x0
        self.assertTrue(v.girar(0.1, 0.0))
        self.assertLess(v.x0, x0)                  # el rango se mueve a la izquierda (el contenido va a la derecha)

    def test_desplazamiento_proporcional_al_ancho_visible(self):
        v = vista()
        v.girar(0.1, 0.0)
        self.assertAlmostEqual(v.x1 - v.x0, 10.0)  # el ancho no cambia al desplazar
        self.assertAlmostEqual(v.x0, -0.5 - 1.0)   # 0,1 · ancho 10

    def test_vertical_desplaza_el_eje_y_sin_cambiar_el_alto(self):
        v = vista()
        y0, alto = v.y0, v.y1 - v.y0
        v.girar(0.0, 0.1)
        self.assertAlmostEqual(v.y1 - v.y0, alto)
        self.assertAlmostEqual(v.y0, y0 + 0.1 * alto)

    def test_zona_muerta_acumulada_no_mueve_por_temblor(self):
        v = vista()
        x0 = v.x0
        for _ in range(10):                        # ida y vuelta: el temblor se cancela
            v.girar(0.001, 0.0)
            v.girar(-0.001, 0.0)
        self.assertEqual(v.x0, x0)

    def test_movimiento_lento_sostenido_si_llega(self):
        v = vista()
        x0 = v.x0
        for _ in range(20):
            v.girar(0.001, 0.0)                    # cada fotograma es menor que la zona muerta
        self.assertLess(v.x0, x0)


class TestZoom(unittest.TestCase):
    def test_acercar_reduce_el_rango_alrededor_del_centro(self):
        v = vista()
        cx = (v.x0 + v.x1) / 2
        ancho = v.x1 - v.x0
        self.assertTrue(v.zoom(2.0))
        self.assertAlmostEqual((v.x0 + v.x1) / 2, cx)
        self.assertAlmostEqual(v.x1 - v.x0, ancho / 2)

    def test_alejar_amplia_el_rango(self):
        v = vista()
        ancho = v.x1 - v.x0
        v.zoom(0.5)
        self.assertAlmostEqual(v.x1 - v.x0, ancho * 2)

    def test_factores_de_temblor_se_ignoran(self):
        v = vista()
        antes = v.a_plotly()
        self.assertFalse(v.zoom(1.004))
        self.assertFalse(v.zoom(0))
        self.assertEqual(v.a_plotly(), antes)

    def test_los_limites_de_zoom_se_respetan(self):
        v = vista()
        for _ in range(60):
            v.zoom(1.5)
        self.assertAlmostEqual(v.x1 - v.x0, v.ancho_inicial * ESCALA_MIN)
        for _ in range(120):
            v.zoom(0.5)
        self.assertAlmostEqual(v.x1 - v.x0, v.ancho_inicial * ESCALA_MAX)


class TestRestablecerYRaton(unittest.TestCase):
    def test_restablecer_vuelve_al_rango_inicial(self):
        v = vista()
        inicial = v.a_plotly()
        v.girar(0.2, 0.2)
        v.zoom(3)
        v.restablecer()
        self.assertEqual(v.a_plotly(), inicial)

    def test_rango_del_raton_parcial_y_completo(self):
        v = vista()
        self.assertTrue(v.desde_plotly({"xaxis.range[0]": 2, "xaxis.range[1]": 7}))
        self.assertEqual((v.x0, v.x1), (2.0, 7.0))
        self.assertEqual((v.y0, v.y1), (-4.0, 1.0))           # el eje Y no cambió
        self.assertTrue(v.desde_plotly({"yaxis.range": [-3, 0]}))
        self.assertEqual((v.y0, v.y1), (-3.0, 0.0))

    def test_datos_del_raton_invalidos_se_ignoran(self):
        v = vista()
        antes = v.a_plotly()
        self.assertFalse(v.desde_plotly({"xaxis.range[0]": 5, "xaxis.range[1]": 5}))
        self.assertFalse(v.desde_plotly("basura"))
        self.assertEqual(v.a_plotly(), antes)

    def test_a_plotly_usa_las_claves_de_relayout(self):
        self.assertEqual(set(vista().a_plotly()), {"xaxis.range", "yaxis.range"})

    def test_rango_inicial_cubre_los_datos(self):
        class F:
            def __init__(self, k, d, r):
                self.k, self.d, self.r = k, d, r
        historial = [F(0, None, 1.0), F(1, 0.5, 0.2), F(2, 0.01, 0.001)]
        x0, x1, y0, y1 = rango_inicial(historial, tolerancia=1e-3)
        self.assertLess(x0, 0)
        self.assertGreater(x1, 2)
        self.assertLess(y0, -3)                    # log10(1e-3) dentro del rango
        self.assertGreater(y1, 0)                  # log10(1) dentro del rango
        VistaPlano2D(x0, x1, y0, y1)               # válido para la navegación


class TestGestosSobreLaVista(unittest.TestCase):
    """La máquina de gestos existente produce las acciones; aquí se comprueba que la vista
    2D las aplica con el sentido correcto."""

    def armado(self):
        it = gi.InterpreteGestos()
        correr(it, [[ms.palma()]] * 15)
        return it

    def test_pinza_que_se_mueve_desplaza_la_vista(self):
        it, v = self.armado(), vista()
        x0 = v.x0
        res = correr(it, [[ms.pinza(cx=0.4 + 0.01 * k)] for k in range(20)], t0=1)
        for r in res:
            for a in r.acciones:
                if a[0] == "girar":
                    v.girar(a[1], a[2])
        self.assertLess(v.x0, x0)

    def test_dos_pinzas_que_se_separan_acercan(self):
        it, v = self.armado(), vista()
        ancho = v.x1 - v.x0
        separacion = [0.3 + 0.02 * k for k in range(15)]
        res = correr(it, [[ms.pinza(cx=0.5 - s / 2), ms.pinza(cx=0.5 + s / 2)] for s in separacion], t0=1)
        for r in res:
            for a in r.acciones:
                if a[0] == "zoom":
                    v.zoom(a[1])
        self.assertLess(v.x1 - v.x0, ancho)

    def test_puno_pausa_y_victoria_restablece(self):
        it, v = self.armado(), vista()
        correr(it, [[ms.puno()]] * 15, t0=1)
        self.assertEqual(it.estado, gi.PAUSADO)
        res = correr(it, [[ms.pinza(cx=0.2 + 0.05 * k)] for k in range(10)], t0=2)
        self.assertFalse(any(a[0] == "girar" for r in res for a in r.acciones))   # en pausa no mueve
        correr(it, [[ms.palma()]] * 15, t0=3)
        v.girar(0.2, 0.0)
        res = correr(it, [[ms.victoria()]] * 40, t0=4)
        self.assertTrue(any(a[0] == "restablecer" for r in res for a in r.acciones))
        v.restablecer()
        self.assertEqual(v.x0, -0.5)


class TestControlConVistaDosD(unittest.TestCase):
    """Hilo de control con el destino 2D y cámara/detector falsos: no se enciende ninguna cámara."""

    def test_el_control_2d_mueve_solo_el_rango_y_libera_la_camara(self):
        cam, det = CamaraFalsa(), DetectorFalso()
        v = vista()
        inicial = v.a_plotly()
        c = gc.ControlGestual(lambda: cam, lambda: det, con_servidor=False, destino=v)
        c.iniciar()
        for _ in range(60):
            c.latido()
            time.sleep(0.05)
        self.assertNotEqual(c.camara_actual(), inicial)            # la vista cambió
        self.assertEqual(set(c.camara_actual()), {"xaxis.range", "yaxis.range"})
        c.detener()
        self.assertTrue(cam.liberada and det.cerrado)
        self.assertFalse(c.activo)

    def test_perro_guardian_tambien_apaga_el_control_2d(self):
        from unittest import mock
        cam, det = CamaraFalsa(), DetectorFalso()
        c = gc.ControlGestual(lambda: cam, lambda: det, con_servidor=False, destino=vista())
        with mock.patch.object(gc, "TIEMPO_SIN_LATIDO", 0.3):
            c.iniciar()
            self.assertTrue(esperar(lambda: not c.activo))
        self.assertTrue(cam.liberada)


if __name__ == "__main__":
    unittest.main()
