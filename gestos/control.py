"""Hilo de trabajo del control gestual y estado compartido con la interfaz.

Separación de hilos (regla del diseño del equipo: el modelo es la frontera entre hilos):

  hilo «gestos-vision»  captura → detección → interpretación → cámara → servidor.publicar()
                        Escribe el estado SOLO a través de _fijar() (con candado).
                        Nunca llama a funciones st.* de Streamlit.
  Streamlit             lee una copia del estado con estado(), llama a latido() mientras la
                        página está abierta y pide iniciar()/detener()/restablecer().

La cámara se libera: al pulsar «Detener», si la página deja de enviar latidos (se cambió
de módulo o se cerró la pestaña: perro guardián de TIEMPO_SIN_LATIDO segundos) y si ocurre
cualquier error.  Los fotogramas solo existen dentro del bucle y se descartan enseguida.
"""

import threading
import time

from gestos.interpretacion import InterpreteGestos
from gestos.movimiento import CamaraOrbital

TIEMPO_SIN_LATIDO = 4.0        # s sin latido de la página → se apaga la cámara
TIEMPO_SIN_IMAGEN = 3.0        # s abierta sin entregar imágenes → error


def _camara_real():
    from gestos.captura import Camara
    return Camara().abrir()


def _detector_real():
    from gestos.deteccion import DetectorManos
    return DetectorManos()


class ControlGestual:
    def __init__(self, fabrica_camara=_camara_real, fabrica_detector=_detector_real,
                 reloj=time.monotonic, con_servidor=True):
        self._fabrica_camara = fabrica_camara
        self._fabrica_detector = fabrica_detector
        self._reloj = reloj
        self._con_servidor = con_servidor
        self._candado = threading.Lock()
        self._hilo = None
        self._parar = threading.Event()
        self._latido = reloj()
        self.camara = CamaraOrbital()
        self.servidor = None
        self._estado = self._estado_inicial()

    @staticmethod
    def _estado_inicial():
        return {"activo": False, "iniciando": False, "modo": "apagado", "gestos": [], "error": "",
                "fps": 0.0, "deteccion_ms": 0.0, "latencia_ms": 0.0, "cpu_proceso": 0.0,
                "fotogramas": 0, "motivo_fin": ""}

    # -- API para Streamlit (no bloquea) ----------------------------------
    def iniciar(self):
        with self._candado:
            if self._hilo is not None and self._hilo.is_alive():
                return
            self._estado = self._estado_inicial()
            self._estado.update(iniciando=True, modo="abriendo cámara")
        self._parar.clear()
        self._latido = self._reloj()
        if self._con_servidor and self.servidor is None:
            from gestos.servidor import ServidorCamara
            self.servidor = ServidorCamara(al_mover_raton=self.sincronizar_raton)
            self.servidor.publicar(self.camara.a_plotly())
        self._hilo = threading.Thread(target=self._bucle, name="gestos-vision", daemon=True)
        self._hilo.start()

    def detener(self, motivo="detenido por el usuario", esperar=True):
        self._parar.set()
        hilo = self._hilo
        if esperar and hilo is not None and hilo is not threading.current_thread():
            hilo.join(timeout=3)
        with self._candado:
            if not self._estado["motivo_fin"]:
                self._estado["motivo_fin"] = motivo
        if self.servidor is not None:
            self.servidor.cerrar()
            self.servidor = None

    def latido(self):
        self._latido = self._reloj()

    def estado(self):
        with self._candado:
            copia = dict(self._estado)
        copia["camara"] = self.camara_actual()
        return copia

    def restablecer(self):
        with self._candado:
            self.camara.restablecer()
            camara = self.camara.a_plotly()
        self._publicar(camara)

    def sincronizar_raton(self, camara):
        """El ratón movió la gráfica: la próxima pinza continúa desde esa vista."""
        with self._candado:
            self.camara.desde_plotly(camara)

    def camara_actual(self):
        with self._candado:
            return self.camara.a_plotly()

    @property
    def activo(self):
        return self._hilo is not None and self._hilo.is_alive()

    # -- hilo de trabajo -------------------------------------------------
    def _fijar(self, **cambios):
        with self._candado:
            self._estado.update(cambios)

    def _publicar(self, camara):
        if self.servidor is not None:
            self.servidor.publicar(camara)

    def _bucle(self):
        camara = detector = None
        try:
            camara = self._fabrica_camara()
            detector = self._fabrica_detector()
            self._fijar(activo=True, iniciando=False, modo="esperando palma", error="")
            interprete = InterpreteGestos()
            inicio = ultimo_ok = t_prev = self._reloj()
            cpu_prev, pared_prev = time.process_time(), time.perf_counter()
            fps = det_ms = lat_ms = 0.0
            n = 0
            while not self._parar.is_set():
                ahora = self._reloj()
                if ahora - self._latido > TIEMPO_SIN_LATIDO:
                    self._fijar(motivo_fin="la página dejó de estar abierta (se cambió de módulo o se cerró)")
                    break
                t0 = time.perf_counter()
                fotograma = camara.leer()
                if fotograma is None:
                    if ahora - ultimo_ok > TIEMPO_SIN_IMAGEN:
                        from gestos.captura import MENSAJE_SIN_IMAGEN
                        raise RuntimeError(MENSAJE_SIN_IMAGEN)
                    time.sleep(0.01)
                    continue
                ultimo_ok = ahora
                t1 = time.perf_counter()
                manos = detector.detectar(fotograma, (ahora - inicio) * 1000)
                del fotograma                      # no se conserva ninguna imagen
                t2 = time.perf_counter()
                resultado = interprete.actualizar(manos, ahora)
                cambio = False
                with self._candado:
                    for accion in resultado.acciones:
                        if accion[0] == "girar":
                            cambio |= self.camara.girar(accion[1], accion[2])
                        elif accion[0] == "zoom":
                            cambio |= self.camara.zoom(accion[1])
                        elif accion[0] == "restablecer":
                            self.camara.restablecer()
                            cambio = True
                    nueva = self.camara.a_plotly() if cambio else None
                if nueva is not None:
                    self._publicar(nueva)
                t3 = time.perf_counter()
                n += 1
                dt = max(ahora - t_prev, 1e-6)
                t_prev = ahora
                a = 0.1                            # promedio exponencial de las métricas
                fps = (1 / dt) if n == 1 else fps + a * (1 / dt - fps)
                det_ms = (t2 - t1) * 1000 if n == 1 else det_ms + a * ((t2 - t1) * 1000 - det_ms)
                lat_ms = (t3 - t0) * 1000 if n == 1 else lat_ms + a * ((t3 - t0) * 1000 - lat_ms)
                cambios = dict(modo=resultado.estado, gestos=resultado.gestos, fotogramas=n,
                               fps=round(fps, 1), deteccion_ms=round(det_ms, 1), latencia_ms=round(lat_ms, 1))
                if n % 30 == 0:
                    cpu, pared = time.process_time(), time.perf_counter()
                    cambios["cpu_proceso"] = round(100 * (cpu - cpu_prev) / max(pared - pared_prev, 1e-6), 1)
                    cpu_prev, pared_prev = cpu, pared
                self._fijar(**cambios)
        except Exception as error:      # cualquier fallo apaga la cámara y se informa
            self._fijar(error=str(error))
        finally:
            if detector is not None:
                detector.cerrar()
            if camara is not None:
                camara.liberar()
            self._fijar(activo=False, iniciando=False, modo="apagado")
            if self._parar.is_set() is False and self.servidor is not None:
                # fin por perro guardián o error: también se cierra el canal
                servidor, self.servidor = self.servidor, None
                servidor.cerrar()
