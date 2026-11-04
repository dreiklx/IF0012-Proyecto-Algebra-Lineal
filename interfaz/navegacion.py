"""Registro de páginas de la aplicación (navegación superior con st.navigation).

Cada módulo es una página propia, con su URL (/sistemas, /iterativos, ...).  La
portada y las pruebas usan las mismas rutas de archivo que app.py, por eso están
definidas una sola vez aquí.
"""

INICIO = "paginas/inicio.py"
SISTEMAS = "paginas/sistemas.py"
CONDICIONAMIENTO = "paginas/condicionamiento.py"
MINIMOS = "paginas/minimos.py"
ITERATIVOS = "paginas/iterativos.py"

# (archivo, título en la barra superior, ruta de la URL)
PAGINAS = [
    (INICIO, "Inicio", "inicio"),
    (SISTEMAS, "I · Sistemas lineales", "sistemas"),
    (CONDICIONAMIENTO, "II · Condicionamiento", "condicionamiento"),
    (MINIMOS, "III · Mínimos cuadrados", "minimos"),
    (ITERATIVOS, "IV · Métodos iterativos", "iterativos"),
]
