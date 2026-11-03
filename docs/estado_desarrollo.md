# Estado del desarrollo

**Última actualización:** 03-nov-2026, comparación con los PDF de la docente y auditoría de las dos rúbricas. El historial completo está en `git log`.

## Datos del proyecto

| Dato | Valor |
|---|---|
| Curso | IF0012 Álgebra Lineal para Informática Empresarial, II Ciclo 2026 |
| Integrantes | Elmer López Hernández, Derek Farley Noguera, Daniel Córdoba Arias, Samir Sandoval Ramírez |
| Entrega | **11 de noviembre de 2026** |
| Defensa individual | Semana del **16 de noviembre de 2026** |
| Número de grupo (01 o 02) | **01, con evidencia fuerte:** el horario del escritorio coincide con el del grupo 01 en el programa (PROG p. 9). Falta que los demás integrantes lo confirmen |

## Revisión del 03-nov-2026: comparación con los PDF y rúbricas

1. **Inventario y lectura de los PDF.** Se usó el inventario de la auditoría documental (19 archivos). Se releyeron en imagen las páginas clave:
   - mínimos cuadrados: S8-30/09 pp. 6-7;
   - condicionamiento: S7-21/09 pp. 17-18;
   - comparación y SOR: S9-05/10 pp. 16-17;
   - precondicionamiento: S9-05/10 pp. 21-24;
   - matrices de iteración y ρ: S9-07/10 pp. 4 y 6.

   También se releyeron el enunciado oficial completo (texto) y PROG p. 9. **No inspeccionados visualmente:** las semanas 1, 2 y 4 y el Quiz (Tema 1, sin procedimientos del proyecto). Resultado en [comparacion_procedimientos.md](comparacion_procedimientos.md).
2. **Hallazgos:**
   - **«Error final» = ‖x⁽ᵏ⁾ − x‖∞** según la lámina S9-05/10 p. 17. Coincide con nuestro e. P-4 resuelto.
   - **Grupo 01** por el horario. P-1 casi resuelto.
   - **Precondicionamiento:** la lámina indica qué comparar (κ y ρ de A frente a B = D⁻¹A).
   - **Procedimientos de clase no visibles en la aplicación:** det([A|b]) y Cramer en mínimos cuadrados; Sarrus en det(T − λI); reordenamiento de ecuaciones para lograr la dominancia.
3. **Implementado:**
   - `algebra/precondicionamiento.py`, con la pestaña «Precondicionamiento diagonal», y `paso_richardson`;
   - `minimos.cramer` y `det_aumentada`, con el desplegable de verificación del procedimiento de clase;
   - `espectral.desarrollo_sarrus`, mostrado para T 3×3;
   - `espectral.analizar_matriz`, una refactorización sin cambio de resultados: los 300 casos aleatorios y los ejemplos precargados dan lo mismo que el 02-nov;
   - `iterativos.reordenamiento_dominante`, mostrado en «Convergencia»;
   - e_k como primera métrica de la gráfica comparativa;
   - la gráfica del precondicionador recorta las curvas divergentes.
4. **Defecto corregido:** con un aᵢᵢ = 0, la pestaña «Convergencia» no mostraba ni la dominancia ni el reordenamiento, porque fallaba al construir T. Ahora los muestra junto con el error (prueba `test_modulo_IV_reordenamiento_y_sarrus`).
5. **Pruebas nuevas (17):**
   - `tests/test_precondicionamiento.py` (14), con oráculos de la lámina, a mano y de la teoría de la tridiagonal;
   - 3 pruebas de interfaz.
   - Auditoría nueva: `auditoria/auditoria_precondicionamiento.py`, 150 casos y 0 fallos.
6. **Revisión visual (Chrome, 03-nov):**
   - pestaña «Precondicionamiento diagonal» de la aplicación real con el ejemplo S: matrices, κ, autovalores, tabla y gráfica;
   - HTML de la guía: portada, índice, tablas, fórmulas y listas, sin restos de Markdown. Se corrigieron una tabla duplicada y asteriscos y guiones bajos mal interpretados.
7. **Documentación actualizada:**
   - matriz de cumplimiento con las dos rúbricas (`auditoria_requisitos.md`);
   - manual;
   - guía de defensa (34 preguntas) y resumen;
   - guía matemática §10;
   - decisiones técnicas #25 y #28-31;
   - casos III-6 e IV-23 a IV-26;
   - pendientes con la docente.
8. **HTML para compartir:** `C:\Users\dfarl\Desktop\Guia_Defensa_IF0012.html`, un solo archivo sin dependencias externas. Contiene la guía completa y el resumen.

## Revisión del 02-nov-2026: qué se hizo

