"""La mano como datos: 21 puntos normalizados que entrega MediaPipe Hand Landmarker.

Coordenadas (documentación de MediaPipe): x e y en [0, 1] respecto al ancho y alto de
la imagen (y crece hacia abajo); z es la profundidad relativa a la muñeca.  La imagen
se procesa ya volteada en espejo, así que mover la mano a la derecha aumenta x.
"""

import math
from dataclasses import dataclass

# Índices de los 21 puntos (modelo de MediaPipe).
MUNECA = 0
PULGAR = (1, 2, 3, 4)       # CMC, MCP, IP, punta
INDICE = (5, 6, 7, 8)       # MCP, PIP, DIP, punta
MEDIO = (9, 10, 11, 12)
ANULAR = (13, 14, 15, 16)
MENIQUE = (17, 18, 19, 20)
DEDOS = {"indice": INDICE, "medio": MEDIO, "anular": ANULAR, "menique": MENIQUE}



@dataclass(frozen=True)
class Punto:
    x: float
    y: float
    z: float = 0.0


@dataclass(frozen=True)
class Mano:
    puntos: tuple          # 21 objetos Punto
    lado: str = ""         # "Left"/"Right" según MediaPipe (informativo; el control no depende de él)

    def __post_init__(self):
        if len(self.puntos) != 21:
            raise ValueError(f"Una mano tiene 21 puntos; se recibieron {len(self.puntos)}.")

    def __getitem__(self, i):
        return self.puntos[i]


def distancia(p, q):
    """Distancia en el plano de la imagen (x, y), la que ve la cámara."""
    return math.hypot(p.x - q.x, p.y - q.y)


def tamano_palma(mano):
    """Muñeca → nudillo del dedo medio.  Sirve de unidad para que los umbrales no
    dependan de lo lejos que esté la mano de la cámara."""
    return max(distancia(mano[MUNECA], mano[MEDIO[0]]), 1e-6)


def punto_medio(p, q):
    return Punto((p.x + q.x) / 2, (p.y + q.y) / 2, (p.z + q.z) / 2)
