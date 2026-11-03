# Pendientes que dependen de la docente o del grupo

**Fecha:** 02-nov-2026. **Entrega:** 11-nov-2026.

**Regla:** aquí **no** hay respuestas de la docente. Cuando llegue una, se anota con su fecha y su medio (correo, Mediación Virtual o clase), y se actualizan este archivo y `auditoria_requisitos.md`.

Se usó un solo criterio: si el enunciado oficial (OFICIAL) basta para decidir, se decide y se explica. Si no basta, el pendiente queda abierto, con una interpretación provisional.

## Resumen

| # | Pendiente | ¿Lo resuelve el enunciado? | Qué parte afecta | Riesgo si no se aclara |
|---|---|---|---|---|
| P-1 | Número de grupo (01 o 02) | No. Es un dato del grupo (el grupo del curso en que están matriculados) | Nombre del ZIP | Alto: nombre de archivo incorrecto |
| P-2 | Autorización del uso de IA | No | Integridad académica (PROG p. 7, §6.2) | **Muy alto** |
| P-3 | Caso de validación obligatorio | No: la docente lo debe entregar (OFICIAL p. 3) | C-07 (3 %) | Medio |
| P-4 | Significado de «error final» | No, pero la aplicación cubre las tres lecturas | M4-07 | Bajo |
| P-5 | Alcance del radio espectral | En parte | M4-05 e incentivo I-05 | Medio |
| P-6 | NumPy como dependencia interna de Streamlit y Matplotlib | **Sí**, en lo esencial | R-02, R-03 | Bajo |
| P-7 | Interpretación de la perturbación porcentual | **Sí**, en lo esencial | M2-03 | Bajo |
| P-8 | Comparación esperada en el precondicionamiento | No | Incentivo I-02 (hasta 1.5 %, opcional) | Bajo: es un incentivo |

---

## P-1. Número definitivo del grupo

- **Por qué está pendiente:** OFICIAL p. 1 pide el nombre `Grupo(01-02)-IF0012-Proyecto-IIC.zip`. «01» o «02» se refiere al grupo (sección) del curso, y ese dato no está en el repositorio.
- **Qué afecta:** solo el nombre del ZIP y de su carpeta raíz. Regenerarlo con otro número tarda segundos: `python empaquetar.py 02`.
- **Interpretación provisional:** `Grupo01`, solo para poder verificar el paquete.
- **Qué hacer:** que un integrante confirme su grupo en la matrícula o en Mediación Virtual. No hace falta preguntarle a la docente, salvo que el grupo de proyecto mezcle estudiantes de ambos grupos.
- **Pregunta, solo en ese caso:** «Profesora, nuestro grupo de proyecto tiene estudiantes de los grupos 01 y 02. ¿Qué número debemos usar en el nombre del ZIP?»

## P-2. Autorización del uso de inteligencia artificial

- **Por qué está pendiente:** el programa del curso (PROG p. 7, §6.2) sanciona el «uso indebido de herramientas de inteligencia artificial no autorizadas». Ni el programa ni el enunciado dicen qué uso está autorizado.
- **Qué afecta:** todo el código entregable y la defensa. En el desarrollo se usaron Claude Code y ChatGPT; está declarado en `docs/herramientas_y_bibliotecas.md` §4.
- **Interpretación provisional:** **ninguna**. No se puede suponer que está autorizado. Mientras tanto, el uso queda declarado sin ocultarlo.
- **Qué hacer:** consultarlo **por escrito**, antes del 11-nov, y guardar la respuesta.
- **Pregunta exacta:** «Profesora, en el desarrollo del proyecto final usamos asistentes de inteligencia artificial (Claude Code y ChatGPT) para escribir y revisar código y documentación. Todos los integrantes estamos estudiando el código para defenderlo. ¿Está permitido este uso? Si lo está, ¿en qué condiciones y cómo debemos declararlo en la entrega?»
- **Si la respuesta es negativa:** hay que decidir con la docente cómo proceder **antes** de entregar. No se debe ocultar el uso.

