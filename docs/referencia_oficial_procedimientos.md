# Referencia oficial de procedimientos (IF0012, II-2026)

**Fecha:** 09-nov-2026.
**Para qué sirve:** reúne lo que enseñan los materiales de la profesora Imelda Sáenz Pineda. Es la referencia académica con la que se compara el proyecto Ax.
**Regla de este documento:** solo se anota lo que aparece en los PDF.
**10-nov:** se repitió el inventario (sin cambios en los PDF). Cómo resuelve la profesora, la clasificación Cat. A/B/C/D y las erratas recalculadas están en [auditoria_textos_profesora.md](auditoria_textos_profesora.md).

- Las explicaciones que necesitan matemática externa van en recuadros **«Interpretación (externa)»**, separadas de lo literal.
- Las erratas de las láminas se registran en la sección 9. No se corrigen en silencio.

## 0. Fuentes y forma de citar

Carpeta revisada: `%USERPROFILE%\Desktop\ALGEBRA LINEAL` (18 PDF y 1 ZIP). Todas las páginas se revisaron **en imagen**; ver la tabla de control de la sección 1.

| Cita | Archivo | Págs. | Tipo | Fecha del PDF* |
|---|---|---:|---|---|
| OFICIAL | `INTRUCCIONES-PROYECTO FINAL-ÁLGEBRA LINEAL-IIC2026.pdf` | 5 | Enunciado y rúbricas del proyecto (texto digital) | 07-oct-2026 |
| PROG | `IF0012_Álgebra_Lineal_para_Informática_Empresarial_II_2026.pdf` | 12 | Programa del curso (texto digital) | 31-jul-2026 |
| T2 | `IF0012-IITarea-Álgebra Lineal-IIC26.pdf` | 3 | Enunciado de la Tarea II (texto digital) | 06-oct-2026 |
| S1-10/08 | `Semana01-10-08-2026-…pdf` | 24 | Láminas y apuntes manuscritos (imagen) | 10-ago |
| S1-12/08 | `Semana01-12-08-2026-…pdf` | 28 | Ídem | 12-ago |
| S2-17/08 | `Semana02-17-08-2026-…pdf` | 40 | Ídem | 19-ago |
| S2-19/08 | `Semana02-19-08-2026-…pdf` | 48 | Ídem | 19-ago |
| S3-24/08 | `Semana03-24-08-2026-…pdf` | 32 | Ídem | 24-ago |
| S3-26/08 | `Semana03-26-08-2026-…pdf` | 38 | Ídem | 27-ago |
| S4-02/09 | `Semana04-02-09-2026-…pdf` | 32 | Ídem | 08-sep |
| Q1 | `Semana05-07-09-2026-…Resolución I QUIZ.pdf` | 8 | Resolución manuscrita del I Quiz | 09-sep |
| S6-14/09 | `Semana06-14-09-2026-…pdf` | 35 | Láminas y apuntes | 16-sep |
| S6-16/09 | `Semana06-16-09-2026-…pdf` | 36 | Ídem | 18-sep |
| S7-21/09 | `Semana07-21-09-2026-…pdf` | 20 | Ídem | 23-sep |
| S8-28/09 | `Semana08-28-09-20220-…pdf` (el nombre dice «20220») | 15 | Ídem | 29-sep |
| S8-30/09 | `Semana08-30-09-2026-…pdf` | 40 | Ídem | 02-oct |
| S9-05/10 | `Semana09-05-10-2026-…pdf` | 34 | Ídem | 06-oct |
| S9-07/10 | `Semana09-07-10-2026-…pdf` | 7 | Ídem | 11-oct |
| ZIP | `TareaII_Algebra_Derek-Daniel.zip` | 8 JPEG | Tarea II resuelta por **estudiantes** (no es material docente) | 11-oct |

\* `creationDate` de los metadatos del PDF.

- «p. N» es la página del archivo PDF, no el número impreso en la diapositiva. Cuando la diapositiva tiene número propio, se indica como «diap. N».
- Varias semanas repiten láminas de la anterior (repaso). Se cita la primera aparición y, si importa, la repetición.

## 1. Tabla de control de la revisión

