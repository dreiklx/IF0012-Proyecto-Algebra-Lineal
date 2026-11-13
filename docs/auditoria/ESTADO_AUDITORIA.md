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

## 8. Pasada nocturna 13-nov-2026 (checkpoint)

Rama de trabajo: `auditoria/primera-pasada` (no se integra en `main` hasta cerrar todas las fases).

- **Fase 1 (context-mode):** desinstalado con `claude plugin uninstall context-mode@context-mode --scope user --keep-data` (datos conservados). Ya no figura en `installed_plugins.json` ni en `claude plugin list`. Caché inerte `plugins/cache/context-mode` no eliminada. Copias de seguridad: `~/.claude/backups-doctor-20261113-021851/`.
  - Pruebas: imágenes de 84 KB y 70 KB leídas sin bloqueo; texto de 17 KB leído completo; varias imágenes seguidas sin bloqueo.
  - Salida Bash de 44,8 KB: el harness la guarda en archivo (límite de salida, no context-mode) y ese archivo se lee completo.
- **Fase 2 (respaldo):** rama `backup/antes-auditoria-final-7acc153` y etiqueta `restore/7acc153` en el commit `7acc153`. Suite base: 331 pruebas OK.
- **Fase 3 (inventario):** 18 PDF, 457 páginas: 20 de documentos oficiales (enunciado, tarea, instrucciones) y 437 de material de clase. ZIP de estudiantes excluido. Sin texto en páginas de imagen: se trabaja con imagen.
- **Fase 4 (primera pasada):** renders en carpeta temporal fuera del repo, generados con `herramientas/renderizar_fuentes.py` (1600 px). Revisadas: 3 de 457 (`IF0012-IITarea…pdf` p. 1-3). Pendientes: 454. Las 14 filas de la revisión previa figuran como «Pendiente» hasta verificarse.
- **Fases 5-15:** no iniciadas.

Próximo paso: continuar la primera pasada en el orden del inventario, desde `IF0012_Álgebra…pdf` p. 1.

## 9. Reanudación 13-nov-2026 (verificada)

- Repositorio local: rama `auditoria/primera-pasada`, HEAD `c7e977a`, árbol limpio. `main` = `origin/main` = `7acc153`.
- Respaldo de esta etapa: rama `backup/antes-auditoria-completa-c7e977a` y etiqueta `restore/c7e977a` (`c7e977a`), subidas a origin. Rama `auditoria/primera-pasada` subida a origin. No se borró ni forzó nada.
- Suite: `.venv\Scripts\python.exe -m unittest` → 331 pruebas OK.
- ZIP `dist/Grupo01-IF0012-Proyecto-IIC.zip`: SHA-256 `990a81b6…008fe`, coincide con `dist/SHA256.txt`.
- context-mode: desinstalado (no aparece en `claude plugin list`; ausente de `enabledPlugins`). Entrada residual en `extraKnownMarketplaces` (inofensiva, pendiente de limpiar).
- Prueba en sesión nueva: `s905_p19.jpg` (191 KB) leída completa sin bloqueo.
- Auditoría: primera pasada 3/457 revisadas visualmente, 454 pendientes. Segunda pasada no iniciada.

## 10. Progreso de la primera pasada (automático)

Revisadas: 262 de 457 páginas. Pendientes: 195.

| Documento | Revisadas/total |
|---|---|
| IF0012-IITarea-Álgebra Lineal-IIC26.pdf | 3/3 |
| IF0012_Álgebra_Lineal_para_Informática_Empresarial_II_2026.pdf | 12/12 |
| INTRUCCIONES-PROYECTO FINAL-ÁLGEBRA LINEAL-IIC2026.pdf | 5/5 |
| Semana01-10-08-2026-Álgebra Lineal-IIC.pdf | 24/24 |
| Semana01-12-08-2026-Álgebra Lineal-IIC.pdf | 28/28 |
| Semana02-17-08-2026-Álgebra Lineal-IIC.pdf | 40/40 |
| Semana02-19-08-2026-Álgebra Lineal.pdf | 48/48 |
| Semana03-24-08-2026-Álgebra Lineal-IIC26.pdf | 32/32 |
| Semana03-26-08-2026-Álgebra Lineal-IIC26.pdf | 38/38 |
| Semana04-02-09-2026-Álgebra Lineal-IIC26.pdf | 32/32 |
| Semana05-07-09-2026-Álgebra Lineal-Resolución I QUIZ.pdf | 0/8 |
| Semana06-14-09-2026-Álgebra Lineal-IIC26.pdf | 0/35 |
| Semana06-16-09-2026-Álgebra Lineal-IIC26.pdf | 0/36 |
| Semana07-21-09-2026-Algebra Lineal-IIC26.pdf | 0/20 |
| Semana08-28-09-20220-Álgebra Lineal-IIC26.pdf | 0/15 |
| Semana08-30-09-2026-Álgebra Lineal-IIC26.pdf | 0/40 |
| Semana09-05-10-2026-Álgebra Lineal-IIC26.pdf | 0/34 |
| Semana09-07-10-2026-Álgebra Lineal-IIC26.pdf | 0/7 |

Desglose de estados: Revisada visualmente: 261; Sin contenido matemático relevante: 1; Pendiente: 195
