"""De movimiento de la mano a cámara 3D: suavizado, zona muerta y cámara orbital con límites.

La cámara de Plotly se describe con `eye` (posición del ojo), `center` y `up`.  Aquí se
usa una cámara ORBITAL en coordenadas esféricas alrededor de center = (0, 0, 0):

    eye = r · (cos φ · cos θ,  cos φ · sin θ,  sin φ)

  θ (azimut)    gira alrededor del eje z         → movimiento horizontal de la pinza
  φ (elevación) sube o baja la mirada           → movimiento vertical de la pinza
  r (distancia) acerca o aleja                   → separar o juntar las dos manos

Con up = (0, 0, 1) fijo y φ limitado a (−80°, 85°) la vista nunca se voltea.
"""

import math
from dataclasses import dataclass, field

EYE_INICIAL = (1.55, -1.55, 1.05)        # la misma vista inicial de visualizacion/interactivas.py
ELEVACION_MIN, ELEVACION_MAX = math.radians(-80), math.radians(85)
DISTANCIA_MIN, DISTANCIA_MAX = 0.9, 5.0


class Suavizador:
    """Media móvil exponencial: s ← s + α·(x − s).  α cerca de 1 sigue rápido a la mano;
    α pequeño elimina el temblor pero agrega retraso."""

    def __init__(self, alfa=0.35):
        if not 0 < alfa <= 1:
            raise ValueError("α debe estar en (0, 1].")
        self.alfa = alfa
        self.valor = None

    def actualizar(self, x, y):
        if self.valor is None:
            self.valor = (x, y)
        else:
            sx, sy = self.valor
            self.valor = (sx + self.alfa * (x - sx), sy + self.alfa * (y - sy))
        return self.valor

    def reiniciar(self):
        self.valor = None


def esfericas(eye):
    x, y, z = eye
    r = math.sqrt(x * x + y * y + z * z)
    return math.atan2(y, x), math.asin(max(-1.0, min(1.0, z / r))), r


@dataclass
class CamaraOrbital:
    """Estado de la cámara: θ, φ, r con límites.  sensibilidad = radianes por unidad de
    desplazamiento normalizado (1 = el ancho completo de la imagen)."""
    sensibilidad: float = math.pi          # cruzar la imagen de lado a lado = media vuelta
    zona_muerta: float = 0.004             # ignora movimientos menores (temblor)
    theta: float = field(init=False)
    phi: float = field(init=False)
    r: float = field(init=False)

    def __post_init__(self):
        self._pendiente = (0.0, 0.0)
        self.restablecer()

    def restablecer(self):
        self.theta, self.phi, self.r = esfericas(EYE_INICIAL)
        self._pendiente = (0.0, 0.0)

    def girar(self, dx, dy):
        """dx, dy: desplazamiento de la mano en coordenadas normalizadas de la imagen
        (y hacia abajo).  Devuelve True si la cámara cambió.

        La zona muerta se aplica al desplazamiento ACUMULADO: el temblor (que va y viene)
        se cancela y no mueve la vista, pero un movimiento lento y sostenido sí llega
        aunque cada fotograma aporte muy poco."""
        dx, dy = self._pendiente[0] + dx, self._pendiente[1] + dy
        if math.hypot(dx, dy) < self.zona_muerta:
            self._pendiente = (dx, dy)
            return False
        self._pendiente = (0.0, 0.0)
        # Mano a la derecha → la escena gira hacia la derecha (el ojo se mueve a la izquierda),
        # como al arrastrar con el ratón.
        # Eje vertical invertido a pedido del equipo (10-nov): mano arriba (dy < 0) → el ojo
        # baja (se mira más desde abajo); mano abajo → se mira más desde arriba.
        self.theta -= dx * self.sensibilidad
        self.phi = min(ELEVACION_MAX, max(ELEVACION_MIN, self.phi + dy * self.sensibilidad))
        return True

    def zoom(self, factor):
        """factor > 1 acerca (manos que se separan); factor < 1 aleja."""
        if factor <= 0 or abs(factor - 1) < 0.01:
            return False
        self.r = min(DISTANCIA_MAX, max(DISTANCIA_MIN, self.r / factor))
        return True

    def desde_plotly(self, camara):
        """Toma la cámara que dejó el ratón, para continuar desde ahí sin saltos."""
        try:
            eye = camara["eye"]
            theta, phi, r = esfericas((float(eye["x"]), float(eye["y"]), float(eye["z"])))
        except (KeyError, TypeError, ValueError, ZeroDivisionError):
            return False
        self.theta = theta
        self.phi = min(ELEVACION_MAX, max(ELEVACION_MIN, phi))
        self.r = min(DISTANCIA_MAX, max(DISTANCIA_MIN, r))
        return True

    def a_plotly(self):
        c = math.cos(self.phi)
        return {"eye": {"x": round(self.r * c * math.cos(self.theta), 5),
                        "y": round(self.r * c * math.sin(self.theta), 5),
                        "z": round(self.r * math.sin(self.phi), 5)},
                "center": {"x": 0, "y": 0, "z": 0},
                "up": {"x": 0, "y": 0, "z": 1}}