| Documento | Páginas | Revisadas | Temas | Estado | Importancia para el proyecto |
|---|---:|---:|---|---|---|
| OFICIAL | 5 | 5 | Requisitos, módulos, validaciones, casos, manual, defensa, rúbricas, incentivos | ✅ texto + imagen | **Máxima** |
| PROG | 12 | 12 | Contenidos 1-5, metodología, evaluación (proyecto 15 %), §6.2 IA, docentes, cronograma, bibliografía | ✅ texto + imagen | Alta (contenidos 2.x y 3.x) |
| T2 | 3 | 3 | MC (ecuaciones normales), dominancia, GS, SOR ω=1,04, A=D+L+U, ρ(T), Gram-Schmidt, valores propios, potencia, SVD, subespacios | ✅ texto + imagen | Alta (casos de prueba) |
| S1-10/08 | 24 | 24 | Vectores, AB = B − A, suma, resta, escalar, producto punto, ortogonalidad (p. 24 en blanco) | ✅ imagen | Baja |
| S1-12/08 | 28 | 28 | Producto punto, norma, distancia, unitario, producto cruz, det 2×2, ángulo, plano; quiz de normas 1 e ∞ de vectores | ✅ imagen | Baja (normas: media) |
| S2-17/08 | 40 | 40 | Matrices, tipos, transpuesta, operaciones, producto; resumen de inversa 2×2 | ✅ imagen | Media |
| S2-19/08 | 48 | 48 | **OEF**, equivalencia, RREF, det 2×2 y 3×3 (**Sarrus**, cofactores), propiedades, adjunta, **inversa por Gauss-Jordan** | ✅ imagen | **Alta** (Módulos I y II) |
| S3-24/08 | 32 | 32 | Repaso de OEF (convención de notación), inversa por GJ (manuscritos), Sarrus, propiedades del det | ✅ imagen | **Alta** |
| S3-26/08 | 38 | 38 | Det por cofactores 4×4, adjunta, **normas de vectores 1, 2 e ∞**, distancia, subespacios | ✅ imagen | Media (norma ∞) |
| S4-02/09 | 32 | 32 | Subespacios, combinación lineal, independencia, N(A), Col(A), base, dimensión, coordenadas, Gram-Schmidt | ✅ imagen | Baja (Col(A): media para MC) |
| Q1 | 8 | 8 | Vectores y normas, operación matricial, det con propiedades, independencia, invertibilidad (det ≠ 0), subespacio, A⁻¹ | ✅ imagen | Baja |
| S6-14/09 | 35 | 35 | Repaso de subespacios; **sistemas: Ax=b, [A\|b], tipos de solución, OEF, eliminación de Gauss, forma escalonada, sustitución hacia atrás y adelante, LU** (p. 35 en blanco) | ✅ imagen | **Máxima** (Módulo I) |
| S6-16/09 | 36 | 36 | Bases ortogonales, Gram-Schmidt; repetición de S5; **Gauss manuscrito con solución (1/3, 4, 5/3)**; LU por eliminación; Ly=b, Ux=y | ✅ imagen | **Máxima** |
| S7-21/09 | 20 | 20 | Sustitución hacia adelante (manuscrito), LU manuscrita; **condicionamiento: κ, normas matriciales, interpretación, cálculo** | ✅ imagen | **Máxima** (Módulo II) |
| S8-28/09 | 15 | 15 | Métodos iterativos (idea, criterio de parada, A=D+L+U, fórmulas); repetición de κ; **condicionamiento en norma 2 (manuscritos)** (p. 8 en blanco) | ✅ imagen | Alta |
| S8-30/09 | 40 | 40 | **Regla de Cramer; mínimos cuadrados manuscritos (det[A\|b], AᵀAx=Aᵀb, Cramer); Jacobi, Gauss-Seidel, SOR (láminas y manuscritos); convergencia, ρ(B), dominancia diagonal** | ✅ imagen | **Máxima** (Módulos III y IV) |
| S9-05/10 | 34 | 34 | SOR manuscrito; **sistemas dispersos, CSR/CSC; iterativos en dispersos; precondicionador M = D**; reordenamiento para dominancia; ρ(T) por det(T−λI) | ✅ imagen | **Máxima** (Módulo IV e incentivos) |
| S9-07/10 | 7 | 7 | Jacobi y Gauss-Seidel matriciales: T, c, ρ(T) por det(T − λI) | ✅ imagen | **Máxima** |
| ZIP | 8 imágenes | 8 | Solución estudiantil de la Tarea II. Contiene nombres y carnés, que no se transcriben | ✅ imagen | Referencia de convenciones aplicadas por estudiantes |
| **Total** | **457 págs. + 8 imágenes** | **457 + 8** | | **Completo** | |

**Método de revisión:**

1. Cada página se renderizó con PyMuPDF a 1150 px de ancho y se revisó visualmente: láminas, fórmulas impresas, manuscritos y resaltados.
2. En los tres PDF digitales se leyó además el texto completo extraído.

Las notas página por página quedaron en el registro de trabajo, que no se entrega. Este documento es su resumen verificable.

---

## 2. Notación de la profesora

