"""Interpretación de gestos: de 21 puntos por mano a acciones sobre la cámara.

Dos niveles (como en el diseño del chat del equipo: «el transporte lleva puntos crudos y
el significado se construye hacia adentro»):

1. `clasificar(mano)`: reglas geométricas sobre UNA mano en UN fotograma.  Todas las
   distancias se dividen por el tamaño de la palma, así no importa lo lejos que esté la
   mano de la cámara (umbral adaptativo).
2. `InterpreteGestos`: memoria entre fotogramas.  Exige que un gesto se mantenga un
   tiempo mínimo (antirrebote), usa histéresis en la pinza (entra con un umbral y sale
   con otro mayor) y suaviza el punto de agarre.

Gestos y acciones:
    palma abierta (sostenida)   activa el control (y calibra la pinza con esa mano)
    pinza: pulgar + índice       agarrar: mover la mano gira la vista
    pinza con las dos manos      zoom: separarlas acerca, juntarlas aleja
    puño (sostenido)             pausa: la vista deja de seguir la mano
    victoria ✌ (sostenida)       restablece la vista inicial
"""

from dataclasses import dataclass, field

from gestos.mano import DEDOS, INDICE, MUNECA, PULGAR, distancia, punto_medio, tamano_palma
from gestos.movimiento import Suavizador

NINGUNO, PALMA, PUNO, PINZA, VICTORIA = "ninguno", "palma abierta", "puño", "pinza", "victoria"
ESPERANDO, LISTO, GIRANDO, ZOOM, PAUSADO = "esperando palma", "listo", "girando", "zoom", "pausado"

PINZA_ENTRA = 0.25       # |pulgar − índice| / palma por debajo de esto: empieza la pinza
PINZA_SALE = 0.40        # por encima de esto: termina (histéresis: 0,25 < 0,40)
EXTENDIDO = 1.15         # un dedo está extendido si punta–muñeca > 1,15 · articulación–muñeca


def dedo_extendido(mano, dedo):
    _, pip, _, punta = dedo
    return distancia(mano[punta], mano[MUNECA]) > EXTENDIDO * distancia(mano[pip], mano[MUNECA])


def razon_pinza(mano):
    return distancia(mano[PULGAR[3]], mano[INDICE[3]]) / tamano_palma(mano)


def clasificar(mano, umbral_pinza=PINZA_ENTRA):
    """Gesto de una mano en un fotograma (sin memoria)."""
    extendidos = {n: dedo_extendido(mano, d) for n, d in DEDOS.items()}
    n_ext = sum(extendidos.values())
    # La punta del índice lejos de la palma distingue la pinza del puño (en el puño el
    # pulgar también queda cerca del índice).
    indice_afuera = distancia(mano[INDICE[3]], mano[MUNECA]) > 1.05 * distancia(mano[INDICE[0]], mano[MUNECA])
    if razon_pinza(mano) < umbral_pinza and indice_afuera:
        return PINZA
    if extendidos["indice"] and extendidos["medio"] and not extendidos["anular"] and not extendidos["menique"]:
        return VICTORIA
    if n_ext == 4:
        return PALMA
    if n_ext == 0:
        return PUNO
    return NINGUNO


@dataclass
class Resultado:
    estado: str
    gestos: list                      # gesto de cada mano detectada
    acciones: list = field(default_factory=list)   # ("girar", dx, dy) | ("zoom", f) | ("restablecer",)


