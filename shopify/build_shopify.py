"""Arma los archivos del tema de Shopify para el acceso de los compradores.

  templates/page.ebook-1.liquid     → versión interactiva del ebook 1 (solo clientes con etiqueta ebook1)
  templates/page.ebook-2.liquid     → versión interactiva del ebook 2 (solo clientes con etiqueta ebook2)
  templates/page.mis-ebooks.liquid  → página "Mis ebooks" con los libros que compró cada cliente

El contenido se arma a partir de ebook/web.html y ebook/web2.html (ver ebook/build_web.py).
El acceso se controla con Liquid en el servidor: si el cliente no inició sesión o no tiene
la etiqueta, el contenido del ebook ni siquiera se envía al navegador.

Uso: python3 build_shopify.py
"""
import os, re

here = os.path.dirname(os.path.abspath(__file__))
root = os.path.dirname(here)
out = os.path.join(here, "templates")
os.makedirs(out, exist_ok=True)

PRODUCT_URL = "/products/consegui-trabajo-en-30-dias"  # ⚠️ handle del producto en tu tienda

HEAD = """{%- layout none -%}
<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="robots" content="noindex">
<title>TITLE · Método 30</title>
</head>
<body style="margin:0">
"""
FOOT = "\n</body>\n</html>\n"

GATE = """<style>
.gate{min-height:100vh;display:flex;align-items:center;justify-content:center;padding:24px;background:radial-gradient(circle at 85% 0%,#3A3F9E 0%,#14213D 55%,#0B1226 100%);font-family:'Source Sans 3','Segoe UI',system-ui,sans-serif;color:#fff;box-sizing:border-box}
.gate-card{max-width:460px;width:100%;background:#fff;color:#1C2333;border-radius:20px;padding:34px 30px;text-align:center;box-shadow:0 30px 70px rgba(0,0,0,.35)}
.gate-card h1{font-family:'Bricolage Grotesque','Segoe UI',sans-serif;font-size:28px;line-height:1.1;margin:0 0 12px;color:#14213D}
.gate-card p{margin:0 0 22px;color:#5A6478;line-height:1.5}
.gate-btn{display:block;background:#E8632E;color:#fff;text-decoration:none;font-weight:700;padding:15px 20px;border-radius:999px;margin-bottom:12px}
.gate-link{color:#14213D;font-weight:600}
</style>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,800&family=Source+Sans+3:wght@400;600;700&display=swap">
<div class="gate"><div class="gate-card"><div style="font:800 13px/1 'Bricolage Grotesque',sans-serif;letter-spacing:.14em;text-transform:uppercase;color:#E8632E;margin-bottom:14px">Método 30</div>
{%- if customer -%}
  <h1>Todavía no tenés este ebook</h1>
  <p>Iniciaste sesión como {{ customer.email }}, pero esta cuenta no tiene acceso a este ebook. Si ya lo compraste con otro mail, cerrá sesión y entrá con ese. Si acabás de comprar, esperá unos minutos y recargá la página.</p>
  <a class="gate-btn" href="PRODUCT_URL">Conseguir el ebook</a>
  <a class="gate-link" href="{{ routes.account_logout_url }}">Cerrar sesión</a>
{%- else -%}
  <h1>Entrá para leer tu ebook</h1>
  <p>No necesitás contraseña ni registrarte antes:</p>
  <ol style="text-align:left;margin:0 0 22px;padding-left:22px;color:#5A6478;line-height:1.6">
    <li>Tocá <b>Iniciar sesión</b>.</li>
    <li>Escribí el <b>mismo mail que usaste al comprar</b>.</li>
    <li>Te llega un <b>código de 6 dígitos</b> a ese mail: pegalo y listo.</li>
  </ol>
  <a class="gate-btn" href="{{ routes.account_login_url }}">Iniciar sesión</a>
  <a class="gate-link" href="PRODUCT_URL">¿Todavía no lo tenés? Conocelo acá</a>
{%- endif -%}
</div></div>
"""


def page_from_web(web_file, tag, title):
    html = open(os.path.join(root, "ebook", web_file), encoding="utf-8").read()
    html = re.sub(r"<title>.*?</title>\s*", "", html, count=1)
    html = re.sub(r'<meta name="claude:viewport-fit-sides"[^>]*>\s*', "", html, count=1)
    # el link "Índice" vuelve al índice; sumamos "Mis ebooks"
    html = html.replace('<a class="to-top" href="#indice" aria-label="Volver al índice">Índice</a>',
                        '<a class="to-top" href="#indice" aria-label="Volver al índice">Índice</a>'
                        '<a class="to-top to-library" href="/pages/mis-ebooks">Mis ebooks</a>')
    extra_css = "<style>.to-library{right:auto!important;left:max(16px,calc(env(safe-area-inset-left,0px) + 16px))}</style>"
    body = ("{%- if customer and customer.tags contains '" + tag + "' -%}\n{% raw %}\n" + html + extra_css +
            "\n{% endraw %}\n{%- else -%}\n" + GATE.replace("PRODUCT_URL", PRODUCT_URL) + "{%- endif -%}")
    return HEAD.replace("TITLE", title) + body + FOOT


