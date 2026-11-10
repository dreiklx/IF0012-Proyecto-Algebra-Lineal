# Revisión del chat «Configuración profesional de MediaPipe y OpenCV para Windows»

**Fecha de la revisión:** 10-nov-2026.

**Fuente:** conversación fijada en claude.ai, proyecto «Mediapipe».

- 35 mensajes, del 19-jun al 16-jul-2026.
- Se hizo en el equipo de un integrante del grupo.
- No se copian aquí rutas personales ni datos de ese equipo.

**Acceso:**

- Se leyeron completos los 35 mensajes y los adjuntos de texto de los mensajes 4, 6, 8 y 18.
- También se leyeron las dos respuestas alternativas al mensaje 28, que son los mensajes 29 y 30.
- No hubo partes inaccesibles.
- Los documentos Word que se generaron en el chat (guía de 8 y de 12 páginas) no se descargaron; se usó el texto del chat que los describe.

## 1. Qué se hizo en el chat

| Etapa | Mensajes | Contenido |
|---|---|---|
| Objetivo | 0-1 | Guía por fases: diagnóstico, limpieza, instalación limpia, validación, prueba de MediaPipe Hands y depuración de 13 errores. El destino final era una aplicación **Java Swing (JDK 1.8, Eclipse)** |
| Diagnóstico | 3-9 | Había un único Python 3.13 instalado con Laragon, sin el lanzador `py`. Tenía instalados **a la vez** `opencv-python` y `opencv-contrib-python` 4.13 (conflicto), con mediapipe 0.10.35 y numpy 2.4. En PowerShell, `where` es un alias de `Where-Object`: hay que usar `where.exe`. Se desactivó el alias de Python de la Microsoft Store |
| Instalación | 11-13 | Python 3.11.9 de python.org, con el lanzador `py` y un entorno virtual. Se recomienda no instalar `opencv-python` aparte |
| Problema central | 14-21 | `mp.solutions` daba `AttributeError`. Se verificó que el wheel oficial de **mediapipe 0.10.22 en adelante ya no trae `mediapipe/python`, ni el `.pyd`, ni `solutions`**: solo `tasks` y `modules`. La 0.10.21 era la última con `solutions` para cp311 |
| Descarga | 22-24 | Un `IncompleteRead` al bajar `jaxlib` se resolvió con `--timeout 120 --retries 10`. Resultado final: mediapipe 0.10.21, numpy 1.26.4, `mp.solutions.hands` funcionando |
| Prueba | 25 | `hands_test.py` con `VideoCapture(0, CAP_DSHOW)`, espejo, BGR → RGB, `Hands(model_complexity=0, max_num_hands=2, 0.5, 0.5)` y dibujo de los 21 puntos |
| Errores | 27 | Guía de 13 errores, entre ellos: «DLL load failed» → instalar VC++ Redistributable; «camera not found» → probar otro índice o `CAP_DSHOW`; «cannot open» → la cámara está ocupada o falta permiso |
| Integración con Java | 29-32 | Servidor Python por **socket TCP 127.0.0.1:5005** que envía los landmarks como texto. Protocolo: manos separadas por `\|`, puntos por `;`, coordenadas `x,y,z` con 4 decimales. Del lado Java, un cliente con 7 clases (`HandLandmark`, `Hand`, `HandDataParser`, `HandDataListener`, `HandTrackingClient`, `HandPanel`, `MainApp`) |
| Arquitectura | 33-34 | N capas / MVC: «el transporte lleva puntos crudos y el significado se construye hacia adentro». `GestureRecognizer` con reglas Strategy (`FistRule`, `OpenPalmRule`, enum `Gesture`). `MotionService` con suavizado lerp de 0,3 sobre la punta del índice. `SceneModel` como frontera entre hilos. `SceneView` repinta con un Timer de 16 ms |

## 2. Qué sirve para Ax y qué no

| Del chat | En Ax | Motivo |
|---|---|---|
| `mp.solutions.hands` (mediapipe ≤ 0.10.21) | **No se usa.** Se usa la API **Tasks** (`HandLandmarker`) de mediapipe 1.2.2 | Ax corre en Python 3.13 y 0.10.21 no tiene wheels para 3.13. Se verificó en PyPI el 10-nov que 1.2.2 publica `py3-none-win_amd64` |
| `opencv-python` + `opencv-contrib-python` juntos | **Solo `opencv-contrib-python`**, que instala MediaPipe como dependencia | Evita el conflicto que encontró el chat |
| `VideoCapture(0, CAP_DSHOW)`, espejo, BGR → RGB | **Igual**, en `gestos/captura.py` y `gestos/deteccion.py` | Es la opción probada en Windows |
| Servidor TCP + cliente Java | **No se usa Java.** El servidor local de Ax envía solo la cámara (9 números) a la gráfica | Ver [portabilidad_java_python.md](portabilidad_java_python.md) |
| Reglas Strategy, enum de gestos, lerp de 0,3 | **Se adoptan en Python:** `gestos/interpretacion.py` (reglas y máquina de estados) y `gestos/movimiento.py` (suavizado con α = 0,35) | Misma idea, sin clases Java |
| `SceneModel` como frontera entre hilos | `ControlGestual` con candado y copia del estado. El hilo de visión **nunca** llama a `st.*` | Es la misma regla de diseño |
| Guía de 13 errores | Los mensajes de `gestos/captura.py` cubren «no hay cámara», «ocupada» y «privacidad de Windows» | El ratón sigue funcionando siempre |

## 3. Datos del chat que no se trasladan

- Las rutas y el usuario de Windows del integrante.
- Los comandos de PowerShell específicos de ese equipo (Laragon, desactivar alias de la Store).
- Los documentos Word.
