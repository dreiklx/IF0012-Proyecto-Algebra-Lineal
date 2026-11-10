# Investigación: control gestual de la gráfica 3D con MediaPipe

**Fecha:** 10-nov-2026.
**Estado:** **solo investigación. No hay nada implementado.**

- No se instaló MediaPipe.
- No se modificó `requirements.txt`.
- No hay JavaScript de cámara.
- La aplicación no pide ningún permiso.

La implementación esperará el código de referencia del equipo y una instrucción expresa.

**Objetivo futuro:** durante una exposición, rotar, acercar, desplazar y restablecer la gráfica 3D del Módulo I (planos y solución) con gestos de la mano, conservando el ratón como alternativa.

**Cómo leer este documento:**

- **[Doc]** es un dato tomado de la documentación oficial (fuentes al final).
- **[Verificado]** se comprobó en este equipo.
- **[Estimación]** es un razonamiento sin medir.
- **[Por medir]** solo se sabrá al implementar.

## 1. Tecnologías

| Pieza | Qué aporta | Datos clave |
|---|---|---|
| MediaPipe **Hand Landmarker** (paquete npm `@mediapipe/tasks-vision`) | 21 puntos por mano en cada fotograma | [Doc] Dos modelos: detección de palma y puntos sobre la mano recortada. `landmarks`: x e y normalizados en [0, 1] y z relativa a la muñeca. `worldLandmarks`: en metros, con el origen en el centro de la mano. `handedness`: «Left»/«Right», que se invierte si la imagen está en espejo. Opciones: `runningMode` (`IMAGE`/`VIDEO`), `numHands` (1 por defecto), `minHandDetectionConfidence`, `minHandPresenceConfidence` y `minTrackingConfidence` (0,5 por defecto). En modo `VIDEO` reutiliza el recuadro del fotograma anterior y solo vuelve a detectar la palma si pierde la mano |
| MediaPipe **Gesture Recognizer** | Gestos ya entrenados + los mismos 21 puntos | [Doc] Gestos predefinidos: `Closed_Fist`, `Open_Palm`, `Pointing_Up`, `Thumb_Down`, `Thumb_Up`, `Victory`, `ILoveYou` (y `None`). Admite un clasificador propio. Las opciones son las mismas, más `cannedGesturesClassifierOptions` (lista de gestos permitidos o bloqueados y umbral) |
| **Streamlit Components v2** | Ejecutar JavaScript propio dentro de la página y devolver valores a Python | [Verificado] Streamlit 1.66.1, el instalado, incluye `st.components.v2.component(name, html=, css=, js=, isolate_styles=)`. La función JS recibe `component` con `setTriggerValue`/`setStateValue`; el montaje acepta `key` y `data`. [Doc] Los componentes v2 **no van en un iframe**: forman parte de la página. La documentación advierte que el código es «confiable» y no está aislado (el estilo puede ir en shadow DOM) |
| **plotly.js** | Cambiar la cámara 3D sin redibujar | [Doc] `Plotly.relayout(graphDiv, update)` actualiza el layout con rutas con punto, «comparable a `Plotly.react`, más rápido que `newPlot`». La cámara 3D es `scene.camera` = {`eye`, `center`, `up`}; la aplicación ya fija `eye` en `visualizacion/interactivas.py` (línea 103) |
| **getUserMedia** | Acceso a la cámara | [Doc] Solo funciona en contextos seguros: HTTPS, `localhost` o `file:`. En un iframe hace falta `allow="camera"`. Errores: `NotAllowedError` (permiso denegado), `NotFoundError` (no hay cámara), `NotReadableError` (cámara ocupada o fallo). El navegador muestra un indicador obligatorio de cámara activa; `track.stop()` libera el dispositivo |

**Consecuencias para Ax:**

- La aplicación corre en `http://localhost:8501`, que es un contexto seguro. No hace falta HTTPS para la defensa en la misma computadora.
- Como los componentes v2 no usan iframe, no hace falta configurar `allow="camera"`. [Por medir] Hay que confirmar el diálogo de permiso en Brave y en Chrome.

## 2. Arquitectura propuesta

