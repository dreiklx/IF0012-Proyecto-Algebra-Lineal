"""Navegación 2D de una gráfica cartesiana (Módulo IV) a partir de los gestos.

Es el equivalente 2D de `movimiento.CamaraOrbital`: tiene la misma interfaz (girar, zoom,
restablecer, a_plotly, desde_plotly) para que `ControlGestual` la use sin cambios, pero
solo modifica el RANGO VISIBLE de los ejes de Plotly.  No conoce datos, historiales ni
errores; no importa algebra/.

Coordenadas: los rangos se expresan en las unidades de Plotly (si un eje es logarítmico,
el rango es log10 del valor).  Así el desplazamiento y el zoom son lineales en el espacio
en que Plotly dibuja el eje.

Convención de gestos (igual que en 3D):
  pinza que se mueve a la derecha → el contenido sigue a la mano (el rango X se desplaza a la izquierda)
  pinza que se mueve hacia abajo  → el contenido baja (el rango Y sube)
  dos manos que se separan (factor > 1) → acercar (el rango se reduce)
"""

import math

ZONA_MUERTA = 0.004       # desplazamiento acumulado mínimo (fracción de la imagen) para mover
ZOOM_MINIMO = 0.01        # factores con |f − 1| menor que esto se ignoran (temblor)
ESCALA_MIN, ESCALA_MAX = 0.05, 4.0   # el ancho visible no baja de 5 % ni sube de 400 % del inicial


class VistaPlano2D:
    """Rango visible de X e Y con límites de zoom respecto al rango inicial."""

    def __init__(self, x0, x1, y0, y1):
        self._inicial = self._validar(x0, x1, y0, y1)
        self._pendiente = (0.0, 0.0)
        self.restablecer()

    @staticmethod
    def _validar(x0, x1, y0, y1):
        valores = [float(v) for v in (x0, x1, y0, y1)]
        if not all(math.isfinite(v) for v in valores) or x1 <= x0 or y1 <= y0:
            raise ValueError("El rango inicial debe ser finito y con máximo mayor que mínimo.")
        return tuple(valores)

    def restablecer(self):
        self.x0, self.x1, self.y0, self.y1 = self._inicial
        self._pendiente = (0.0, 0.0)

    @property
    def ancho_inicial(self):
        return self._inicial[1] - self._inicial[0]

    @property
    def alto_inicial(self):
        return self._inicial[3] - self._inicial[2]

    def girar(self, dx, dy):
        """dx, dy: desplazamiento de la mano en coordenadas normalizadas de la imagen (y hacia
        abajo), igual que CamaraOrbital.girar.  Devuelve True si el rango cambió."""
        dx, dy = self._pendiente[0] + dx, self._pendiente[1] + dy
        if math.hypot(dx, dy) < ZONA_MUERTA:
            self._pendiente = (dx, dy)
            return False
        self._pendiente = (0.0, 0.0)
        ancho, alto = self.x1 - self.x0, self.y1 - self.y0
        self.x0, self.x1 = self.x0 - dx * ancho, self.x1 - dx * ancho
        self.y0, self.y1 = self.y0 + dy * alto, self.y1 + dy * alto
        return True

    def zoom(self, factor):
        """factor > 1 acerca (las manos se separan); factor < 1 aleja."""
        if factor <= 0 or abs(factor - 1) < ZOOM_MINIMO:
            return False
        cx, cy = (self.x0 + self.x1) / 2, (self.y0 + self.y1) / 2
        mitad_x = (self.x1 - self.x0) / 2 / factor
        mitad_y = (self.y1 - self.y0) / 2 / factor
        mitad_x = min(max(mitad_x, self.ancho_inicial * ESCALA_MIN / 2),
                      self.ancho_inicial * ESCALA_MAX / 2)
        mitad_y = min(max(mitad_y, self.alto_inicial * ESCALA_MIN / 2),
                      self.alto_inicial * ESCALA_MAX / 2)
        self.x0, self.x1 = cx - mitad_x, cx + mitad_x
        self.y0, self.y1 = cy - mitad_y, cy + mitad_y
        return True

    def desde_plotly(self, camara):
        """Toma el rango que dejó el ratón.  Plotly envía solo los extremos que cambiaron
        («xaxis.range[0]», «yaxis.range[1]», …): los que faltan se conservan."""
        if not isinstance(camara, dict):
            return False
        actual = {"x0": self.x0, "x1": self.x1, "y0": self.y0, "y1": self.y1}
        try:
            for eje in ("x", "y"):
                if f"{eje}axis.range" in camara:
                    lo, hi = camara[f"{eje}axis.range"]
                    actual[eje + "0"], actual[eje + "1"] = float(lo), float(hi)
                for i in (0, 1):
                    clave = f"{eje}axis.range[{i}]"
                    if clave in camara:
                        actual[f"{eje}{i}"] = float(camara[clave])
            valores = self._validar(actual["x0"], actual["x1"], actual["y0"], actual["y1"])
        except (TypeError, ValueError):
            return False
        self.x0, self.x1, self.y0, self.y1 = valores
        return True

    def a_plotly(self):
        """Argumentos de Plotly.relayout para aplicar el rango actual."""
        return {"xaxis.range": [self.x0, self.x1], "yaxis.range": [self.y0, self.y1]}


def rango_inicial(historial, tolerancia=None):
    """Rango por defecto de la gráfica de convergencia (Plotly units).  X: iteraciones con
    un margen; Y: log10 de los valores positivos de d_k y r_k (y de ε si se usa)."""
    ks = [f.k for f in historial] or [0]
    valores = [v for f in historial for v in (f.d, f.r) if v is not None and v > 0]
    if tolerancia and tolerancia > 0:
        valores.append(float(tolerancia))
    if valores:
        lo, hi = math.log10(min(valores)), math.log10(max(valores))
    else:
        lo, hi = -6.0, 1.0
    if hi - lo < 1:
        lo, hi = lo - 0.5, hi + 0.5
    margen = 0.15 * (hi - lo)
    return (min(ks) - 0.5, max(ks) + 0.5, lo - margen, hi + margen)
