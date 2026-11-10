"""Panel «Control con gestos» de la gráfica 3D (Módulo I).

Solo presentación.  La visión y la cámara orbital están en gestos/; aquí se muestran
los botones, el indicador de cámara activa, el estado y las métricas, y se monta el
puente que aplica la cámara en la gráfica (interfaz/compartido/puente_camara.js).

Reglas de privacidad: la cámara solo se enciende al pulsar «Activar»; nunca al cargar
la página.  Se apaga con «Detener», al salir del módulo o al cerrar la pestaña (el
fragmento deja de enviar latidos) y ante cualquier error.  No se guarda ni se envía
ninguna imagen.  El ratón sigue funcionando siempre.
"""

import os

import streamlit as st

import gestos
from interfaz.compartido.estilo import insignias

_JS = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "puente_camara.js"),
           encoding="utf-8").read()
_puente = st.components.v2.component("ax_puente_camara", js=_JS)

GUIA = [
    ("✋ Palma abierta (½ s)", "activa el control y calibra la pinza con su mano"),
    ("🤏 Pinza pulgar-índice", "agarra la vista: mueva la mano para girar"),
    ("🤏🤏 Pinza con las dos manos", "sepárelas para acercar, júntelas para alejar"),
    ("✊ Puño (½ s)", "pausa; vuelva a abrir la palma para continuar"),
    ("✌️ Victoria (1 s)", "restablece la vista inicial"),
]


@st.cache_resource
def control():
    """Un único control por servidor: la cámara es un solo dispositivo físico."""
    from gestos.control import ControlGestual
    return ControlGestual()


def camara_para_figura():
    """Cámara a usar al dibujar la figura mientras el control está activo (evita que un
    rerun devuelva la gráfica a la vista inicial)."""
    ok, _ = gestos.disponible()
    if not ok:
        return None
    c = control()
    return c.camara_actual() if c.activo else None


def panel(clave_grafica):
    st.markdown("**Control con gestos de la mano** · opcional, con la cámara de este equipo")
    ok, motivo = gestos.disponible()
    if not ok:
        st.info("🖐️ Control gestual no disponible. " + motivo)
        return
    c = control()
    activo = c.activo
    b1, b2, b3 = st.columns(3)
    # on_click: Streamlit ejecuta la acción ANTES de volver a dibujar la página, así la
    # figura de este mismo rerun ya usa la cámara nueva (sin carrera con el puente).
    b1.button("📷 Activar cámara y gestos", key="gest_activar", disabled=activo, width="stretch",
              on_click=c.iniciar,
              help="Enciende la cámara web. Las imágenes se procesan en memoria en este equipo; "
                   "no se guardan ni se envían.")
    b2.button("⏹ Detener y apagar cámara", key="gest_detener", disabled=not activo, width="stretch",
              on_click=c.detener)
    b3.button("⟲ Vista inicial", key="gest_vista", disabled=not activo, width="stretch",
              on_click=c.restablecer)

    servidor = c.servidor
    if activo and servidor is not None:
        _puente(key="gest_puente", data={"clave": clave_grafica, "puerto": servidor.puerto,
                                          "token": servidor.token})
        _estado_en_vivo()
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
def _estado_en_vivo():
    """Se ejecuta cada 0,5 s solo mientras el control está activo: envía el latido (si la
    página se cierra o se cambia de módulo, deja de llegar y la cámara se apaga) y
    muestra el estado.  Lee una copia del estado; el hilo de visión no toca Streamlit."""
    c = control()
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