| Concepto | Notación en los PDF | Fuente |
|---|---|---|
| Operaciones elementales por fila (OEF) | Fᵢ ↔ Fⱼ; Fᵢ → kFᵢ (k ≠ 0); Fᵢ → Fᵢ + kFⱼ. En los manuscritos escribe el múltiplo antes de la fila destino: «−5F₁ + F₂», «½F₁», «−F₂» | S2-19/08 p. 27; S3-24/08 pp. 4-5; S6-14/09 p. 27 |
| Matriz aumentada | [A \| b] ∈ ℝ^{m×(n+1)} | S6-14/09 p. 25 |
| Sistema | Ax = b; A ∈ ℝ^{m×n}, x ∈ ℝ^{n×1}, b ∈ ℝ^{m×1} | S6-14/09 pp. 22-24 |
| Determinante | \|A\|, det(A) | S2-19/08 pp. 29-38 |
| Transpuesta | Aᵗ o Aᵀ | S2-17/08; S7-21/09 p. 1 |
| Descomposición para iterar | A = D + L + U, con L y U **estrictamente** triangulares y con los signos que tienen en A | S8-28/09 p. 7; S8-30/09 p. 14 |
| Matriz de iteración | G, B o T (B_J, T_J, T_GS); x⁽ᵏ⁺¹⁾ = Gx⁽ᵏ⁾ + c, o T_J x⁽ᵏ⁾ + C_J | S8-28/09 p. 4; S8-30/09 p. 16; S9-07/10 pp. 3-7 |
| Radio espectral | ρ(T) = máx{\|λ\|}. En los manuscritos y en T2 aparece como «P(T)» | S9-05/10 pp. 32-34; S9-07/10 p. 4; T2 p. 2 |
| Tolerancia | ε, o «T = 0,01» en los manuscritos y en T2 («T = 10⁻³») | S8-30/09 pp. 19, 24; T2 p. 1 |
| Precondicionador | M, M⁻¹Ax = M⁻¹b, B = M⁻¹A, b̃ = M⁻¹b | S9-05/10 pp. 19-22 |

## 3. Tema 1: fundamentos que usa el proyecto

### 3.1 Normas de vectores (S3-26/08 pp. 18-32; S1-12/08 p. 28; Q1 p. 3)

- ‖x‖₁ = Σ\|xᵢ\|; ‖x‖₂ = √(Σxᵢ²); **‖x‖∞ = máx{\|x₁\|, …, \|xₙ\|}** (S3-26/08 pp. 21-26).
- Distancia: d(x, y) = ‖x − y‖ (S3-26/08 pp. 29-31).
- **Ejemplo de referencia:** x = (−2, −1), y = (3, 2) dan d₁ = 8, d₂ = √34 ≈ 5,83 y d∞ = 5 (S3-26/08 p. 30).

### 3.2 Determinante (S2-19/08 pp. 29-38; S3-24/08 pp. 10-18)

- 2×2: ad − bc.
- 3×3: **regla de Sarrus**. Ejemplo de la lámina: det = 42 − 4 = 38 (S2-19/08 pp. 33-34).
- Cofactores: Cᵢⱼ = (−1)^{i+j}Mᵢⱼ, desarrollo por fila o columna (S2-19/08 pp. 36-37); 4×4 en S3-26/08 p. 6.
- **Propiedades** (S2-19/08 p. 38):
  - det(I) = 1, det(AB) = det A·det B, det(Aᵀ) = det A, det(kA) = kⁿ det A;
  - triangular: el det es el producto de la diagonal;
  - un intercambio de filas cambia el signo; sumar un múltiplo de otra fila no lo cambia.
- A es invertible ⇔ det(A) ≠ 0; si A no es singular, Ax = b tiene solución única (S2-19/08 pp. 39-40; Q1 p. 7).

> **Interpretación (externa):** el código del proyecto calcula el determinante como (−1)^{intercambios}·Π(pivotes). Eso es la combinación de las propiedades «triangular» e «intercambio» de la p. 38; para 3×3 coincide con Sarrus.

### 3.3 Inversa (S2-19/08 pp. 41-44; S3-24/08 pp. 6-8)

1. Adjunta: A⁻¹ = adj(A)/det(A), con adj(A) = Cᵀ (S2-19/08 pp. 41-43).
2. **Gauss-Jordan:** [A \| Iₙ] → [Iₙ \| A⁻¹] con OEF. «Si en algún paso no existe pivote no nulo, A⁻¹ no existe»; «trabajar con fracciones o decimales exactos» (S2-19/08 p. 44).

Procedimiento manuscrito (S3-24/08 pp. 4-5 y 7-8):

1. Normalizar el pivote (½F₁).
2. Anular debajo del pivote.
3. Anular arriba hasta obtener I.
4. Verificar que A·A⁻¹ = I.

