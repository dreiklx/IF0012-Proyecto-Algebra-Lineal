"""Pruebas de gestos/interpretacion.py con manos sintéticas (sin cámara)."""

import unittest

from gestos import interpretacion as gi
from tests.gestos import manos_sinteticas as ms


def correr(interprete, secuencia, t0=0.0, dt=1 / 30):
    """Aplica una lista de fotogramas (listas de manos); devuelve los resultados."""
    return [interprete.actualizar(manos, t0 + k * dt) for k, manos in enumerate(secuencia)]


class TestClasificar(unittest.TestCase):
    def test_cada_gesto(self):
        self.assertEqual(gi.clasificar(ms.palma()), gi.PALMA)
        self.assertEqual(gi.clasificar(ms.puno()), gi.PUNO)
        self.assertEqual(gi.clasificar(ms.victoria()), gi.VICTORIA)
        self.assertEqual(gi.clasificar(ms.pinza()), gi.PINZA)

    def test_no_depende_de_la_distancia_a_la_camara(self):
        # umbral adaptativo: todo se mide en unidades de palma
        for escala in (0.04, 0.1, 0.3):
            self.assertEqual(gi.clasificar(ms.pinza(escala=escala)), gi.PINZA)
            self.assertEqual(gi.clasificar(ms.puno(escala=escala)), gi.PUNO)

    def test_el_puno_no_se_confunde_con_pinza(self):
        # en el puño el pulgar queda cerca del índice; lo distingue la punta del índice
        self.assertLess(gi.razon_pinza(ms.puno()), gi.PINZA_ENTRA)
        self.assertEqual(gi.clasificar(ms.puno()), gi.PUNO)


class TestInterprete(unittest.TestCase):
    def armado(self):
        it = gi.InterpreteGestos()
        correr(it, [[ms.palma()]] * 15)
        self.assertEqual(it.estado, gi.LISTO)
        return it

    def test_empieza_esperando_y_se_activa_con_palma_sostenida(self):
        it = gi.InterpreteGestos()
        correr(it, [[ms.palma()]] * 5)          # 0,13 s: todavía no (antirrebote)
        self.assertEqual(it.estado, gi.ESPERANDO)
        correr(it, [[ms.palma()]] * 10, t0=5 / 30)
        self.assertEqual(it.estado, gi.LISTO)

    def test_sin_activar_la_pinza_no_mueve_nada(self):
        it = gi.InterpreteGestos()
        res = correr(it, [[ms.pinza(cx=0.4 + 0.01 * k)] for k in range(20)])
        self.assertFalse(any(r.acciones for r in res))

    def test_pinza_y_movimiento_giran(self):
        it = self.armado()
        res = correr(it, [[ms.pinza(cx=0.4 + 0.01 * k)] for k in range(20)], t0=1)
        giros = [a for r in res for a in r.acciones if a[0] == "girar"]
        self.assertEqual(it.estado, gi.GIRANDO)
        self.assertTrue(giros)
        self.assertTrue(all(a[1] > 0 for a in giros))           # mano a la derecha → dx > 0
        self.assertAlmostEqual(sum(a[1] for a in giros), 0.19, delta=0.06)  # suavizado: algo de retraso

    def test_al_agarrar_no_hay_salto(self):
        it = self.armado()
        res = correr(it, [[ms.pinza(cx=0.9)]], t0=1)     # la pinza empieza lejos: sin acción
        self.assertEqual(res[0].acciones, [])

    def test_histeresis_de_la_pinza(self):
        it = self.armado()
        correr(it, [[ms.pinza()]] * 3, t0=1)
        self.assertEqual(it.estado, gi.GIRANDO)
        self.assertGreater(it.umbral_sale, it.umbral_entra)

    def test_soltar_la_pinza_vuelve_a_listo(self):
        it = self.armado()
        correr(it, [[ms.pinza()]] * 3, t0=1)
        correr(it, [[ms.palma()]] * 3, t0=2)
        self.assertEqual(it.estado, gi.LISTO)

    def test_puno_pausa_y_palma_reanuda(self):
        it = self.armado()
        correr(it, [[ms.puno()]] * 15, t0=1)
        self.assertEqual(it.estado, gi.PAUSADO)
        res = correr(it, [[ms.pinza(cx=0.4 + 0.01 * k)] for k in range(10)], t0=2)
        self.assertFalse(any(r.acciones for r in res))          # en pausa no gira
        correr(it, [[ms.palma()]] * 15, t0=3)
        self.assertEqual(it.estado, gi.LISTO)

    def test_victoria_sostenida_restablece_una_sola_vez(self):
        it = self.armado()
        res = correr(it, [[ms.victoria()]] * 60, t0=1)          # 2 s
        restablecer = [a for r in res for a in r.acciones if a[0] == "restablecer"]
        self.assertEqual(len(restablecer), 1)
        res = correr(it, [[ms.victoria()]] * 10, t0=3)          # breve: no dispara
        self.assertEqual(len([a for r in res for a in r.acciones]), 0)

    def test_dos_manos_hacen_zoom(self):
        it = self.armado()
        secuencia = [[ms.pinza(cx=0.4 - 0.01 * k, lado="Left"), ms.pinza(cx=0.6 + 0.01 * k)] for k in range(10)]
        res = correr(it, secuencia, t0=1)
        zooms = [a[1] for r in res for a in r.acciones if a[0] == "zoom"]
        self.assertEqual(it.estado, gi.ZOOM)
        self.assertTrue(zooms and all(f > 1 for f in zooms))   # se separan → acercar

    def test_perder_la_mano_suelta(self):
        it = self.armado()
        correr(it, [[ms.pinza()]] * 3, t0=1)
        correr(it, [[]] * 30, t0=2)                              # 1 s sin mano
        self.assertEqual(it.estado, gi.LISTO)

    def test_calibracion_ajusta_el_umbral_dentro_de_limites(self):
        it = gi.InterpreteGestos()
        it.calibrar(ms.palma())
        self.assertLessEqual(it.umbral_entra, gi.PINZA_ENTRA)
        self.assertGreaterEqual(it.umbral_entra, 0.18)
        self.assertAlmostEqual(it.umbral_sale, 1.5 * it.umbral_entra)


if __name__ == "__main__":
    unittest.main()
