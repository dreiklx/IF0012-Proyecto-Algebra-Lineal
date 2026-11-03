# Estado del desarrollo

**Última actualización:** 02-nov-2026, revisión completa del estado real. El historial completo está en `git log`.

## Datos del proyecto

| Dato | Valor |
|---|---|
| Curso | IF0012 Álgebra Lineal para Informática Empresarial, II Ciclo 2026 |
| Integrantes | Elmer López Hernández, Derek Farley Noguera, Daniel Córdoba Arias, Samir Sandoval Ramírez |
| Entrega | **11 de noviembre de 2026** |
| Defensa individual | Semana del **16 de noviembre de 2026** |
| Número de grupo (01 o 02) | **Sin confirmar.** El ZIP usa 01 de forma **provisional** |

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

## Pruebas: resultados reales (02-nov-2026)

```
.venv\Scripts\python -m unittest
Ran 185 tests ... OK            (0 fallos, 0 omitidas)
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
| test_app | 12 | La interfaz con AppTest (sin navegador) y el CSV | **Superficiales:** comprueban que no hay excepciones y que aparecen los mensajes, **no** el contenido visual de las gráficas |

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
| P-1 | **Número de grupo** (01 o 02) | Nombre del ZIP; regenerarlo tarda segundos (`python empaquetar.py 02`) | Grupo |
| P-2 | **Autorización expresa del uso de IA** (PROG p. 7 §6.2) | Integridad académica: **prioridad máxima** | Grupo → docente |
| P-3 | **Caso de validación obligatorio** | C-07 (3 %) | Docente |
| P-4 | Significado oficial de «error final» | M4-07 (riesgo bajo: se muestran d, r y e) | Docente |
| P-5 | Alcance del radio espectral (métodos que no se vieron en clase) | M4-05 | Docente |
| P-6 | NumPy como dependencia interna | Resuelto por el enunciado; confirmación opcional | — |
| P-7 | Perturbación porcentual | Resuelto: ‖Δb‖/‖b‖ = p/100 en ambas lecturas; confirmación opcional | — |
| P-8 | Comparación esperada en el precondicionamiento | Incentivo I-02 (opcional) | Docente |
| G-1 | Una persona ajena sigue el manual en **otro** equipo | C-06, lista de verificación | Grupo |
| G-2 | Cada integrante instala, ensaya la demostración y estudia la guía | Defensa (35 %) | Los 4 integrantes |
| G-3 | Mirar dentro del navegador la figura 3D y las fracciones | C-05 (estético) | Grupo |

## Verificación del ZIP

ZIP generado el 02-nov-2026 con `python empaquetar.py 01`: `dist/Grupo01-IF0012-Proyecto-IIC.zip`. El número 01 es **provisional**.

- **Contenido:** 59 archivos, una sola carpeta raíz (`Grupo01-IF0012-Proyecto-IIC/`) y `testzip` sin errores.
- **Exclusiones:** sin `.venv`, `__pycache__`, `.pyc`, `.git`, `dist`, imágenes ni `secrets.toml`.
- **Fines de línea:** `ejecutar.bat` tiene fin de línea CRLF.
- **Prueba en una copia limpia:**
  - El ZIP se extrajo en una carpeta nueva.
  - `ejecutar.bat` creó `.venv` (Python 3.14.1) e instaló Streamlit 1.66.1 y Matplotlib 3.11.2 (más NumPy 2.5.4 como dependencia interna).
  - El servidor respondió `ok` a los ~60 s. Se usó el puerto 8502 (`STREAMLIT_SERVER_PORT`) porque el 8501 estaba ocupado por la sesión de trabajo.
  - En esa copia: **185 pruebas OK** y auditoría independiente con **0 fallos**.
- **Candidato anterior:** el del 27-oct (SHA-256 `54f76588…6946c`) se conservó, sin sobrescribirlo, en `dist/anteriores/`.
- **Después de la verificación** solo se añadió esta sección a `estado_desarrollo.md` y se regeneró el ZIP. El SHA-256 final está en `dist/SHA256.txt`.
- **Si el grupo resulta ser el 02:** `python empaquetar.py 02`.
