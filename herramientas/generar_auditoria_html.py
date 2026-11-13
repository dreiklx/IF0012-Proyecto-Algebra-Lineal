"""Genera docs/auditoria_visual_procedimientos_profesora.html a partir de la auditoría.

Herramienta de desarrollo (no entra en la aplicación).  Lee:
  docs/auditoria/resultados_comparacion.csv   una fila por procedimiento comparado
  docs/auditoria/inventario_paginas.csv       estado de revisión de cada página
  docs/auditoria/evidencias/modulo_*/*.jpg    páginas reales extraídas de los PDF
  docs/auditoria/discrepancias.md             texto de las discrepancias (se enlaza tal cual)

El HTML es autónomo salvo las imágenes, que van con rutas relativas.  Sin recursos externos.
Uso: python herramientas/generar_auditoria_html.py
"""
import csv
import glob
import html
import os
from collections import Counter, defaultdict

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
AUD = os.path.join(RAIZ, "docs", "auditoria")
SALIDA = os.path.join(RAIZ, "docs", "auditoria_visual_procedimientos_profesora.html")

MODULOS = {
    "I": "Módulo I · Sistemas lineales (Gauss, Gauss-Jordan)",
    "II": "Módulo II · Determinantes, inversa, normas y condicionamiento",
    "III": "Módulo III · Mínimos cuadrados, ecuaciones normales, Cramer, ajuste",
    "IV": "Módulo IV · Jacobi, Gauss-Seidel, SOR, convergencia y radio espectral",
}
COLOR = {"Coincide": "ok", "Coincide con Ax": "ok", "Coincide (exacto)": "ok", "Coincide (dominancia es suficiente; la lámina la usa para concluir)": "ok",
         "Error": "err", "Diferencia justificada": "dif", "Pendiente": "pen"}


def clase_resultado(texto):
    for clave, cls in COLOR.items():
        if texto.startswith(clave):
            return cls
    if "Error" in texto or "errata" in texto:
        return "err"
    if "Pendiente" in texto or "pendiente" in texto or "dudosa" in texto:
        return "pen"
    return "ok"


def leer_csv(ruta):
    with open(ruta, encoding="utf-8") as f:
        return list(csv.DictReader(f))


def evidencia(fuente, pagina, modulo):
    """Imagen real de la página (docs/auditoria/evidencias/modulo_X/<doc>_p<n>.jpg), o None."""
    nombre = f"{fuente.split('/')[0]}_p{pagina}.jpg"
    ruta = os.path.join(AUD, "evidencias", f"modulo_{modulo}", nombre)
    if os.path.exists(ruta):
        return f"auditoria/evidencias/modulo_{modulo}/{nombre}"
    return None


