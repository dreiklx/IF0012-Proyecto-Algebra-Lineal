# Propuesta: evolución de la navegación y de la identidad visual de Ax

**Estado: IMPLEMENTADA la Opción A** (03-nov-2026, rama `feature/navegacion-superior`). El resultado y las mediciones están en `diseno_visual.md` §8. El resto del documento se conserva como registro de la decisión.

**Diferencias con lo propuesto:**

- **Tipografía de títulos:** Bahnschrift, que viene con Windows 10/11, en lugar de Space Grotesk. No hay que distribuir archivos de fuentes y funciona sin internet.
- **Ayuda de formato de entrada:** no pasó a un popover de la barra. Ya está en cada editor (pestaña «Pegar» y ayuda del campo) y en la portada («Cómo introducir los datos»).
- **Páginas:** son archivos (`paginas/*.py`) en lugar de funciones, para que las pruebas puedan abrir cada módulo con `AppTest.switch_page`.
- **Etiquetas de la barra:** caben completas a 1024 px («IV · Métodos iterativos»), así que no hizo falta abreviarlas.

## 1. Arquitectura actual (lo que condiciona cualquier rediseño)

- `app.py` usa `st.sidebar.radio(key="navegacion")` con 5 páginas. Cada módulo es una función `mostrar()` en `interfaz/`, y no hay rutas ni URL por módulo.
- **Modelo de Streamlit:**
  - Cada interacción **vuelve a ejecutar el script entero** y dibuja la página de nuevo en el servidor. No hay un estado del lado del navegador que persista entre pantallas.
  - Las animaciones CSS se reproducen cada vez que un elemento se vuelve a montar, no solo al «aparecer» por primera vez.
- **Dependencias del rediseño:**
  - El estilo está centralizado en `interfaz/compartido/estilo.py` (CSS inyectado) y `.streamlit/config.toml`.
  - Las pruebas de interfaz (`tests/interfaz/test_app.py`, `tests/interfaz/test_editor.py`) navegan con `at.sidebar.radio(key="navegacion")`. Si cambia la navegación, hay que adaptar esas 30 pruebas sin cambiar lo que verifican.
  - Las claves de los widgets (`dir_resolver`, `it_ejecutar`, …) no dependen de la navegación y no cambiarían.

## 2. Qué permite Streamlit 1.66 (verificado en la documentación de la versión instalada)

| Recurso | Para qué sirve | Limitación |
|---|---|---|
| `st.navigation(pages, position="top")` con `st.Page` | **Barra superior nativa**, con una URL por página (`/sistemas`, `/condicionamiento`…), botón «atrás» del navegador e icono por página | Obliga a convertir cada módulo en una página `st.Page`; el estado compartido debe ir en `st.session_state` (ya es así) |
| `st.segmented_control` / `st.pills` | Selector horizontal dentro de la página | No da URL propia |
| CSS inyectado (ya lo usamos) | Tipografía, colores, `:hover`, transiciones de color o sombra, `@keyframes` | Las clases internas de Streamlit (`st-emotion-cache-…`) cambian entre versiones; conviene apoyarse en `data-testid` y `st-key-…`, como ya se hace |
| `st.container(key=…)` | Anclas estables para estilos | — |
| Componentes HTML propios (`st.components.v1.html`) | Portada totalmente libre | Se ejecutan en un iframe: no comparten estilos ni estado sin trabajo adicional |

## 3. Opción A: navegación horizontal superior (`st.navigation`, `position="top"`)

**Propuesta visual:**

```
┌──────────────────────────────────────────────────────────────────────────────┐
│ [Ax] Álgebra Lineal Numérica   Inicio  I Sistemas  II Condición  III Mínimos  IV Iterativos │
│                                  ───────                                        ⓘ Grupo 01 │
└──────────────────────────────────────────────────────────────────────────────┘
  (barra fija de 56 px, fondo #0E1528 con borde inferior #1F2A44; la pestaña activa
   lleva un subrayado cian de 2 px y texto blanco; las inactivas, gris #93A1BC)
```

- **Marca:** monograma «Ax» y nombre en una tipografía de títulos con más carácter, por ejemplo *Space Grotesk* o *IBM Plex Sans* servida localmente. No se usaría Google Fonts en tiempo de ejecución, para no depender de internet en la defensa.
- **Pestañas:** el número romano va en cian, en tipografía monoespaciada; el nombre corto, en la tipografía de texto.
- **Barra lateral:** desaparece. La ayuda de formato de entrada pasa a un icono «ⓘ» con un popover.

| Ventajas | Desventajas |
|---|---|
| Más espacio horizontal para matrices y gráficas (+280 px) | Reescribir `app.py` como páginas `st.Page` (cambio de arquitectura, moderado) |
| Una URL por módulo: se puede abrir directamente «IV» en la defensa | Hay que adaptar unas 30 pruebas de interfaz que navegan por la barra lateral |
| Aspecto de producto, no de plantilla | A 1024 px, 5 pestañas más la marca quedan justas: hay que abreviar («I Sistemas») |
| Navegación del navegador (atrás/adelante) | Riesgo de diferencias de estilo entre versiones de Streamlit en la barra nativa |

