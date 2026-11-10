# Control gestual de la gráfica 3D con MediaPipe (Python)

**Estado (10-nov-2026):** implementado en la rama `feature/mediapipe-python` y probado. Se integra a la entrega por decisión del equipo.

**Documentos relacionados:**

- la versión del 10-nov por la mañana proponía MediaPipe en el navegador con JavaScript; **se descartó** porque el equipo pidió que todo fuera Python;
- el razonamiento y las mediciones están en [portabilidad_java_python.md](portabilidad_java_python.md);
- lo que se tomó del chat del equipo está en [revision_chat_mediapipe.md](revision_chat_mediapipe.md).

**Cómo leer este documento:**

- **[Medido]** se midió en este equipo el 10-nov.
- **[Doc]** se tomó de la documentación oficial.
- **[No probado]** no se pudo comprobar y queda pendiente.

## 1. Arquitectura

```text
 cámara web ─► gestos/captura.py ─► gestos/deteccion.py ─► gestos/interpretacion.py ─► gestos/movimiento.py
 (OpenCV,       fotograma en          21 puntos por mano      gesto + acción              cámara orbital θ, φ, r
  DirectShow)   memoria, espejo       (MediaPipe Tasks)       (reglas, antirrebote,       (suavizado, zona muerta,
                                                              histéresis, calibración)     límites)
                                     gestos/control.py: hilo «gestos-vision» + estado con candado + perro guardián
                                                │ servidor.publicar(cámara)
                                     gestos/servidor.py: 127.0.0.1, token, Server-Sent Events
                                                │ 9 números
                         interfaz/compartido/puente_camara.js → Plotly.relayout sobre st.plotly_chart («graf_planos»)
                                                │ POST /raton (vista que dejó el ratón)
                         interfaz/compartido/control_gestual.py: botones, indicador, métricas (fragmento cada 0,5 s)
```

**Separación del núcleo:** `algebra/` no se tocó. `gestos/` no importa nada de `algebra/` y `algebra/` no importa `gestos/`.

## 2. Dependencias (verificadas el 10-nov)

| Paquete | Versión | Tamaño instalado | Licencia | Nota |
|---|---|---|---|---|
| mediapipe | 1.2.2 (wheel `py3-none-win_amd64`) | 71 MB | Apache-2.0 [PyPI] | Solo la API Tasks. Desde 0.10.22 no trae `mp.solutions` |
| opencv-contrib-python | 5.0.0.93 (dependencia de mediapipe) | 139 MB | Apache-2.0 [PyPI] | No instalar también `opencv-python` (conflicto visto en el chat) |
| absl-py, flatbuffers, sounddevice, cffi, pycparser | dependencias de mediapipe | pequeños | — | `pip check`: sin conflictos |
| numpy | 2.5.4 | — | — | Ya estaba (Streamlit) |
| Modelo `hand_landmarker.task` (float16) | publicado el 26-abr-2023 | 7,8 MB | Apache-2.0 (model card, p. 2) | SHA-256 `fbc2a300…7cde1`. Uso previsto según su ficha: «Gesture recognition, Hand control» |

**Entorno:** Python 3.13 (el `.venv` del proyecto). La instalación aislada en un entorno nuevo se probó antes de tocar el `.venv`.

**Gesture Recognizer:** se evaluó y no se usó. Sus gestos predefinidos (puño, palma, victoria) se obtienen con reglas propias, que se pueden explicar y defender, y la pinza no viene predefinida. Así se ahorra un segundo modelo de 8,4 MB.

## 3. Gestos

| Gesto | Acción | Regla (todo dividido por el tamaño de la palma = muñeca → nudillo medio) |
|---|---|---|
| ✋ Palma abierta sostenida 0,35 s | Activa el control y **calibra** la pinza | Los 4 dedos extendidos (punta–muñeca > 1,15 · articulación PIP–muñeca) |
| 🤏 Pinza pulgar-índice | Agarrar y girar: horizontal = azimut θ, vertical = elevación φ | \|punta pulgar − punta índice\| / palma < umbral de entrada. Sale con un umbral 1,5 veces mayor (histéresis). La punta del índice debe quedar fuera de la palma, para no confundirla con el puño |
| 🤏🤏 Pinza con las dos manos | Zoom: separar acerca, juntar aleja | Cociente de distancias entre los dos puntos de agarre |
| ✊ Puño sostenido 0,35 s | Pausa | Ningún dedo extendido |
| ✌️ Victoria sostenida 0,8 s | Restablece la vista inicial (una vez por gesto) | Índice y medio extendidos; anular y meñique doblados |

**Estabilidad:**

- **Antirrebote:** tiempos mínimos por gesto.
- **Histéresis** en la pinza.
- **Calibración:** el umbral de entrada es 0,35 × la separación medida con la palma abierta, limitado a [0,18; 0,25].
- **Suavizado exponencial** del punto de agarre, con α = 0,35.
- **Zona muerta acumulada** de 0,004. El temblor se cancela, y el movimiento lento y sostenido sí llega.
- **Límites:** elevación entre −80° y 85°; distancia entre 0,9 y 5; `up` fijo, así la vista nunca se voltea.
- **Al agarrar no hay salto:** el primer fotograma de la pinza solo fija la referencia.
- **Si se pierde la mano** durante 0,5 s, se suelta.

