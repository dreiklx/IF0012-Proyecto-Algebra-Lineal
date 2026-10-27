# Estado del desarrollo

**Última actualización:** 27-oct-2026, tras la auditoría final. El historial completo está en `git log`.

## Datos del proyecto (confirmados por el grupo)

| Dato | Valor |
|---|---|
| Curso | IF0012 Álgebra Lineal para Informática Empresarial, II Ciclo 2026 |
| Integrantes | Elmer López Hernández, Derek Farley Noguera, Daniel Córdoba Arias, Samir Sandoval Ramírez |
| Entrega | **11 de noviembre de 2026** |
| Defensa individual | Semana del **16 de noviembre de 2026** |
| Número de grupo (01 o 02) | **Sin confirmar**. Determina el nombre del ZIP |

## Pruebas: resultados reales

```
.venv\Scripts\python -m unittest
Ran 184 tests ... OK            (0 fallos, 0 omitidas)
```

| Archivo | Pruebas | Qué cubre | Tipo de oráculo |
|---|---:|---|---|
| test_matriz | 47 | Validación, operaciones, normas, residuo | Valores calculados a mano y ejemplos del curso |
| test_validacion | 13 | Lectura de texto, parámetros, formato | Casos construidos a mano |
| test_directos | 26 | Gauss, Gauss-Jordan, clasificación, inversa, determinante | Sustitución a mano; inversa por adjunta |
| test_condicion | 13 | κ∞, escala, perturbaciones | Inversa 2×2 por fórmula; estructura I + 10J |
| test_minimos | 10 | Ecuaciones normales, residuo, ajuste | Cramer; fórmula cerrada de la recta; Aᵀr = 0 |
| test_iterativos | 31 | Jacobi, GS y SOR, criterios A/B/C, motivos, comparación | Programa independiente (27-oct) más contrastes con manuscritos y el ZIP |
| test_espectral | 24 | T, polinomio, autovalores, ρ, regresiones de la auditoría | Sarrus a mano, formas cerradas, bisección, teoría tridiagonal |
| test_dispersas | 8 | Formato CSR | Construcción a mano; igualdad con la versión densa |
| test_app | 12 | La interfaz con AppTest (sin navegador) y el contenido del CSV | **Superficiales:** comprueban que no hay excepciones y que aparecen los mensajes esperados, **no** el contenido visual de las gráficas |

**Auditoría independiente** (`auditoria/`, unos 20 s, semilla fija):

- 4500 sistemas: rangos por menores (Leibniz), soluciones y direcciones;
- 400 inversas, determinantes y κ (adjunta);
- 200 perturbaciones (Cramer);
- 300 mínimos cuadrados (Cramer, Aᵀr = 0);
- 600 ejecuciones iterativas (implementación independiente);
- 300 análisis espectrales: cada λ anula det(T − λI) por Leibniz, el producto es igual a det(T) y ρ concuerda con Gelfand ‖Tᵏ‖^(1/k).

Resultado: **0 fallos**.

**Revisión visual manual** (Chrome, 27-oct):

- **Vistos:**
  - Módulo I: solución y pasos (fase VII).
  - Módulo II: κ, inversa, tabla de perturbación y errores.
  - Módulo III: ecuaciones normales, x̂, residuos y la gráfica del ajuste.
  - Módulo IV: tabla de iteraciones (fase VII), comparación homogénea (tabla y gráfica), pestaña de convergencia (T, polinomio, autovalores, ρ).
  - Planos 3D: figuras de solución única e infinitas guardadas como PNG y revisadas fuera del navegador.
- **No vistos:** varias capturas agotaron el tiempo mientras la página se redibujaba, y no se dan por vistas:
  - la gráfica de convergencia de una ejecución individual (Módulo IV);
  - la figura 3D dentro del navegador;
  - el espaciado corregido de las fracciones.

## Defectos encontrados y corregidos en la auditoría final