## 4. Tema 2.1-2.2: sistemas lineales y métodos directos (Módulo I)

### 4.1 Representación y tipos de solución (S6-14/09 pp. 21-26)

- Ax = b; matriz aumentada [A \| b].
- **Tipos de solución** (p. 26):
  1. **única** (sistema compatible determinado: los planos se cortan en un punto);
  2. **infinitas** (compatible indeterminado: se cortan en una recta o un plano);
  3. **sin solución** (incompatible: los planos no tienen un punto común).
- «La solución de un sistema lineal tiene un significado geométrico: la intersección de los planos» (p. 26).
- Clasificación manuscrita (S6-16/09 p. 29): «3 ecuaciones no nulas, 3 incógnitas → solución única».

### 4.2 Eliminación de Gauss (S6-14/09 pp. 27-29; S6-16/09 pp. 24-26)

| Paso | Literal de la lámina (S6-14/09 p. 28) |
|---|---|
| 1 | Formar la matriz aumentada [A \| b] |
| 2 | Aplicar OEF para obtener ceros debajo de los pivotes |
| 3 | Obtener la forma escalonada (triangular superior) |
| 4 | Resolver el sistema: sustitución hacia atrás o continuar hasta la forma escalonada reducida |

- **Forma escalonada** (p. 30): las filas nulas al final; cada pivote está a la derecha del anterior; ceros debajo de cada pivote. Si todos los pivotes son 1, es la RREF.
- **Sustitución hacia atrás** (pp. 31-32): se resuelve la última ecuación, se sustituye hacia arriba y se verifica.
- **Sustitución hacia adelante** (p. 33): para una matriz triangular inferior; se resuelven x₁, x₂, … en orden.
- **Ejemplos de referencia:**
  - **Manuscrito (S6-16/09 p. 29):** x + y + z = 6, 2x + y − z = 3, −x + y + 2z = 7. Con −2F₁+F₂, F₁+F₃, −F₂, −2F₂+F₃ y −⅓F₃ se llega a **(1/3, 4, 5/3)**. Es el primer ejemplo precargado de Ax.
  - **Lámina (S6-14/09 p. 29):** 2x + y − z = 1, x − 3y + 2z = 4, 3x + 2y + z = 0, con los multiplicadores F₂ − ½F₁, F₃ − (3/2)F₁ y F₃ + (1/7)F₂. La lámina declara x = 1/2, y = −1, z = −1, pero **es errónea** (sección 9).
  - **Sustitución hacia atrás (S6-16/09 p. 29):** (5, 2, 1); **sustitución hacia adelante (S7-21/09 p. 5):** (1, 8, 10) y (3, 1, 7/2).

### 4.3 Descomposición LU (S6-14/09 p. 34; S6-16/09 pp. 32-36; S7-21/09 pp. 6-12)

- A = LU, con L triangular inferior **con unos en la diagonal** y U triangular superior.
- Se obtiene «por eliminación de Gauss **sin pivoteo**, registrando los multiplicadores en L» (S6-16/09 p. 34).
- Ax = b se resuelve en dos pasos: Ly = b (hacia adelante) y Ux = y (hacia atrás) (p. 35).
- **Ejemplo:** A = [[2,1,1],[4,−6,0],[−2,7,2]], b = (5,−2,9); y = (5,−12,2), **x = (1,1,2)**.
- La lámina S6-14/09 p. 34 menciona: «en la práctica, se suele usar una versión con pivoteo (PA = LU) para mayor estabilidad numérica».

### 4.4 Regla de Cramer (S8-30/09 p. 4)

xᵢ = det(Aᵢ)/det(A), donde Aᵢ es A con la columna i reemplazada por b; requiere det(A) ≠ 0.

Procedimiento en 4 pasos:

1. D = det(A).
2. Formar Aᵢ.
3. Dᵢ = det(Aᵢ).
4. xᵢ = Dᵢ/D.

**Ejemplo:** 2x + y = 5, x − y = 1 → (2, 1).

## 5. Tema 2.3: condicionamiento (Módulo II)

### 5.1 Definiciones (S7-21/09 pp. 13-19)

- κ(A) = ‖A‖‖A⁻¹‖ (p. 17).
- ‖A‖₁ = máx_j Σᵢ\|aᵢⱼ\| (suma por **columnas**); **‖A‖∞ = máx_i Σⱼ\|aᵢⱼ\| (suma por filas)**; ‖A‖₂ = σ_máx (p. 17).
- Propiedades: κ ≥ 1; κ(A) = κ(A⁻¹); si A es ortogonal, κ = 1 (p. 17).
- **Cota:** ‖Δx‖/‖x‖ ≤ κ(A)·‖Δb‖/‖b‖ (p. 18).
- Escala de la lámina (p. 18): κ ≈ 1 muy bien condicionada; 1 < κ ≤ 10 bien; 10 < κ ≤ 10³ moderadamente; 10³ < κ ≤ 10⁶ mal; κ > 10⁶ muy mal.
- **Procedimiento (p. 19):**
  1. elegir la norma;
  2. calcular ‖A‖;
  3. calcular A⁻¹ (verificar que A sea invertible);
  4. calcular ‖A⁻¹‖ en la misma norma;
  5. multiplicar.
