# Discrepancias entre los documentos de la profesora y Ax

Fecha de la revisión: 12-nov-2026. Estado: **parcial** (ver `inventario_paginas.csv`).

| # | Documento y página | Qué dice la fuente | Verificación | Clasificación | Ax | Acción |
|---|---|---|---|---|---|---|
| D1 | S9-07/10 p. 7 (Gauss-Seidel) | Escribe «C_GS = −(D+L)⁻¹·b» y calcula «T_GS·b», obteniendo x⁽¹⁾ = (−7, 25/3, −13/9) | Exacto: (D+L)⁻¹b = (3, 0, 7/3); T_GS·b = (−7, 25/3, −13/9). La iteración de Gauss-Seidel desde x⁽⁰⁾ = 0 da x⁽¹⁾ = (3, 0, 7/3) | **Error de la lámina** (signo y producto equivocado) | c_GS = (D+L)⁻¹b = (3, 0, 7/3) | Ninguna en el código. Erratas documentadas en la guía |
| D2 | S9-05/10 p. 23 y S9-07/10 p. 5 (radio espectral de Jacobi) | El polinomio de la lámina omite el término 4/3: queda −λ³ − (4/9)λ = 0 y ρ = 0 | det(T_J − λI) = −λ³ − (4/9)λ + 4/3. Raíz de módulo 1,1744 | **Error de la lámina** | Polinomio correcto (`polinomio_caracteristico`), ρ = 1,17436 | Ninguna en el código |
| D3 | S9-05/10 p. 23 | «Jacobi con M = D converge más rápido» | Con M = D, D⁻¹A tiene diagonal 1 y T_J no cambia: iteraciones idénticas | **Error de la lámina** | Iteraciones idénticas (`analizar_precondicionador`) | Documentado |
| D4 | S8-28/09 p. 6 y S8-30/09 p. 9 | La fórmula impresa es ‖x⁽ᵏ⁺¹⁾ − x⁽ᵏ⁾‖ < ε (sin división). El título dice «norma del error relativo» | Verificado en imagen. Mi lectura anterior por OCR, que daba una división, era **errónea** | **Sin discrepancia de fórmula**: Ax usa la misma fórmula absoluta (norma ∞) | Sin cambio de cálculo; la interfaz lo aclara | Corregida la nota de la interfaz y los documentos que decían lo contrario |
| D8 | S8-28/09 p. 6 (ejemplo) | Ejemplo con ε = 10⁻³ al inicio, pero la conclusión usa 0,01 y detiene en k = 8 con ‖x⁽⁸⁾ − x⁽⁷⁾‖ = 0,002 < 0,01. Con 0,01, la fila k = 7 ya tiene 0,005 < 0,01; con 10⁻³ no se cumple en k = 8 | Cálculo directo de la tabla de la lámina | **Errata interna de la lámina** (ε inconsistente) | Ax usa la ε que introduce el usuario | Documentada; no se copia la conclusión |
| D5 | S9-07/10 p. 5 | Tercera componente de x⁽²⁾ de Jacobi: lectura dudosa a 480 px (se lee «4/3» en un fragmento) | Ax da x⁽²⁾₃ = 13/3; el cálculo a mano con T_J y c_J da 13/3 | **Pendiente de verificar** con zoom mayor | 13/3 | Revisar la imagen a más resolución |
| D6 | Richardson, Faddeev-LeVerrier, Durand-Kerner | No aparecen en ninguna lámina (búsqueda OCR en 15 PDF de clase y lectura de S9-07/10) | — | **Retirados** (13-nov-2026) por fidelidad académica | Eliminados de código e interfaz | Ver docs/auditoria/matriz_fidelidad_academica.md |
| D7 | Notación de la lámina S9-07/10 p. 6 | Usa T_GS = −(D+L)⁻¹U | Coincide con la fórmula de Ax | Coincide | Igual | — |

## Pendiente de revisión visual (no hay diferencias confirmadas todavía)

Módulos I, II y III y el resto de Módulo IV (S8-28, S8-30, S9-05, S7-21, S6-14/16, S3-24/26, S2-17/19, S1-10/12, S4-02/09, S6-14, S7-21 cond., etc.). Ver `inventario_paginas.csv`.