```text
 Python (Streamlit)                                Navegador (todo local)
 ─────────────────                                 ──────────────────────
 visualizacion/interactivas.py                     componente v2 «control_gestual»
   figura 3D (planos + solución)  ── data ──►       ├─ dibuja la figura con plotly.js LOCAL
                                                    ├─ botón «Activar cámara» (gesto del usuario)
                                                    ├─ getUserMedia → <video> (no se graba)
                                                    ├─ HandLandmarker.detectForVideo (WASM/GPU)
                                                    ├─ intérprete de gestos (JS propio)
                                                    │     suavizado + zona muerta + histéresis
                                                    └─ Plotly.relayout({'scene.camera': …})
                        ◄── setStateValue ──  estado: activo/pausado, error, cámara final (opcional)
```

**Decisión recomendada:** que **el componente dibuje su propia copia de la figura 3D** con plotly.js, en lugar de manipular el gráfico que crea `st.plotly_chart`.

- El objeto `Plotly` de `st.plotly_chart` está dentro del paquete de Streamlit. No hay garantía de que sea accesible desde otro código, y depender de eso se rompería con una actualización.
- El componente recibe en `data` las mismas trazas que ya calcula `visualizacion/interactivas.py`, es decir, los datos del núcleo; no se recalcula nada.
- [Verificado] El paquete `plotly` instalado trae `plotly.min.js` (4,6 MB) en `package_data/`. Puede servirse localmente, sin internet.

**Flujo (los 8 pasos de la propuesta del equipo):**

1. Streamlit muestra la gráfica 3D habitual, con el ratón como hasta ahora.
2. El usuario pulsa «Activar control con gestos». Es una acción expresa y el navegador la exige para pedir el permiso.
3. `getUserMedia({video: true})` abre el diálogo de permiso.
4. MediaPipe procesa cada fotograma **en el propio navegador**, con WASM y WebGL.
5. Se obtienen los 21 puntos y, opcionalmente, la categoría de gesto.
6. El intérprete traduce los puntos en cambios de `eye`, `center` y `up`.
7. `Plotly.relayout` aplica la cámara.
8. La gráfica cambia de perspectiva en tiempo real. Desactivar, o salir del módulo, libera la cámara.

## 3. Sistema de gestos propuesto

| Gesto | Acción | Detección | Fiabilidad esperada |
|---|---|---|---|
| Palma abierta sostenida ~0,5 s | Activar el modo de control (armar) | `Open_Palm` del Gesture Recognizer o 5 dedos extendidos (puntas por encima de sus articulaciones PIP) | [Estimación] Alta: gesto predefinido |
| **Pinza** (pulgar e índice juntos) | «Agarrar»: mientras dura, el movimiento de la mano rota la vista | **Algoritmo propio:** distancia 4–8 normalizada por el tamaño de la mano (0–9); entra con d < 0,25 y sale con d > 0,35 (histéresis) | [Estimación] Media-alta; es el patrón usual en interfaces de pellizco. No es un gesto predefinido |
| Movimiento horizontal con pinza | Rotar alrededor del eje z (azimut) | Δx del punto medio de la pinza → Δθ | Depende del suavizado |
| Movimiento vertical con pinza | Elevación (ángulo polar, con límites para no voltear) | Δy → Δφ, con φ entre 5° y 85° | Ídem |
| Dos manos con pinza, separándose o acercándose | Zoom (radio de `eye`) | `numHands: 2`; cociente entre la distancia actual y la inicial de los dos puntos de pinza | [Estimación] Media: requiere dos manos visibles y más cómputo |
| Puño cerrado | Pausar (la cámara sigue encendida, la gráfica no se mueve) | `Closed_Fist` | [Estimación] Alta |
| `Victory` sostenido 1 s | Restablecer la vista inicial | Gesto predefinido | Alta, con temporizador para evitar disparos accidentales |
| Botón | Desactivar y apagar la cámara | No es un gesto | Siempre disponible |

**Matemática del control (para defenderla):** la cámara de Plotly se describe en **coordenadas esféricas** alrededor de `center`.

- `eye` = center + r·(cos φ cos θ, cos φ sin θ, sin φ).
- La pinza cambia θ y φ en proporción al desplazamiento.
- El zoom cambia r.

Así el movimiento es continuo y nunca invierte `up`.

**Estabilidad y falsos positivos:**

