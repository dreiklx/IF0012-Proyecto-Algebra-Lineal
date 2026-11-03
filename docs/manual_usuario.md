# Manual de usuario — Aplicación IF0012 Álgebra Lineal

## 1. Requisitos e instalación

- Windows 10/11 con **Python 3.11 o superior**. Se probó con Python 3.13.0. Si no lo tiene, descárguelo de https://www.python.org/downloads/ y marque «Add python.exe to PATH» al instalar.
- Internet **solo la primera vez**, para instalar las dependencias: Streamlit 1.66.1 y Matplotlib 3.11.2.

### Opción A: con doble clic (Windows)

1. Descomprima la carpeta del proyecto.
2. Haga doble clic en **`ejecutar.bat`**.
   - La primera vez crea el entorno virtual `.venv` e instala las dependencias, lo que tarda unos minutos.
   - Luego inicia la aplicación y abre el navegador en `http://localhost:8501`.
3. Para cerrar la aplicación, cierre la ventana negra de la consola.

### Opción B: desde una terminal

```
cd ruta\del\proyecto
python -m venv .venv
.venv\Scripts\python -m pip install -r requirements.txt
.venv\Scripts\python -m streamlit run app.py
```

Abra `http://localhost:8501` en el navegador. La aplicación solo es accesible desde el propio equipo y no envía estadísticas de uso (ver `.streamlit/config.toml`).

### Pruebas automáticas

Ejecute `ejecutar_pruebas.bat` o `.venv\Scripts\python -m unittest -v`.

## 2. Formato de las entradas

| Dato | Formato | Ejemplo |
|---|---|---|
| Matriz | Una fila por línea; números separados por espacios | `2 1 -1`<br>`1 -3 2`<br>`3 2 1` |
| Vector | Números separados por espacios o uno por línea | `1 4 0` |
| Número | Entero, decimal con punto o coma, fracción o notación científica | `3`, `-2.5`, `2,5`, `1/3`, `1e-3` |

Si un dato no es válido, la aplicación lo indica en rojo con la posición exacta (por ejemplo, «el elemento (2, 2) de la matriz A …») y no se cierra.

Cada módulo tiene un selector **«Cargar un ejemplo»** con ejemplos del curso. Al elegir uno se rellenan los campos, que luego se pueden modificar.

## 3. Navegación

La barra lateral izquierda tiene cinco opciones: Inicio y los módulos I a IV. Es una sola aplicación integrada.

## 4. Módulo I — Sistemas lineales

1. Escriba A (m × n) y b (m componentes).
2. Elija el **método**:
   - Gauss: escalona la matriz y luego aplica sustitución hacia atrás.
   - Gauss-Jordan: lleva la matriz a la forma escalonada reducida.
3. Elija el **pivote**:
   - «primer elemento no nulo», como en clase;
   - «pivoteo parcial», que elige el mayor |elemento| de la columna.
4. Pulse **Resolver**.

**Resultados:**

- **Clasificación:**
  - **solución única** (verde): rango(A) = rango([A|b]) = n;
  - **infinitas soluciones** (amarillo): rango(A) = rango([A|b]) < n; se muestra la forma paramétrica x = xₚ + t₁v₁ + …;
  - **inconsistente** (rojo): aparece una fila 0 = c con c ≠ 0.
- **rango(A), rango([A|b]) y det(A)**, este último si A es cuadrada.
- **Solución** en fracciones exactas y en decimal, con la comprobación b − Ax.
- **Procedimiento paso a paso:** cada operación elemental (Fi ↔ Fj, Fi → Fi − m·Fj, …) con la matriz resultante. Los intercambios de filas indican su motivo.
- **Interpretación geométrica** (2 o 3 incógnitas): rectas o planos y su intersección.
- **Advertencias:** pivotes numéricamente problemáticos.

*Ejemplo:* el ejemplo «S6-16/09 p. 29» da solución única x = (1/3, 4, 5/3).

## 5. Módulo II — Condicionamiento y sensibilidad

1. Escriba A (cuadrada) y b.
2. Elija la perturbación:
   - **Valor absoluto:** un número que se suma a todas las componentes, o un vector Δb.
   - **Porcentaje:** Δbᵢ = p/100·bᵢ.
3. Pulse **Calcular**.

**Resultados:**

