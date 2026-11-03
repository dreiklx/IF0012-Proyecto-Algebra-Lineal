"""Genera un HTML autónomo (sin dependencias externas) con la guía de defensa
(docs/guia_defensa_equipo.md) y el resumen por módulo (docs/resumen_logica_por_modulo.md).

Herramienta de desarrollo: no forma parte del ZIP de entrega.  Requiere el paquete
`markdown` (requirements-desarrollo.txt).

Uso, desde la raíz del proyecto:
    .venv/Scripts/python herramientas/generar_guia_html.py [salida_extra.html ...]
Siempre escribe dist/Guia_Defensa_IF0012.html; las rutas extra reciben una copia idéntica
(por ejemplo, la del escritorio que se compartió con el equipo).
"""
import html
import os
import re
import sys
import unicodedata

import markdown

raiz = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
salidas = [os.path.join(raiz, "dist", "Guia_Defensa_IF0012.html")] + sys.argv[1:]


def leer(nombre):
    with open(os.path.join(raiz, "docs", nombre), encoding="utf-8") as f:
        return f.read()


def preparar(md):
    """Python-Markdown exige 4 espacios para anidar listas; los documentos usan 2-3.
    Se duplica la sangría inicial de cada línea (fuera de los bloques de código)."""
    salida, en_codigo = [], False
    for linea in md.splitlines():
        if linea.lstrip().startswith("```"):
            en_codigo = not en_codigo
            salida.append(linea.lstrip() if not linea.startswith(" ") else " " * (2 * (len(linea) - len(linea.lstrip()))) + linea.lstrip())
            continue
        if en_codigo:
            salida.append(linea)
            continue
        sangria = len(linea) - len(linea.lstrip(" "))
        # «x*» (solución exacta) no debe abrir una cursiva: se escapa el asterisco
        # suelto que sigue a una letra, fuera del código en línea.
        partes = linea.lstrip(" ").split("`")
        for k in range(0, len(partes), 2):
            partes[k] = re.sub(r"(?<=[A-Za-z0-9)])\*(?!\*)", r"\*", partes[k])
            partes[k] = partes[k].replace("_", r"\_").replace("<", "&lt;")   # los documentos no usan _ para cursiva
        salida.append(" " * (2 * sangria) + "`".join(partes))
    return "\n".join(salida)


def slug(texto, usados):
    base = unicodedata.normalize("NFKD", re.sub(r"<[^>]+>", "", texto))
    base = "".join(c for c in base if not unicodedata.combining(c)).lower()
    base = re.sub(r"[^a-z0-9]+", "-", base).strip("-") or "seccion"
    s, k = base, 2
    while s in usados:
        s, k = f"{base}-{k}", k + 1
    usados.add(s)
    return s


def convertir(md, prefijo, usados, toc):
    cuerpo = markdown.markdown(preparar(md), extensions=["tables", "fenced_code", "sane_lists", "nl2br"])
    # Las tablas se envuelven para permitir desplazamiento horizontal.
    cuerpo = cuerpo.replace("<table>", '<div class="tabla"><table>').replace("</table>", "</table></div>")

    def poner_id(m):
        nivel, texto = m.group(1), m.group(2)
        ident = slug(prefijo + " " + texto, usados)
        if nivel in ("2", "3"):
            toc.append((int(nivel), ident, re.sub(r"<[^>]+>", "", texto)))
        return f'<h{nivel} id="{ident}">{texto}</h{nivel}>'

    return re.sub(r"<h([1-4])>(.*?)</h\1>", poner_id, cuerpo)