- **Ejemplos:** κ₁ = 3 para [[2,1],[1,2]]; **κ∞(B) = 4·(4/5) = 16/5 ≈ 3,2** para B = [[1,2],[3,1]] (p. 19). Matriz bien condicionada [[4,1],[1,3]], κ₁ = 25/11 ≈ 2,27, con Δb = (0,01, −0,01) (p. 20).
- Perturbaciones: (A + ΔA)x = b + Δb (p. 16).

### 5.2 Manuscritos en norma 2 (S8-28/09 pp. 12-15)

- ‖A‖₂ = √(λ_máx(AᵀA)) y ‖A⁻¹‖₂ = 1/√(λ_mín). Se verifica la cota con normas 2. Ejemplo: cond₂ = 2,618 y 0,004937 ≤ 0,0234 (p. 15).
- Para A = I + 10J (p. 13), la profesora usa que es simétrica: κ₂ = máx\|λ\|/mín\|λ\| = 31.

> **Decisión del enunciado (no de las láminas):** OFICIAL p. 2 exige **κ∞**, la clasificación de **3 niveles** (κ < 10 baja, 10 ≤ κ < 100 moderada, κ ≥ 100 alta) y los errores relativos en **norma ∞**. Prevalece el enunciado; las láminas usan otra escala y otras normas.

## 6. Tema 2.4: mínimos cuadrados (Módulo III)

Procedimiento manuscrito (S8-30/09 pp. 5-7):

1. **Sobredeterminado:** A ∈ ℝ^{m×n} con m > n y **b ∉ Col(A)**. Para 3×2 se comprueba con det([A \| b]) ≠ 0 por Sarrus (−11 ≠ 0, «Ran = 3»).
2. «Teorema»: **AᵀAx = Aᵀb** es el «sistema de ecuaciones normales asociado». Se usa «cuando el sistema de ecuaciones es inconsistente».
3. Resolver las ecuaciones normales con la **regla de Cramer**.

**Ejemplo de referencia:** x + 3y = −1, 3x − 2y = 8, −2x + 5y = −8.

- AᵀA = [[14, −13], [−13, 38]] y Aᵀb = (39, −59).
- \|A\| = 363, \|Aₓ\| = 715 y \|A_y\| = −319, de donde **x̂ = (65/33, −29/33)**.

**Ejercicios propuestos (p. 8):** 2x + y = 1, x − 2y = −1, y = 2; y el ajuste x + y = 2, 2x + y = 2,5, 3x + y = 3,7, 4x + y = 4,1.

- La Tarea II #1 (T2 p. 1) pide la «independencia lineal de A», el sistema de ecuaciones normales y el conjunto solución.
- La solución estudiantil del ZIP lo resuelve por Cramer: (4/11, 15/11).

> **Decisión del enunciado:** OFICIAL p. 2 manda resolver las ecuaciones normales «con un método directo ya implementado» (en Ax, Gauss) y calcular r = b − Ax̂ y ‖r‖₂. Las láminas no tienen un ajuste lineal resuelto ni fórmula del residuo.

## 7. Tema 3: métodos iterativos (Módulo IV)

### 7.1 Marco general (S8-28/09 pp. 3-7; S8-30/09 pp. 9-14)

- x⁽ᵏ⁺¹⁾ = Gx⁽ᵏ⁾ + c, donde G es la matriz de iteración; lím x⁽ᵏ⁾ = x*.
- **Criterio de parada** (S8-28/09 p. 6; S8-30/09 p. 13):
  - ε > 0 (por ejemplo 10⁻², 10⁻⁴ o 10⁻⁶);
  - ‖x⁽ᵏ⁺¹⁾ − x⁽ᵏ⁾‖ < ε (la lámina lo rotula «norma del error relativo», aunque es una diferencia absoluta);
  - o el residuo ‖b − Ax⁽ᵏ⁾‖ < ε;
  - «también se suele establecer un número máximo de iteraciones k_max».
- En los ejemplos se usa la **norma ∞** (S8-30/09 pp. 18, 23, 39).
- Preparación: A = D + L + U (estrictas); despejar cada variable (S8-28/09 p. 7).

### 7.2 Jacobi (S8-30/09 pp. 15-20)

