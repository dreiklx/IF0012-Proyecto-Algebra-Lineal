"""Pruebas de integración de la interfaz con streamlit.testing (AppTest).

Ejecutan app.py sin navegador, pulsan botones y comprueban los mensajes que
se muestran.  Se omiten si Streamlit no está instalado (por ejemplo al usar
un Python sin el entorno virtual del proyecto).
"""

import os
import unittest

from interfaz import navegacion as nav
from tests.rutas import RUTA_APP

try:
    from streamlit.testing.v1 import AppTest
except ImportError:  # pragma: no cover
    AppTest = None



def textos(elementos):
    return " | ".join(str(e.value) for e in elementos)


@unittest.skipIf(AppTest is None, "Streamlit no está instalado en este intérprete")
class TestAplicacion(unittest.TestCase):

    def abrir(self, pagina):
        at = AppTest.from_file(RUTA_APP, default_timeout=60)
        at.run()
        self.assertFalse(at.exception, at.exception)
        if pagina:
            at.switch_page(pagina)
            at.run()
            self.assertFalse(at.exception, at.exception)
        return at

    def test_inicio(self):
        at = self.abrir(None)
        self.assertIn("Álgebra Lineal", at.title[0].value)

    def test_modulo_I_unica_infinitas_inconsistente(self):
        at = self.abrir(nav.SISTEMAS)
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
        at = self.abrir(nav.SISTEMAS)
        nombre = at.selectbox(key="dir_ejemplo").value
        at.text_area(key=f"dir_A_{nombre}").input("1 2\n3 x")
        at.button(key="dir_resolver").click()
        at.run()
        self.assertFalse(at.exception)
        self.assertIn("(2, 2)", textos(at.error))

    def test_modulo_II(self):
        at = self.abrir(nav.CONDICIONAMIENTO)
        at.button(key="cond_calcular").click()
        at.run()
        self.assertFalse(at.exception)
        self.assertIn("Sensibilidad baja", textos(at.success))
        self.assertIn("la cota se cumple", textos(at.info))

    def test_modulo_II_singular(self):
        at = self.abrir(nav.CONDICIONAMIENTO)
        nombre = at.selectbox(key="cond_ejemplo").value
        at.text_area(key=f"cond_A_{nombre}").input("1 2\n2 4")
        at.button(key="cond_calcular").click()
        at.run()
        self.assertFalse(at.exception)
        self.assertIn("singular", textos(at.error))

    def test_modulo_III(self):
        at = self.abrir(nav.MINIMOS)
        at.button(key="mc_resolver").click()
        at.button(key="aj_calcular").click()
        at.run()
        self.assertFalse(at.exception)
        self.assertIn("y = 3/4 x + 6/5", textos(at.success))

    def test_modulo_IV_ejecutar_y_comparar(self):
        at = self.abrir(nav.ITERATIVOS)
        at.button(key="it_ejecutar").click()
        at.run()
        self.assertFalse(at.exception)
        self.assertIn("Criterio satisfecho: $d_{7}$", textos(at.success))
        at.button(key="it_comparar").click()
        at.run()
        self.assertFalse(at.exception)
        self.assertIn("Experimento homogéneo", textos(at.success))
        at.button(key="it_conv").click()
        at.run()
        self.assertFalse(at.exception)
        todo = " ".join([textos(at.success), textos(at.warning), textos(at.info), textos(at.error)] + [str(m.value) for m in at.markdown])
        self.assertIn("ρ(T)", todo)

    def test_modulo_IV_criterio_C_y_validacion(self):
        at = self.abrir(nav.ITERATIVOS)
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

    def test_modulo_IV_formato_csr(self):
        at = self.abrir(nav.ITERATIVOS)
        at.checkbox(key="it_csr").check()
        at.button(key="it_ejecutar").click()
        at.run()
        self.assertFalse(at.exception)
        self.assertIn("Formato CSR: nnz = 9", textos(at.info))
        # La estrategia CSR se explica en la aplicación (incentivo «Matrices dispersas»).
        self.assertIn("O(nnz)", " ".join(str(m.value) for m in at.markdown))
        self.assertIn("Criterio satisfecho: $d_{7}$", textos(at.success))

    def test_modulo_IV_precondicionamiento(self):
        at = self.abrir(nav.ITERATIVOS)
        at.button(key="it_prec").click()
        at.run()
        self.assertFalse(at.exception, at.exception)
        texto = textos(at.info)
        self.assertIn("EXACTAMENTE los mismos", texto)
        # Richardson se retiró: ya no aparece en la aplicación.
        self.assertNotIn("Richardson", " ".join(texto + textos(at.warning)))

    def test_modulo_IV_reordenamiento_y_sarrus(self):
        at = self.abrir(nav.ITERATIVOS)
        at.text_area(key=f"it_A_{at.selectbox(key='it_ejemplo').value}").input(
            "-1 4 -1\n0 -1 3\n4 -1 0")
        at.text_area(key=f"it_b_{at.selectbox(key='it_ejemplo').value}").input("10\n10\n15")
        at.button(key="it_conv").click()
        at.run()
        self.assertFalse(at.exception, at.exception)
        # a_33 = 0: no hay matriz de iteración, pero sí la sugerencia de reordenar.
        self.assertIn("Reordenando las ecuaciones", textos(at.info))
        self.assertIn("diagonal nulo", textos(at.error))
        # Con el ejemplo por defecto (3x3) se muestra el desarrollo de Sarrus.
        at = self.abrir(nav.ITERATIVOS)
        at.button(key="it_conv").click()
        at.run()
        self.assertIn("coincide con el polinomio calculado", textos(at.caption))

    def test_modulo_III_verificacion_cramer(self):
        at = self.abrir(nav.MINIMOS)
        at.button(key="mc_resolver").click()
        at.run()
        self.assertFalse(at.exception, at.exception)
        texto = " | ".join(str(m.value) for m in at.markdown)
        self.assertIn(r"$\det[A \mid b]$ = **−11**", texto)       # el valor −11 de la hoja
        self.assertIn("coincide exactamente", texto)

    def test_modulo_IV_jacobi_no_converge(self):
        at = self.abrir(nav.ITERATIVOS)
        at.selectbox(key="it_ejemplo").set_value("S9-07/10 — Jacobi no converge (ρ ≈ 1.174)")
        at.run()
        at.button(key="it_conv").click()
        at.run()
        self.assertFalse(at.exception)
        # S9-07/10 p. 5: el polinomio de Jacobi (grado 3, sin factor λ) no se factoriza con los
        # procedimientos del curso: ρ no se calcula.
        todo = " ".join([textos(at.success), textos(at.warning), textos(at.info), textos(at.error)] + [str(m.value) for m in at.markdown])
        self.assertIn("No se calcula ρ(T)", todo)
        at.button(key="it_ejecutar").click()
        at.run()
        self.assertIn("máximo de iteraciones sin satisfacer", textos(at.warning))


