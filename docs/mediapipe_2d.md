# Control gestual de la gráfica 2D del Módulo IV

Extensión de experiencia de usuario (Cat. C, incentivo «Experiencia de usuario», 0,5 %).
Reutiliza la captura, la detección, la interpretación y el hilo de `gestos/` que ya controlan
la gráfica 3D del Módulo I. **No calcula nada del álgebra**: solo cambia el rango visible de
los ejes de la gráfica de convergencia.

## Qué cambia y qué no

| Cambia | No cambia |
|---|---|
| Rango visible de los ejes X e Y de la gráfica de convergencia | `algebra/` (ningún archivo) |
| Estado del panel «Control con gestos» del Módulo IV | Iteraciones, historiales, errores d_k y r_k, códigos de terminación |
| Acción de zoom y desplazamiento | Criterios de parada y tolerancia |
| Vista inicial al pulsar «⟲ Vista inicial» o la palma de victoria | Selección de iteración (clic o deslizador) y tabla de la zona seleccionada |

## Arquitectura

```text
cámara ─► captura ─► deteccion ─► interpretacion ─► ControlGestual ─┬─ CamaraOrbital  → puente 3D (Módulo I)
                                  (InterpreteGestos)  (hilo, latido) └─ VistaPlano2D    → puente 2D (Módulo IV)
                                                                          │
                                       servidor SSE 127.0.0.1 ─► puente_camara.js (data.tipo = "2d")
```

| Archivo | Función |
|---|---|
| `gestos/vista2d.py` | `VistaPlano2D`: `girar`, `zoom`, `restablecer`, `desde_plotly`, `a_plotly`. `rango_inicial(historial, tolerancia)` calcula el rango por defecto en log10 |
| `gestos/control.py` | `ControlGestual(destino=...)`: acepta la vista 2D sin cambios en el hilo |
| `interfaz/compartido/control_gestual.py` | `panel(clave, tipo, rango_inicial)`, `rango_para_figura`, exclusión mutua entre objetivos |
| `interfaz/compartido/puente_camara.js` | `data.tipo === "2d"`: aplica `xaxis.range`/`yaxis.range` y envía al ratón solo los rangos |
| `interfaz/modulos/modulo_IV_iterativos/pestana_ejecutar.py` | `explorar_convergencia`: aplica el rango gestual a la figura y muestra el panel |

El cálculo de la vista está separado de la cámara: `VistaPlano2D` no importa MediaPipe ni
Streamlit, y `CamaraOrbital` no cambia.

## Gestos (mismos que en 3D)

| Gesto | Acción en la gráfica 2D |
|---|---|
| ✋ Palma abierta, ½ s | Activa el control y calibra la pinza |
| 🤏 Pinza con una mano que se mueve | Desplaza la vista: la gráfica sigue a la mano (X y Y) |
| 🤏🤏 Dos pinzas que se separan | Acerca (reduce el rango alrededor del centro) |
| 🤏🤏 Dos pinzas que se juntan | Aleja (amplía el rango) |
| ✊ Puño, ½ s | Pausa: no se mueve nada hasta que vuelva la palma |
| ✌️ Victoria, ≈ 1 s | Restablece la vista inicial |

**Conflictos evaluados:** el puño, la palma y la victoria se distinguen por la extensión de
los dedos; la pinza se distingue del puño por la distancia de la punta del índice a la
muñeca. Una sola pinza gira la vista y dos pinzas hacen zoom: el intérprete ya impide que
ambas acciones se mezclen (`interpretacion.py`, `actualizar`).

**Estabilidad:** antirrebote de 0,35 s (puño y palma) y 0,8 s (victoria); histéresis de la
pinza; suavizado exponencial del punto de agarre; zona muerta acumulada de 0,004 del ancho
de la imagen, que se aplica al desplazamiento acumulado para que el temblor no mueva la vista.

**Límites de zoom:** el ancho visible queda entre 5 % y 400 % del inicial (`ESCALA_MIN`,
`ESCALA_MAX`), así la vista nunca desaparece ni se vuelve ilegible.

## Objetivo activo

- Una sola cámara: solo un control está activo a la vez.
- Al pulsar «Activar» en un módulo, el control del otro objetivo se detiene.
- El panel muestra «Objetivo de los gestos» con el nombre de la gráfica controlada.
- Si el usuario cambia de módulo, el latido deja de llegar y la cámara se apaga en 4 s.

## Privacidad y permisos

- La cámara se enciende solo con el botón; nunca al cargar la página.
- Los fotogramas se procesan en memoria y se descartan. No se guardan ni se envían.
- Solo viajan 127.0.0.1 los rangos (cuatro números), con token.
- Al detener, al salir del módulo o ante un error se libera la cámara y se informa el motivo.
- El ratón sigue funcionando: `plotly_relayout` del ratón se envía a Python para mantener la vista.

## Pruebas

| Archivo | Qué prueba | Tipo |
|---|---|---|
| `tests/gestos/test_vista2d.py` | Desplazamiento (sentido, proporción, zona muerta), zoom (centro, límites, temblor), restablecer, entrada del ratón parcial y completa, rango inicial, gestos sobre la vista | **Sintética** |
| `tests/gestos/test_vista2d.py` (`TestControlConVistaDosD`) | Hilo de control con cámara y detector falsos; liberación de la cámara; perro guardián | **Sintética** (no se abre ninguna cámara) |
| `tests/gestos/test_control.py`, `test_interpretacion.py`, `test_movimiento.py` | Ya existentes para 3D | Sintética |
| `tests/interfaz/test_control_gestual.py` | Panel, botones y estado | Interfaz (sin cámara) |

**Qué NO está probado:** ningún gesto ha sido reconocido con una mano real frente a una
cámara. Las manos de las pruebas son geometrías construidas en `tests/gestos/manos_sinteticas.py`.

## Validación física

- **Confirmada por el usuario (12-nov-2026):** la navegación 2D se probó personalmente con cámara
  en Brave. El comportamiento se considera correcto y no se modificó tras la prueba.
- Los resultados de las pruebas automatizadas (`tests/gestos/test_vista2d.py`) siguen siendo
  sintéticos; la validación física es la prueba con mano real del usuario.

## Validación física adicional (opcional)

1. Abrir Ax en Brave: `http://localhost:8501`, módulo IV, pestaña «Ejecutar».
2. Pulsar «📷 Activar cámara y gestos» en el panel 2D y mostrar la palma durante medio segundo.
3. Probar cada gesto: pinza, dos pinzas que se separan y juntan, puño, victoria.
4. Comprobar que el texto «Mano: …» y el estado coinciden con lo que se hace.
5. Anotar cualquier gesto que se dispare solo; ajustar los umbrales en `interpretacion.py` solo con evidencia.

Si la cámara falla durante la defensa: el ratón (arrastrar, rueda y los botones de Plotly)
funciona igual.