- xᵢ⁽ᵏ⁺¹⁾ = (1/aᵢᵢ)(bᵢ − Σ_{j≠i} aᵢⱼxⱼ⁽ᵏ⁾), con aᵢᵢ ≠ 0 para todo i.
- Forma matricial: x⁽ᵏ⁺¹⁾ = D⁻¹(b − (L + U)x⁽ᵏ⁾) = B_J x⁽ᵏ⁾ + c, con **B_J = −D⁻¹(L + U)** y **c = D⁻¹b** (p. 16).
- **Pasos** (p. 16):
  1. descomponer A = D + L + U;
  2. elegir x⁽⁰⁾;
  3. calcular x⁽ᵏ⁺¹⁾;
  4. verificar ‖x⁽ᵏ⁺¹⁾ − x⁽ᵏ⁾‖ < ε;
  5. si no se cumple, repetir desde el paso 3.
- **Ejemplo de lámina:** 10x − y + 2z = 6, −x + 11y − z = 25, 2x − y + 10z = −11, con ε = 10⁻³ y ‖·‖∞; x ≈ (1,273, 2,858, −0,399) en k = 7 (p. 18).
- **Ejemplo manuscrito (pp. 19-20):** 6x₁ + 2x₂ + x₃ = 22, −x₁ + 8x₂ + 2x₃ = 30, x₁ − x₂ + 6x₃ = 23, T = 0,01, solución (2, 3, 4).
  - **Convención de la profesora:** el vector inicial es **x⁽⁰⁾ᵢ = bᵢ/aᵢᵢ** = (11/3, 15/4, 23/6).
  - El error T₁ = ‖x⁽¹⁾ − x⁽⁰⁾‖ se rotula «∞» pero se calcula **sumando** las diferencias: 1,888 + 0,5 + 0,0139 = 2,402 (sección 9).

### 7.3 Gauss-Seidel (S8-30/09 pp. 21-25; S9-05/10 p. 15)

- xᵢ⁽ᵏ⁺¹⁾ = (1/aᵢᵢ)(bᵢ − Σ_{j<i} aᵢⱼxⱼ⁽ᵏ⁺¹⁾ − Σ_{j>i} aᵢⱼxⱼ⁽ᵏ⁾); usa los valores ya actualizados.
- Forma matricial: (D + L)x⁽ᵏ⁺¹⁾ = b − Ux⁽ᵏ⁾ (S9-05/10 p. 15).
- **Ejemplo:** el mismo sistema, con ε = 10⁻³; x ≈ (1,2725, 2,8562, −0,3971) en k = 8 (S8-30/09 p. 23).
- **Manuscrito (p. 24):** mismo sistema 6x₁…, x⁽⁰⁾ = bᵢ/aᵢᵢ («vector inicial»), T = 0,01.

### 7.4 SOR (S8-30/09 pp. 27-33; S9-05/10 pp. 2-5 y 16)

- xᵢ⁽ᵏ⁺¹⁾ = (1 − ω)xᵢ⁽ᵏ⁾ + (ω/aᵢᵢ)(bᵢ − Σ_{j<i} aᵢⱼxⱼ⁽ᵏ⁺¹⁾ − Σ_{j>i} aᵢⱼxⱼ⁽ᵏ⁾), con ω > 0 (S8-30/09 p. 28).
  - ω = 1 da Gauss-Seidel; 0 < ω < 1 es subrelajación; ω > 1, sobre-relajación.
  - S9-05/10 p. 16 escribe 0 < ω < 2; S8-30/09 p. 30 usa 1 < ω < 2 como rango de sobre-relajación.
- **Procedimiento** (p. 28):
  1. escribir Ax = b;
  2. elegir x⁽⁰⁾;
  3. elegir ω;
  4. iterar;
  5. verificar ‖x⁽ᵏ⁺¹⁾ − x⁽ᵏ⁾‖ < ε o ‖Ax⁽ᵏ⁾ − b‖ < ε;
  6. analizar la convergencia.
- **Manuscrito (pp. 32-33; S9-05/10 pp. 2-4):** 10x + 2y + z = 9, 2x + 10y + 2z = 13, x + 2y + 10z = 14, con ω = 1,2, ε = 10⁻³ y x⁽⁰⁾ = 0.
  - **Convención:** primero se calcula el valor de Gauss-Seidel x^GS y después x⁽ᵏ⁺¹⁾ = (1 − ω)x⁽ᵏ⁾ + ω·x^GS, componente por componente.
  - El error es máx{\|Δx\|, \|Δy\|, \|Δz\|}.
  - x⁽¹⁾ = (1,08, 1,3008, 1,2382).
- No aparece en los PDF la **forma matricial** T_ω de SOR.