guia = leer("guia_defensa_equipo.md")
# Datos de la portada tomados de la propia guía, para que no se desactualicen.
version = re.search(r"\*\*Versión:\*\* (\S+)", guia).group(1)
pruebas = re.search(r"Deben salir \*\*(\d+) pruebas OK\*\*", guia).group(1)
resumen = leer("resumen_logica_por_modulo.md")
# Se quitan el título (va en la portada) y el índice manual (se genera la barra lateral).
guia = re.sub(r"^# .*\n", "", guia, count=1)
guia = re.sub(r"## Índice\n.*?\n---\n", "", guia, count=1, flags=re.S)
resumen = re.sub(r"^# .*\n", "", resumen, count=1)
resumen = resumen.replace("](guia_defensa_equipo.md)", "](#parte-1)")
guia = guia.replace("](resumen_logica_por_modulo.md)", "](#parte-2)")
for nombre in ("pendientes_docente.md", "comparacion_procedimientos.md"):
    guia = guia.replace(f"]({nombre})", f"](docs/{nombre})")
    resumen = resumen.replace(f"]({nombre})", f"](docs/{nombre})")

usados, toc = set(), []
html_guia = convertir(guia, "g", usados, toc)
toc_guia = list(toc)
toc.clear()
html_resumen = convertir(resumen, "r", usados, toc)
toc_resumen = list(toc)

# Enlaces a otros documentos del repositorio: se convierten en texto (no existen junto al HTML).
def desenlazar(h):
    return re.sub(r'<a href="(?!#|https?:)[^"]*">(.*?)</a>', r'<span class="ref">\1</span>', h)

html_guia, html_resumen = desenlazar(html_guia), desenlazar(html_resumen)


def lista_toc(entradas):
    partes, abierta = [], False
    for nivel, ident, texto in entradas:
        if nivel == 2:
            if abierta:
                partes.append("</ul></li>")
            partes.append(f'<li><a href="#{ident}">{html.escape(texto, quote=False)}</a><ul>')
            abierta = True
        else:
            partes.append(f'<li class="n3"><a href="#{ident}">{html.escape(texto, quote=False)}</a></li>')
    if abierta:
        partes.append("</ul></li>")
    return "\n".join(partes)


