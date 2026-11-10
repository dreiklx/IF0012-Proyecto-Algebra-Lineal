"""Genera un HTML autónomo (sin internet) de docs/guia_estudio_if0012.md.

Herramienta de desarrollo: no forma parte del ZIP de entrega.  Reutiliza, sin
modificarlos, el estilo (CSS), el script de navegación y las funciones de conversión
de generar_guia_html.py: los lee de su código fuente con el AST, porque ese archivo
genera la guía de defensa al importarse.  Requiere el paquete `markdown`.

Uso, desde la raíz del proyecto:
    python herramientas/generar_guia_estudio_html.py [salida.html ...]
Siempre escribe dist/Guia_Estudio_IF0012.html; las rutas extra reciben una copia idéntica.
"""
import ast
import html
import os
import re
import sys
import unicodedata

import markdown

raiz = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
fuente = os.path.join(raiz, "herramientas", "generar_guia_html.py")
arbol = ast.parse(open(fuente, encoding="utf-8").read())
comun = {"re": re, "html": html, "unicodedata": unicodedata, "markdown": markdown}
for nodo in arbol.body:
    if isinstance(nodo, ast.FunctionDef) and nodo.name in ("preparar", "slug", "convertir", "lista_toc"):
        exec(compile(ast.Module([nodo], []), fuente, "exec"), comun)
    elif isinstance(nodo, ast.Assign) and getattr(nodo.targets[0], "id", "") in ("CSS", "JS"):
        comun[nodo.targets[0].id] = ast.literal_eval(nodo.value)

with open(os.path.join(raiz, "docs", "guia_estudio_if0012.md"), encoding="utf-8") as f:
    md = f.read()
version = re.search(r"\*\*Versión:\*\* (\S+?)\.?\s", md).group(1)
md = re.sub(r"^# .*\n", "", md, count=1)
md = re.sub(r"## Índice\n.*?\n---\n", "", md, count=1, flags=re.S)

usados, toc = set(), []
cuerpo = comun["convertir"](md, "e", usados, toc)
cuerpo = re.sub(r'<a href="(?!#|https?:)[^"]*">(.*?)</a>', r'<span class="ref">\1</span>', cuerpo)

CSS_EXTRA = """
.portada{background:linear-gradient(135deg,#0f3d7a,#1f6fb2)}
td code,th code{white-space:nowrap}
"""

documento = f"""<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Guía de estudio Ax</title>
<style>{comun["CSS"]}{CSS_EXTRA}</style>
</head>
<body>
<div class="marco">
<nav>
<div class="marca">Guía de estudio · Ax</div>
<div class="sub">IF0012 · Grupo 01 · {html.escape(version)}</div>
<input id="filtro" type="search" placeholder="Buscar en el índice…" aria-label="Buscar en el índice">
<h4>Contenido</h4>
<ul>
{comun["lista_toc"](toc)}
</ul>
</nav>
<main>
<header class="portada">
<h1>Guía de estudio del proyecto Ax</h1>
<p>IF0012 Álgebra Lineal para Informática Empresarial · UCR Sede del Caribe · II Ciclo 2026</p>
<p>Elmer López Hernández · Derek Farley Noguera · Daniel Córdoba Arias · Samir Sandoval Ramírez</p>
<div class="insignias"><span>Versión {html.escape(version)}</span><span>Entrega 11-nov</span><span>Defensa semana del 16-nov</span><span>Cat. A clase · B enunciado · C extensión</span></div>
</header>
<section class="parte">
{cuerpo}
</section>
<p class="pie">Generado desde docs/guia_estudio_if0012.md · funciona sin internet</p>
</main>
</div>
<button class="tema" id="tema" type="button">Tema</button>
<button class="arriba" id="arriba" type="button" aria-label="Volver arriba">↑</button>
<script>{comun["JS"]}</script>
</body>
</html>
"""

salidas = [os.path.join(raiz, "dist", "Guia_Estudio_IF0012.html")] + sys.argv[1:]
for salida in salidas:
    with open(salida, "w", encoding="utf-8") as f:
        f.write(documento)
    print(salida, len(documento), "caracteres;", len(toc), "entradas de índice")
