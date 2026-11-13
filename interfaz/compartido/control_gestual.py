"""Panel «Control con gestos» de las gráficas (Módulo I: 3D; Módulo IV: 2D).

Solo presentación.  La visión, la máquina de gestos y el servidor están en gestos/; aquí se
muestran los botones, el indicador de cámara activa, el objetivo, el estado y las métricas,
y se monta el puente que aplica la vista en la gráfica (interfaz/compartido/puente_camara.js).

Un solo dispositivo de cámara: dos controles (uno por objetivo) que nunca están activos a la
vez.  Al activar uno, el otro se detiene (exclusión mutua).

Reglas de privacidad: la cámara solo se enciende al pulsar «Activar»; nunca al cargar la
página.  Se apaga con «Detener», al salir del módulo o al cerrar la pestaña (el fragmento
deja de enviar latidos) y ante cualquier error.  No se guarda ni se envía ninguna imagen.
El ratón sigue funcionando siempre.
"""

import os

import streamlit as st

import gestos
from interfaz.compartido.estilo import insignias

_JS = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "puente_camara.js"),
           encoding="utf-8").read()
_puente = st.components.v2.component("ax_puente_camara", js=_JS)

OBJETIVOS = {
    "3d": "Gráfica 3D · Módulo I (planos)",
    "2d": "Gráfica 2D · Módulo IV (convergencia)",
    "2d_m2": "Gráfica de normas · Módulo II",
    "2d_m3": "Gráfica de mínimos cuadrados · Módulo III",
}
TIPOS_2D = ("2d", "2d_m2", "2d_m3")

GUIA = [
    ("✋ Palma abierta (½ s)", "activa el control y calibra la pinza con su mano"),
    ("🤏 Pinza pulgar-índice", "agarra la vista: mueva la mano para girar (3D) o desplazar (2D)"),
    ("🤏🤏 Pinza con las dos manos", "sepárelas para acercar, júntelas para alejar"),
    ("✊ Puño (½ s)", "pausa; vuelva a abrir la palma para continuar"),
    ("✌️ Victoria (1 s)", "restablece la vista inicial"),
]


@st.cache_resource
def control(tipo="3d"):
    """Un control por objetivo y servidor: la cámara es un solo dispositivo físico."""
    from gestos.control import ControlGestual
    if tipo in TIPOS_2D:
        from gestos.vista2d import VistaPlano2D
        return ControlGestual(destino=VistaPlano2D(0.0, 1.0, 0.0, 1.0))
    return ControlGestual()


def _clave(base, tipo):
    """Claves de widgets: el 3D conserva las de siempre (las pruebas las usan)."""
    return base if tipo == "3d" else f"{base}_{tipo}"


def _otros(tipo):
    return [t for t in OBJETIVOS if t != tipo]


def _activar(tipo, rango=None):
    """on_click: detiene el otro objetivo y arranca este.  Antes de arrancar fija la vista
    inicial (rango de la gráfica) para que el primer gesto parta de la vista que se ve."""
    for otro_tipo in _otros(tipo):
        otro = control(otro_tipo)
        if otro.activo:
            otro.detener(motivo="se activó el control de otra gráfica")
    c = control(tipo)
    if rango is not None and not c.activo:
        from gestos.vista2d import VistaPlano2D
        c.camara = VistaPlano2D(*rango)
    c.iniciar()


def camara_para_figura():
    """Cámara 3D a usar al dibujar la figura mientras el control 3D está activo (evita que un
    rerun devuelva la gráfica a la vista inicial)."""
    ok, _ = gestos.disponible()
    if not ok:
        return None
    c = control("3d")
    return c.camara_actual() if c.activo else None