if __name__ == "__main__":
    unittest.main()


@unittest.skipIf(AppTest is None, "Streamlit no está instalado en este intérprete")
class TestComponentes(unittest.TestCase):

    def test_latex_separa_filas_con_fracciones(self):
        from fractions import Fraction
        from interfaz.compartido.formulas import latex_matriz
        con = latex_matriz([[Fraction(65, 33)], [Fraction(-29, 33)]])
        self.assertIn(r"\[6pt]", con)
        self.assertIn(r"\frac{65}{33}", con)
        self.assertIn(r"-\frac{29}{33}", con)
        sin = latex_matriz([[1, 2], [3, 4]])
        self.assertNotIn("6pt", sin)

    def test_csv_exportado_contiene_historial_completo(self):
        import csv
        import io
        from algebra.modulo_IV_iterativos.ejecucion import ConfiguracionIterativa, ejecutar
        from interfaz.modulos.modulo_IV_iterativos.pestana_ejecutar import csv_historial
        r = ejecutar([[10, -1, 2], [-1, 11, -1], [2, -1, 10]], [6, 25, -11],
                     ConfiguracionIterativa())
        filas = list(csv.reader(io.StringIO(csv_historial(r))))
        self.assertTrue(filas[0][0].startswith("# Método: Jacobi"))
        self.assertIn("Criterio satisfecho", filas[1][0])
        self.assertEqual(filas[2], ["k", "x1", "x2", "x3", "d_k", "r_k"])
        datos = filas[3:]
        self.assertEqual(len(datos), len(r.historial))          # k = 0..7
        self.assertEqual(datos[0][4], "")                        # d_0 no existe
        # precisión completa: los valores se pueden reconstruir exactamente
        self.assertEqual([float(v) for v in datos[-1][1:4]], r.x_final)
        self.assertEqual(float(datos[-1][4]), r.d_final)


