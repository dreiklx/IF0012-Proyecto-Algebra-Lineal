# `gestos/`: control con la mano de la gráfica 3D (MediaPipe)

Es opcional y no forma parte del núcleo: no importa `algebra/` ni `interfaz/`. La cámara se enciende solo cuando el usuario pulsa «Activar cámara y gestos», y las imágenes nunca salen de la memoria del equipo.

```text
captura.py ──► deteccion.py ──► mano.py ──► interpretacion.py ──► movimiento.py
 (OpenCV)       (MediaPipe)     (21 puntos)  (qué gesto es)         (cámara θ, φ, r)
                                                     │
                     control.py (hilo «gestos-vision», candado, perro guardián de 4 s)
                                                     │
                     servidor.py (127.0.0.1, SSE, con token) ──► puente_camara.js ──► Plotly
```

| Archivo | Responsabilidad |
|---|---|
| `captura.py` | abrir y leer la cámara web (OpenCV, DirectShow) |
| `deteccion.py` | `DetectorManos`: MediaPipe Hand Landmarker en modo VIDEO con el modelo `modelos/hand_landmarker.task` |
| `mano.py` | los 21 puntos de una mano, distancias y tamaño de la palma |
| `interpretacion.py` | reglas de los gestos con antirrebote, histéresis y calibración (`InterpreteGestos`) |
| `movimiento.py` | suavizado exponencial y cámara orbital con límites (`CamaraOrbital`) |
| `control.py` | `ControlGestual`: une todo en un hilo propio; nunca llama a `st.*` |
| `servidor.py` | entrega la cámara al navegador unas 30 veces por segundo |

Gestos y detalles: [docs/investigacion_mediapipe.md](../docs/investigacion_mediapipe.md). Pruebas con manos sintéticas: `tests/gestos/`.