def rango_para_figura(rango_inicial, tipo="2d"):
    """Rango (x0, x1, y0, y1) para dibujar la gráfica 2D: el de la vista gestual si el control
    2D está activo; si no, `rango_inicial`.  Mantiene el zoom al volver a dibujar."""
    ok, _ = gestos.disponible()
    if not ok:
        return rango_inicial
    c = control(tipo)
    if not c.activo:
        return rango_inicial
    vista = c.camara_actual()
    return (vista["xaxis.range"][0], vista["xaxis.range"][1],
            vista["yaxis.range"][0], vista["yaxis.range"][1])


def panel(clave_grafica, tipo="3d", rango_inicial=None):
    """Panel de control.  Para «2d», `clave_grafica` es la clave del st.plotly_chart y
    `rango_inicial` el rango por defecto de la gráfica."""
    st.markdown("**Control con gestos de la mano** · opcional, con la cámara de este equipo")
    ok, motivo = gestos.disponible()
    if not ok:
        st.info("🖐️ Control gestual no disponible. " + motivo)
        return
    c = control(tipo)
    activo = c.activo
    st.caption(f"Objetivo de los gestos: **{OBJETIVOS[tipo]}**. "
               + ("Activo ahora." if activo else "Solo responde al activar este control."))
    b1, b2, b3 = st.columns(3)
    # on_click: Streamlit ejecuta la acción ANTES de volver a dibujar la página, así la
    # figura de este mismo rerun ya usa la cámara nueva (sin carrera con el puente).
    b1.button("📷 Activar cámara y gestos", key=_clave("gest_activar", tipo), disabled=activo,
              width="stretch", on_click=_activar, args=(tipo, rango_inicial),
              help="Enciende la cámara web. Las imágenes se procesan en memoria en este equipo; "
                   "no se guardan ni se envían.")
    b2.button("⏹ Detener y apagar cámara", key=_clave("gest_detener", tipo), disabled=not activo,
              width="stretch", on_click=c.detener)
    b3.button("⟲ Vista inicial", key=_clave("gest_vista", tipo), disabled=not activo, width="stretch",
              on_click=c.restablecer)

    servidor = c.servidor
    if activo and servidor is not None:
        _puente(key=_clave("gest_puente", tipo), data={"clave": clave_grafica, "puerto": servidor.puerto,
                                                  "token": servidor.token,
                                                  "tipo": "2d" if tipo in TIPOS_2D else "3d"})
        _estado_en_vivo(tipo)
    else:
        e = c.estado()
        if e["error"]:
            st.warning("⚠️ " + e["error"])
        elif e["motivo_fin"]:
            st.caption(f"Cámara apagada ({e['motivo_fin']}).")
        with st.expander("Gestos disponibles"):
            for gesto, accion in GUIA:
                st.markdown(f"- **{gesto}**: {accion}")


@st.fragment(run_every=0.5)
def _estado_en_vivo(tipo):
    """Se ejecuta cada 0,5 s solo mientras el control está activo: envía el latido (si la
    página se cierra o se cambia de módulo, deja de llegar y la cámara se apaga) y
    muestra el estado.  Lee una copia del estado; el hilo de visión no toca Streamlit."""
    c = control(tipo)
    c.latido()
    e = c.estado()
    if not c.activo and not e["iniciando"]:
        st.rerun(scope="app")       # terminó (error o perro guardián): redibuja el panel
    insignias([("● Cámara activa", "error"), (f"Estado: {e['modo']}", "info"),
               ("Mano: " + (", ".join(e["gestos"]) if e["gestos"] else "no detectada"), "")])
    st.caption(f"{e['fps']:.0f} fotogramas/s · detección {e['deteccion_ms']:.0f} ms · "
               f"procesamiento total {e['latencia_ms']:.0f} ms · CPU del proceso {e['cpu_proceso']:.0f} % "
               f"de un núcleo · {e['fotogramas']} fotogramas procesados (ninguno guardado)")
    if e["modo"] == "esperando palma":
        st.caption("Muestre la palma abierta a la cámara durante medio segundo para empezar.")
    elif e["modo"] == "pausado":
        st.caption("En pausa. Abra la palma para continuar.")
