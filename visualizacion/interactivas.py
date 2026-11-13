"""Gráficas interactivas (Plotly): rotar, acercar, desplazar, consultar valores y
activar o desactivar series.

Son todas las gráficas que muestra la aplicación.  SOLO dibujan resultados ya
calculados por el núcleo (algebra/): no resuelven, no iteran y no ajustan nada.
Los datos que se dibujan (esquinas de los planos, región dibujada, valores
positivos para la escala logarítmica) salen de datos_graficas.py; la notación
(d<sub>k</sub>, x<sup>(k)</sup>) de notacion.py.

| Módulo | Función            | Gráfica                                         |
|--------|--------------------|-------------------------------------------------|
| I      | rectas_2d          | rectas de un sistema 2×2 (opcional)             |
| I      | planos_3d          | planos 3D con control gestual (opcional)        |
| III    | ajuste             | datos y recta de mejor ajuste (OBLIGATORIA)     |
| IV     | convergencia       | error vs. iteración de un método (OBLIGATORIA)  |
| IV     | comparacion        | los tres métodos superpuestos (OBLIGATORIA)     |
| IV     | autovalores        | λ de T y círculo unidad (extensión)             |
| IV     | precondicionador   | efecto de M = D (incentivo)                     |

La barra de herramientas (zoom +/−, zoom por región, desplazamiento, rotación 3D,
restablecer vista) se configura en interfaz/compartido/componentes.py::mostrar_interactiva.
"""

import math

import plotly.graph_objects as go

from visualizacion import notacion
from visualizacion.datos_graficas import (
    MARCADORES,
    TITULOS_METRICA,
    centro_y_radio,
    esquinas_plano,
    positivos,
    serie_metrica,
)
from visualizacion.tema import (
    COLOR_DATOS,
    COLOR_EPSILON,
    COLOR_RECTA,
    COLOR_RESIDUO,
    COLOR_SOLUCION,
    COLORES_METODOS,
    COLORES_PLANOS,
    FONDO,
    FONDO_EJES,
    REJILLA,
    SUAVE,
    TEXTO,
)

SIMBOLOS = {"o": "circle", "s": "square", "^": "triangle-up", "D": "diamond"}
FUENTE = "Segoe UI, Inter, system-ui, sans-serif"


def _eje(titulo, log=False, **extra):
    if log:
        extra.setdefault("dtick", 1)          # solo potencias de 10: sin marcas intermedias
    return dict(title=dict(text=titulo, font=dict(size=13, color=TEXTO)), type="log" if log else "linear",
                gridcolor=REJILLA, zerolinecolor=SUAVE, linecolor=REJILLA, tickfont=dict(color=SUAVE),
                exponentformat="power", showspikes=True, spikecolor=SUAVE, spikethickness=1, **extra)


def _base(titulo, alto=440, revision=True):
    fig = go.Figure()
    fig.update_layout(
        title=dict(text=titulo, x=0.01, font=dict(size=15, color=TEXTO)),
        paper_bgcolor=FONDO, plot_bgcolor=FONDO_EJES, font=dict(family=FUENTE, color=TEXTO, size=12),
        height=alto, margin=dict(l=60, r=52, t=56, b=40),
        # barra de herramientas vertical, a la derecha: nunca tapa el título
        modebar=dict(orientation="v", bgcolor="rgba(0,0,0,0)", color=SUAVE, activecolor="#22D3EE"),
        legend=dict(orientation="h", y=-0.2, x=0.5, xanchor="center", bgcolor="rgba(0,0,0,0)",
                    font=dict(size=12)),
        hoverlabel=dict(bgcolor="#18223A", bordercolor=REJILLA, font=dict(color=TEXTO, family=FUENTE)),
        dragmode="zoom")
    if revision:
        # uirevision fija: el zoom y las series ocultas se conservan cuando la figura se
        # vuelve a enviar (por ejemplo, al elegir otra iteración en el deslizador).
        fig.update_layout(uirevision=titulo)
    return fig


# Módulo I: rectas (2 incógnitas) y planos (3 incógnitas)