@unittest.skipIf(AppTest is None, "Streamlit no está instalado en este intérprete")
class TestNavegacion(unittest.TestCase):
    """Navegación superior (st.navigation): una página por módulo, sin barra lateral."""

    def test_registro_de_paginas(self):
        raiz = os.path.dirname(RUTA_APP)
        archivos = [p[0] for p in nav.PAGINAS]
        self.assertEqual(archivos, [nav.INICIO, nav.SISTEMAS, nav.CONDICIONAMIENTO, nav.MINIMOS, nav.ITERATIVOS])
        self.assertEqual(len({p[2] for p in nav.PAGINAS}), 5)              # rutas URL distintas
        for archivo in archivos:
            self.assertTrue(os.path.isfile(os.path.join(raiz, archivo)), archivo)

    def test_cada_pagina_abre_su_modulo_sin_barra_lateral(self):
        at = AppTest.from_file(RUTA_APP, default_timeout=60)
        at.run()
        self.assertEqual(len(at.sidebar.children), 0)                       # la barra lateral queda vacía
        esperados = {nav.SISTEMAS: ("I", "dir_resolver"), nav.CONDICIONAMIENTO: ("II", "cond_calcular"),
                     nav.MINIMOS: ("III", "mc_resolver"), nav.ITERATIVOS: ("IV", "it_ejecutar")}
        for archivo, (numero, boton) in esperados.items():
            at.switch_page(archivo).run()
            self.assertFalse(at.exception, at.exception)
            self.assertIn(f"MÓDULO {numero}</div>", " ".join(m.value for m in at.markdown))
            self.assertIn(boton, [b.key for b in at.button])
            self.assertEqual(len(at.sidebar.children), 0)
        at.switch_page(nav.INICIO).run()
        self.assertIn("Álgebra Lineal", at.title[0].value)

    def test_portada_enlaza_los_cuatro_modulos_y_los_cinco_incentivos(self):
        from interfaz import portada
        at = AppTest.from_file(RUTA_APP, default_timeout=60)
        at.run()
        enlaces = [(e.proto.label, e.proto.page) for e in at.get("page_link")]
        rutas = {archivo: ruta for archivo, _, ruta in nav.PAGINAS}
        self.assertEqual(enlaces[:4], [(f"Abrir el módulo {m[0]}  →", rutas[m[2]]) for m in portada.MODULOS])
        self.assertEqual([e[1] for e in enlaces[4:]], [rutas[i[2]] for i in portada.INCENTIVOS])
        texto = " ".join(m.value for m in at.markdown)
        for nombre in ("Visualización avanzada", "Precondicionamiento", "Matrices dispersas",
                       "Experiencia de usuario", "Extensión matemática"):
            self.assertIn(nombre, texto)

    def test_figura_de_la_portada_es_el_resultado_del_nucleo(self):
        at = AppTest.from_file(RUTA_APP, default_timeout=60)
        at.run()
        texto = " ".join(m.value for m in at.markdown)
        self.assertIn("x = (1/3, 4, 5/3)", texto)                           # solución del ejemplo S6-16/09