- **Suavizado:** media exponencial (α ≈ 0,3) sobre el punto de control, o el filtro «1€», que es estándar para seguimiento de manos. [Por medir] El α adecuado.
- **Zona muerta:** se ignoran desplazamientos menores que ~1 % del ancho, para eliminar el temblor.
- **Histéresis y tiempos mínimos:** los gestos discretos (activar, restablecer) exigen varios fotogramas seguidos con una confianza de al menos 0,7.
- **Espejo:** el video se muestra en espejo para que el movimiento resulte natural. La etiqueta `handedness` se invierte [Doc], pero el control no depende de ella.
- **Sensibilidad configurable:** un deslizador de grados de rotación por fracción de pantalla.

## 4. Cámara y privacidad

| Aspecto | Propuesta |
|---|---|
| Cuándo se pide | Solo al pulsar el botón. Nunca al cargar la página |
| Indicador | El del navegador [Doc], más uno propio: «● Cámara activa», con botón «Apagar cámara» |
| Detener | `stream.getTracks().forEach(t => t.stop())` al desactivar, al ocultarse la pestaña (`visibilitychange`) y al desmontar el componente (cambio de página) |
| Permiso denegado (`NotAllowedError`) | Mensaje: «Permiso denegado; puede seguir usando el ratón». No se reintenta solo |
| Sin cámara (`NotFoundError`) u ocupada (`NotReadableError`) | Mensaje específico; el botón queda deshabilitado |
| Almacenamiento | **Ninguno.** Los fotogramas van del `<video>` al modelo en memoria; no hay `MediaRecorder`, ni `canvas.toBlob`, ni envío a ningún servidor. A Python solo vuelven, como mucho, los valores de la cámara 3D (seis números) |
| Procesamiento | Local. **Para que funcione sin internet**, los archivos WASM y el modelo `.task` deben servirse desde el proyecto, no desde el CDN (jsDelivr) que usan los ejemplos [Doc] |
| Alternativa | El ratón sigue funcionando siempre; el control gestual es un complemento |

## 5. Rendimiento

| Dato | Valor | Tipo |
|---|---|---|
| Latencia de Hand Landmarker (completo), Pixel 6 | CPU 17,12 ms; GPU 12,27 ms | [Doc] |
| Latencia de Gesture Recognizer, Pixel 6 | CPU 16,76 ms; GPU 20,87 ms | [Doc] |
| En un portátil con Chrome o Brave y WebGL | Probablemente igual o mejor que en el Pixel 6; objetivo de 25 a 30 fps | [Estimación]; [Por medir] |
| Costo de `Plotly.relayout` de la cámara | Bajo (no redibuja las trazas) | [Doc: comparable a `react`]; [Por medir] en esta figura |
| Bloqueo del hilo principal | `detectForVideo` es síncrono [Doc]. A 15 ms por fotograma con `requestAnimationFrame` deja margen, pero compite con Streamlit y con el render de Plotly | [Estimación] |
| Web Worker | Posible mejora: procesar en un worker con `OffscreenCanvas`/`ImageBitmap` | [Por medir]: la guía web oficial no documenta el uso en worker; probar antes de depender de ello |
| Tamaño de los recursos | Modelo `.task` + WASM (varios MB) + plotly.js (4,6 MB, ya local) | [Por medir]: el tamaño exacto del modelo |
| Brave | Usa Chromium, con WebGL y WASM; el permiso de cámara es por sitio. Shields podría afectar la carga desde el CDN, pero no desde `localhost` | [Por medir] |

**Medidas previstas para no saturar:**

- procesar solo cuando el control está activo;
- `numHands: 1` salvo para el zoom con dos manos;
- limitar a ~20 detecciones por segundo si el equipo de la defensa es lento;
- no hacer `setStateValue` en cada fotograma (Python no debe recibir 30 eventos por segundo).

## 6. Riesgos