### 7.5 Convergencia (S8-30/09 pp. 34-39; S9-05/10 pp. 18 y 28-34; S9-07/10)

- Convergencia, divergencia y oscilación (S8-30/09 p. 35).
- **Criterios** (p. 36):
  - dominancia diagonal (suficiente);
  - simétrica definida positiva (para Gauss-Seidel);
  - **ρ(B) < 1 ⇒ el método converge**;
  - ‖B‖ < 1 ⇒ ‖x⁽ᵏ⁾ − x‖ ≤ ‖B‖ᵏ‖x⁽⁰⁾ − x‖.
- **Dominancia diagonal estricta por filas:** \|aᵢᵢ\| > Σ_{j≠i}\|aᵢⱼ\| para todo i. La no estricta (≥) no garantiza nada.
  - Puede verificarse por filas o por columnas.
  - «Es posible **reordenar las ecuaciones** para intentar obtener una matriz diagonalmente dominante» (S8-30/09 p. 37). Se hace en S9-05/10 p. 32, T2 #3 y la solución estudiantil.
- **ρ(T) = máx{\|λ\|}, donde λ es valor propio de T: det(T − λI) = 0** (S9-05/10 p. 32; S9-07/10 p. 2).
- **Procedimiento matricial de Jacobi (S9-07/10 pp. 3-5):**
  1. descomponer A = D + L + U;
  2. calcular D⁻¹;
  3. calcular **T_J = −D⁻¹(L + U)**;
  4. calcular **C_J = D⁻¹b**;
  5. hallar ρ(T) con det(T_J − λI) = 0, desarrollado por Sarrus;
  6. iterar con x⁽ᵏ⁺¹⁾ = T_J x⁽ᵏ⁾ + C_J.
- **Gauss-Seidel (S9-07/10 pp. 6-7):** **T_GS = −(D + L)⁻¹U**; det(T_GS − λI) = 0 da λ ≈ 0,9351, −0,7129 y 0, de modo que ρ = 0,9351 < 1.
- Velocidad: ‖e⁽ᵏ⁾‖ ≤ Cρ(B)ᵏ‖e⁽⁰⁾‖ (S9-05/10 p. 18).

> **Interpretación (externa):** las láminas S8-30/09 p. 36 y S9-05/10 p. 29 escriben B_J = D⁻¹(L + U) y B_GS = (D − L)⁻¹U. Es la convención A = D − L − U. Con la descomposición A = D + L + U que usan los manuscritos, lo coherente es T_J = −D⁻¹(L + U) y T_GS = −(D + L)⁻¹U, que es lo que escribe la profesora a mano (S9-07/10).

### 7.6 Comparación y «error final» (S9-05/10 pp. 16-18)

Tabla «Método, ω, iteraciones, **error final ‖x⁽ᵏ⁾ − x‖∞**» (p. 17) y gráfica del error relativo frente a k en escala logarítmica.

## 8. Tema 3.3: dispersas y precondicionamiento (incentivos)

### 8.1 Matrices dispersas (S9-05/10 pp. 8-17)

- Una matriz es dispersa si el número de no nulos es mucho menor que n² (p. 8).
- Tipos: tridiagonal, banda y bloques.
- **Representación en memoria: formatos CSR (Compressed Sparse Row) y CSC**, con tablas Fila/Columna/Valor (p. 9).
- Memoria O(nnz) frente a O(n²) (p. 11).
- **Los iterativos en dispersos solo usan los elementos no nulos**; el costo por iteración es proporcional a nnz (p. 13).
- Ejemplo: tridiagonal [−1, 4, −1] de 4×4 con b = (1, 0, 0, 1), cuya solución es (1/3, 1/15, 1/15, 1/3) (p. 14).

### 8.2 Precondicionador (S9-05/10 pp. 19-23 y 26-27)

- **Definición (p. 19):** M invertible y de bajo costo; se resuelve el sistema equivalente **M⁻¹Ax = M⁻¹b** y «se aplica el método iterativo (Jacobi, Gauss-Seidel, SOR, entre otros) al sistema precondicionado».
  - Ejemplo típico: **M = D = diag(a₁₁, …, aₙₙ)** (precondicionador de Jacobi), con D⁻¹ = diag(1/aᵢᵢ).
- Izquierdo: M⁻¹Ax = M⁻¹b; derecho: AM⁻¹y = b con x = M⁻¹y (p. 20).
  - Esquema: sistema original → M → sistema equivalente → «aplicar método iterativo (Jacobi, Gauss-Seidel, SOR, **etc.**)» → solución.
