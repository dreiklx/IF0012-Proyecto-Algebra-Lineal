"""Detección de manos con MediaPipe Tasks (Hand Landmarker), en este equipo.

Se usa la API Tasks porque desde mediapipe 0.10.22 el paquete ya no trae la API antigua
`mp.solutions` (lo comprobó el chat del equipo; ver docs/revision_chat_mediapipe.md).
Modelo: hand_landmarker.task (float16, Apache-2.0), incluido en gestos/modelos/.
"""

import cv2
import mediapipe as mp
from mediapipe.tasks.python import BaseOptions, vision

from gestos import RUTA_MODELO
from gestos.mano import Mano, Punto


class DetectorManos:
    """Modo VIDEO: entre fotogramas MediaPipe sigue la mano ya encontrada y solo vuelve a
    buscar la palma cuando la pierde (más rápido que detectar cada imagen desde cero)."""

    def __init__(self, ruta_modelo=RUTA_MODELO, max_manos=2, confianza=0.5):
        opciones = vision.HandLandmarkerOptions(
            base_options=BaseOptions(model_asset_path=ruta_modelo),
            running_mode=vision.RunningMode.VIDEO,
            num_hands=max_manos,
            min_hand_detection_confidence=confianza,
            min_hand_presence_confidence=confianza,
            min_tracking_confidence=confianza)
        self._detector = vision.HandLandmarker.create_from_options(opciones)
        self._ultimo_ms = -1

    def detectar(self, fotograma_bgr, t_ms):
        """Lista de Mano.  t_ms debe crecer estrictamente (lo exige el modo VIDEO)."""
        t_ms = max(int(t_ms), self._ultimo_ms + 1)
        self._ultimo_ms = t_ms
        rgb = cv2.cvtColor(fotograma_bgr, cv2.COLOR_BGR2RGB)
        resultado = self._detector.detect_for_video(mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb), t_ms)
        manos = []
        for i, puntos in enumerate(resultado.hand_landmarks):
            lado = resultado.handedness[i][0].category_name if i < len(resultado.handedness) else ""
            manos.append(Mano(tuple(Punto(p.x, p.y, p.z) for p in puntos), lado))
        return manos

    def cerrar(self):
        self._detector.close()