- ‖A‖∞, ‖A⁻¹‖∞ y κ∞(A), con la clasificación del proyecto: κ < 10 baja, 10 ≤ κ < 100 moderada, κ ≥ 100 alta.
- A⁻¹ y su cálculo por Gauss-Jordan, con la verificación A·A⁻¹ = I.
- Una tabla con b, b̃, x, x̃ y Δx.
- ‖Δb‖∞/‖b‖∞, ‖Δx‖∞/‖x‖∞ y la cota κ·‖Δb‖/‖b‖, más una interpretación. Si un denominador es cero, se indica «no definido».
- Si A es singular, se informa que κ no está definido. Es un caso distinto de «κ grande».

*Ejemplo:* «S7-21/09 p. 20» da κ∞ = 25/11 ≈ 2.27, sensibilidad baja, y x̃ = (26/275, 139/220).

## 6. Módulo III — Mínimos cuadrados y ajuste lineal

**Pestaña «Sistema sobredeterminado»:**

1. Escriba A (m × n) y b.
2. Pulse **Resolver por mínimos cuadrados**.

La aplicación detecta si el sistema es sobredeterminado (m > n). Después muestra AᵀA, Aᵀb, x̂, la tabla de residuos rᵢ, ‖r‖₂, ‖r‖₂² y ‖r‖∞, y la comprobación Aᵀr = 0. Si las columnas de A son dependientes, advierte que no hay un x̂ único.

El desplegable **«Verificación con el procedimiento de clase»** repite los pasos del manuscrito S8-30/09 pp. 6-7:

1. det([A | b]), cuando m = n + 1;
2. las ecuaciones normales;
3. la regla de Cramer (para n ≤ 3), que debe coincidir exactamente con Gauss.

**Pestaña «Ajuste lineal de datos»:**

1. Escriba los valores de x y de y; el punto i es (xᵢ, yᵢ).
2. Pulse **Calcular recta de ajuste**.

Se muestra la ecuación y = m x + c, la gráfica de los datos con la recta y los residuos.

*Ejemplo:* «S8-30/09 p. 8» da y = 3/4 x + 6/5.

## 7. Módulo IV — Métodos iterativos

### Datos y parámetros (comunes a las cuatro pestañas)

- A (n × n) y b.
- **Criterio de parada:**
  - **A:** ‖x⁽ᵏ⁾ − x⁽ᵏ⁻¹⁾‖∞ < ε (cambio entre iteraciones; predeterminado).
  - **B:** ‖b − Ax⁽ᵏ⁾‖∞ < ε (residuo del sistema original).
  - **C:** número fijo de iteraciones N. Completar N iteraciones **no** demuestra convergencia.
- **ε** (> 0) y **máximo de iteraciones** (entero de 1 a 100 000) para A y B. **N** para C.
- **ω** (0 < ω < 2): solo se usa con SOR. Este rango no garantiza la convergencia.
- **Vector inicial:** cero (predeterminado), xᵢ⁽⁰⁾ = bᵢ/aᵢᵢ o personalizado.

### Pestaña «Ejecutar un método»

Elija Jacobi, Gauss-Seidel o SOR y pulse **Ejecutar**. La casilla **«Usar almacenamiento disperso (CSR)»** guarda solo los elementos no nulos e informa nnz, la densidad y la memoria usada; las iteraciones son idénticas. Se muestran:

- **El encabezado** con la configuración usada.
- **El motivo de terminación:**
  - tolerancia satisfecha;
  - máximo de iteraciones sin cumplir el criterio, que **no** se presenta como divergencia;
  - N completadas;
  - diagonal cero;
  - error numérico.
- **Las métricas finales:** iteraciones, d final, r final y si se cumplió el criterio.
- **La tabla de iteraciones** con k, x⁽ᵏ⁾, d_k y r_k. La columna que actúa como criterio dice «(criterio de parada)» y la otra «(informativo)».
- **El botón «Descargar tabla de iteraciones (CSV)»**, que exporta los valores con precisión completa.
- **La gráfica** de d_k y r_k en escala logarítmica, con la línea ε.

### Pestaña «Comparar métodos»

Ejecuta los tres métodos con las mismas condiciones y avisa si el experimento no es homogéneo. La tabla muestra:

- iteraciones y motivo de parada;
- d final y r final;
- **error final e** = ‖x⁽ᵏ⁾ − x*‖∞, donde x* es la solución del método directo. Es el «error final ‖x⁽ᵏ⁾ − x‖∞» de la tabla de la lámina S9-05/10 p. 17;
- ρ(T) de cada método.