## P-3. Caso de validación obligatorio

- **Por qué está pendiente:** OFICIAL p. 3 dice: «La docente proporcionará al menos un caso de validación obligatorio antes de la entrega». A 02-nov no está en la carpeta del curso ni en el repositorio.
- **Qué afecta:** criterio C-07 (3 %) y la lista de verificación de la p. 5.
- **Interpretación provisional:** ninguna. No se considera recibido.
- **Qué hacer al recibirlo:** seguir `casos_prueba/README.md`. Es decir: crear `caso_obligatorio.md` con la entrada exacta, calcular la salida esperada de forma independiente, ejecutarlo en la aplicación, añadir una prueba automática y regenerar el ZIP.
- **Pregunta exacta:** «Profesora, ¿cuándo y por qué medio publicará el caso de validación obligatorio del proyecto final? ¿Debemos incluir en el ZIP alguna salida en un formato particular?»

## P-4. Significado de «error final» en la comparación de métodos

- **Por qué está pendiente:** OFICIAL p. 2 dice «Comparar Jacobi, Gauss-Seidel y SOR mediante número de iteraciones y error final», pero no define «error final». En las láminas, el «error» de la tabla es ‖x⁽ᵏ⁾ − x⁽ᵏ⁻¹⁾‖∞ (S8-30/09 p. 13), aunque la lámina lo llame «error relativo».
- **Qué afecta:** la tabla de la pestaña «Comparar métodos» (`comparar_metodos`).
- **Interpretación provisional:** la tabla muestra las **tres** lecturas posibles:
  - d final = ‖x⁽ᵏ⁾ − x⁽ᵏ⁻¹⁾‖∞, el criterio de las láminas;
  - r final = ‖b − Ax⁽ᵏ⁾‖∞;
  - e final = ‖x⁽ᵏ⁾ − x*‖∞, con x* la solución exacta de Gauss.

  Por eso el riesgo es bajo.
- **Pregunta exacta:** «Profesora, en la comparación de métodos, ¿el "error final" es la diferencia entre las dos últimas iteraciones ‖x⁽ᵏ⁾ − x⁽ᵏ⁻¹⁾‖∞, el residuo ‖b − Ax⁽ᵏ⁾‖∞ o el error respecto a la solución exacta? La aplicación muestra las tres; ¿debemos destacar alguna?»

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

## P-8. Comparación esperada en el incentivo de precondicionamiento

- **Por qué está pendiente:** OFICIAL p. 5 pide una «implementación correcta de un precondicionador diagonal y comparación documentada de su efecto». Pero con M = D (el precondicionador diagonal de S9-05/10) se aplica Jacobi, Gauss-Seidel o SOR a D⁻¹Ax = D⁻¹b, y las iteraciones son **exactamente las mismas** que sin precondicionar. La razón es que D̃ = I, L̃ = D⁻¹L y Ũ = D⁻¹U, así que T̃ = T y c̃ = c (demostración en `guia_matematica.md` §10).
- **Qué sí cambia con M = D:**
  - el residuo (r̃ = D⁻¹r);
  - el número de condición κ(D⁻¹A).
  - Además, el método de Richardson precondicionado con M = D, x ← x + D⁻¹(b − Ax), **es** Jacobi.
- **Qué afecta:** solo el incentivo I-02, que es opcional. No está implementado.
- **Propuesta provisional, si la docente lo pide:**
  1. Calcular κ∞(A) y κ∞(D⁻¹A) con el código del Módulo II.
  2. Mostrar que las iteraciones de los tres métodos no cambian.
  3. Explicar la equivalencia entre Richardson y Jacobi.
- **Pregunta exacta:** «Profesora, comprobamos que con el precondicionador diagonal M = D las iteraciones de Jacobi, Gauss-Seidel y SOR no cambian, porque la matriz de iteración es la misma. ¿Qué comparación espera en este incentivo? ¿Por ejemplo, el efecto sobre el número de condición κ(D⁻¹A) o sobre el método de Richardson?»
