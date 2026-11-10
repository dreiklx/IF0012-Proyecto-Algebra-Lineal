"""Raíz del proyecto para las pruebas (no depende de la carpeta donde esté cada prueba)."""

import os

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RUTA_APP = os.path.join(RAIZ, "app.py")