| # | Defecto | Efecto | Corrección | Prueba de regresión |
|---|---|---|---|---|
| 1 | Tolerancia de Durand-Kerner (10⁻¹⁵) inalcanzable por redondeo | Raíces **simples** marcadas «no fiables» y conclusión «indeterminado» en casos que convergen (5 de 300 en la auditoría aleatoria, por ejemplo ρ = 0.595) | Tolerancia 10⁻¹²; se mantiene la verificación posterior | test_raices_simples_no_deben_marcarse_no_fiables |
| 2 | λ = ±1 exacto (por ejemplo, A singular) con grado ≥ 3 | Se informaba «indeterminado» aunque ρ ≥ 1 es seguro | Comprobación exacta p(±1) = 0 con fracciones → «no converge» | test_autovalor_uno_exacto_decide_no_convergencia |
| 3 | Con raíces casi repetidas el error de ρ (~10⁻⁸) superaba la banda de 10⁻⁹ | Riesgo de conclusión invertida si ρ ≈ 1 | Banda de 10⁻⁶ cuando hay raíces casi repetidas; función `concluir` | test_bandas, test_raiz_doble_cerca_de_uno |
| 4 | Aviso de raíz múltiple ausente cuando Durand-Kerner no converge | Mensaje poco claro | El aviso menciona el «autovalor múltiple» | test_raiz_multiple_se_declara_indeterminada |
| 5 | ε positiva que se anula en float (10⁻⁴⁰⁰) | Mensaje engañoso: «debe ser mayor que 0» | Mensaje específico | test_tolerancias_extremas_mensajes |
| 6 | «El tolerancia es demasiado grande» | Error gramatical | Mensaje genérico correcto | ídem |
| 7 | Fracciones apiladas que se montaban en vectores y matrices LaTeX | Defecto visual (Módulos III y IV) | Espacio entre filas cuando hay fracciones | test_latex_separa_filas_con_fracciones (visual **sin confirmar**) |
| 8 | P21 aceptaba dos resultados posibles | Prueba débil | Ahora comprueba el resultado determinista | P21 |
| 9 | La exportación CSV no tenía prueba | Funcionalidad sin evidencia | Prueba del contenido y de la precisión completa | test_csv_exportado_contiene_historial_completo |

## Limitaciones conocidas (no resueltas)

1. Autovalores múltiples: ρ queda como «indeterminado» (ver auditoria_requisitos.md).
2. La interfaz no tiene pruebas automáticas del contenido visual de las gráficas.
3. La instalación se probó en entornos virtuales nuevos **en este equipo**, no en otro computador.
4. Streamlit y Matplotlib instalan NumPy como dependencia interna; nuestro código no lo importa.

## Instalación aislada

- **Fase anterior:** `ejecutar.bat` en una copia extraída del ZIP creó `.venv` (Python 3.14.1), instaló las dependencias y el servidor respondió `ok`. En esa copia pasaron 167 pruebas (la versión de entonces).
- **ZIP de la auditoría final (27-oct):** 56 archivos (119 KB), una sola carpeta raíz, sin `.venv`, cachés, `.git` ni imágenes; `ejecutar.bat` con fin de línea CRLF.
  - Extraído en una carpeta nueva, el propio `ejecutar.bat` creó `.venv` (Python 3.14.1), instaló las dependencias y el servidor respondió `ok` a los 51 s.
  - En esa copia: **184 pruebas OK** y auditoría independiente con **0 fallos**.
  - El ZIP se generó con el nombre provisional `Grupo01-…` solo para esta verificación y **se borró**: el número de grupo no está confirmado.

## Pendientes que no dependen del código

| # | Pendiente | Impacto | Quién |
|---|---|---|---|
| 1 | **Autorización expresa del uso de IA** en el código entregable (PROG p. 7 §6.2) | Integridad académica | Grupo → docente |
| 2 | **Número de grupo** (01 o 02) | Nombre del ZIP | Grupo |
| 3 | **Caso de validación obligatorio** | C-07 (3 %) | Docente |
| 4 | Significado oficial del **«error final»** | M4-07 | Docente |
| 5 | **Alcance exigido del radio espectral** (n > 3, autovalores complejos o múltiples, métodos extra) | M4-05 | Docente |
| 6 | NumPy como dependencia transitiva; `math.sqrt` como operación elemental | R-02, R-03 | Docente |
| 7 | Interpretación de la perturbación porcentual | M2-03 | Docente |
| 8 | Comparación esperada en el precondicionamiento diagonal | I-02 (1.5 %) | Docente |
| 9 | Revisión visual de lo no confirmado; manual probado por un tercero | C-05, C-06 | Grupo |
| 10 | Preparación de la defensa individual | 35 % | Los 4 integrantes |