1. **Requisitos.** Se releyó el enunciado oficial (pp. 1-5) y se rehízo la matriz de cumplimiento con los estados COMPLETADO, INCOMPLETO, FALLIDO y PENDIENTE DE CONFIRMACIÓN EXTERNA. Ver [auditoria_requisitos.md](auditoria_requisitos.md). **Ningún requisito queda FALLIDO.**
2. **Revisión matemática de los cuatro módulos.** Se leyeron completos `matriz`, `validacion`, `directos`, `condicion`, `minimos`, `iterativos`, `espectral` y `dispersas`, y las interfaces.
   - Se comprobaron:
     - las fórmulas: Gauss, Gauss-Jordan, determinante, κ∞, ecuaciones normales, los tres pasos iterativos, T_J, T_GS, T_ω, Faddeev-LeVerrier, Schur-Cohn y Durand-Kerner;
     - el tratamiento de los casos especiales;
     - la coherencia entre lo que se calcula y lo que se muestra.
   - **No se encontró ningún error matemático, así que no se modificó el código del núcleo ni de la interfaz.**
   - Pruebas adicionales ejecutadas en esta revisión:
     - casos límite: matriz cero (infinitas o inconsistente), sistemas 1×1, 3×2 consistente e inconsistente, 1×3 y 2×3, inversa 1×1, κ(I) = 1, mínimos cuadrados cuadrado y subdeterminado, iterativos con n = 1, SOR con ω = 1 igual a GS, y radio espectral en 2×2 con raíces complejas o λ = ±1;
     - tiempos: ρ para n = 8 en 0.03 s; comparación con n = 50 en 0.07 s;
     - **todos los ejemplos precargados** recalculados con oráculos escritos aparte: Cramer con determinantes de Leibniz (I), inversa por adjunta (κ), fórmula cerrada de la recta (III) y fórmula de Gelfand ‖T¹²⁸‖^(1/128) (ρ). Todos coinciden.
3. **Nuevo caso verificado (IV-22).** En S9-07/10 con SOR y ω = 6/5 (el ω por defecto), λ = −1 es autovalor exacto: det((2 − ω)D + ωL − ωU) = 0, comprobado a mano. Se añadió la prueba `test_sor_s9_omega_6_5_autovalor_menos_uno_exacto`, de modo que ahora hay **185 pruebas**.
4. **Revisión visual pendiente.** La gráfica de convergencia de una ejecución individual (criterios A y B, sistema S) se generó como imagen y se revisó: d₇ = 3.78·10⁻⁴ < ε y r₇ = 8.79·10⁻⁴ < ε, como en IV-1 e IV-4. **Siguen sin verse dentro del navegador** la figura 3D y el espaciado de las fracciones.
5. **Correcciones de documentación.**
   - La precisión con raíces múltiples ahora es exacta: ≈10⁻⁸ en una raíz doble, que suele decidirse con la banda de 10⁻⁶, y ≈10⁻⁵ en una triple, que queda «indeterminado».
   - Se añadieron `dispersas.py` y `auditoria/` al árbol de `arquitectura.md`.
6. **Documentos nuevos:**
   - [guia_defensa_equipo.md](guia_defensa_equipo.md): guía completa para el equipo;
   - [resumen_logica_por_modulo.md](resumen_logica_por_modulo.md): resumen de estudio;
   - [pendientes_docente.md](pendientes_docente.md): pendientes con la docente, con su interpretación provisional y la pregunta exacta.

## Pruebas: resultados reales (03-nov-2026)

```
.venv\Scripts\python -m unittest
Ran 202 tests ... OK            (0 fallos, 0 omitidas; 03-nov-2026)
```

| Archivo | Pruebas | Qué cubre | Tipo de oráculo |
|---|---:|---|---|
| test_matriz | 47 | Validación, operaciones, normas, residuo | Valores calculados a mano y ejemplos del curso |
| test_validacion | 13 | Lectura de texto, parámetros, formato | Casos construidos a mano |
| test_directos | 26 | Gauss, Gauss-Jordan, clasificación, inversa, determinante | Sustitución a mano; inversa por adjunta |
| test_condicion | 13 | κ∞, escala, perturbaciones | Inversa 2×2 por fórmula; estructura I + 10J |
| test_minimos | 10 | Ecuaciones normales, residuo, ajuste | Cramer; fórmula cerrada de la recta; Aᵀr = 0 |
| test_iterativos | 31 | Jacobi, GS y SOR, criterios A/B/C, motivos, comparación | Programa independiente, manuscritos y el ZIP de la Tarea II |
| test_espectral | 25 | T, polinomio, autovalores, ρ, regresiones | Sarrus a mano, formas cerradas, bisección, teoría tridiagonal, determinante a mano (IV-22) |
| test_dispersas | 8 | Formato CSR | Construcción a mano; igualdad con la versión densa |
| test_precondicionamiento | 14 | Precondicionador M = D, Richardson, reordenamiento, Sarrus, Cramer | Lámina S9-05/10 diap. 18; inversas 2×2 a mano; autovalores teóricos de la tridiagonal; manuscrito S8-30/09 |
| test_app | 15 | La interfaz con AppTest (sin navegador) y el CSV | **Superficiales:** comprueban que no hay excepciones y que aparecen los mensajes, **no** el contenido visual de las gráficas |

