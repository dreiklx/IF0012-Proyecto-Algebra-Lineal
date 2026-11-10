"""Pruebas del editor interactivo de matrices, vectores y puntos (interfaz/editor.py).

  * Funciones puras: normalización de separadores, conversión texto <-> celdas,
    celdas vacías y redimensionado (resultados construidos a mano).
  * Interacción real con AppTest: editar una celda, botones de filas y columnas,
    identidad, pegado con comas, dimensiones incompatibles (botón bloqueado) y
    la tabla de puntos del Módulo III.  Los valores esperados del cálculo se
    obtienen a mano: no dependen de la interfaz.
"""

import os
import unittest
from fractions import Fraction as F

try:
    from streamlit.testing.v1 import AppTest
except ImportError:  # pragma: no cover
    AppTest = None

from interfaz import navegacion as nav
from interfaz.compartido.editor import (
    PUNTOS,
    VECTOR,
    analizar,
    celdas_de_texto,
    celdas_vacias,
    normalizar,
    problema_dimensiones,
    redimensionar,
    texto_de_celdas,
)

RUTA_APP = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "app.py")


class TestConversion(unittest.TestCase):

    def test_separadores(self):
        self.assertEqual(normalizar("4, -1, 1\n-2;6;1\n1\t1\t5"), "4 -1 1\n-2 6 1\n1 1 5")
        self.assertEqual(normalizar("[1, 2]\n[3, 4]"), "1 2\n3 4")
        # la coma sin espacio es decimal y se conserva; también fracciones y notación científica
        self.assertEqual(normalizar("2,5 1/3 1e-3 -0.25"), "2,5 1/3 1e-3 -0.25")

    def test_ida_y_vuelta(self):
        texto = "1 2 3\n4 5 6"
        self.assertEqual(texto_de_celdas(celdas_de_texto(texto)), texto)

    def test_celdas_vacias_se_marcan(self):
        celdas = [["1", ""], ["", "4"]]
        self.assertEqual(texto_de_celdas(celdas), "1 ?\n? 4")
        self.assertEqual(celdas_vacias(celdas_de_texto("1 ?\n? 4")), [(1, 2), (2, 1)])

    def test_filas_desiguales_se_rellenan(self):
        self.assertEqual(celdas_de_texto("1 2 3\n4"), [["1", "2", "3"], ["4", "", ""]])

    def test_redimensionar(self):
        self.assertEqual(redimensionar([["1", "2"], ["3", "4"]], 3, 1), [["1"], ["3"], [""]])

    def test_analizar(self):
        valor, mensaje, estado = analizar("1 2\n3 4", "matriz", "matriz A")
        self.assertEqual((estado, len(valor)), ("ok", 2))
        self.assertIn("2×2", mensaje)
        _, mensaje, estado = analizar("1 ?\n3 4", "matriz", "matriz A")
        self.assertEqual(estado, "aviso")
        self.assertIn("(1, 2)", mensaje)
        _, mensaje, estado = analizar("1 2\n3 x", "matriz", "matriz A")
        self.assertEqual(estado, "error")
        self.assertIn("(2, 2)", mensaje)          # posición exacta, del lector del núcleo
        _, mensaje, estado = analizar("1 2 3", PUNTOS, "tabla de puntos")
        self.assertEqual(estado, "error")
        valor, _, estado = analizar("6\n3\n7", VECTOR, "vector b")
        self.assertEqual((estado, len(valor)), ("ok", 3))

    def test_problema_dimensiones(self):
        A3 = [[1, 2, 3]] * 3
        self.assertIsNone(problema_dimensiones(A3, [1, 2, 3], cuadrada=True))
        self.assertIn("b debe tener 3", problema_dimensiones(A3, [1, 2]))
        self.assertIn("cuadrada", problema_dimensiones([[1, 2]] * 3, [1, 2, 3], cuadrada=True))
        # una matriz rectangular es válida si el método lo permite (Módulos I y III)
        self.assertIsNone(problema_dimensiones([[1, 2]] * 3, [1, 2, 3]))
        self.assertIn("x⁽⁰⁾", problema_dimensiones(A3, [1, 2, 3], cuadrada=True, x0=[0, 0]))


