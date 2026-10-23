"""Builds the web (artifact) version of the ebook from the same markdown as the PDF.

Usage: python3 build_web.py ebook.md web.html
"""
import sys, os, html, re

SRC, OUT = sys.argv[1], sys.argv[2]
here = os.path.dirname(os.path.abspath(__file__))

# Reuse the PDF builder's parsing, illustrations and chapter metadata.
code = open(os.path.join(here, "build.py"), encoding="utf-8").read()
code = code[: code.index('_cp = foto("portada")')]
ns = {"__file__": os.path.join(here, "build.py")}
sys.argv = ["build.py", SRC, os.devnull]
exec(compile(code, "build.py", "exec"), ns)
chapters, metas, body_html, ILLU = ns["chapters"], ns["metas"], ns["body_html"], ns["ILLU"]


def anchor(m):
    return {"00": "intro", "+": "herramientas"}.get(m["num"], ("bonus" + m["num"][1:]) if m["num"].startswith("B") else "cap" + m["num"])


sections, toc = [], []
for m, (title, body) in zip(metas, chapters):
    body = re.sub(r"^.*· @\S+\s*$", "", body, flags=re.M)
    a, b = m["theme"]
    aid = anchor(m)
    cls = "opener bonus" if m["bonus"] else "opener"
    toc.append(
        f'<li class="{"is-bonus" if m["bonus"] else ""}"><a href="#{aid}"><span class="toc-n">{m["num"]}</span>'
        f'<span class="toc-k">{html.escape(m["kicker"])}</span><span class="toc-t">{html.escape(m["main"])}</span></a></li>'
    )
    sections.append(f'''
<section class="chapter" id="{aid}">
  <header class="{cls}" style="--op-a:{a};--op-b:{b}">
    <div class="wrap op-grid">
      <div class="op-text">
        <div class="op-num">{m["num"]}</div>
        <div class="op-kicker">{html.escape(m["kicker"])}</div>
        <h2 class="op-title">{html.escape(m["main"])}</h2>
      </div>
      <div class="op-illu" aria-hidden="true">{ILLU[m["illu"]]}</div>
    </div>
  </header>
  <div class="wrap prose">{body_html(body)}</div>
</section>''')

css = open(os.path.join(here, "web.css"), encoding="utf-8").read()
js = open(os.path.join(here, "web.js"), encoding="utf-8").read()

page = f'''<title>Conseguí trabajo en 30 días</title>
<meta name="claude:viewport-fit-sides" content="cover">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,500;12..96,700;12..96,800&family=Source+Sans+3:ital,wght@0,400;0,600;0,700;1,400&display=swap">
<style>{css}</style>
<div class="progress" aria-hidden="true"><span id="progress-bar"></span></div>

<header class="cover">
  <div class="wrap cover-grid">
    <div class="cover-text">
      <div class="cover-badge">Guía práctica · Plan de 30 días</div>
      <h1 class="cover-title">Conseguí trabajo <span>en 30 días</span></h1>
      <p class="cover-sub">CV, LinkedIn y entrevistas: el sistema paso a paso para ser el mejor postulante en cualquier rubro.</p>
      <ul class="cover-pills"><li>CV que pasa filtros</li><li>LinkedIn magnético</li><li>Entrevistas ganadoras</li><li>Negociación</li><li>Secretos de reclutador</li></ul>
      <a class="cover-cta" href="#indice">Ver el contenido</a>
    </div>
    <div class="cover-art" aria-hidden="true">
      <div class="cal"><div class="cal-top"></div><div class="cal-n">30</div><div class="cal-l">días</div></div>
      {ILLU[0]}
    </div>
  </div>
</header>

<section class="welcome wrap" id="indice">
  <p class="eyebrow">Antes de empezar</p>
  <h2 class="welcome-title">Tu próximo trabajo empieza hoy</h2>
  <p class="welcome-lead">Este no es un libro para leer y guardar. Es un plan de acción: cada día tiene tareas concretas, plantillas listas para copiar y checklists para tildar. Tocá las casillas para ir marcando tu avance: quedan guardadas en este dispositivo.</p>
  <dl class="stats">
    <div><dt>7</dt><dd>etapas con tareas día por día</dd></div>
    <div><dt>15</dt><dd>preguntas de entrevista con respuesta</dd></div>
    <div><dt>8</dt><dd>plantillas de mensajes listas para copiar</dd></div>
    <div><dt>4</dt><dd>capítulos bonus con secretos de reclutador</dd></div>
  </dl>
  <h3 class="toc-title">Contenido</h3>
  <ol class="toc">{"".join(toc)}</ol>
</section>

{"".join(sections)}

<section class="closing">
  <div class="wrap">
    <p class="eyebrow">Último paso</p>
    <h2 class="closing-title">Ahora te toca a vos</h2>
    <p class="closing-lead">Ya tenés el mapa completo. La diferencia entre quien consigue trabajo y quien sigue buscando no es el talento: es la ejecución constante.</p>
    <ol class="closing-steps">
      <li><b>1</b>Abrí el checklist del día 1</li>
      <li><b>2</b>Bloqueá tu horario fijo de búsqueda</li>
      <li><b>3</b>Cargá tu primera empresa en el tracker</li>
    </ol>
    <p class="closing-small">El resultado depende de tu dedicación, tu perfil y el mercado de cada rubro. Este plan te da el método; la constancia la ponés vos.</p>
  </div>
</section>

<a class="to-top" href="#indice" aria-label="Volver al índice">Índice</a>
<script>{js}</script>
'''
open(OUT, "w", encoding="utf-8").write(page)
print("ok", len(page))