def planos_3d(A, b, resultado):
    """Cada ecuación a·(x, y, z) = bᵢ como una porción cuadrada del plano (las mismas
    esquinas que la figura estática), más el punto o la recta de soluciones."""
    fig = _base("Interpretación geométrica: cada ecuación es un plano", alto=560, revision=False)
    centro, radio = centro_y_radio(resultado)
    for i, fila in enumerate(A):
        a = [float(v) for v in fila]
        if all(v == 0 for v in a):
            continue
        p0, p1, p2, p3 = esquinas_plano(a, float(b[i]), centro, radio)
        color = COLORES_PLANOS[i % len(COLORES_PLANOS)]
        ecuacion = notacion.ecuacion(a, "xyz", float(b[i]))
        fig.add_trace(go.Surface(
            x=[[p0[0], p1[0]], [p3[0], p2[0]]], y=[[p0[1], p1[1]], [p3[1], p2[1]]],
            z=[[p0[2], p1[2]], [p3[2], p2[2]]], name=f"Ecuación {i + 1}", showlegend=True,
            showscale=False, opacity=0.55, colorscale=[[0, color], [1, color]],
            hovertemplate=f"<b>Ecuación {i + 1}</b>: {ecuacion}<br>x = %{{x:.4g}}<br>"
                          f"y = %{{y:.4g}}<br>z = %{{z:.4g}}<extra></extra>"))
    if resultado.solucion is not None:
        x, y, z = (float(v) for v in resultado.solucion)
        fig.add_trace(go.Scatter3d(
            x=[x], y=[y], z=[z], mode="markers", name=f"Solución única ({x:.4g}, {y:.4g}, {z:.4g})",
            marker=dict(size=7, color=COLOR_SOLUCION, line=dict(color="#0B1020", width=2)),
            hovertemplate="<b>Solución única</b><br>x = %{x:.6g}<br>y = %{y:.6g}<br>z = %{z:.6g}<extra></extra>"))
    elif resultado.solucion_particular is not None and len(resultado.direcciones) == 1:
        p = [float(v) for v in resultado.solucion_particular]
        v = [float(t) for t in resultado.direcciones[0]]
        escala = radio / max(1e-12, max(abs(t) for t in v))
        extremos = [[p[j] - escala * v[j], p[j] + escala * v[j]] for j in range(3)]
        fig.add_trace(go.Scatter3d(
            x=extremos[0], y=extremos[1], z=extremos[2], mode="lines", name="Recta de soluciones",
            line=dict(color=COLOR_SOLUCION, width=7),
            hovertemplate="<b>Recta de soluciones</b><br>x = %{x:.4g}<br>y = %{y:.4g}<br>z = %{z:.4g}<extra></extra>"))
    escena = {f"{n}axis": dict(title=n, range=[centro[j] - radio, centro[j] + radio], backgroundcolor=FONDO_EJES,
                               gridcolor=REJILLA, zerolinecolor=SUAVE, color=SUAVE, showbackground=True)
              for j, n in enumerate("xyz")}
    fig.update_layout(scene=dict(**escena, aspectmode="cube",
                                 camera=dict(eye=dict(x=1.55, y=-1.55, z=1.05))),
                      margin=dict(l=0, r=52, t=56, b=10), dragmode="orbit",
                      # uirevision fija: si la cámara de la figura no cambia, Plotly conserva la
                      # vista que dejó el ratón (o el control gestual) entre ejecuciones.
                      uirevision="planos",
                      legend=dict(orientation="v", y=0.98, x=0.01, xanchor="left", bgcolor="rgba(24,34,58,.85)"))
    return fig