class TestEditorNoAlteraLosDatos(unittest.TestCase):
    """Auditoría del editor: para TODOS los ejemplos precargados, pasar por la rejilla
    (texto -> celdas -> texto) produce exactamente la misma matriz o vector que leer el
    texto original: mismos valores exactos, dimensiones, orden, decimales y signos."""

    def misma_lectura(self, texto, vector=False):
        from algebra.compartido.validacion import leer_matriz, leer_vector
        leer = leer_vector if vector else leer_matriz
        original = leer(texto)
        por_editor = leer(normalizar(texto_de_celdas(celdas_de_texto(texto))))
        self.assertEqual(por_editor, original)
        return original

    def test_todos_los_ejemplos(self):
        from interfaz.compartido import ejemplos
        for A, b in ejemplos.DIRECTOS.values():
            self.misma_lectura(A)
            self.misma_lectura(b.replace(" ", "\n"), vector=True)
        for A, b, _ in ejemplos.CONDICION.values():
            self.misma_lectura(A)
            self.misma_lectura(b.replace(" ", "\n"), vector=True)
        for A, b in ejemplos.MINIMOS.values():
            M = self.misma_lectura(A)
            self.assertGreater(len(M), len(M[0]))                   # rectangulares se conservan
        for x, y in ejemplos.AJUSTE.values():
            pares = "\n".join(f"{a} {c}" for a, c in zip(x.split(), y.split()))
            P = self.misma_lectura(pares)
            self.assertEqual([p[0] for p in P], [F(v) for v in x.split()])
            self.assertEqual([p[1] for p in P], [F(v) for v in y.split()])
        for A, b in ejemplos.ITERATIVOS.values():
            self.misma_lectura(A)
            self.misma_lectura(b.replace(" ", "\n"), vector=True)

    def test_decimales_signos_y_formatos(self):
        M = self.misma_lectura("-2.5 0 1/3\n1e-3 -0,25 7")
        self.assertEqual(M, [[F(-5, 2), F(0), F(1, 3)], [F(1, 1000), F(-1, 4), F(7)]])
        # pegar con comas o tabulaciones da la misma matriz que con espacios
        from algebra.compartido.validacion import leer_matriz
        self.assertEqual(leer_matriz(normalizar("4, -1, 1\n-2,\t6, 1")), [[4, -1, 1], [-2, 6, 1]])


