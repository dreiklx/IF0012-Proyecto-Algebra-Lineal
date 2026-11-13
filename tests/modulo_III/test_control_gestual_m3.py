"""Pruebas sintéticas del control gestual de la gráfica de mínimos cuadrados (Módulo III).

La cámara y el detector son dobles de prueba (no se enciende ninguna cámara). Se comprueba
que los gestos cambian solo la vista de los ejes y que los datos, la recta, los valores
estimados y los residuos no cambian nunca.  No es una prueba física con manos.
"""

import copy
import time
import unittest
from fractions import Fraction as F

from gestos import control as gc
from gestos.vista2d import ESCALA_MIN, VistaPlano2D
from algebra.modulo_III_minimos.minimos import ajuste_lineal
from interfaz.compartido import control_gestual as cg
from tests.gestos.test_control import CamaraFalsa, DetectorFalso
from visualizacion.interactivas import ajuste, rango_ajuste


def caso():
    xs, ys = [1, 2, 3, 4], [2, F(5, 2), F(37, 10), F(41, 10)]
    return ajuste_lineal(xs, ys)


def trazos(figura):
    """Coordenadas de todos los trazos (datos, residuos y recta), para comprobar que no cambian."""
    return [(list(t.x), list(t.y)) for t in figura.data]


class TestVistaDelAjuste(unittest.TestCase):
    def test_rango_inicial_cubre_datos_residuos_y_recta(self):
        r = caso()
        x0, x1, y0, y1 = rango_ajuste(r.xs, r.ys, r.minimos.estimados)
        self.assertLess(x0, min(float(v) for v in r.xs))
        self.assertGreater(x1, max(float(v) for v in r.xs))
        for y, e in zip(r.ys, r.minimos.estimados):
            self.assertTrue(y0 <= min(float(y), float(e)) and max(float(y), float(e)) <= y1)

    def test_rango_solo_cambia_la_vista_no_los_trazos(self):
        r = caso()
        base = ajuste(r.xs, r.ys, r.pendiente, r.intercepto, r.minimos.estimados)
        otro = (0.0, 10.0, -5.0, 9.0)
        con_vista = ajuste(r.xs, r.ys, r.pendiente, r.intercepto, r.minimos.estimados, rango=otro)
        self.assertEqual(trazos(base), trazos(con_vista))
        self.assertEqual(list(con_vista.layout.xaxis.range), [0.0, 10.0])
        self.assertEqual(list(con_vista.layout.yaxis.range), [-5.0, 9.0])

    def test_gestos_sobre_la_vista_no_alteran_el_calculo(self):
        r = caso()
        antes = copy.deepcopy((r.pendiente, r.intercepto, list(r.minimos.estimados), list(r.minimos.residuo)))
        x0, x1, y0, y1 = rango_ajuste(r.xs, r.ys, r.minimos.estimados)
        v = VistaPlano2D(x0, x1, y0, y1)
        v.girar(0.2, -0.1)
        v.zoom(2.0)
        figura = ajuste(r.xs, r.ys, r.pendiente, r.intercepto, r.minimos.estimados,
                        rango=(v.x0, v.x1, v.y0, v.y1))
        self.assertIsNotNone(figura)
        despues = (r.pendiente, r.intercepto, list(r.minimos.estimados), list(r.minimos.residuo))
        self.assertEqual(antes, despues)