def rectas_2d(A, b, resultado):
    fig = _base("Interpretación geométrica: cada ecuación es una recta", alto=500)
    centro, radio = centro_y_radio(resultado)
    for i, fila in enumerate(A):
        a1, a2, bi = float(fila[0]), float(fila[1]), float(b[i])
        color = COLORES_PLANOS[i % len(COLORES_PLANOS)]
        etiqueta = f"Ecuación {i + 1}: {notacion.ecuacion([a1, a2], 'xy', bi)}"
        if a2 != 0:
            xs = [centro[0] - radio, centro[0] + radio]
            ys = [(bi - a1 * x) / a2 for x in xs]
        elif a1 != 0:
            xs, ys = [bi / a1, bi / a1], [centro[1] - radio, centro[1] + radio]
        else:
            continue
        fig.add_trace(go.Scatter(x=xs, y=ys, mode="lines", name=etiqueta, line=dict(color=color, width=2.6),
                                 hovertemplate=f"{etiqueta}<br>x = %{{x:.4g}}<br>y = %{{y:.4g}}<extra></extra>"))
    if resultado.solucion is not None:
        x, y = (float(v) for v in resultado.solucion)
        fig.add_trace(go.Scatter(x=[x], y=[y], mode="markers", name=f"Solución ({x:.4g}, {y:.4g})",
                                 marker=dict(size=11, color=COLOR_SOLUCION, line=dict(color="#0B1020", width=2)),
                                 hovertemplate="<b>Solución</b><br>x = %{x:.6g}<br>y = %{y:.6g}<extra></extra>"))
    fig.update_layout(xaxis=_eje("x", range=[centro[0] - radio, centro[0] + radio]),
                      yaxis=_eje("y", range=[centro[1] - radio, centro[1] + radio], scaleanchor="x"))
    return fig


# Módulo III: ajuste lineal

def rango_ajuste(xs, ys, estimados):
    """Rango por defecto (x0, x1, y0, y1) de la gráfica de ajuste: datos, recta y residuos."""
    xs_f = [float(v) for v in xs]
    ys_f = [float(v) for v in ys]
    margen = (max(xs_f) - min(xs_f)) * 0.08 or 1.0
    ys_todos = ys_f + [float(e) for e in estimados]
    my = (max(ys_todos) - min(ys_todos)) * 0.1 or 1.0
    return (min(xs_f) - margen, max(xs_f) + margen, min(ys_todos) - my, max(ys_todos) + my)


def ajuste(xs, ys, pendiente, intercepto, estimados, rango=None):
    """Datos, recta de mejor ajuste y residuos.  `rango` (opcional) solo fija la vista de los
    ejes; los datos y los trazos no cambian."""
    fig = _base("Ajuste lineal por mínimos cuadrados")
    xs_f, ys_f = [float(v) for v in xs], [float(v) for v in ys]
    m, c = float(pendiente), float(intercepto)
    x0, x1 = rango_ajuste(xs, ys, estimados)[0:2]
    rx, ry = [], []
    for x, y, y_est in zip(xs_f, ys_f, estimados):
        rx += [x, x, None]
        ry += [y, float(y_est), None]
    fig.add_trace(go.Scatter(x=rx, y=ry, mode="lines", name="Residuos r<sub>i</sub>", hoverinfo="skip",
                             line=dict(color=COLOR_RESIDUO, dash="dot", width=1.6)))
    fig.add_trace(go.Scatter(x=[x0, x1], y=[m * x0 + c, m * x1 + c], mode="lines",
                             name=f"Recta: y = {m:.6g}x {'+' if c >= 0 else '−'} {abs(c):.6g}",
                             line=dict(color=COLOR_RECTA, width=3),
                             hovertemplate="Recta<br>x = %{x:.4g}<br>y = %{y:.6g}<extra></extra>"))
    residuos = [y - float(e) for y, e in zip(ys_f, estimados)]
    # El dato con mayor |rᵢ| (donde el ajuste falla más) se resalta; solo cambia el estilo.
    mayor = max(range(len(residuos)), key=lambda i: abs(residuos[i])) if residuos else None
    fig.add_trace(go.Scatter(
        x=xs_f, y=ys_f, mode="markers", name="Datos (x<sub>i</sub>, y<sub>i</sub>)",
        customdata=[[float(e), y - float(e)] for y, e in zip(ys_f, estimados)],
        marker=dict(size=[13 if i == mayor else 10 for i in range(len(xs_f))], color=COLOR_DATOS,
                    line=dict(color=[COLOR_RESIDUO if i == mayor else "#0B1020" for i in range(len(xs_f))],
                              width=[2.6 if i == mayor else 1.5 for i in range(len(xs_f))])),
        hovertemplate="<b>Dato</b> (%{x:.6g}, %{y:.6g})<br>ŷ<sub>i</sub> = %{customdata[0]:.6g}<br>"
                      "r<sub>i</sub> = y<sub>i</sub> − ŷ<sub>i</sub> = %{customdata[1]:.6g}<extra></extra>"))
    if mayor is not None and residuos[mayor] != 0:
        fig.add_annotation(x=xs_f[mayor], y=ys_f[mayor], text=f"mayor |r<sub>i</sub>| = {abs(residuos[mayor]):.4g}",
                           showarrow=True, arrowhead=0, ax=0, ay=-34 if residuos[mayor] > 0 else 34,
                           arrowcolor=COLOR_RESIDUO, font=dict(size=11, color=COLOR_RESIDUO))
    fig.update_layout(xaxis=_eje("x"), yaxis=_eje("y"), hovermode="closest")
    if rango is not None:
        fig.update_layout(xaxis_range=[rango[0], rango[1]], yaxis_range=[rango[2], rango[3]])
    return fig


