"""Control de la gráfica 3D del Módulo I con gestos de la mano (MediaPipe, en Python).

Este paquete NO forma parte del núcleo matemático: no calcula nada del álgebra.  Solo
convierte lo que ve la cámara en una posición de la cámara 3D de Plotly.

    cámara web ──► captura.py ──► deteccion.py ──► interpretacion.py ──► movimiento.py
    (OpenCV)        fotograma      21 puntos por      gesto y acción       cámara orbital
                                   mano (MediaPipe)   (reglas, histéresis)  (suavizado, límites)
                                                                  │
                                         control.py: hilo de trabajo y estado compartido
                                                                  │
                         servidor.py: envía solo la cámara (6 números) al navegador, 127.0.0.1

Toda la visión ocurre en este equipo.  Los fotogramas no se guardan, no se graban y no
se envían a ningún lado: se procesan en memoria y se descartan.

Los módulos con lógica pura (mano, interpretacion, movimiento) no importan MediaPipe ni
OpenCV, para poder probarlos sin cámara.  `disponible()` dice si las bibliotecas de
visión están instaladas.
"""

import importlib.util
import os

RUTA_MODELO = os.path.join(os.path.dirname(os.path.abspath(__file__)), "modelos", "hand_landmarker.task")


def disponible():
    """(True, "") si MediaPipe, OpenCV y el modelo están presentes; si no, (False, motivo)."""
    faltan = [m for m in ("mediapipe", "cv2") if importlib.util.find_spec(m) is None]
    if faltan:
        return False, ("Faltan bibliotecas: " + ", ".join(faltan)
                       + ". Instale las dependencias con: pip install -r requirements.txt")
    if not os.path.isfile(RUTA_MODELO):
        return False, f"Falta el modelo de MediaPipe: {RUTA_MODELO}"
    return True, ""