- **B = M⁻¹A**; un buen precondicionador busca **ρ(B) < ρ(A) y κ(B) < κ(A)**, con los valores propios de B agrupados cerca de 1 (p. 21).
- **Construcción (p. 22):** en la tridiagonal, M = D = 4I, M⁻¹A = ¼A y M⁻¹b = ¼b.
- **«Efecto del precondicionamiento en la convergencia» (p. 23, diap. 19):** Jacobi sin y con M = D, en una tabla con iterados distintos y errores 0,75 / 0,625 / … frente a 0,5 / 0,25 / …
  - **No es reproducible:** ver la sección 9 y `docs/investigacion_richardson.md`.
- **Prácticas (pp. 26-27):** «Ejercicio 2. Efecto del precondicionamiento»: Jacobi con y sin M = D durante 10 iteraciones, comparando ‖e⁽ᵏ⁾‖∞.
- **El método de Richardson no aparece en ningún PDF.**

## 9. Erratas detectadas en los materiales

Ninguna salida de lámina se usa como resultado esperado sin recalcularla.

| Fuente | Lo que dice | Valor correcto / observación | ¿Afecta al proyecto? |
|---|---|---|---|
| S2-19/08 pp. 42-43 | A = [[2,−1,0],[1,3,2],[0,−2,1]] con det = 42 | det = 15 | No (Tema 1) |
| S3-26/08 p. 26 | «‖x‖₂ ≤ ‖x‖∞ ≤ ‖x‖₁» | ‖x‖∞ ≤ ‖x‖₂ ≤ ‖x‖₁ (x = (3,−4): 4 ≤ 5 ≤ 7) | No |
| S6-14/09 p. 29 | Gauss del sistema 2x+y−z=1… da (1/2, −1, −1) | (19/20, −5/4, −7/20), verificado con fracciones | Sí: el ejemplo de Ax lo señala |
| S7-21/09 p. 14 | 2.01x + y = 4, x + y = 3 da (100, −97) | Da (100/101, 203/101) ≈ (0,990, 2,010) | No |
| S7-21/09 p. 20 | x̃₂ = 7,93/11 | 6,95/11 ≈ 0,6318 (el ejemplo precargado está «corregido») | Sí, documentado |
| S8-28/09 p. 12 | AᵀA de [[2,1,0],[0,3,0],[0,0,4]] con a₂₂ = 4 | a₂₂ = 1 + 9 = 10 | No (norma 2) |
| S8-30/09 pp. 19-20 y 24 | T = ‖Δx‖ rotulada ∞ pero calculada como suma | La norma ∞ es el máximo; la suma es la norma 1 | Sí: Ax usa el máximo (IV-7) |
| S8-30/09 pp. 17-18, 23 y 29; S9-05/10 pp. 14-17 | Tablas de iteraciones | Contienen errores aritméticos (verificados en la auditoría del 26-oct) | No se usan como oráculo |
| S8-30/09 p. 36; S9-05/10 p. 29 | B_J = D⁻¹(L+U), B_GS = (D−L)⁻¹U | Convención de signos inconsistente con A = D + L + U | Ax usa la de los manuscritos |
| S9-05/10 p. 23 | Jacobi con M = D converge más rápido | Con M = D las iteraciones son idénticas; la columna «sin» tampoco es Jacobi | Sí: ver `investigacion_richardson.md` |
| S9-07/10 p. 4 | ρ(T_J) = 0 para [[3,3,3],[3,3,2],[−3,−2,3]] | ρ(T_J) ≈ 1,174 (no converge) | Sí: ejemplo precargado |
| S9-07/10 p. 7 | C_GS = −(D+L)⁻¹b | C_GS = (D+L)⁻¹b | Ax usa el signo correcto |

## 10. Lo que el enunciado exige y los PDF no enseñan (o enseñan distinto)

| Exigencia del enunciado | Material | Consecuencia |
|---|---|---|
| κ∞ y su escala de 3 niveles | La lámina usa norma 1 o 2 y una escala de 5 niveles | Se usa el enunciado |
| Perturbación «por porcentaje» | No aparece | Interpretación propia, documentada (P-7) |
| ‖r‖₂ del residuo | No aparece resuelto | Definición estándar |
| «Gauss o Gauss-Jordan» y «detección de pivotes nulos o numéricamente problemáticos» | Gauss sin pivoteo; intercambio si el pivote es 0; PA = LU solo mencionado | Pivote «primer no nulo» por defecto; pivoteo parcial como opción |
| ρ(T) «mediante los procedimientos estudiados» | det(T − λI) por Sarrus (3×3); raíces a mano o con calculadora | Polinomio y raíces programados (ver `investigacion_richardson.md`, categoría C) |
| «Error final» en la comparación | ‖x⁽ᵏ⁾ − x‖∞ (S9-05/10 p. 17) | Implementado así |
