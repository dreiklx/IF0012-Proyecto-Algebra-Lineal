"""Gráficas de exploración (10-nov): los hitos, resaltes y paneles salen de los datos reales.

Oráculos: el historial y el código de terminación que devuelve el núcleo.  Se comprueba
que nunca se rotula «ε alcanzado» si el método no cumplió el criterio, que los tramos
sombreados son exactamente los k en que d_k creció y que los datos de las trazas no
cambiaron respecto a la versión anterior (mismas comprobaciones que
test_graficas_interactivas.py).
"""

import os
import unittest

from algebra.modulo_III_minimos.minimos import ajuste_lineal
from algebra.modulo_IV_iterativos.comparacion import comparar_metodos, configuraciones_homogeneas
from algebra.modulo_IV_iterativos.ejecucion import ConfiguracionIterativa, ejecutar
from algebra.modulo_IV_iterativos.espectral import radio_espectral
from interfaz import navegacion as nav
from tests.rutas import RUTA_APP
from visualizacion import interactivas

S = [[10, -1, 2], [-1, 11, -1], [2, -1, 10]]
B = [6, 25, -11]
NO_CONVERGE = [[3, 3, 3], [3, 3, 2], [-3, -2, 3]]      # S9-07/10: ρ(T_J) ≈ 1,174


def textos(fig):
    return [a.text for a in fig.layout.annotations]


def traza(fig, contiene):
    return [t for t in fig.data if t.name and contiene in t.name][0]


class TestConvergencia(unittest.TestCase):

    def test_criterio_cumplido_se_rotula_con_el_codigo_real(self):
        r = ejecutar(S, B, ConfiguracionIterativa())
        self.assertEqual(r.codigo, "TOLERANCIA_CAMBIO")
        fig = interactivas.convergencia(r.historial, "A", 1e-3, metodo="Jacobi", codigo=r.codigo)
        self.assertIn(f"Criterio A cumplido en k = {r.k_final}: d_k < ε", textos(fig))
        self.assertIn("ε alcanzado", textos(fig))
        # los datos siguen siendo los del historial
        self.assertEqual(list(traza(fig, "d_k").y), [f.d for f in r.historial if f.d is not None])
        self.assertEqual(list(traza(fig, "r_k").y), [f.r for f in r.historial])
        self.assertEqual(fig.layout.shapes[0].y0, 1e-3)          # ε sigue siendo la primera forma

    def test_k_max_no_se_presenta_como_convergencia(self):
        r = ejecutar(S, B, ConfiguracionIterativa(k_max=2))
        self.assertEqual(r.codigo, "MAXIMO_ITERACIONES")
        fig = interactivas.convergencia(r.historial, "A", 1e-3, codigo=r.codigo)
        self.assertIn("Se alcanzó k_max = 2 sin cumplir el criterio", textos(fig))
        self.assertNotIn("ε alcanzado", textos(fig))
        self.assertFalse(any("cumplido en" in t for t in textos(fig)))

    def test_metodo_que_no_converge_sombrea_solo_donde_d_crece(self):
        r = ejecutar(NO_CONVERGE, [9, 9, -2], ConfiguracionIterativa(k_max=30))
        self.assertNotIn(r.codigo, ("TOLERANCIA_CAMBIO", "TOLERANCIA_RESIDUO"))
        fig = interactivas.convergencia(r.historial, "A", 1e-3, codigo=r.codigo)
        self.assertFalse(any("cumplido en" in t or t == "ε alcanzado" for t in textos(fig)))
        crecen = {f1.k for f0, f1 in zip(r.historial, r.historial[1:])
                  if f0.d is not None and f1.d is not None and f0.d > 0 and f1.d > f0.d}
        sombreados = set()
        for forma in fig.layout.shapes:
            if forma.type == "rect":
                sombreados |= set(range(int(forma.x0) + 1, int(forma.x1) + 1))
        self.assertEqual(sombreados, crecen)
        self.assertTrue(crecen)

    def test_iteracion_destacada_y_x_en_el_cursor(self):
        r = ejecutar(S, B, ConfiguracionIterativa())
        fig = interactivas.convergencia(r.historial, "A", 1e-3, k_destacada=3)
        lineas = [f for f in fig.layout.shapes if f.type == "line" and f.x0 == 3 and f.x1 == 3]
        self.assertEqual(len(lineas), 1)
        rk = traza(fig, "r_k")
        self.assertEqual(rk.marker.size[list(rk.x).index(3)], 13)
        # el cursor muestra x⁽ᵏ⁾ exactamente como está en el historial
        for k, texto in zip(rk.x, rk.customdata):
            fila = r.historial[k]
            self.assertEqual(texto, "<br>x⁽ᵏ⁾ = (" + ", ".join(f"{v:.6g}" for v in fila.x) + ")")

    def test_criterio_c_sin_linea_epsilon(self):
        r = ejecutar(S, B, ConfiguracionIterativa(criterio="C", n_iteraciones=4))
        fig = interactivas.convergencia(r.historial, "C", None, codigo=r.codigo)
        self.assertFalse([f for f in fig.layout.shapes if f.type == "line" and f.y0 == f.y1])
        self.assertTrue(any("no demuestra convergencia" in t for t in textos(fig)))