| Riesgo | Mitigación |
|---|---|
| Iluminación o fondo del aula: el seguimiento falla | Umbrales configurables; el ratón como alternativa; probar en el aula |
| Equipo de la defensa sin cámara o con el permiso bloqueado | Funciona sin gestos; mensaje claro |
| Sin internet en la defensa | Recursos de MediaPipe y plotly.js empaquetados localmente |
| API v2 de Streamlit reciente: puede cambiar entre versiones | Versión fijada (1.66.1) en `requirements.txt`; pruebas con `AppTest` del lado Python |
| Distracción en la exposición | Solo se activa a demanda; pausa con el puño |
| Licencias | MediaPipe y plotly.js son Apache-2.0 / MIT [Por confirmar en el repositorio de cada uno antes de empaquetarlos] |
| Rúbrica | No es un requisito. Podría contar en «Visualización avanzada» o «Experiencia de usuario», pero **no debe poner en riesgo la entrega**: conviene una rama aparte |

## 7. Dependencias futuras (no instaladas)

- `@mediapipe/tasks-vision` (WASM y modelo `hand_landmarker.task` o `gesture_recognizer.task`) como archivos estáticos del componente. **No es un paquete de Python** y no se añadiría a `requirements.txt`.
- `plotly.min.js`, ya presente dentro del paquete `plotly` instalado.
- Ninguna dependencia nueva de Python.

## 8. Plan de pruebas

1. **Python (automáticas):** `AppTest` comprueba que la página carga con el componente montado y desactivado, que la figura recibe los mismos datos del núcleo y que sin cámara no hay errores.
2. **Intérprete de gestos (automáticas en JS o Python):** secuencias de puntos grabadas a mano (sin imágenes) → cambios de cámara esperados; histéresis de la pinza; zona muerta.
3. **Manuales en Chrome y Brave:** permiso concedido, denegado y revocado; sin cámara; cámara ocupada por otra aplicación; cambio de página (la luz de la cámara debe apagarse); 10 minutos de uso continuo (CPU y temperatura).
4. **Rendimiento:** fps de detección y latencia gesto→movimiento (`performance.now()`), en el equipo real de la defensa.
5. **Sin internet:** desconectar la red y comprobar que todo carga.

## 9. Pasos de implementación (cuando se autorice)

1. Estudiar el código de referencia que entregará el equipo.
2. Rama `feature/control-gestual`.
3. Componente v2 que solo dibuja la figura con plotly.js local (sin cámara) y comprueba que coincide con la actual.
4. Botón, permiso, indicador y apagado de la cámara, con todos los errores.
5. Hand Landmarker con la pinza para rotar, suavizado y zona muerta.
6. Zoom con dos manos, pausa y restablecer.
7. Recursos locales (sin CDN) y prueba sin internet.
8. Pruebas de la sección 8, documentación y decisión de incluirlo o no en la entrega.

## 10. Preguntas para cuando llegue el código de referencia

1. ¿Usa Hand Landmarker, Gesture Recognizer o ambos? ¿Qué versión de `@mediapipe/tasks-vision`?
2. ¿Carga los recursos desde un CDN? (Para la defensa conviene local).
3. ¿Qué gestos implementa y con qué umbrales y suavizado?
4. ¿Controla Plotly, Three.js u otra biblioteca? ¿Cómo mapea la mano a la cámara?
5. ¿Corre en el hilo principal o en un worker? ¿A cuántos fps en su equipo?
6. ¿Tiene licencia compatible para incluirlo en la entrega?
7. ¿Debe estar en la entrega del 11-nov o es una mejora posterior?

## Fuentes

- Hand Landmarker (web): https://developers.google.com/edge/mediapipe/solutions/vision/hand_landmarker/web_js
- Hand Landmarker (modelo y referencias de rendimiento): https://developers.google.com/edge/mediapipe/solutions/vision/hand_landmarker
- Gesture Recognizer (web): https://developers.google.com/edge/mediapipe/solutions/vision/gesture_recognizer/web_js
- Gesture Recognizer (gestos y rendimiento): https://developers.google.com/edge/mediapipe/solutions/vision/gesture_recognizer
- Streamlit Custom Components: https://docs.streamlit.io/develop/concepts/custom-components/overview, más el docstring de `st.components.v2.component` en Streamlit 1.66.1 instalado
- Plotly.js, referencia de funciones: https://plotly.com/javascript/plotlyjs-function-reference/
- MDN, `getUserMedia`: https://developer.mozilla.org/en-US/docs/Web/API/MediaDevices/getUserMedia