## 4. Opción B: conservar la barra lateral y mejorarla (menor riesgo)

```
┌─────────────┐
│ [Ax] IF0012 │   ← marca más compacta
│ ─────────── │
│ ● I  Sistemas lineales      │  ← número romano en «badge»; estado del módulo:
│   └ resuelto ✓              │     punto verde si ya hay un resultado en la sesión
│ ○ II Condicionamiento       │
│ ○ III Mínimos cuadrados     │
│ ○ IV Iterativos             │
│ ─────────── │
│ Atajos: Ejemplo · Pegar      │
└─────────────┘   + una «miga de pan» delgada arriba del contenido: Ax / IV · Iterativos / Comparar
```

| Ventajas | Desventajas |
|---|---|
| Sin cambio de arquitectura; las pruebas no se tocan | Sigue pareciéndose a la disposición clásica de Streamlit |
| Se puede implementar por partes | Menos espacio horizontal |
| Indicador de progreso por módulo (útil en la defensa) | — |

## 5. Animaciones posibles sin perjudicar el rendimiento

**Criterios:**

- solo `opacity` y `transform`, que la GPU compone sin recalcular el diseño;
- duraciones de 120 a 220 ms;
- respetar `prefers-reduced-motion`;
- **nunca** animar matrices, tablas ni fórmulas al reescribir valores, porque distrae y Streamlit las vuelve a montar en cada interacción.

| Microinteracción | Implementación | Coste |
|---|---|---|
| Aparición del resultado principal (tarjeta `res_…`): `fade + translateY(6px→0)` 180 ms | `@keyframes` sobre `div[class*="st-key-res_"]` | Muy bajo. Atención: se repetiría en cada rerun mientras la tarjeta exista; se limitaría con una clase que solo exista en la ejecución que produjo el resultado |
| Botones: elevación de 1 px y sombra al pasar el cursor; «presión» al hacer clic | `:hover`, `:active` con `transition: transform .12s` | Muy bajo |
| Pestaña activa: el subrayado se desliza | `transition` en el borde del tab activo | Bajo |
| Celdas del editor: realce cian al enfocar | `:focus` | Muy bajo (ya hay realce de fondo) |
| Cambio de módulo: fundido del contenido 150 ms | `@keyframes` sobre el contenedor principal | Bajo, pero se reproduce en **todos** los reruns, no solo al cambiar de módulo. Con la Opción A se puede limitar al cambio de página |
| Chip «converge / no converge»: pulso único | `@keyframes` una vez | Muy bajo |

**Descartadas:** paralaje, partículas o fondos animados, transiciones de página largas y animación de los números. Consumen CPU durante los cálculos y restan seriedad.

## 6. Identidad visual menos «genérica»

1. **Tipografía:** una fuente de títulos con personalidad (Space Grotesk / IBM Plex Sans), con una escala tipográfica fija (32/24/18/15/13) y números tabulares (`font-variant-numeric: tabular-nums`) en tablas y métricas, para que las columnas de dígitos queden alineadas.
2. **Menos tarjetas:**
   - los resultados se presentan como un «panel de instrumento»: el valor principal grande a la izquierda y, a la derecha, una columna de diagnósticos (rango, det, κ, ρ) separados por reglas finas, no cajas;
   - las tarjetas se reservan para el resultado principal.
3. **Portada:**
   - en lugar de la rejilla de tarjetas, una composición asimétrica con una matriz real animada una sola vez (la eliminación de Gauss de un 3×3 en tres pasos) como pieza visual, junto a los cuatro módulos en lista numerada con su descripción;
   - los incentivos, en una franja inferior.
4. **Rejilla de fondo** muy tenue (líneas cada 24 px, 2 % de opacidad), evocando papel cuadriculado de cálculo, solo en la portada.
5. **Color:** mantener la paleta, pero usar el cian solo para lo «activo» o «resultado» y el violeta solo para los incentivos. Hoy el azul y el cian se usan para casi todo.

## 7. Recomendación

**Implementar la Opción A (barra superior con `st.navigation`) junto con las microinteracciones de la tabla 5 y los puntos 1-2 de la sección 6**, en una rama propia y **después** de la entrega del 11-nov si el tiempo es justo. Si se quiere antes de la entrega, hacer primero la Opción B (sin riesgo para las pruebas) y dejar la A para después.

**Motivos:**

- La Opción A es la que más cambia la percepción («producto» frente a «plantilla») y gana espacio para matrices y gráficas.
- `st.navigation` es nativo, no un truco de CSS, así que es estable.
- El coste real está en adaptar las pruebas de navegación, que es mecánico: cambia la forma de abrir cada módulo, no lo que se verifica.

**Estimación:**

- Opción A: 1 a 1,5 días (páginas, estilos, adaptación de las pruebas, revisión visual a 1440 y 1024 px).
- Opción B: medio día.
- Microinteracciones: medio día.