class TestComparacion(unittest.TestCase):

    def setUp(self):
        self.comp = comparar_metodos(S, B, configuraciones_homogeneas())

    def test_destacar_no_cambia_los_datos(self):
        fig = interactivas.comparacion(self.comp.resultados, "d", destacado="Gauss-Seidel", k_destacada=2,
                                       criterio="A", tolerancia=1e-3)
        self.assertEqual(len(fig.data), 3)
        for t, r in zip(fig.data, self.comp.resultados):
            self.assertEqual(list(zip(t.x, t.y)), [(f.k, f.d) for f in r.historial if f.d is not None and f.d > 0])
            self.assertEqual(t.opacity, 1.0 if r.configuracion.metodo == "Gauss-Seidel" else 0.22)
        self.assertTrue(any(f.y0 == 1e-3 for f in fig.layout.shapes))      # d con criterio A: hay ε

    def test_epsilon_solo_si_la_metrica_es_la_del_criterio(self):
        for metrica in ("r", "e"):
            fig = interactivas.comparacion(self.comp.resultados, metrica, self.comp.errores_historial,
                                           criterio="A", tolerancia=1e-3)
            self.assertFalse([f for f in fig.layout.shapes if f.y0 == 1e-3 and f.y1 == 1e-3])

    def test_rotulo_final_de_cada_metodo(self):
        fig = interactivas.comparacion(self.comp.resultados, "d")
        self.assertEqual(sorted(textos(fig)), sorted(f"k = {r.k_final}" for r in self.comp.resultados))


class TestOtras(unittest.TestCase):

    def test_autovalor_dominante_resaltado(self):
        esp = radio_espectral(NO_CONVERGE, [9, 9, -2], "Jacobi")
        fig = interactivas.autovalores(esp.autovalores, esp.rho)
        puntos = traza(fig, "Autovalores")
        for z, tam in zip(esp.autovalores, puntos.marker.size):
            self.assertEqual(tam, 16 if abs(z) >= esp.rho * (1 - 1e-9) else 12)
        self.assertIn("|λ| = ρ(T)", textos(fig))

    def test_ajuste_resalta_el_mayor_residuo(self):
        r = ajuste_lineal([1, 2, 3, 4], [2, 2.5, 3.7, 4.1])
        fig = interactivas.ajuste(r.xs, r.ys, r.pendiente, r.intercepto, r.minimos.estimados)
        residuos = [float(y) - float(e) for y, e in zip(r.ys, r.minimos.estimados)]
        mayor = max(range(4), key=lambda i: abs(residuos[i]))
        self.assertEqual(list(traza(fig, "Datos").marker.size), [13 if i == mayor else 10 for i in range(4)])


@unittest.skipIf(os.environ.get("SIN_APPTEST"), "AppTest desactivado")
class TestExploracionEnLaAplicacion(unittest.TestCase):

    def abrir_iterativos(self):
        try:
            from streamlit.testing.v1 import AppTest
        except ImportError:  # pragma: no cover
            self.skipTest("Streamlit no está instalado")
        at = AppTest.from_file(RUTA_APP, default_timeout=60)
        at.run()
        at.switch_page(nav.ITERATIVOS).run()
        return at

    def test_deslizador_muestra_la_iteracion_elegida(self):
        at = self.abrir_iterativos()
        at.button(key="it_ejecutar").click().run()
        self.assertFalse(at.exception, at.exception)
        deslizador = at.slider(key="it_k_conv")
        self.assertEqual(deslizador.value, deslizador.max)          # empieza en la última iteración
        deslizador.set_value(2).run()
        self.assertFalse(at.exception, at.exception)
        metricas = {m.label: m.value for m in at.metric}
        self.assertEqual(metricas["Iteración k"], "2")
        self.assertIn("x⁽ᵏ⁾ = (", " ".join(str(m.value) for m in at.markdown))

    def test_comparacion_destacar_y_tabla_por_iteracion(self):
        at = self.abrir_iterativos()
        at.button(key="it_comparar").click().run()
        self.assertFalse(at.exception, at.exception)
        at.radio(key="it_destacar").set_value("Jacobi").run()
        at.slider(key="it_k_comp").set_value(1).run()
        self.assertFalse(at.exception, at.exception)
        tablas = [d.value for d in at.dataframe]
        self.assertTrue(any("Estado en k = 1" in list(t.columns) for t in tablas))


if __name__ == "__main__":
    unittest.main()