## 4. Cámara y privacidad

| Requisito | Implementación | Comprobado |
|---|---|---|
| Solo a petición | Botón «Activar cámara y gestos». No hay arranque automático | Prueba `test_control_gestual`: tras resolver, la cámara sigue apagada |
| Indicador | Insignia «● Cámara activa» más la luz de la cámara del equipo | [Medido] en Brave |
| Detener | «Detener y apagar cámara» → `cap.release()` y cierre del modelo y del canal | [Medido]: «Cámara apagada (detenido por el usuario)» |
| Al salir del módulo o cerrar la pestaña | El fragmento envía un latido cada 0,5 s. A los 4 s sin latido, el hilo se detiene y libera la cámara | [Medido]: al ir al Módulo II y volver, «la página dejó de estar abierta» |
| Sin cámara, ocupada o sin permiso | Mensaje específico (incluye la ruta de privacidad de Windows); el ratón sigue funcionando | Prueba con una fábrica de cámara que falla. [No probado] con la privacidad de Windows desactivada: no se cambió la configuración del sistema |
| Sin guardar, grabar ni enviar | El fotograma solo vive dentro del bucle (`del fotograma`). Al navegador solo van 9 números | Revisión de código; el contador dice «ninguno guardado» |
| El ratón sigue funcionando | El puente no bloquea la gráfica. La vista del ratón vuelve a Python por `POST /raton` y se conserva tras los reruns | [Medido]: después de arrastrar y de un rerun completo, la vista se mantiene |
| Brave no pide permiso de cámara | La cámara la abre Python, no el navegador; rige el permiso de Windows para aplicaciones de escritorio | — |

## 5. Rendimiento

Medido el 10-nov en Windows 11, con Ryzen 5 8645HS (6 núcleos, 12 hilos), RTX 4050 Laptop, 39 GB de RAM, Brave sin cabeza y cámara real a 640×480.

| Métrica | Valor | Tipo |
|---|---|---|
| Carga del modelo | 92 ms | [Medido] |
| Detección por fotograma, sin mano (busca la palma en cada fotograma) | 17–47 ms; típico 18–22 ms | [Medido] |
| Detección con 2 manos, imagen oficial de ejemplo de MediaPipe (640×960) | mediana 28,1 ms; p90 29,2 ms | [Medido] |
| Fotogramas procesados por segundo (cámara real) | 22–34; típico 32–33 | [Medido] |
| Procesamiento total por fotograma (lectura → cámara publicada) | 32–48 ms | [Medido] |
| CPU del proceso de Streamlit con la cámara activa | 63–122 % de un núcleo (≈ 5–10 % del total de 12 hilos) | [Medido] |
| Memoria del proceso | 208 MB sin cámara → 262 MB activa (estable durante 3 min) → 211 MB al detener | [Medido] |
| Estabilidad | 3 min seguidos, 4716 fotogramas, sin errores ni crecimiento de memoria | [Medido] |
| Canal Python → gráfica | 29,7 cambios/s; navegador a 60 fps; peor cuadro 18–34 ms; la gráfica no se vuelve a montar | [Medido] |
| GPU | MediaPipe corre en CPU en Python/Windows (no se configuró delegado GPU). La GPU solo la usa el navegador para dibujar | — |
| Latencia de gesto real a movimiento visible | [No probado]: requiere una persona frente a la cámara. Estimación: procesamiento (~35 ms) + suavizado + un cuadro del navegador (~16 ms) | — |

## 6. Pruebas

| Prueba | Qué comprueba |
|---|---|
| `tests/gestos/test_interpretacion.py` (14) | Cada gesto; independencia de la distancia a la cámara; el puño no se confunde con la pinza; activación con antirrebote; sin activar no se mueve nada; giro y su signo; sin salto al agarrar; histéresis; pausa y reanudación; victoria una sola vez; zoom con dos manos; perder la mano; calibración |
| `tests/gestos/test_movimiento.py` (11) | Suavizado; vista inicial igual a la de la figura; radio constante al girar; zona muerta; movimiento lento acumulado; temblor sin efecto; límites; `up` fijo; restablecer; continuar desde el ratón |
| `tests/gestos/test_control.py` (9) | El hilo gira la cámara con un detector falso; libera al detener; perro guardián; error al abrir; el servidor solo escucha en 127.0.0.1; token obligatorio; flujo SSE; POST del ratón; el modelo real carga y no ve manos en una imagen negra |
| `tests/interfaz/test_control_gestual.py` | El panel aparece en el Módulo I y la cámara no se enciende sola |
| Punta a punta (guion de medición en Brave, no incluido en la suite) | Activar, métricas, canal SSE, ratón → Python, vista inicial, detener, perro guardián y 3 min de estabilidad |

**Pendiente con una persona frente a la cámara** (no se puede automatizar aquí):

- pinza y giro reales;
- zoom con dos manos;
- puño y victoria;
- iluminación del aula;
- prueba en una ventana normal de Brave.