**Auditoría independiente** (`auditoria/`, semilla fija) — **0 fallos**:

- 4500 sistemas;
- 400 inversas, determinantes y κ;
- 200 perturbaciones;
- 300 mínimos cuadrados;
- 600 ejecuciones iterativas;
- 300 análisis espectrales aleatorios (0 indeterminados, 0 no fiables);
- casos difíciles: con raíces casi iguales, escalas muy distintas o ρ = 0.999999 el resultado es fiable; con el par complejo doble y la raíz cuádruple se marca «no fiable», como corresponde.

## Limitaciones conocidas (no resueltas)

1. **Autovalores múltiples.** Con raíces triples o de mayor multiplicidad ρ suele quedar «indeterminado». Con raíces dobles se decide con la banda de 10⁻⁶ y un aviso.
2. Las gráficas no tienen pruebas automáticas de su contenido visual.
3. La instalación se probó en entornos virtuales nuevos **en este equipo**, no en otro computador.
4. Streamlit y Matplotlib instalan NumPy como dependencia interna. Ningún archivo del proyecto lo importa.

## Empaquetado

Ver la sección «Verificación del ZIP», al final de este archivo.

## Pendientes

Los que dependen de la docente están detallados en [pendientes_docente.md](pendientes_docente.md), con la pregunta exacta para cada uno.

| # | Pendiente | Impacto | Quién |
|---|---|---|---|
| P-1 | **Número de grupo**: evidencia fuerte de que es el 01 | Falta que los demás integrantes lo confirmen | Grupo |
| P-2 | **Autorización expresa del uso de IA** (PROG p. 7 §6.2) | Integridad académica: **prioridad máxima** | Grupo → docente |
| P-3 | **Caso de validación obligatorio** | C-07 (3 %) | Docente |
| P-4 | Significado de «error final» | **Resuelto** con la lámina S9-05/10 p. 17 | — |
| P-5 | Alcance del radio espectral (métodos que no se vieron en clase) | M4-05 | Docente |
| P-6 | NumPy como dependencia interna | Resuelto por el enunciado; confirmación opcional | — |
| P-7 | Perturbación porcentual | Resuelto: ‖Δb‖/‖b‖ = p/100 en ambas lecturas; confirmación opcional | — |
| P-8 | Precondicionamiento | **Implementado** con la comparación de la lámina; confirmación opcional | — |
| G-1 | Una persona ajena sigue el manual en **otro** equipo | C-06, lista de verificación | Grupo |
| G-2 | Cada integrante instala, ensaya la demostración y estudia la guía | Defensa (35 %) | Los 4 integrantes |
| G-3 | Mirar dentro del navegador la figura 3D y las fracciones | C-05 (estético) | Grupo |

## Verificación del ZIP

ZIP generado el 03-nov-2026 con `python empaquetar.py 01`: `dist/Grupo01-IF0012-Proyecto-IIC.zip`. El número 01 tiene evidencia fuerte, pero falta la confirmación del grupo.

- **Contenido:** 63 archivos, una sola carpeta raíz (`Grupo01-IF0012-Proyecto-IIC/`) y `testzip` sin errores. Incluye `algebra/precondicionamiento.py`, `tests/test_precondicionamiento.py`, `auditoria/auditoria_precondicionamiento.py` y `docs/comparacion_procedimientos.md`.
- **Exclusiones:** sin `.venv`, `__pycache__`, `.pyc`, `.git`, `dist`, imágenes ni `secrets.toml`.
- **Prueba en una copia limpia** (03-nov):
  - el ZIP se extrajo en una carpeta nueva;
  - `ejecutar.bat` creó `.venv` (Python 3.14.1) e instaló las dependencias;
  - el servidor respondió `ok` a los ~58 s (puerto 8502);
  - en esa copia: **202 pruebas OK** y las 3 auditorías con **0 fallos**.
- **Candidatos anteriores** (27-oct y 02-nov): se conservaron, sin sobrescribirlos, en `dist/anteriores/`.
- **Después de la verificación** solo se modificó esta sección y se regeneró el ZIP. El SHA-256 final está en `dist/SHA256.txt`.
- **Si el grupo resultara ser el 02:** `python empaquetar.py 02`.
