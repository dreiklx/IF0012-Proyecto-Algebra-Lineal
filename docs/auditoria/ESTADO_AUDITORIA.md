# Estado de la auditoría completa de Ax (checkpoint)

Fecha: 13-nov-2026. Repositorio: `main` = `origin/main` = `046ba9f`. Suite: 331 pruebas OK.

**Este archivo es un checkpoint, no una conclusión.** La auditoría NO está terminada.

## 1. Causa de las interrupciones anteriores (verificada)

No es un límite de turnos ni de contexto, ni permisos, ni CLAUDE.md (el proyecto no tiene `CLAUDE.md` ni `.claude/`).

La causa es el plugin **context-mode** (`~/.claude/settings.json`, activado). Su hook `PreToolUse` deniega la
lectura directa de archivos por encima de un tamaño (observado: aprox. 13–17 KB; mensaje
«over the one-read limit», código en `plugins/cache/context-mode/.../hook.mjs`). Además sustituye
las salidas grandes de Bash por un resumen («searches the whole output»).

Consecuencias observadas:
- Las imágenes de página de los PDF se rechazaban al leerlas con la herramienta Read.
- Las salidas largas de comandos se sustituían por un mensaje de búsqueda, no por el texto.

Solución aplicada: imágenes de cuadrante de ~480 px, en escala de grises y con calidad 20 (ok con el límite), y
comandos con salida corta. No se ha desactivado ningún mecanismo de seguridad. Pendiente de decisión
del usuario: si quiere que el plugin no bloquee las lecturas de imagen, debe cambiarse su configuración.

## 2. Inventario de fuentes (verificado)

18 PDF y 457 páginas (ver `inventario_fuentes.csv`). Además, un ZIP de soluciones de estudiantes
(`TareaII_Algebra_Derek-Daniel.zip`, 8 JPEG) que no es material de la profesora.

## 3. Primera auditoría (página a página)

Registro: `primera_auditoria_completa.csv` (457 filas).

| Estado | Páginas |
|---|---:|
| Revisada visualmente y comparada con Ax | 9 |
| Revisada visualmente (parcial) | 3 |
| Pendiente de revisión visual | 443 |

**Incompleta.** Faltan 443 páginas por revisar visualmente. No se ha revisado ninguna página de los
documentos de Módulo I (S2-17, S2-19 salvo p. 38, S3-24, S3-26, S6-14, S6-16 salvo p. 29) de forma sistemática.

## 4. Segunda auditoría

No iniciada. `segunda_auditoria_completa.csv` y la reconciliación no existen todavía.

## 5. Procedimientos y pruebas

Matriz: `matriz_fidelidad_academica.md` (con estados «Pendiente de verificación» en varias filas).
Pruebas de referencia: 16 (`tests/referencia_profesora/`). Cobertura **no** completa.

## 6. Pasos para reanudar (orden)

1. Por documento, en el orden del inventario: revisar cada página en cuadrantes (480 px, gris) y registrar el resultado.
2. Tras cada documento: actualizar la fila de `primera_auditoria_completa.csv`, las pruebas que correspondan y la matriz.
3. Commit por documento.
4. Terminada la primera pasada: segunda pasada independiente (nuevo registro), y reconciliación.
5. Solo después: guías, limpieza de comentarios, ZIP y SHA-256.

No se debe declarar ninguna auditoría completa mientras existan filas «Pendiente».

## 7. Desactivación de context-mode (13-nov-2026)

- Configuración original: `~/.claude/settings.json`, línea `"context-mode@context-mode": true`.
- Respaldo: `~/.claude/settings.json.bak-antes-context-mode-20261113-020036`.
- Cambio: `"context-mode@context-mode": false`. JSON validado. Resto de la configuración intacta.
- No hay `hooks` de context-mode en `settings.json`: el hook `PreToolUse` lo registra el propio plugin al cargarse.
- **Prueba:** tras el cambio, la lectura de `s905_p19.jpg` (191 KB) seguía bloqueada en la sesión actual. Los plugins se cargan al iniciar Claude Code: hace falta reiniciarlo para que el cambio tenga efecto.
- Pendiente: reiniciar Claude Code y repetir la prueba de lectura antes de continuar la auditoría.