LIBRARY = """<style>
:root{--navy:#14213D;--orange:#E8632E;--gold:#F5D27A;--muted:#5A6478;--line:#E1E5EE}
body{background:#F6F7FB;color:#1C2333;font-family:'Source Sans 3','Segoe UI',system-ui,sans-serif}
.lib-top{background:radial-gradient(circle at 85% 0%,#3A3F9E 0%,#14213D 55%,#0B1226 100%);color:#fff}
.lib-wrap{max-width:960px;margin:0 auto;padding-left:max(20px,env(safe-area-inset-left,0px));padding-right:max(20px,env(safe-area-inset-right,0px))}
.lib-top .lib-wrap{padding-block:48px 56px}
.lib-top small{color:var(--gold);font-weight:700;letter-spacing:.14em;text-transform:uppercase;font-size:13px}
.lib-top h1{font-family:'Bricolage Grotesque','Segoe UI',sans-serif;font-size:clamp(32px,6vw,46px);line-height:1.05;margin:10px 0 8px}
.lib-top p{color:rgba(255,255,255,.8);margin:0}
.lib-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:24px;padding-block:40px 64px}
.lib-card{background:#fff;border:1px solid var(--line);border-radius:20px;padding:22px;display:grid;grid-template-columns:120px minmax(0,1fr);gap:20px;align-items:center;text-decoration:none;color:inherit;transition:box-shadow .2s,transform .2s}
.lib-card:hover{box-shadow:0 18px 40px rgba(20,33,61,.14);transform:translateY(-2px)}
.lib-card img{width:100%;aspect-ratio:210/297;object-fit:cover;border-radius:4px 8px 8px 4px;box-shadow:8px 12px 20px rgba(0,0,0,.25)}
.lib-card h2{font-family:'Bricolage Grotesque','Segoe UI',sans-serif;font-size:21px;line-height:1.15;margin:0 0 6px;color:var(--navy)}
.lib-card p{margin:0 0 14px;color:var(--muted);font-size:15px}
.lib-card span{display:inline-block;background:var(--orange);color:#fff;font-weight:700;padding:9px 16px;border-radius:999px;font-size:15px}
.lib-card.locked{opacity:.75}
.lib-card.locked span{background:var(--navy)}
.lib-foot{text-align:center;padding-bottom:48px;color:var(--muted);font-size:15px}
.lib-foot a{color:var(--navy);font-weight:600}
@media(max-width:700px){.lib-grid{grid-template-columns:minmax(0,1fr)}.lib-card{grid-template-columns:96px minmax(0,1fr)}}
</style>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,800&family=Source+Sans+3:wght@400;600;700&display=swap">
{%- if customer -%}
<header class="lib-top"><div class="lib-wrap">
  <small>Método 30 · Tu biblioteca</small>
  <h1>Hola{% if customer.first_name != blank %}, {{ customer.first_name }}{% endif %}. Estos son tus ebooks</h1>
  <p>Leelos en la versión interactiva: tildá tus tareas y copiá las plantillas con un toque. Los PDF te llegaron por mail.</p>
</div></header>
<main class="lib-wrap lib-grid">
  {%- assign has1 = false -%}{%- if customer.tags contains 'ebook1' -%}{%- assign has1 = true -%}{%- endif -%}
  {%- assign has2 = false -%}{%- if customer.tags contains 'ebook2' -%}{%- assign has2 = true -%}{%- endif -%}
  <a class="lib-card{% unless has1 %} locked{% endunless %}" href="{% if has1 %}/pages/ebook-1{% else %}PRODUCT_URL{% endif %}">
    <img src="{{ 'tapa-consegui-trabajo.png' | file_url }}" alt="Tapa de Conseguí trabajo en 30 días" width="420" height="594">
    <div><h2>Conseguí trabajo en 30 días</h2><p>El plan día por día: CV, LinkedIn, entrevistas y negociación.</p><span>{% if has1 %}Leer ahora{% else %}Conseguirlo{% endif %}</span></div>
  </a>
  <a class="lib-card{% unless has2 %} locked{% endunless %}" href="{% if has2 %}/pages/ebook-2{% else %}PRODUCT_URL{% endif %}">
    <img src="{{ 'tapa-secretos-de-reclutador.png' | file_url }}" alt="Tapa de Secretos de reclutador" width="420" height="594">
    <div><h2>Secretos de reclutador</h2><p>El manual avanzado: lo que pasa del otro lado de la mesa.</p><span>{% if has2 %}Leer ahora{% else %}Sumarlo{% endif %}</span></div>
  </a>
</main>
<p class="lib-foot">¿Problemas para entrar? Escribinos a somosmetodo30@gmail.com · <a href="{{ routes.account_logout_url }}">Cerrar sesión</a></p>
{%- else -%}
""" + GATE.replace("Entrá para leer tu ebook", "Entrá a tu biblioteca").replace("PRODUCT_URL", "PRODUCT_URL") + """
{%- endif -%}
"""

files = {
    "page.ebook-1.liquid": page_from_web("web.html", "ebook1", "Conseguí trabajo en 30 días"),
    "page.ebook-2.liquid": page_from_web("web2.html", "ebook2", "Secretos de reclutador"),
    "page.mis-ebooks.liquid": HEAD.replace("TITLE", "Mis ebooks") + LIBRARY.replace("PRODUCT_URL", PRODUCT_URL) + FOOT,
}
for name, content in files.items():
    open(os.path.join(out, name), "w", encoding="utf-8").write(content)
    print(name, len(content.encode()) // 1024, "KB")