@unittest.skipIf(AppTest is None, "Streamlit no está instalado en este intérprete")
class TestEditorEnLaAplicacion(unittest.TestCase):

    def abrir(self, pagina):
        at = AppTest.from_file(RUTA_APP, default_timeout=60)
        at.run()
        at.switch_page(pagina)
        at.run()
        self.assertFalse(at.exception, at.exception)
        return at

    def test_editar_celda_actualiza_el_texto_y_el_calculo(self):
        at = self.abrir(nav.SISTEMAS)
        nombre = at.selectbox(key="dir_ejemplo").value      # A = [[1,1,1],[2,1,-1],[-1,1,2]]
        clave = f"dir_A_{nombre}"
        at.text_input(key=f"{clave}__c0_0").input("2")      # a11: 1 -> 2
        at.run()
        self.assertEqual(at.text_area(key=clave).value, "2 1 1\n2 1 -1\n-1 1 2")
        at.button(key="dir_resolver").click()
        at.run()
        # det de [[2,1,1],[2,1,-1],[-1,1,2]] por Sarrus: 4+1+2-(-1)-(-2)-4 = 6  (a mano)
        self.assertIn("Solución única", " ".join(str(s.value) for s in at.success))
        self.assertIn("6", " ".join(str(m.value) for m in at.metric))

    def test_botones_de_filas_columnas_identidad_y_restaurar(self):
        at = self.abrir(nav.SISTEMAS)
        clave = f"dir_A_{at.selectbox(key='dir_ejemplo').value}"
        at.button(key=f"{clave}__mas_col").click()
        at.run()
        self.assertEqual(at.text_area(key=clave).value.splitlines()[0], "1 1 1 ?")
        at.button(key=f"{clave}__menos_col").click()
        at.button(key=f"{clave}__mas_fila").click()
        at.run()
        self.assertEqual(len(at.text_area(key=clave).value.splitlines()), 4)
        at.button(key=f"{clave}__identidad").click()
        at.run()
        filas = at.text_area(key=clave).value.splitlines()
        self.assertEqual(len(filas), 4)                       # identidad 4×4 (4 filas actuales)
        self.assertEqual([f.split() for f in filas],
                         [["1", "0", "0", "0"], ["0", "1", "0", "0"], ["0", "0", "1", "0"], ["0", "0", "0", "1"]])
        at.button(key=f"{clave}__restaurar").click()
        at.run()
        self.assertEqual(at.text_area(key=clave).value, "1 1 1\n2 1 -1\n-1 1 2")

    def test_pegar_con_comas(self):
        at = self.abrir(nav.SISTEMAS)
        nombre = at.selectbox(key="dir_ejemplo").value
        at.text_area(key=f"dir_A_{nombre}").input("4, -1, 1\n-2, 6, 1\n1, 1, 5")
        at.run()
        # la rejilla se reconstruye con los valores pegados
        self.assertEqual(at.text_input(key=f"dir_A_{nombre}__c1_1").value, "6")
        at.button(key="dir_resolver").click()
        at.run()
        self.assertFalse(at.exception, at.exception)
        self.assertIn("Solución única", " ".join(str(s.value) for s in at.success))

    def test_dimensiones_incompatibles_bloquean_el_calculo(self):
        at = self.abrir(nav.SISTEMAS)
        nombre = at.selectbox(key="dir_ejemplo").value
        at.text_area(key=f"dir_b_{nombre}").input("6\n3")
        at.run()
        self.assertTrue(at.button(key="dir_resolver").disabled)
        self.assertIn("b debe tener 3", " ".join(str(e.value) for e in at.error))

    def test_modulo_IV_exige_matriz_cuadrada_y_x0_compatible(self):
        at = self.abrir(nav.ITERATIVOS)
        nombre = at.selectbox(key="it_ejemplo").value
        at.text_area(key=f"it_A_{nombre}").input("10 -1\n-1 11\n2 -1")
        at.run()
        self.assertTrue(at.button(key="it_ejecutar").disabled)
        self.assertIn("cuadrada", " ".join(str(e.value) for e in at.error))
        at.text_area(key=f"it_A_{nombre}").input("10 -1 2\n-1 11 -1\n2 -1 10")
        at.radio(key="it_x0_tipo").set_value("Personalizado")
        at.run()
        self.assertFalse(at.button(key="it_ejecutar").disabled)
        at.text_area(key=f"it_x0_{nombre}").input("0\n0")
        at.run()
        self.assertTrue(at.button(key="it_ejecutar").disabled)
        at.text_area(key=f"it_x0_{nombre}").input("0\n0\n0")
        at.run()
        at.button(key="it_ejecutar").click()
        at.run()
        self.assertIn("Criterio satisfecho: d_7", " ".join(str(s.value) for s in at.success))

    def test_tabla_de_puntos_modulo_III(self):
        at = self.abrir(nav.MINIMOS)
        nombre = at.selectbox(key="aj_ejemplo").value       # (1,2) (2,2.5) (3,3.7) (4,4.1)
        clave = f"aj_xy_{nombre}"
        self.assertEqual(at.text_area(key=clave).value, "1 2\n2 2.5\n3 3.7\n4 4.1")
        at.button(key=f"{clave}__menos_fila").click()        # quedan 3 puntos
        at.run()
        at.button(key="aj_calcular").click()
        at.run()
        # Puntos (1,2), (2,2.5), (3,3.7): Σx=6, Σy=8.2, Σx²=14, Σxy=18.1, k=3
        # m = (3·18.1 − 6·8.2)/(3·14 − 36) = 5.1/6 = 17/20;  c = (8.2 − 6·17/20)/3 = 31/30  (a mano)
        self.assertIn("y = 17/20 x + 31/30", " ".join(str(s.value) for s in at.success))


if __name__ == "__main__":
    unittest.main()