# Módulo IV: convergencia, comparación, autovalores y precondicionador

def _texto_vector(x):
    return "(" + ", ".join(f"{v:.6g}" for v in x) + ")"


def _resaltes(ks_dibujados, especiales, base=8, grande=13):
    """Tamaño y borde de cada marcador: los puntos de `especiales` ({k: color del borde})
    se dibujan más grandes y con borde claro.  Solo cambia el estilo, nunca los datos."""
    tamanos = [grande if k in especiales else base for k in ks_dibujados]
    bordes = [especiales.get(k, "#0B1020") for k in ks_dibujados]
    anchos = [2.4 if k in especiales else 1 for k in ks_dibujados]
    return tamanos, bordes, anchos


def _y_log(valor):
    """Las anotaciones sobre un eje logarítmico se ubican con log10 del valor."""
    return math.log10(valor)


def _serie(ks, valores, nombre, color, simbolo, guion="solid", detalle=None, especiales=None):
    """detalle: {k: texto extra para el cursor}; especiales: {k: color del borde resaltado}."""
    puntos, ceros = positivos(ks, valores)
    trazas = []
    if puntos:
        xs = [p[0] for p in puntos]
        tamanos, bordes, anchos = _resaltes(xs, especiales or {})
        extra = [(detalle or {}).get(k, "") for k in xs]
        trazas.append(go.Scatter(x=xs, y=[p[1] for p in puntos], mode="lines+markers",
                                 name=nombre, line=dict(color=color, width=2.4, dash=guion),
                                 customdata=extra,
                                 marker=dict(symbol=simbolo, size=tamanos, color=color,
                                             line=dict(color=bordes, width=anchos)),
                                 hovertemplate=f"<b>{nombre}</b><br>k = %{{x}}<br>valor = %{{y:.6e}}"
                                               "%{customdata}<extra></extra>"))
    if ceros:
        trazas.append(go.Scatter(x=ceros, y=[1e-17] * len(ceros), mode="markers",
                                 name=f"{nombre.split(' =')[0]} = 0 exactamente",
                                 marker=dict(symbol="triangle-down", size=10, color=color),
                                 hovertemplate="k = %{x}<br>valor = 0 exactamente<extra></extra>"))
    return trazas


# Estado final según el código de terminación del núcleo (algebra/.../ejecucion.py).
# El texto se elige por el código: nunca se deduce «converge» a partir de la curva.
# {d}, {r} y {kmax} se rellenan con la forma del símbolo que corresponda (estado_final).
ESTADOS_FINALES = {
    "TOLERANCIA_CAMBIO": ("Criterio A cumplido en k = {k}: {d} < ε", COLOR_EPSILON),
    "TOLERANCIA_RESIDUO": ("Criterio B cumplido en k = {k}: {r} < ε", COLOR_EPSILON),
    "N_COMPLETADAS": ("Se completaron N = {k} iteraciones (criterio C: no demuestra convergencia)", SUAVE),
    "MAXIMO_ITERACIONES": ("Se alcanzó {kmax} = {k} sin cumplir el criterio", COLOR_RESIDUO),
    "ERROR_NO_FINITO": ("Aparecieron valores no finitos: el cálculo se detuvo en k = {k}", "#F87171"),
}
COLOR_SELECCION = "#E6ECF7"


