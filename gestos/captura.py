"""Cámara web con OpenCV.  Solo lee fotogramas en memoria: nunca los guarda ni los envía."""

import cv2


class ErrorCamara(RuntimeError):
    """La cámara no se pudo abrir o dejó de entregar imágenes (mensaje para el usuario)."""


MENSAJE_SIN_CAMARA = (
    "No se pudo abrir la cámara. Puede que el equipo no tenga cámara, que otra aplicación "
    "la esté usando (Teams, Zoom, la app Cámara) o que Windows no permita el acceso: "
    "Configuración → Privacidad y seguridad → Cámara → «Permitir que las aplicaciones de "
    "escritorio accedan a la cámara». El ratón sigue funcionando con normalidad.")
MENSAJE_SIN_IMAGEN = (
    "La cámara se abrió pero no entrega imágenes (puede estar bloqueada por la privacidad de "
    "Windows o tapada). El ratón sigue funcionando con normalidad.")


class Camara:
    """cv2.VideoCapture con DirectShow (en Windows abre más rápido y es la opción probada
    en el chat del equipo).  Uso: with Camara() as c: fotograma = c.leer()"""

    def __init__(self, indice=0, ancho=640, alto=480):
        self.indice, self.ancho, self.alto = indice, ancho, alto
        self._cap = None

    def abrir(self):
        cap = cv2.VideoCapture(self.indice, cv2.CAP_DSHOW)
        if not cap.isOpened():
            cap.release()
            raise ErrorCamara(MENSAJE_SIN_CAMARA)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.ancho)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.alto)
        cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)       # siempre el fotograma más reciente
        self._cap = cap
        return self

    def leer(self):
        """Fotograma BGR volteado en espejo (como un espejo, para que el movimiento sea
        natural), o None si no llegó imagen."""
        if self._cap is None:
            return None
        ok, fotograma = self._cap.read()
        if not ok or fotograma is None:
            return None
        return cv2.flip(fotograma, 1)

    def liberar(self):
        if self._cap is not None:
            self._cap.release()
            self._cap = None

    @property
    def abierta(self):
        return self._cap is not None

    def __enter__(self):
        return self.abrir()

    def __exit__(self, *_):
        self.liberar()
