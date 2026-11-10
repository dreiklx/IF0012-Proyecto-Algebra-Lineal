// Puente mínimo entre Python y la gráfica 3D (único JavaScript propio de la aplicación).
// Aprobado por el equipo el 10-nov: Python calcula TODO (cámara, MediaPipe, gestos, cámara
// orbital); este código solo aplica en la gráfica de st.plotly_chart la cámara que llega
// desde 127.0.0.1 y avisa a Python cuando el ratón mueve la vista.  No usa la cámara web
// ni recibe imágenes.
export default function (component) {
  const { data } = component;
  if (!data || !data.puerto) return;
  const base = "http://127.0.0.1:" + data.puerto;
  const conexiones = window.__axConexiones || (window.__axConexiones = {});
  const id = data.clave + ":" + data.puerto;
  if (conexiones[id]) return;                       // ya conectado en un rerun anterior
  for (const k of Object.keys(conexiones)) { conexiones[k].close(); delete conexiones[k]; }

  const grafica = () => document.querySelector(".st-key-" + data.clave + " .js-plotly-plot");
  const fuente = new EventSource(base + "/camara?t=" + data.token);
  conexiones[id] = fuente;
  let pendiente = null, aplicando = false, escuchada = null;

  fuente.onmessage = (evento) => {
    const primera = pendiente === null;
    pendiente = JSON.parse(evento.data);
    if (primera) requestAnimationFrame(aplicar);    // como mucho una vez por cuadro
  };

  function aplicar() {
    const gd = grafica();
    if (gd && window.Plotly && pendiente) {
      aplicando = true;
      Promise.resolve(window.Plotly.relayout(gd, { "scene.camera": pendiente }))
        .finally(() => { aplicando = false; });
      if (escuchada !== gd) { escuchada = gd; gd.on("plotly_relayout", alMoverRaton); }
    }
    pendiente = null;
  }

  function alMoverRaton(cambio) {
    if (aplicando || !cambio || !cambio["scene.camera"]) return;
    fetch(base + "/raton?t=" + data.token,
          { method: "POST", body: JSON.stringify(cambio["scene.camera"]) }).catch(() => {});
  }

  return () => { fuente.close(); delete conexiones[id]; };
}