def estado_final(codigo, k, forma="html"):
    """Texto del estado final con la notación de `forma` ("html" para Plotly, "texto"
    para insignias y tablas).  None si el código no tiene estado final."""
    if codigo not in ESTADOS_FINALES:
        return None
    plantilla = ESTADOS_FINALES[codigo][0]
    return plantilla.format(k=k, d=getattr(notacion.D_K, forma), r=getattr(notacion.R_K, forma),
                            kmax=getattr(notacion.K_MAX, forma))


def _tramos_crecientes(ks, valores):
    """Intervalos [k_ini, k_fin] en los que d_k aumenta de una iteración a la siguiente."""
    tramos = []
    for (k0, v0), (k1, v1) in zip(zip(ks, valores), zip(ks[1:], valores[1:])):
        if v0 is not None and v1 is not None and v0 > 0 and v1 > v0:
            if tramos and tramos[-1][1] == k0:
                tramos[-1][1] = k1
            else:
                tramos.append([k0, k1])
    return tramos


def convergencia(historial, criterio, tolerancia=None, metodo=None, codigo=None, k_destacada=None):
    """d_k y r_k frente a k.  Con `codigo` (código de terminación del núcleo) se rotula el
    estado final real; con `k_destacada` se marca una iteración elegida por el usuario."""
    fig = _base("Evolución del cambio entre iteraciones y del residuo" + (f" · {metodo}" if metodo else ""),
                alto=470)
    ks = [f.k for f in historial]
    k_final = ks[-1] if ks else None
    detalle = {f.k: f"<br>{notacion.X_K.html} = {_texto_vector(f.x)}" for f in historial}
    especiales = {}
    if ks:
        especiales[ks[0]] = SUAVE
        especiales[k_final] = COLOR_SELECCION
    if k_destacada is not None:
        especiales[k_destacada] = "#22D3EE"
    series = [(notacion.D_K_DEF.html, [f.d for f in historial], COLOR_RECTA, "circle", "solid", "A"),
              (notacion.R_K_DEF.html, [f.r for f in historial], COLOR_RESIDUO, "square", "dash", "B")]
    for nombre, valores, color, simbolo, guion, letra in series:
        etiqueta = nombre + (" (criterio de parada)" if criterio == letra else " (informativo)")
        for traza in _serie(ks, valores, etiqueta, color, simbolo, guion,
                            detalle if letra == "B" else None, especiales):
            fig.add_trace(traza)
    if tolerancia is not None and criterio in ("A", "B"):
        fig.add_hline(y=float(tolerancia), line=dict(color=COLOR_EPSILON, dash="dashdot", width=1.6),
                      annotation_text=f"ε = {float(tolerancia):.3g}", annotation_font_color=COLOR_EPSILON)
    # Tramos en que d_k aumenta: es un dato observado, no un diagnóstico de divergencia.
    tramos = _tramos_crecientes(ks, [f.d for f in historial])
    for k0, k1 in tramos:
        fig.add_vrect(x0=k0, x1=k1, fillcolor="rgba(251,191,36,0.08)", line_width=0, layer="below")
    if tramos:
        fig.add_annotation(text=f"Sombreado: tramos en que {notacion.D_K.html} aumentó", xref="paper",
                           yref="paper", x=0, y=1.0, xanchor="left", yanchor="bottom", showarrow=False,
                           font=dict(size=11, color=COLOR_RESIDUO))
    if codigo in ESTADOS_FINALES and k_final is not None:
        color = ESTADOS_FINALES[codigo][1]
        fig.add_annotation(text=estado_final(codigo, k_final), xref="paper", yref="paper", x=1, y=1.0,
                           xanchor="right", yanchor="bottom", showarrow=False,
                           font=dict(size=12, color=color))
        serie = {"TOLERANCIA_CAMBIO": historial[-1].d, "TOLERANCIA_RESIDUO": historial[-1].r}.get(codigo)
        if serie is not None and serie > 0:
            fig.add_annotation(x=k_final, y=_y_log(serie), text="ε alcanzado", showarrow=True, arrowhead=0,
                               ax=-60, ay=-80, arrowcolor=COLOR_EPSILON, font=dict(size=11, color=COLOR_EPSILON))
    if k_destacada is not None and k_destacada in ks:
        fig.add_vline(x=k_destacada, line=dict(color="#22D3EE", dash="dot", width=1.4))
    fig.update_layout(xaxis=_eje("Iteración k", dtick=1 if len(ks) <= 25 else None, zeroline=False),
                      yaxis=_eje("Valor (escala logarítmica)", log=True), hovermode="x unified")
    return fig