CSS = r"""
:root{--fondo:#f6f7fb;--papel:#ffffff;--texto:#1d2433;--suave:#5b6478;--borde:#dfe3ec;
--primario:#1f4e9c;--primario2:#e8eefb;--acento:#b4232c;--codigo:#f1f3f8;--zebra:#f8f9fc}
@media (prefers-color-scheme:dark){:root:not([data-tema=claro]){--fondo:#11151d;--papel:#171c26;--texto:#e6e9f0;
--suave:#a3acbf;--borde:#2c3443;--primario:#8fb2ff;--primario2:#1e2a44;--acento:#ff8a8f;--codigo:#202736;--zebra:#1b212c}}
:root[data-tema=oscuro]{--fondo:#11151d;--papel:#171c26;--texto:#e6e9f0;--suave:#a3acbf;--borde:#2c3443;
--primario:#8fb2ff;--primario2:#1e2a44;--acento:#ff8a8f;--codigo:#202736;--zebra:#1b212c}
*{box-sizing:border-box}
html{scroll-behavior:smooth;scroll-padding-top:16px}
body{margin:0;background:var(--fondo);color:var(--texto);font:16px/1.62 "Segoe UI",system-ui,-apple-system,Roboto,"Helvetica Neue",Arial,sans-serif}
.marco{display:grid;grid-template-columns:300px minmax(0,1fr);min-height:100vh}
nav{position:sticky;top:0;height:100vh;overflow:auto;background:var(--papel);border-right:1px solid var(--borde);padding:18px 16px 40px}
nav .marca{font-weight:700;color:var(--primario);font-size:15px;margin-bottom:4px}
nav .sub{font-size:12px;color:var(--suave);margin-bottom:12px}
nav input{width:100%;padding:7px 10px;border:1px solid var(--borde);border-radius:8px;background:var(--fondo);color:var(--texto);font-size:13px;margin-bottom:12px}
nav h4{font-size:11px;letter-spacing:.08em;text-transform:uppercase;color:var(--suave);margin:16px 0 6px}
nav ul{list-style:none;margin:0;padding:0}
nav li{margin:1px 0}
nav li ul{padding-left:12px;border-left:2px solid var(--borde);margin:2px 0 6px 4px}
nav a{color:var(--texto);text-decoration:none;font-size:13.5px;display:block;padding:3px 6px;border-radius:6px}
nav li.n3 a{font-size:12.5px;color:var(--suave)}
nav a:hover,nav a.activo{background:var(--primario2);color:var(--primario)}
main{padding:28px 40px 80px;max-width:1080px;width:100%}
.portada{background:linear-gradient(135deg,#1f4e9c,#3b6fd1);color:#fff;border-radius:16px;padding:28px 30px;margin-bottom:26px}
.portada h1{margin:0 0 6px;font-size:30px;line-height:1.2}
.portada p{margin:4px 0;opacity:.95}
.insignias{display:flex;flex-wrap:wrap;gap:8px;margin-top:14px}
.insignias span{background:rgba(255,255,255,.17);border:1px solid rgba(255,255,255,.35);border-radius:999px;padding:3px 12px;font-size:13px}
.parte{background:var(--papel);border:1px solid var(--borde);border-radius:14px;padding:6px 34px 30px;margin-bottom:28px}
.parte>h1.titulo-parte{font-size:24px;color:var(--primario);border-bottom:3px solid var(--primario);padding-bottom:8px;margin-top:26px}
h2{font-size:22px;color:var(--primario);margin:40px 0 12px;padding-top:12px;border-top:1px solid var(--borde)}
h3{font-size:18px;margin:28px 0 8px}
h4{font-size:16px;margin:20px 0 6px}
p{margin:8px 0}
a{color:var(--primario)}
strong{color:inherit}
blockquote{margin:14px 0;padding:10px 16px;background:var(--primario2);border-left:4px solid var(--primario);border-radius:0 10px 10px 0}
code{font-family:Consolas,"Cascadia Mono","SFMono-Regular",Menlo,monospace;font-size:.88em;background:var(--codigo);padding:1px 5px;border-radius:5px}
pre{background:var(--codigo);border:1px solid var(--borde);border-radius:10px;padding:12px 14px;overflow:auto;line-height:1.4}
pre code{background:none;padding:0;font-size:13px}
ul,ol{padding-left:26px}
li{margin:3px 0}
.tabla{overflow-x:auto;margin:12px 0;border:1px solid var(--borde);border-radius:10px}
table{border-collapse:collapse;width:100%;font-size:14px}
th{background:var(--primario2);color:var(--primario);text-align:left;font-weight:600}
th,td{padding:7px 10px;border-bottom:1px solid var(--borde);vertical-align:top}
tr:nth-child(even) td{background:var(--zebra)}
.ref{font-style:italic}
.arriba{position:fixed;right:20px;bottom:20px;background:var(--primario);color:#fff;border:none;border-radius:999px;width:42px;height:42px;font-size:20px;cursor:pointer;box-shadow:0 4px 12px rgba(0,0,0,.25)}
.tema{position:fixed;right:70px;bottom:20px;background:var(--papel);color:var(--texto);border:1px solid var(--borde);border-radius:999px;height:42px;padding:0 14px;cursor:pointer;font-size:13px}
.pie{color:var(--suave);font-size:13px;text-align:center;margin-top:30px}
@media (max-width:900px){.marco{grid-template-columns:1fr}nav{position:static;height:auto;max-height:50vh;border-right:none;border-bottom:1px solid var(--borde)}
main{padding:16px}.parte{padding:4px 16px 20px}.portada h1{font-size:24px}}
@media print{nav,.arriba,.tema{display:none}.marco{display:block}main{max-width:none;padding:0}
.parte{border:none;padding:0}h2{break-before:page}.portada{background:#1f4e9c;-webkit-print-color-adjust:exact;print-color-adjust:exact}
tr,pre,blockquote{break-inside:avoid}}
"""

