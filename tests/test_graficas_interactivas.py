"""Las gráficas interactivas (visualizacion/interactivas.py) dibujan exactamente los
mismos datos que el núcleo y que las figuras estáticas de Matplotlib.

Oráculos: los resultados del núcleo (historiales, autovalores, solución) y las
líneas de las figuras de Matplotlib; para los planos, la ecuación a·p = bᵢ.
"""

import os
import unittest
from fractions import Fraction as F

from algebra.espectral import radio_espectral
from algebra.iterativos import (
    ConfiguracionIterativa,
    comparar_metodos,
    configuraciones_homogeneas,
    ejecutar,
)
from algebra.minimos import ajuste_lineal
from algebra.modulo_I_sistemas.directos import resolver_gauss
from algebra.precondicionamiento import analizar_precondicionador
from interfaz import navegacion as nav
from visualizacion import graficos, interactivas
from visualizacion.geometria_3d import _centro_y_radio, _esquinas_plano

S = [[10, -1, 2], [-1, 11, -1], [2, -1, 10]]
B = [6, 25, -11]


def trazas(fig, nombre_contiene):
    return [t for t in fig.data if t.name and nombre_contiene in t.name]


class TestDatosIdenticos(unittest.TestCase):

    def test_convergencia_igual_al_historial_y_a_matplotlib(self):
        r = ejecutar(S, B, ConfiguracionIterativa())
        fig = interactivas.convergencia(r.historial, "A", 1e-3)
        d = trazas(fig, "d_k")[0]
        rk = trazas(fig, "r_k")[0]
        self.assertEqual(list(d.x), [f.k for f in r.historial if f.d is not None])
        self.assertEqual(list(d.y), [f.d for f in r.historial if f.d is not None])
        self.assertEqual(list(rk.y), [f.r for f in r.historial])
        estatica = graficos.grafica_convergencia(r.historial, "A", 1e-3)
        linea_d = estatica.axes[0].lines[0].get_xydata()
        self.assertEqual([tuple(p) for p in linea_d], list(zip(d.x, d.y)))
        graficos.cerrar(estatica)
        # el eje es logarítmico y la línea ε está en su lugar
        self.assertEqual(fig.layout.yaxis.type, "log")
        self.assertEqual(fig.layout.shapes[0].y0, 1e-3)

    def test_comparacion_un_trazo_por_metodo_con_sus_datos(self):
        comp = comparar_metodos(S, B, configuraciones_homogeneas())
        for metrica in ("d", "r", "e"):
            fig = interactivas.comparacion(comp.resultados, metrica, comp.errores_historial)
            self.assertEqual(len(fig.data), 3)
            for traza, r, e in zip(fig.data, comp.resultados, comp.errores_historial):
                esperados = {"d": [f.d for f in r.historial], "r": [f.r for f in r.historial], "e": e}[metrica]
                pares = [(f.k, v) for f, v in zip(r.historial, esperados) if v is not None and v > 0]
                self.assertEqual(list(zip(traza.x, traza.y)), pares)
        # color fijo por método, el mismo que en las figuras estáticas
        self.assertEqual([t.line.color for t in fig.data],
                         [graficos.COLORES[m] for m in ("Jacobi", "Gauss-Seidel", "SOR")])

    def test_autovalores(self):
        esp = radio_espectral([[3, 3, 3], [3, 3, 2], [-3, -2, 3]], [9, 9, -2], "Jacobi")
        fig = interactivas.autovalores(esp.autovalores, esp.rho)
        puntos = trazas(fig, "Autovalores")[0]
        self.assertEqual(list(puntos.x), [z.real for z in esp.autovalores])
        self.assertEqual(list(puntos.y), [z.imag for z in esp.autovalores])
        self.assertEqual(list(puntos.customdata), [abs(z) for z in esp.autovalores])

    def test_planos_satisfacen_su_ecuacion_y_la_solucion_es_la_del_nucleo(self):
        A = [[1, 1, 1], [2, 1, -1], [-1, 1, 2]]
        b = [6, 3, 7]
        r = resolver_gauss(A, b)
        fig = interactivas.planos_3d(A, b, r)
        superficies = [t for t in fig.data if t.type == "surface"]
        self.assertEqual(len(superficies), 3)
        centro, radio = _centro_y_radio(r)
        for i, s in enumerate(superficies):
            esquinas = _esquinas_plano([float(v) for v in A[i]], float(b[i]), centro, radio)
            dibujadas = [(s.x[f][c], s.y[f][c], s.z[f][c]) for f, c in ((0, 0), (0, 1), (1, 1), (1, 0))]
            self.assertEqual(dibujadas, esquinas)                    # mismas esquinas que la figura estática
            for p in dibujadas:                                      # cada esquina está en su plano
                self.assertAlmostEqual(sum(a * x for a, x in zip(A[i], p)), b[i], places=9)
        punto = [t for t in fig.data if t.type == "scatter3d"][0]
        self.assertEqual((punto.x[0], punto.y[0], punto.z[0]), tuple(float(v) for v in r.solucion))
        self.assertEqual(fig.layout.scene.aspectmode, "cube")       # escala igual en los 3 ejes
        self.assertEqual(list(fig.layout.scene.xaxis.range), [centro[0] - radio, centro[0] + radio])

    def test_recta_de_soluciones_cuando_hay_infinitas(self):
        A = [[1, 1, 1], [2, 2, 2], [1, -1, 0]]
        r = resolver_gauss(A, [1, 2, 0])
        fig = interactivas.planos_3d(A, [1, 2, 0], r)
        recta = [t for t in fig.data if t.type == "scatter3d"][0]
        self.assertEqual(recta.name, "Recta de soluciones")
        # los extremos están en todos los planos (A·p = b)
        for k in range(2):
            p = (recta.x[k], recta.y[k], recta.z[k])
            for fila, bi in zip(A, [1, 2, 0]):
                self.assertAlmostEqual(sum(a * x for a, x in zip(fila, p)), bi, places=9)

    def test_ajuste(self):
        r = ajuste_lineal([1, 2, 3, 4], [2, 2.5, 3.7, 4.1])
        fig = interactivas.ajuste(r.xs, r.ys, r.pendiente, r.intercepto, r.minimos.estimados)
        datos = trazas(fig, "Datos")[0]
        self.assertEqual(list(datos.x), [1.0, 2.0, 3.0, 4.0])
        self.assertEqual(list(datos.y), [2.0, 2.5, 3.7, 4.1])
        recta = trazas(fig, "Recta")[0]
        m, c = float(r.pendiente), float(r.intercepto)
        for x, y in zip(recta.x, recta.y):
            self.assertAlmostEqual(y, m * x + c, places=12)

    def test_precondicionador_vista_acotada_pero_datos_completos(self):
        A = [[4, -1, 0, 0], [-1, 4, -1, 0], [0, -1, 4, -1], [0, 0, -1, 4]]
        r = analizar_precondicionador(A, [1, 0, 0, 1], ConfiguracionIterativa(tolerancia=1e-4, k_max=60))
        fig = interactivas.precondicionador(r.comparaciones)
        rich = trazas(fig, "Richardson (original)")[0]
        historial = [f for f in r.comparaciones if f.metodo == "Richardson"][0].original.historial
        self.assertEqual(list(rich.y), [f.d for f in historial if f.d is not None and f.d > 0])
        self.assertGreater(max(rich.y), interactivas.TOPE_GRAFICA)    # el dato divergente está entero
        self.assertEqual(fig.layout.yaxis.range[1], 6.0)               # solo la vista inicial se acota


@unittest.skipIf(os.environ.get("SIN_APPTEST"), "AppTest desactivado")
class TestGraficasEnLaAplicacion(unittest.TestCase):

    def test_los_modulos_muestran_graficas_plotly(self):
        try:
            from streamlit.testing.v1 import AppTest
        except ImportError:  # pragma: no cover
            self.skipTest("Streamlit no está instalado")
        ruta = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "app.py")
        at = AppTest.from_file(ruta, default_timeout=60)
        at.run()
        at.switch_page(nav.ITERATIVOS)
        at.run()
        at.button(key="it_ejecutar").click()
        at.run()
        self.assertFalse(at.exception, at.exception)
        graficas = at.get("plotly_chart")
        self.assertEqual(len(graficas), 1)
        self.assertIn("d_k", graficas[0].proto.spec)


if __name__ == "__main__":
    unittest.main()
