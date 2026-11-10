# Del diseño Java del chat a Python en Ax

**Fecha:** 10-nov-2026.

**Regla del equipo:** Ax es solo Python.

- No hay archivos `.java`, ni JVM, ni Gradle.
- La única excepción es un puente JavaScript mínimo, aprobado por el equipo el 10-nov (sección 3).

## 1. Correspondencia de piezas

| Chat (Java Swing + servidor Python) | Ax (Python) | Archivo |
|---|---|---|
| `hand_server.py`: captura + MediaPipe + socket TCP | Captura y detección en un hilo del mismo proceso de Streamlit, sin socket de landmarks | `gestos/captura.py`, `gestos/deteccion.py` |
| `HandLandmark` (inmutable), `Hand` (21 puntos y `CONNECTIONS`) | `Punto` y `Mano` (dataclasses congeladas), `CONEXIONES` | `gestos/mano.py` |
| `HandDataParser` (texto → objetos) | No hace falta: MediaPipe entrega los objetos dentro de Python | — |
| `GestureRecognizer` + `GestureRule` (Strategy) + enum `Gesture` | `clasificar(mano)`, con reglas por gesto y constantes `PALMA`, `PUNO`, `PINZA`, `VICTORIA` | `gestos/interpretacion.py` |
| `MotionService` (lerp 0,3) | `Suavizador` (media exponencial, α = 0,35) y `CamaraOrbital` | `gestos/movimiento.py` |
| `SceneModel` (volatile, snapshots, cola) | `ControlGestual`: candado, copia del estado y acciones aplicadas dentro del candado | `gestos/control.py` |
| `HandTrackingClient implements Runnable` | Hilo `gestos-vision` con un evento de parada | `gestos/control.py` |
| `SceneView` con `javax.swing.Timer(16 ms)` | Plotly en el navegador: el puente aplica la cámara en cada cuadro (`requestAnimationFrame`) | `interfaz/compartido/puente_camara.js` |
| `MainApp` (raíz de composición) | `interfaz/compartido/control_gestual.py`: crea un único `ControlGestual` por servidor (`st.cache_resource`) | — |

## 2. Por qué la cámara viaja por un canal propio (mediciones del 10-nov)

**Requisito:** girar la gráfica Plotly del Módulo I sin reconstruirla y sin que se trabe en una presentación.

**Cómo se midió:**

- Brave en modo sin cabeza (ANGLE / Direct3D11 sobre una RTX 4050 Laptop).
- Equipo con Ryzen 5 8645HS, 39 GB de RAM y Windows 11.
- La cámara 3D se leyó desde la gráfica en cada cuadro del navegador.

| Arquitectura probada (prototipos en el scratchpad, fuera del repositorio) | Cambios de cámara/s | Fluidez del navegador | ¿Vuelve a montar la gráfica? |
|---|---:|---|---|
| Fragmento `st.fragment(run_every=0,1 s)` que reenvía la figura con otra `scene.camera` | 1,5 | 28 fps; peor cuadro 674 ms | Sí (WebGL de nuevo) |
| Lo mismo con `on_select="rerun"` | 1,8 | 4,7 fps; peor cuadro 715 ms | Sí |
| Lo mismo cada 0,25 s | 3,3 | 17 fps; peor cuadro 302 ms | Sí |
| Vista 3D renderizada en Python (Matplotlib) y enviada como imagen | 4,5–6,2 | 60–144 fps | No, pero cada render cuesta 120–157 ms en Python |
| Componente v2 que recibe la cámara por **rerun** y llama a `Plotly.relayout` | ~1,3 (Python ejecutó el fragmento 12 veces/s, pero Streamlit agrupa las actualizaciones) | 60 fps | No |
| **Componente v2 + Server-Sent Events desde un servidor Python local (elegida)** | **29,7** (la fuente emitía 30/s) | **60 fps; peor cuadro 18–34 ms** | **No** |

**Conclusiones:**

- **Sin código de frontend no se puede** mover la gráfica Plotly con fluidez.
- Se detuvo el trabajo y se consultó al equipo, que eligió el puente JS mínimo.

**Qué hace el puente** (`puente_camara.js`, unas 50 líneas):

- recibe la cámara (`eye`, `center`, `up`) desde `http://127.0.0.1:<puerto>/camara`;
- la aplica con `window.Plotly.relayout` sobre la gráfica que ya dibujó `st.plotly_chart`;
- cuando el ratón mueve la vista, la envía a Python (`POST /raton`), para que la siguiente pinza continúe desde ahí.

**Qué no hace:** no usa la cámara web, no recibe imágenes y no hace cálculos.

## 3. Seguridad y privacidad del canal

- `ThreadingHTTPServer` de la biblioteca estándar, ligado a **127.0.0.1**: no es accesible desde otra máquina.
- Usa un puerto libre, que elige el sistema.
- Exige un **token aleatorio** (`secrets.token_urlsafe`). Cualquier otra petición recibe 403.
- Solo viajan 9 números de cámara. **Ninguna imagen** sale del hilo de visión. Los fotogramas se procesan en memoria y se descartan; no hay grabación ni archivos.
- El canal se cierra con «Detener», con el perro guardián o ante un error.

## 4. Riesgo aceptado

`window.Plotly` lo publica el propio Streamlit 1.66.1, que la aplicación instala con la versión fijada en `requirements.txt`. No es una API documentada de Streamlit. Si una versión futura dejara de exponerlo:

- el puente no hace nada;
- el ratón sigue funcionando;
- el panel sigue mostrando el estado.
