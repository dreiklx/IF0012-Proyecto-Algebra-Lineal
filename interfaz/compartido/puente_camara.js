// Puente entre Python y las gráficas de Plotly: aplica en el navegador la vista que calcula
// Python (127.0.0.1) y le avisa cuando el ratón mueve la gráfica.  No usa la cámara ni imágenes.
//   data.tipo === "3d" (por defecto): aplica «scene.camera» (Módulo I).
//   data.tipo === "2d": aplica «xaxis.range» e «yaxis.range» (Módulo IV).
export default function (component) {
  const { data } = component;
  if (!data || !data.puerto) return;
  const base = "http://127.0.0.1:" + data.puerto;
  const conexiones = window.__axConexiones || (window.__axConexiones = {});
  const id = data.clave + ":" + data.puerto;
  if (conexiones[id]) return;                       // ya conectado en un rerun anterior
  for (const k of Object.keys(conexiones)) { conexiones[k].close(); delete conexiones[k]; }

  const dos_d = data.tipo === "2d";
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
      Promise.resolve(window.Plotly.relayout(gd, dos_d ? pendiente : { "scene.camera": pendiente }))
        .finally(() => { aplicando = false; });
      if (escuchada !== gd) { escuchada = gd; gd.on("plotly_relayout", alMoverRaton); }
    }
    pendiente = null;
  }

  function alMoverRaton(cambio) {
    if (aplicando || !cambio) return;
    let cuerpo = null;
    if (dos_d) {
      // Solo los rangos de los ejes: el zoom por rueda, el arrastre y los botones de Plotly.
      const claves = Object.keys(cambio).filter((k) => /^(xaxis|yaxis)\.range/.test(k));
      if (claves.length) cuerpo = Object.fromEntries(claves.map((k) => [k, cambio[k]]));
    } else if (cambio["scene.camera"]) {
      cuerpo = cambio["scene.camera"];
    }
    if (!cuerpo) return;
    fetch(base + "/raton?t=" + data.token,
          { method: "POST", body: JSON.stringify(cuerpo) }).catch(() => {});
  }

  return () => { fuente.close(); delete conexiones[id]; };
}