JS = r"""
const filtro=document.getElementById('filtro');
filtro.addEventListener('input',()=>{const q=filtro.value.toLowerCase();
document.querySelectorAll('nav li').forEach(li=>{li.style.display=li.textContent.toLowerCase().includes(q)?'':'none';});});
const enlaces=[...document.querySelectorAll('nav a')];
const mapa=new Map(enlaces.map(a=>[a.getAttribute('href').slice(1),a]));
const obs=new IntersectionObserver(es=>{es.forEach(e=>{if(e.isIntersecting){enlaces.forEach(a=>a.classList.remove('activo'));
const a=mapa.get(e.target.id);if(a)a.classList.add('activo');}});},{rootMargin:'0px 0px -75% 0px'});
document.querySelectorAll('main h2[id],main h3[id]').forEach(h=>obs.observe(h));
document.getElementById('arriba').onclick=()=>window.scrollTo({top:0});
const raiz=document.documentElement;
try{const t=localStorage.getItem('tema-guia');if(t)raiz.dataset.tema=t;}catch(e){}
document.getElementById('tema').onclick=()=>{const oscuro=raiz.dataset.tema==='oscuro'||(!raiz.dataset.tema&&matchMedia('(prefers-color-scheme: dark)').matches);
raiz.dataset.tema=oscuro?'claro':'oscuro';try{localStorage.setItem('tema-guia',raiz.dataset.tema);}catch(e){}};
"""

documento = f"""<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Guía de defensa IF0012</title>
<style>{CSS}</style>
</head>
<body>
<div class="marco">
<nav aria-label="Índice">
  <div class="marca">Guía de defensa · IF0012</div>
  <div class="sub">Álgebra Lineal · II Ciclo 2026</div>
  <input id="filtro" type="search" placeholder="Buscar en el índice…" aria-label="Buscar en el índice">
  <h4><a href="#parte-1">Parte 1 · Guía completa</a></h4>
  <ul>{lista_toc(toc_guia)}</ul>
  <h4><a href="#parte-2">Parte 2 · Resumen por módulo</a></h4>
  <ul>{lista_toc(toc_resumen)}</ul>
</nav>
<main>
<header class="portada">
  <h1>Guía de defensa del equipo — Proyecto final IF0012</h1>
  <p>Álgebra Lineal para Informática Empresarial · Universidad de Costa Rica, Sede del Caribe (Siquirres) · II Ciclo 2026</p>
  <p>Elmer López Hernández · Derek Farley Noguera · Daniel Córdoba Arias · Samir Sandoval Ramírez</p>
  <div class="insignias"><span>Versión {version}</span><span>{pruebas} pruebas automáticas OK</span>
  <span>Auditoría independiente: 0 fallos</span><span>Entrega: 11-nov-2026</span><span>Defensa: semana del 16-nov-2026</span></div>
</header>
<section class="parte" id="parte-1"><h1 class="titulo-parte">Parte 1 · Guía completa</h1>
{html_guia}
</section>
<section class="parte" id="parte-2"><h1 class="titulo-parte">Parte 2 · Resumen de la lógica por módulo</h1>
{html_resumen}
</section>
<p class="pie">Generado a partir de <code>docs/guia_defensa_equipo.md</code> y <code>docs/resumen_logica_por_modulo.md</code>.
Funciona sin conexión a internet: no usa archivos externos.</p>
</main>
</div>
<button class="tema" id="tema" title="Cambiar tema">Claro / oscuro</button>
<button class="arriba" id="arriba" title="Volver arriba" aria-label="Volver arriba">↑</button>
<script>{JS}</script>
</body>
</html>
"""
for salida in salidas:
    os.makedirs(os.path.dirname(os.path.abspath(salida)), exist_ok=True)
    with open(salida, "w", encoding="utf-8") as f:
        f.write(documento)
    print(salida, len(documento), "caracteres;", len(toc_guia), "+", len(toc_resumen), "entradas de índice")