Hay una gráfica superpuesta de e (por defecto), d o r. En «Influencia de ω en SOR» se pueden probar varios valores de ω.

### Pestaña «Convergencia: dominancia y radio espectral»

Para el método elegido muestra:

- la tabla de dominancia diagonal por filas, con su conclusión (condición suficiente);
- si no es dominante, el **reordenamiento de las ecuaciones** que la haría dominante, si existe (como en la Tarea II #2-3). La aplicación no cambia los datos: hay que copiar A' y b' a mano. Se muestra aunque algún aᵢᵢ sea 0;
- D, L y U;
- la matriz de iteración T y el vector c;
- det(T − λI) y, si T es 3×3, el desarrollo de clase por Sarrus (tr(T), suma de menores, det(T)), comprobado contra el polinomio;
- los autovalores, incluidos los complejos;
- ρ(T) y la conclusión: converge, no converge o indeterminado;
- la gráfica de los autovalores con el círculo unidad.

### Pestaña «Precondicionamiento diagonal» (incentivo)

Pulse **Analizar el precondicionador M = D**. Se usan los mismos criterio, ε, k_max, x⁽⁰⁾ y ω de arriba. Se muestran:

- M = D, B = D⁻¹A y b̃ = D⁻¹b;
- κ∞(A) y κ∞(D⁻¹A), y los autovalores de A y de B;
- una tabla con Jacobi, Gauss-Seidel, SOR y Richardson sobre el sistema original y el precondicionado: iteraciones, motivo, ρ(T), si T y c son idénticas (comparación exacta) y si las iteraciones coinciden;
- las conclusiones y una gráfica de d_k (original con línea continua, precondicionado con línea discontinua).

Resultado esperado con la tridiagonal [−1, 4, −1]:

- κ no cambia, porque la diagonal es uniforme;
- Jacobi, GS y SOR dan las mismas iteraciones;
- Richardson pasa de ρ ≈ 4.618 (no converge) a ρ ≈ 0.405 (converge).

*Ejemplo:* «S8-30/09 — 10x−y+2z=6» con Jacobi y criterio A termina en 7 iteraciones. «S9-07/10» con Jacobi da ρ ≈ 1.174 > 1, es decir, no converge.

## 8. Funciones principales del código

| Función | Archivo | Qué hace |
|---|---|---|
| `resolver_gauss`, `resolver_gauss_jordan` | `algebra/directos.py` | Resuelven y clasifican A x = b con registro de pasos |
| `inversa_gauss_jordan`, `determinante` | `algebra/directos.py` | [A\|I] → [I\|A⁻¹]; det por eliminación |
| `numero_condicion_infinito`, `analizar_perturbacion` | `algebra/condicion.py` | κ∞ y análisis de Δb |
| `minimos_cuadrados`, `ajuste_lineal`, `cramer` | `algebra/minimos.py` | Ecuaciones normales, residuo, recta y verificación por Cramer |
| `ejecutar`, `comparar_metodos`, `dominancia_diagonal` | `algebra/iterativos.py` | Jacobi, GS y SOR con criterios A, B y C |
| `reordenamiento_dominante` | `algebra/iterativos.py` | Orden de las ecuaciones que logra la dominancia diagonal |
| `matriz_iteracion`, `radio_espectral`, `analizar_matriz`, `desarrollo_sarrus` | `algebra/espectral.py` | T, polinomio característico (y Sarrus en 3×3), autovalores y ρ |
| `precondicionar_diagonal`, `analizar_precondicionador` | `algebra/precondicionamiento.py` | M = D, D⁻¹A y comparación original frente a precondicionado |
| `a_csr` y pasos CSR | `algebra/dispersas.py` | Almacenamiento disperso |
| `leer_matriz`, `leer_vector`, … | `algebra/validacion.py` | Lectura y validación del texto introducido |

## 9. Problemas frecuentes

| Problema | Solución |
|---|---|
| `ejecutar.bat` dice que no encuentra Python | Instale Python 3.11 o superior y marque «Add to PATH» |
| El navegador muestra «no se puede acceder» | Espere unos segundos y recargue: el servidor tarda en arrancar |
| El puerto 8501 está ocupado | Cierre otra instancia de la aplicación, o ejecute `.venv\Scripts\python -m streamlit run app.py --server.port 8502` |
