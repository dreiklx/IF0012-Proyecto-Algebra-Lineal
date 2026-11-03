# Pendientes que dependen de la docente o del grupo

**Fecha:** 03-nov-2026 (revisada tras releer los PDF). **Entrega:** 11-nov-2026.

**Regla:** aquí **no** hay respuestas de la docente. Cuando llegue una, se anota con su fecha y su medio (correo, Mediación Virtual o clase), y se actualizan este archivo y `auditoria_requisitos.md`.

Se usó un solo criterio: si el enunciado oficial (OFICIAL) basta para decidir, se decide y se explica. Si no basta, el pendiente queda abierto, con una interpretación provisional.

## Resumen

| # | Pendiente | ¿Lo resuelve el enunciado? | Qué parte afecta | Riesgo si no se aclara |
|---|---|---|---|---|
| P-1 | Número de grupo | **Resuelto:** grupo 01, confirmado por el equipo | Nombre del ZIP | Ninguno |
| P-2 | Autorización del uso de IA | No | Integridad académica (PROG p. 7, §6.2) | **Muy alto** |
| P-3 | Caso de validación obligatorio | No: la docente lo debe entregar (OFICIAL p. 3); no está en ningún PDF | Rúbrica «Casos de prueba» (3 %) | Medio |
| P-4 | Significado de «error final» | **Sí: la lámina S9-05/10 p. 17 lo define** | M4-07 | **Resuelto** |
| P-5 | Alcance del radio espectral | En parte | M4-05 e incentivo I-05 | Medio |
| P-6 | NumPy como dependencia interna de Streamlit y Matplotlib | **Sí**, en lo esencial | R-02, R-03 | Bajo |
| P-7 | Interpretación de la perturbación porcentual | **Sí**, en lo esencial | M2-03 | Bajo |
| P-8 | Comparación esperada en el precondicionamiento | **En gran parte:** la lámina S9-05/10 p. 21 dice qué comparar (κ y ρ de A frente a B) | Incentivo I-02 (hasta 1.5 %) | Bajo. **Implementado el 03-nov**; queda por ver si la docente acepta el resultado (efecto nulo en Jacobi, GS y SOR) |

---

## P-1. Número definitivo del grupo — RESUELTO

- **Confirmado por el equipo el 03-nov-2026:** el proyecto es del **grupo 01**, integrado exclusivamente por Elmer López Hernández, Derek Farley Noguera, Daniel Córdoba Arias y Samir Sandoval Ramírez.
- **Evidencia documental coincidente:** el horario del grupo (L 16:00-17:50 y M 13:00-15:50) corresponde en el programa (PROG p. 9, Sede del Caribe, Aula de Siquirres) al grupo 01, de la profesora Imelda Sáenz Pineda.
- **Nombre de entrega:** `Grupo01-IF0012-Proyecto-IIC.zip`, generado con `python empaquetar.py 01`.

## P-2. Autorización del uso de inteligencia artificial

- **Por qué está pendiente:** el programa del curso (PROG p. 7, §6.2) sanciona el «uso indebido de herramientas de inteligencia artificial no autorizadas». Ni el programa ni el enunciado dicen qué uso está autorizado.
- **Qué afecta:** todo el código entregable y la defensa. En el desarrollo se usaron Claude Code y ChatGPT; está declarado en `docs/herramientas_y_bibliotecas.md` §4.
- **Interpretación provisional:** **ninguna**. No se puede suponer que está autorizado. Mientras tanto, el uso queda declarado sin ocultarlo.
- **Qué hacer:** consultarlo **por escrito**, antes del 11-nov, y guardar la respuesta.
- **Pregunta exacta:** «Profesora, en el desarrollo del proyecto final usamos asistentes de inteligencia artificial (Claude Code y ChatGPT) para escribir y revisar código y documentación. Todos los integrantes estamos estudiando el código para defenderlo. ¿Está permitido este uso? Si lo está, ¿en qué condiciones y cómo debemos declararlo en la entrega?»
- **Si la respuesta es negativa:** hay que decidir con la docente cómo proceder **antes** de entregar. No se debe ocultar el uso.

## P-3. Caso de validación obligatorio

**Qué dice exactamente el enunciado** (releído el 03-nov-2026; no hay otro documento que lo trate):

