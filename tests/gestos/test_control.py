"""Pruebas del hilo de control, del canal local y del detector real.

La cámara y el detector se sustituyen por dobles de prueba (manos sintéticas), así que
estas pruebas no encienden ninguna cámara.  El detector real solo se prueba con una
imagen negra generada en memoria (comprueba que el modelo carga y no ve manos).
"""

import http.client
import json
import threading
import time
import unittest
from unittest import mock

import gestos
from gestos import control as gc
from gestos.servidor import ServidorCamara
from tests.gestos import manos_sinteticas as ms


class CamaraFalsa:
    def __init__(self):
        self.liberada = False

    def leer(self):
        time.sleep(0.005)
        return object()          # el detector falso no mira la imagen

    def liberar(self):
        self.liberada = True


class DetectorFalso:
    """Palma 0,6 s y luego una pinza que se mueve a la derecha."""

    def __init__(self):
        self.k = 0
        self.cerrado = False

    def detectar(self, _fotograma, t_ms):
        self.k += 1
        if t_ms < 600:
            return [ms.palma()]
        return [ms.pinza(cx=min(0.9, 0.3 + 0.0005 * (t_ms - 600)))]

    def cerrar(self):
        self.cerrado = True


def esperar(condicion, limite=5.0):
    fin = time.time() + limite
    while time.time() < fin:
        if condicion():
            return True
        time.sleep(0.02)
    return False


class TestControl(unittest.TestCase):
    def nuevo(self):
        self.cam, self.det = CamaraFalsa(), DetectorFalso()
        return gc.ControlGestual(lambda: self.cam, lambda: self.det, con_servidor=False)

    def test_gira_la_camara_y_libera_al_detener(self):
        c = self.nuevo()
        inicial = c.camara_actual()
        c.iniciar()
        for _ in range(60):
            c.latido()
            time.sleep(0.05)
        self.assertEqual(c.estado()["modo"], "girando")
        self.assertNotEqual(c.camara_actual(), inicial)
        self.assertGreater(c.estado()["fps"], 0)
        c.detener()
        self.assertFalse(c.activo)
        self.assertTrue(self.cam.liberada and self.det.cerrado)
        self.assertEqual(c.estado()["motivo_fin"], "detenido por el usuario")

    def test_perro_guardian_apaga_la_camara_sin_latidos(self):
        c = self.nuevo()
        with mock.patch.object(gc, "TIEMPO_SIN_LATIDO", 0.3):
            c.iniciar()
            self.assertTrue(esperar(lambda: not c.activo))
        self.assertTrue(self.cam.liberada)
        self.assertIn("dejó de estar abierta", c.estado()["motivo_fin"])

    def test_error_al_abrir_la_camara_se_informa(self):
        def falla():
            raise RuntimeError("No se pudo abrir la cámara.")
        c = gc.ControlGestual(falla, DetectorFalso, con_servidor=False)
        c.iniciar()
        self.assertTrue(esperar(lambda: not c.activo))
        self.assertIn("No se pudo abrir", c.estado()["error"])

    def test_restablecer_y_raton(self):
        c = self.nuevo()
        c.sincronizar_raton({"eye": {"x": 0, "y": 2, "z": 0}})
        self.assertAlmostEqual(c.camara_actual()["eye"]["y"], 2)
        c.restablecer()
        self.assertAlmostEqual(c.camara_actual()["eye"]["x"], 1.55, places=3)


class TestServidor(unittest.TestCase):
    def setUp(self):
        self.recibido = []
        self.s = ServidorCamara(al_mover_raton=self.recibido.append)

    def tearDown(self):
        self.s.cerrar()

    def test_solo_escucha_en_127_0_0_1(self):
        self.assertEqual(self.s._http.server_address[0], "127.0.0.1")

    def test_token_obligatorio(self):
        con = http.client.HTTPConnection("127.0.0.1", self.s.puerto, timeout=5)
        con.request("GET", "/camara?t=otro")
        self.assertEqual(con.getresponse().status, 403)

    def test_envia_la_camara_por_sse(self):
        self.s.publicar({"eye": {"x": 1, "y": 2, "z": 3}})
        con = http.client.HTTPConnection("127.0.0.1", self.s.puerto, timeout=5)
        con.request("GET", f"/camara?t={self.s.token}")
        r = con.getresponse()
        self.assertEqual(r.getheader("Content-Type"), "text/event-stream")
        linea = r.fp.readline().decode()
        self.assertEqual(json.loads(linea[len("data: "):]), {"eye": {"x": 1, "y": 2, "z": 3}})
        threading.Timer(0.1, self.s.publicar, args=({"eye": {"x": 4, "y": 5, "z": 6}},)).start()
        r.fp.readline()
        self.assertIn('"x": 4', r.fp.readline().decode())
        con.close()

    def test_raton_actualiza_python(self):
        con = http.client.HTTPConnection("127.0.0.1", self.s.puerto, timeout=5)
        con.request("POST", f"/raton?t={self.s.token}", body=json.dumps({"eye": {"x": 0, "y": 1, "z": 0}}))
        self.assertEqual(con.getresponse().status, 204)
        self.assertEqual(self.recibido, [{"eye": {"x": 0, "y": 1, "z": 0}}])


@unittest.skipUnless(gestos.disponible()[0], "MediaPipe/OpenCV o el modelo no están instalados")
class TestDetectorReal(unittest.TestCase):
    def test_modelo_carga_y_no_ve_manos_en_negro(self):
        import numpy as np
        from gestos.deteccion import DetectorManos
        d = DetectorManos()
        try:
            negro = np.zeros((480, 640, 3), np.uint8)
            self.assertEqual(d.detectar(negro, 0), [])
            self.assertEqual(d.detectar(negro, 0), [])     # tiempo repetido: se corrige solo
        finally:
            d.cerrar()


if __name__ == "__main__":
    unittest.main()