def comparacion(resultados, metrica, errores_historial=None, destacado=None, k_destacada=None,
                criterio=None, tolerancia=None):
    """Una traza por método.  `destacado` atenúa los demás métodos; `k_destacada` marca una
    iteración; ε se dibuja solo si la métrica es la del criterio real (d con A, r con B)."""
    simbolo, definicion = notacion.METRICAS[metrica]
    fig = _base("Comparación de métodos: " + TITULOS_METRICA[metrica] + " " + simbolo.html, alto=470)
    for indice, r in enumerate(resultados):
        serie = serie_metrica(r, indice, metrica, errores_historial)
        if serie is None:
            continue
        ks, valores = serie
        metodo = r.configuracion.metodo
        nombre = metodo + (f" (ω = {float(r.configuracion.omega):.3g})" if metodo == "SOR" else "")
        puntos, _ = positivos(ks, valores)
        if puntos:
            xs = [p[0] for p in puntos]
            color = COLORES_METODOS.get(metodo)
            especiales = {xs[-1]: COLOR_SELECCION}
            if k_destacada is not None:
                especiales[k_destacada] = "#22D3EE"
            tamanos, bordes, anchos = _resaltes(xs, especiales)
            atenuado = destacado is not None and destacado != metodo
            fig.add_trace(go.Scatter(
                x=xs, y=[p[1] for p in puntos], mode="lines+markers", name=nombre,
                opacity=0.22 if atenuado else 1.0,
                line=dict(color=color, width=1.6 if atenuado else (3.2 if destacado else 2.4)),
                marker=dict(symbol=SIMBOLOS[MARCADORES.get(metodo, "o")], size=tamanos,
                            color=color, line=dict(color=bordes, width=anchos)),
                hovertemplate=f"<b>{nombre}</b><br>k = %{{x}}<br>{simbolo.html} = %{{y:.6e}}<extra></extra>"))
            if not atenuado:
                fig.add_annotation(x=xs[-1], y=_y_log(puntos[-1][1]), text=f"k = {xs[-1]}", showarrow=False,
                                   xshift=18, font=dict(size=11, color=color))
    if tolerancia is not None and (metrica, criterio) in (("d", "A"), ("r", "B")):
        fig.add_hline(y=float(tolerancia), line=dict(color=COLOR_EPSILON, dash="dashdot", width=1.6),
                      annotation_text=f"ε = {float(tolerancia):.3g}", annotation_font_color=COLOR_EPSILON)
    if k_destacada is not None:
        fig.add_vline(x=k_destacada, line=dict(color="#22D3EE", dash="dot", width=1.4))
    fig.update_layout(xaxis=_eje("Iteración k", zeroline=False),
                      yaxis=_eje(definicion.html + " (escala log.)", log=True), hovermode="x unified")
    return fig