| Página | Texto (literal) | Qué implica |
|---|---|---|
| OFICIAL p. 1, entregables | «Carpeta de casos de prueba, incluyendo los casos obligatorios indicados por la docente» | El caso o los casos deben ir **dentro de la carpeta de casos de prueba del ZIP** |
| OFICIAL p. 3, §4 | «La docente proporcionará al menos un caso de validación obligatorio antes de la entrega» | Lo **proporciona la docente**: no lo diseña el grupo. Puede ser más de uno («al menos») |
| OFICIAL p. 3, §4 | «la aplicación deberá superar casos de prueba comunes para verificar que los algoritmos no estén construidos para un único conjunto de datos» | El propósito es comprobar que la aplicación resuelve **datos que el grupo no eligió** |
| OFICIAL p. 3, §4 | «Las diferencias numéricas deberán justificarse mediante la tolerancia utilizada y no mediante redondeos arbitrarios» | Si nuestro resultado difiere del de la docente en los decimales, hay que explicarlo con ε (iterativos) o mostrar que el nuestro es exacto (directos) |
| OFICIAL p. 4, rúbrica «Casos de prueba» (3 %) | Excelente: «Casos documentados y aplicación supera el caso obligatorio». Insuficiente: «No presenta pruebas o falla el caso obligatorio» | Es el criterio que acredita: **3 % de la nota del proyecto** |
| OFICIAL p. 5, lista final | «Se incluyeron casos de prueba y se verificó el caso obligatorio» | Debe quedar **evidencia de la verificación** en la entrega |

**Lo que el enunciado NO dice** (y por eso no se puede suponer):

- qué módulo o módulos cubre;
- en qué formato llegan los datos;
- si la docente da también la salida esperada;
- la fecha y el medio de entrega.

**Búsqueda realizada:** el texto de los 18 PDF de la carpeta del curso (`pdftotext`) y la auditoría visual de las láminas. **No contienen ningún caso obligatorio.** Al 03-nov-2026 se considera **no recibido**.

**Qué hay que hacer cuando llegue** (ya está preparado):

1. Copiar la entrada exacta en `casos_prueba/caso_obligatorio.md`, con la fecha y el medio por el que llegó.
2. Si la docente da la salida esperada, anotarla tal cual. Si no la da, calcularla de forma independiente (a mano, con Cramer o con la adjunta, como en los demás casos).
3. Ejecutarla en la aplicación y registrar el resultado obtenido en la misma tabla: entrada, salida esperada, resultado obtenido y si coincide.
4. Crear la prueba automática `tests/test_caso_obligatorio.py`, que reproduzca exactamente los datos y compare con la salida esperada (con la tolerancia indicada si es iterativo).
5. Ejecutar todas las pruebas y la auditoría, regenerar el ZIP y subir los cambios a GitHub.

**Pregunta exacta para la docente:** «Profesora, el enunciado indica que usted proporcionará al menos un caso de validación obligatorio antes de la entrega. ¿Podría indicarnos cuándo y por qué medio lo publicará, a qué módulo o módulos corresponde, y si incluye la salida esperada y la tolerancia que debemos usar? ¿Debemos entregar en el ZIP alguna evidencia en un formato particular?»

## P-4. Significado de «error final» — RESUELTO con el material de la docente

- **Evidencia (releída el 03-nov-2026):** la lámina S9-05/10 p. 17 (diapositiva 13, «Comparación de Jacobi, Gauss-Seidel y SOR en un sistema disperso») tiene una tabla con la columna **«Error final (‖x⁽ᵏ⁾ − x‖∞)»**. La p. 16 (diapositiva 12) usa la misma columna.
- **Qué hace la aplicación:** la tabla de comparación tiene la columna «Error final e = ‖x⁽ᵏ⁾ − x*‖∞», con x* la solución exacta obtenida por Gauss. Es la misma definición. Desde el 03-nov, e_k es además la primera métrica de la gráfica comparativa, como en la lámina («Evolución del error»).
- **No hace falta preguntar.** Se siguen mostrando d y r como información complementaria.

## P-5. Alcance del radio espectral

- **Qué resuelve el enunciado:** OFICIAL p. 2 pide calcular ρ(T) «cuando el procedimiento estudiado lo permita, mediante los procedimientos estudiados en el curso». Esto autoriza a **no** calcularlo cuando el procedimiento no lo permite. Por eso el límite n ≤ 8 y la respuesta «indeterminado» con autovalores múltiples son coherentes con el texto.
- **Qué no resuelve:**
  - El procedimiento del curso es det(T − λI) = 0 por Sarrus (3×3) y luego hallar las raíces (S9-05/10 pp. 32-34; S9-07/10).
  - Para n ≤ 3 el polinomio que calcula la aplicación (Faddeev-LeVerrier) es **idéntico** al de Sarrus; hay una prueba que lo comprueba.
  - En cambio, para hallar las raíces de una cúbica y para n > 3 se usa Durand-Kerner, que **no se vio en clase**.
  - El programa (PROG 4.3) menciona el método de la potencia, pero no hay material de clase sobre él en la carpeta.
- **Qué afecta:** M4-05 y la defensa del incentivo I-05.
- **Interpretación provisional:** mantener la implementación actual, que es correcta y está verificada, y presentarla como una extensión.
  - Faddeev-LeVerrier produce el mismo polinomio que Sarrus.
  - Durand-Kerner es un método propio de aproximación de raíces, cuyo resultado se verifica con |p(λ)| ≈ 0 y con Σλ = traza(T).