class InterpreteGestos:
    """Máquina de estados.  `actualizar(manos, t)` con t en segundos."""

    def __init__(self, t_confirmar=0.35, t_victoria=0.8, t_sin_mano=0.5, alfa=0.35):
        self.t_confirmar = t_confirmar
        self.t_victoria = t_victoria
        self.t_sin_mano = t_sin_mano
        self.estado = ESPERANDO
        self.umbral_entra = PINZA_ENTRA
        self.umbral_sale = PINZA_SALE
        self.suave = Suavizador(alfa)
        self._candidato = None          # (gesto, desde_t)
        self._disparado = False         # el gesto sostenido ya produjo su acción
        self._ultima_mano = None
        self._previo = None             # último punto de agarre suavizado
        self._dist_zoom = None

    def calibrar(self, mano):
        """Con la palma abierta mide la separación natural pulgar–índice de ESTA mano y
        ajusta los umbrales de la pinza (umbral adaptativo), dentro de límites seguros."""
        abierta = razon_pinza(mano)
        self.umbral_entra = min(PINZA_ENTRA, max(0.18, 0.35 * abierta))
        self.umbral_sale = self.umbral_entra * 1.5

    def _sostenido(self, gesto, t, duracion):
        """True una sola vez cuando `gesto` lleva `duracion` segundos seguidos."""
        if self._candidato is None or self._candidato[0] != gesto:
            self._candidato = (gesto, t)
            self._disparado = False
            return False
        if not self._disparado and t - self._candidato[1] >= duracion:
            self._disparado = True
            return True
        return False

    def _es_pinza(self, mano):
        umbral = self.umbral_sale if self.estado in (GIRANDO, ZOOM) else self.umbral_entra
        return clasificar(mano, umbral) == PINZA

    def _soltar(self):
        self._previo = None
        self._dist_zoom = None
        self.suave.reiniciar()

    def actualizar(self, manos, t):
        if manos:
            self._ultima_mano = t
        elif self._ultima_mano is None or t - self._ultima_mano > self.t_sin_mano:
            if self.estado in (GIRANDO, ZOOM):
                self.estado = LISTO
            self._soltar()
            self._candidato = None
            return Resultado(self.estado, [])

        gestos = [clasificar(m, self.umbral_sale if self.estado in (GIRANDO, ZOOM) else self.umbral_entra)
                  for m in manos]
        resultado = Resultado(self.estado, gestos)
        principal = gestos[0] if gestos else NINGUNO

        if self.estado == ESPERANDO:
            if principal == PALMA and self._sostenido(PALMA, t, self.t_confirmar):
                self.calibrar(manos[0])
                self.estado = LISTO
        elif self.estado == PAUSADO:
            if principal == PALMA and self._sostenido(PALMA, t, self.t_confirmar):
                self.estado = LISTO
        else:
            pinzas = [m for m in manos if self._es_pinza(m)]
            if len(pinzas) >= 2:
                self._zoom(pinzas[0], pinzas[1], resultado)
            elif len(pinzas) == 1:
                self._girar(pinzas[0], resultado)
            else:
                if self.estado in (GIRANDO, ZOOM):
                    self.estado = LISTO
                    self._soltar()
                if principal == PUNO and self._sostenido(PUNO, t, self.t_confirmar):
                    self.estado = PAUSADO
                elif principal == VICTORIA and self._sostenido(VICTORIA, t, self.t_victoria):
                    resultado.acciones.append(("restablecer",))
                elif principal not in (PUNO, VICTORIA):
                    self._candidato = None
        resultado.estado = self.estado
        return resultado

    def _girar(self, mano, resultado):
        if self.estado != GIRANDO:
            self._soltar()
            self.estado = GIRANDO
        agarre = punto_medio(mano[PULGAR[3]], mano[INDICE[3]])
        x, y = self.suave.actualizar(agarre.x, agarre.y)
        if self._previo is not None:
            resultado.acciones.append(("girar", x - self._previo[0], y - self._previo[1]))
        self._previo = (x, y)

    def _zoom(self, a, b, resultado):
        if self.estado != ZOOM:
            self._soltar()
            self.estado = ZOOM
        d = distancia(punto_medio(a[PULGAR[3]], a[INDICE[3]]), punto_medio(b[PULGAR[3]], b[INDICE[3]]))
        if self._dist_zoom is not None and self._dist_zoom > 1e-6:
            resultado.acciones.append(("zoom", d / self._dist_zoom))
        self._dist_zoom = d