def main():
    filas = leer_csv(os.path.join(AUD, "resultados_comparacion.csv"))
    inventario = leer_csv(os.path.join(AUD, "inventario_paginas.csv"))
    estados = Counter(f["estado_revision"] for f in inventario)
    por_modulo = defaultdict(list)
    for f in filas:
        por_modulo[f["modulo"]].append(f)

    nav = []
    cuerpo = []
    for clave, titulo in MODULOS.items():
        nav.append(f'<li><a href="#m{clave}">{html.escape(titulo)}</a></li>')
        cuerpo.append(f'<section id="m{clave}"><h2>{html.escape(titulo)}</h2>')
        if not por_modulo[clave]:
            cuerpo.append('<p class="pen">Sin revisión visual todavía. Estas páginas están marcadas como '
                          '«Solo OCR (pendiente de revisión visual)» en docs/auditoria/inventario_paginas.csv.</p>')
        for f in por_modulo[clave]:
            img = (f"auditoria/evidencias/{f['imagen']}" if f.get("imagen")
                   else evidencia(f["fuente"], f["pagina"], clave))
            es_pdf = not f["fuente"].startswith("Visualización")
            cuerpo.append('<article class="proc">')
            cuerpo.append(f'<h3>{html.escape(f["procedimiento"])}</h3>')
            if es_pdf:
                cuerpo.append(f'<p class="fuente"><b>Fuente:</b> {html.escape(f["fuente"])}, página {html.escape(f["pagina"])}'
                              ' · imagen extraída del PDF original (sin recrear)</p>')
            else:
                cuerpo.append('<p class="fuente"><b>Visualización complementaria</b> (no es materia expresamente '
                              'explicada en clase): captura de la aplicación real.</p>')
            if img:
                cuerpo.append(f'<a href="{img}" target="_blank"><img src="{img}" alt="{html.escape(f["procedimiento"])}"></a>')
            cuerpo.append('<h4>Cómo lo hace la profesora</h4>')
            cuerpo.append(f'<p class="mono">{html.escape(f["formula_o_paso_profesora"])}</p>')
            cuerpo.append('<h4>Implementación en Ax</h4>')
            cuerpo.append(f'<p class="mono">{html.escape(f["implementacion_ax"])}</p>')
            cuerpo.append('<h4>Comparación</h4>')
            cuerpo.append(f'<p class="res {clase_resultado(f["resultado"])}">{html.escape(f["resultado"])}</p>')
            cuerpo.append(f'<p class="small">Revisión: {html.escape(f["revision"])}</p>')
            cuerpo.append("</article>")
        cuerpo.append("</section>")

    discrepancias = ""
    ruta_d = os.path.join(AUD, "discrepancias.md")
    if os.path.exists(ruta_d):
        discrepancias = html.escape(open(ruta_d, encoding="utf-8").read())

    resumen = "".join(f"<tr><td>{html.escape(k)}</td><td>{v}</td></tr>" for k, v in estados.most_common())
    doc = f"""<!doctype html>
<html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Auditoría visual · procedimientos de la profesora</title>
<style>
:root{{--fondo:#f7f8fb;--texto:#1c2330;--acento:#1f6fb2;--ok:#1b7f4b;--dif:#9a6700;--err:#b42318;--pen:#6b5b95;--borde:#d9dee8}}
@media (prefers-color-scheme: dark){{:root:not([data-theme="light"]){{--fondo:#0f1521;--texto:#e6ebf3;--acento:#60a5fa;--borde:#263142}}}}
:root[data-theme="dark"]{{--fondo:#0f1521;--texto:#e6ebf3;--acento:#60a5fa;--borde:#263142}}
body{{margin:0;background:var(--fondo);color:var(--texto);font:16px/1.5 system-ui,Segoe UI,sans-serif}}
nav{{position:fixed;left:0;top:0;bottom:0;width:280px;overflow:auto;padding:16px;border-right:1px solid var(--borde);background:var(--fondo)}}
main{{margin-left:300px;padding:24px 32px;max-width:1100px}}
nav a{{color:var(--acento);text-decoration:none;display:block;padding:4px 0}}
h1{{font-size:1.6rem}} h2{{border-bottom:2px solid var(--acento);padding-bottom:4px;margin-top:36px}}
.proc{{border:1px solid var(--borde);border-radius:10px;padding:16px 20px;margin:18px 0}}
.proc img{{max-width:100%;border:1px solid var(--borde);border-radius:6px}}
.mono{{font-family:Consolas,monospace;white-space:pre-wrap;background:rgba(127,127,127,.08);padding:8px;border-radius:6px}}
.res{{font-weight:600;padding:6px 10px;border-radius:6px}}
.ok{{color:var(--ok)}} .dif{{color:var(--dif)}} .err{{color:var(--err)}} .pen{{color:var(--pen)}}
.fuente,.small{{font-size:.9rem;opacity:.85}}
table{{border-collapse:collapse}} td,th{{border:1px solid var(--borde);padding:4px 8px}}
pre{{white-space:pre-wrap;font-size:.85rem}}
@media print{{nav{{display:none}} main{{margin:0}} .proc{{page-break-inside:avoid}}}}
@media (max-width:900px){{nav{{position:static;width:auto;border:0}} main{{margin:0;padding:16px}}}}
</style></head><body>
<nav><b>Auditoría visual</b><ul style="list-style:none;padding:0">{''.join(nav)}</ul>
<a href="#resumen">Resumen del inventario</a><a href="#discrepancias">Discrepancias</a></nav>
<main>
<h1>Auditoría visual de los procedimientos de la profesora frente a Ax</h1>
<p>Cada imagen es una página original extraída de los PDF de clase (no recreada). Los estados se asignan
solo tras revisar la página visualmente; las páginas leídas solo por OCR se indican como tales.</p>
<h2 id="resumen">Resumen del inventario (18 PDF, 457 páginas)</h2>
<table><tr><th>Estado de revisión</th><th>Páginas</th></tr>{resumen}</table>
{''.join(cuerpo)}
<section id="discrepancias"><h2>Discrepancias y pendientes</h2><pre>{discrepancias}</pre></section>
</main></body></html>
"""
    with open(SALIDA, "w", encoding="utf-8") as f:
        f.write(doc)
    print(SALIDA, len(doc), "caracteres;", len(filas), "procedimientos;", sum(estados.values()), "páginas en inventario")


if __name__ == "__main__":
    main()