- **Pregunta exacta:** «Profesora, para el radio espectral usamos el polinomio característico det(T − λI) como en clase. Para matrices 3×3 lo obtenemos exactamente igual que con Sarrus, pero para hallar sus raíces (que pueden ser complejas) y para n > 3 implementamos nosotros mismos los métodos de Faddeev-LeVerrier y Durand-Kerner. ¿Es aceptable, o prefiere que limitemos el cálculo a n ≤ 3?»

## P-6. NumPy como dependencia interna de Streamlit y Matplotlib

- **Qué resuelve el enunciado:**
  - OFICIAL p. 1 prohíbe «utilizar librerías o funciones que implementen directamente los métodos solicitados». También permite usar bibliotecas «únicamente para visualización, interfaz o manejo de archivos», siempre que se indiquen en la documentación.
  - **Ningún archivo del proyecto importa NumPy** (comprobado el 02-nov con una búsqueda en todos los `.py`). NumPy solo se instala porque Streamlit y Matplotlib lo necesitan internamente.
  - Eso no es «utilizar» NumPy para los métodos. **Se considera resuelto por el propio enunciado.**
- **Qué afecta:** R-02 y R-03. Está documentado en `docs/herramientas_y_bibliotecas.md`.
- **Pregunta (opcional, para mayor seguridad):** «Profesora, nuestro código no usa NumPy, pero Streamlit y Matplotlib lo instalan como dependencia interna. ¿Hay algún inconveniente?»

## P-7. Interpretación de la perturbación porcentual

- **Qué resuelve el enunciado:** OFICIAL p. 2 pide «una perturbación controlada en el vector b (por valor absoluto o porcentaje)», sin precisar más. La aplicación usa Δbᵢ = (p/100)·bᵢ en cada componente, y también acepta un vector de porcentajes.
- **Por qué esta lectura no pierde nada:**
  - Con un único porcentaje p, Δb = (p/100)·b, de modo que ‖Δb‖∞/‖b‖∞ = |p|/100 exactamente.
  - Es el mismo error relativo que daría la otra lectura posible («perturbar b en un p % de su norma»).
  - El dato que pide el enunciado, ‖Δb‖∞/‖b‖∞, coincide en ambas lecturas. Lo único que cambia es la dirección de Δb.
  - Límite: una componente bᵢ = 0 no se perturba en modo porcentual. Para eso existe el modo absoluto.
- **Qué afecta:** M2-03 (`construir_delta_b`).
- **Estado:** resuelto con la interpretación documentada.
- **Pregunta (opcional):** «Profesora, en la perturbación porcentual de b aplicamos el porcentaje a cada componente (Δbᵢ = p/100·bᵢ). ¿Le parece adecuado?»

## P-8. Comparación esperada en el incentivo de precondicionamiento — IMPLEMENTADO

- **Qué dice el material (releído el 03-nov-2026, S9-05/10 pp. 21-23, diapositivas 17-19):**
  - M = D; se resuelve M⁻¹Ax = M⁻¹b aplicando «el método iterativo (Jacobi, Gauss-Seidel, SOR, etc.)».
  - Un buen precondicionador busca ρ(B) < ρ(A) y κ(B) < κ(A), con B = M⁻¹A.
  - La diapositiva 19 muestra a Jacobi «con precondicionamiento» convergiendo más rápido.
- **Qué se implementó** (`algebra/precondicionamiento.py`, pestaña «Precondicionamiento diagonal»):
  - exactamente esa comparación: κ∞(A) frente a κ∞(B), y los autovalores y ρ de A y de B;
  - las iteraciones de Jacobi, GS, SOR y Richardson sobre los dos sistemas;
  - la comparación exacta de las matrices de iteración.
- **Resultado:** con M = D, Jacobi, GS y SOR **no cambian** (T̃ = T, c̃ = c; demostración en guia_matematica §10). La aplicación lo muestra con evidencia, en vez de copiar la tabla de la diapositiva 19, que no es reproducible. Donde M = D sí tiene efecto (κ cuando la diagonal no es uniforme, residuo y Richardson), se muestra.
- **Riesgo:** que la docente esperara ver una aceleración de Jacobi. La respuesta preparada es la demostración de que T̃ = T, que se puede comprobar en vivo en la aplicación.
- **Pregunta (opcional, para comunicarlo con respeto):** «Profesora, al implementar el precondicionador diagonal comprobamos que con M = D las iteraciones de Jacobi, Gauss-Seidel y SOR no cambian, porque la matriz de iteración es la misma. Por eso mostramos también κ(D⁻¹A) y el método de Richardson, donde el efecto sí aparece. ¿Le parece adecuada esta comparación?»