class TestGestosM3(unittest.TestCase):
    def test_pinza_desplaza_y_dos_pinzas_acercan_la_vista(self):
        from tests.gestos import manos_sinteticas as ms
        from tests.gestos.test_interpretacion import correr
        from gestos import interpretacion as gi
        r = caso()
        x0, x1, y0, y1 = rango_ajuste(r.xs, r.ys, r.minimos.estimados)
        v = VistaPlano2D(x0, x1, y0, y1)
        it = gi.InterpreteGestos()
        correr(it, [[ms.palma()]] * 15)
        for res in correr(it, [[ms.pinza(cx=0.4 + 0.01 * k)] for k in range(20)], t0=1):
            for a in res.acciones:
                if a[0] == "girar":
                    v.girar(a[1], a[2])
        self.assertLess(v.x0, x0)                       # la pinza hacia la derecha desplaza el contenido
        ancho = v.x1 - v.x0
        for res in correr(it, [[ms.pinza(cx=0.5 - s / 2), ms.pinza(cx=0.5 + s / 2)] for s in
                               [0.3 + 0.02 * k for k in range(15)]], t0=3):
            for a in res.acciones:
                if a[0] == "zoom":
                    v.zoom(a[1])
        self.assertLess(v.x1 - v.x0, ancho)              # separar las manos acerca

    def test_puno_pausa_y_victoria_restablece(self):
        from tests.gestos import manos_sinteticas as ms
        from tests.gestos.test_interpretacion import correr
        from gestos import interpretacion as gi
        r = caso()
        x0, x1, y0, y1 = rango_ajuste(r.xs, r.ys, r.minimos.estimados)
        v = VistaPlano2D(x0, x1, y0, y1)
        it = gi.InterpreteGestos()
        correr(it, [[ms.palma()]] * 15)
        correr(it, [[ms.puno()]] * 15, t0=1)
        self.assertEqual(it.estado, gi.PAUSADO)
        res = correr(it, [[ms.pinza(cx=0.2 + 0.05 * k)] for k in range(10)], t0=2)
        self.assertFalse(any(a[0] == "girar" for x in res for a in x.acciones))
        correr(it, [[ms.palma()]] * 15, t0=3)           # la palma reanuda tras la pausa
        v.girar(0.2, 0.0)
        res = correr(it, [[ms.victoria()]] * 40, t0=4)
        self.assertTrue(any(a[0] == "restablecer" for x in res for a in x.acciones))
        v.restablecer()
        self.assertEqual((v.x0, v.x1, v.y0, v.y1), (x0, x1, y0, y1))

    def test_limites_de_zoom_y_desplazamiento(self):
        r = caso()
        x0, x1, y0, y1 = rango_ajuste(r.xs, r.ys, r.minimos.estimados)
        v = VistaPlano2D(x0, x1, y0, y1)
        for _ in range(80):
            v.zoom(1.5)
        self.assertGreater(v.x1 - v.x0, 0)
        self.assertAlmostEqual(v.x1 - v.x0, (x1 - x0) * ESCALA_MIN)

    def test_control_de_mco_hilo_sin_tocar_los_datos(self):
        r = caso()
        datos = copy.deepcopy((list(r.xs), list(r.ys)))
        x0, x1, y0, y1 = rango_ajuste(r.xs, r.ys, r.minimos.estimados)
        cam, det = CamaraFalsa(), DetectorFalso()
        c = gc.ControlGestual(lambda: cam, lambda: det, con_servidor=False, destino=VistaPlano2D(x0, x1, y0, y1))
        c.iniciar()
        for _ in range(40):
            c.latido()
            time.sleep(0.05)
        c.detener()
        self.assertTrue(cam.liberada)
        self.assertEqual((list(r.xs), list(r.ys)), datos)


class TestObjetivosNoInterfieren(unittest.TestCase):
    def test_cada_objetivo_excluye_a_los_demas(self):
        for tipo in cg.OBJETIVOS:
            otros = cg._otros(tipo)
            self.assertNotIn(tipo, otros)
            self.assertEqual(sorted(otros + [tipo]), sorted(cg.OBJETIVOS))

    def test_modulo_III_es_una_vista_2d_propia(self):
        self.assertIn("2d_m3", cg.TIPOS_2D)
        self.assertIn("2d_m3", cg.OBJETIVOS)
        self.assertNotEqual(cg._clave("gest_activar", "2d_m3"), cg._clave("gest_activar", "2d"))
        self.assertEqual(cg._clave("gest_activar", "3d"), "gest_activar")


if __name__ == "__main__":
    unittest.main()
