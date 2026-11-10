"""Manos de prueba: 21 puntos construidos a mano (sin imágenes ni cámara).

Geometría en «unidades de palma» (muñeca → nudillo medio = 1), con los dedos hacia arriba
(y negativa, porque en la imagen y crece hacia abajo).  Luego se escala y se traslada.
"""

from gestos.mano import Mano, Punto

_BASES = {"indice": -0.3, "medio": 0.0, "anular": 0.3, "menique": 0.55}
_EXTENDIDO = (-1.0, -1.45, -1.75, -2.05)       # y de MCP, PIP, DIP, punta
_DOBLADO = (-1.0, -1.3, -1.05, -0.8)            # la punta vuelve hacia la palma
_PULGAR_ABIERTO = ((-0.35, -0.3), (-0.65, -0.55), (-0.9, -0.8), (-1.1, -1.05))


def construir(dedos_extendidos=("indice", "medio", "anular", "menique"), pinza=False,
              cx=0.5, cy=0.7, escala=0.12, lado="Right"):
    puntos = [None] * 21
    puntos[0] = (0.0, 0.0)
    pulgar = list(_PULGAR_ABIERTO)
    for k, (nombre, x) in enumerate(_BASES.items()):
        ys = _EXTENDIDO if nombre in dedos_extendidos else _DOBLADO
        for j in range(4):
            puntos[5 + 4 * k + j] = (x, ys[j])
    if pinza:
        # índice algo curvado y pulgar tocando su punta
        puntos[6], puntos[7], puntos[8] = (-0.32, -1.4), (-0.34, -1.6), (-0.36, -1.62)
        pulgar[2], pulgar[3] = (-0.6, -1.3), (-0.4, -1.6)
    elif not dedos_extendidos:
        pulgar[2], pulgar[3] = (-0.4, -0.75), (-0.2, -0.85)      # pulgar cruzado (puño)
    for j in range(4):
        puntos[1 + j] = pulgar[j]
    return Mano(tuple(Punto(cx + escala * x, cy + escala * y) for x, y in puntos), lado)


def palma(**kw):
    return construir(**kw)


def puno(**kw):
    return construir(dedos_extendidos=(), **kw)


def victoria(**kw):
    return construir(dedos_extendidos=("indice", "medio"), **kw)


def pinza(**kw):
    return construir(dedos_extendidos=("medio", "anular", "menique"), pinza=True, **kw)