def autovalores(lista, rho):
    fig = _base("Autovalores de la matriz de iteración", alto=520)
    angulos = [2 * math.pi * k / 200 for k in range(201)]
    fig.add_trace(go.Scatter(x=[math.cos(t) for t in angulos], y=[math.sin(t) for t in angulos], mode="lines",
                             name="|λ| = 1 (frontera de convergencia)", fill="toself",
                             fillcolor="rgba(52,211,153,0.07)", line=dict(color=COLOR_EPSILON, width=2.4),
                             hoverinfo="skip"))
    fig.add_trace(go.Scatter(x=[rho * math.cos(t) for t in angulos], y=[rho * math.sin(t) for t in angulos],
                             mode="lines", name=f"|λ| = ρ(T) = {rho:.4g}", hoverinfo="skip",
                             line=dict(color="#F472B6", dash="dash", width=1.8)))
    # Los autovalores de módulo máximo (los que definen ρ) se resaltan; solo cambia el estilo.
    dominante = [rho > 0 and abs(z) >= rho * (1 - 1e-9) for z in lista]
    fig.add_trace(go.Scatter(
        x=[z.real for z in lista], y=[z.imag for z in lista], mode="markers", name="Autovalores de T",
        customdata=[abs(z) for z in lista],
        marker=dict(size=[16 if d else 12 for d in dominante], color=COLOR_DATOS,
                    line=dict(color=["#F472B6" if d else "#0B1020" for d in dominante],
                              width=[3 if d else 1.5 for d in dominante])),
        hovertemplate="<b>λ</b> = %{x:.6g} %{y:+.6g}i<br>|λ| = %{customdata:.6g}<extra></extra>"))
    if any(dominante):
        z = lista[dominante.index(True)]
        fig.add_annotation(x=z.real, y=z.imag, text="|λ| = ρ(T)", showarrow=True, arrowhead=0, ax=-60, ay=-50,
                           arrowcolor="#F472B6", font=dict(size=11, color="#F472B6"))
    limite = max(1.2, rho * 1.2)
    fig.update_layout(xaxis=_eje("Parte real", range=[-limite, limite]),
                      yaxis=_eje("Parte imaginaria", range=[-limite, limite], scaleanchor="x"),
                      hovermode="closest")
    return fig


TOPE_GRAFICA = 1e6


def precondicionador(comparaciones):
    fig = _base("Efecto del precondicionador diagonal M = D", alto=470)
    minimo, recortado = None, False
    for f in comparaciones:
        for resultado, guion, sufijo in ((f.original, "solid", "original"), (f.precondicionado, "dash", "con M = D")):
            puntos, _ = positivos([fila.k for fila in resultado.historial], [fila.d for fila in resultado.historial])
            if not puntos:
                continue
            recortado = recortado or max(p[1] for p in puntos) > TOPE_GRAFICA
            minimo = min([p[1] for p in puntos] + ([minimo] if minimo else []))
            color = COLORES_METODOS.get(f.metodo)
            fig.add_trace(go.Scatter(
                x=[p[0] for p in puntos], y=[p[1] for p in puntos], mode="lines+markers",
                name=f"{f.metodo} ({sufijo})", legendgroup=f.metodo,
                line=dict(color=color, width=2.2, dash=guion),
                marker=dict(symbol=SIMBOLOS[MARCADORES.get(f.metodo, "o")], size=6, color=color),
                hovertemplate=f"<b>{f.metodo} ({sufijo})</b><br>k = %{{x}}<br>{notacion.D_K.html} = %{{y:.6e}}"
                              "<extra></extra>"))
    eje_y = _eje(notacion.D_K_DEF.html + " (escala log.)", log=True)
    if recortado:
        # Vista inicial acotada: una curva divergente taparía a las demás.  Los datos
        # están completos; «Autoescala» o el zoom muestran la curva entera.
        eje_y["range"] = [math.log10(min(minimo, 1.0) / 10), math.log10(TOPE_GRAFICA)]
        fig.add_annotation(text=f"Vista inicial acotada en {TOPE_GRAFICA:.0e}: una curva diverge "
                                "(use «Autoescala» para verla completa)",
                           xref="paper", yref="paper", x=1, y=0.01, xanchor="right", showarrow=False,
                           font=dict(size=11, color=SUAVE))
    fig.update_layout(xaxis=_eje("Iteración k", zeroline=False), yaxis=eje_y, hovermode="x unified")
    return fig
