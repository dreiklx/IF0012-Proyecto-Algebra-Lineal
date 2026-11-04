"""Aplicación integrada del proyecto final IF0012 — Álgebra Lineal (II Ciclo 2026).

Ejecutar con:   streamlit run app.py      (o con ejecutar.bat en Windows)

La aplicación es una sola interfaz con los cuatro módulos del enunciado
(OFICIAL p. 2).  Todos los cálculos se hacen en el paquete `algebra`
(implementado desde cero); este archivo solo organiza la navegación: una barra
superior con una página por módulo (interfaz/navegacion.py, carpeta paginas/).
"""

import os

import streamlit as st

from interfaz.estilo import aplicar_estilo
from interfaz.navegacion import INICIO, PAGINAS

RAIZ = os.path.dirname(os.path.abspath(__file__))

st.set_page_config(page_title="Ax · Álgebra Lineal", page_icon="🧮", layout="wide")
aplicar_estilo()
st.logo(os.path.join(RAIZ, "interfaz", "recursos", "marca.svg"), size="large")

paginas = [st.Page(archivo, title=titulo, url_path=ruta, default=archivo == INICIO)
           for archivo, titulo, ruta in PAGINAS]
st.navigation(paginas, position="top").run()
