"""Builds the web (artifact) version of the ebook from the same markdown as the PDF.

Usage: python3 build_web.py ebook.md web.html
"""
import sys, os, html, re

SRC, OUT = sys.argv[1], sys.argv[2]
ED = sys.argv[3] if len(sys.argv) > 3 else "main"
here = os.path.dirname(os.path.abspath(__file__))

# Reuse the PDF builder's parsing, illustrations and chapter metadata.
code = open(os.path.join(here, "build.py"), encoding="utf-8").read()
code = code[: code.index('_cp = foto(E["photo"])')]
ns = {"__file__": os.path.join(here, "build.py")}
sys.argv = ["build.py", SRC, os.devnull, ED]
exec(compile(code, "build.py", "exec"), ns)
chapters, metas, body_html, ILLU, E = ns["chapters"], ns["metas"], ns["body_html"], ns["ILLU"], ns["E"]
PRO = ED == "pro"


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
js = open(os.path.join(here, "web.js"), encoding="utf-8").read().replace("ct30-checks", "ct30-checks-" + ED)

page = f'''<title>{E["doc_title"]}</title>
<meta name="claude:viewport-fit-sides" content="cover">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,500;12..96,700;12..96,800&family=Source+Sans+3:ital,wght@0,400;0,600;0,700;1,400&display=swap">
<style>{css}</style>
<div class="progress" aria-hidden="true"><span id="progress-bar"></span></div>

<header class="cover{' pro' if PRO else ''}">
  <div class="wrap cover-grid">
    <div class="cover-text">
      <div class="cover-badge">{E["badge"]}</div>
      <h1 class="cover-title">{E["title"].replace("<br>", " ").replace("<span>", "<span>")}</h1>
      <p class="cover-sub">{E["sub"]}.</p>
      <ul class="cover-pills">{"".join("<li>" + x + "</li>" for x in E["pills"])}</ul>
      <a class="cover-cta" href="#indice">Ver el contenido</a>
    </div>
    <div class="cover-art" aria-hidden="true">
      {'<div class="seal"><b>★</b>Nivel<br>experto</div>' if PRO else '<div class="cal"><div class="cal-top"></div><div class="cal-n">30</div><div class="cal-l">días</div></div>'}
      {E["illu"]}
    </div>
  </div>
</header>

<section class="welcome wrap{' pro' if PRO else ''}" id="indice">
  <p class="eyebrow">Antes de empezar</p>
  <h2 class="welcome-title">{E["wl_title"]}</h2>
  <p class="welcome-lead">{E["wl_lead"]} Tocá las casillas para ir marcando tu avance: quedan guardadas en este dispositivo.</p>
  <dl class="stats">{"".join(f"<div><dt>{n}</dt><dd>{t}</dd></div>" for n, t in E["stats"])}</dl>
  <h3 class="toc-title">Contenido</h3>
  <ol class="toc">{"".join(toc)}</ol>
</section>

{"".join(sections)}

<section class="closing{' pro' if PRO else ''}">
  <div class="wrap">
    <p class="eyebrow">Último paso</p>
    <h2 class="closing-title">{E["cl_title"]}</h2>
    <p class="closing-lead">{E["cl_lead"]}</p>
    <ol class="closing-steps">{"".join(f"<li><b>{i + 1}</b>{t}</li>" for i, t in enumerate(E["steps"]))}</ol>
    <p class="closing-small">El resultado depende de tu dedicación, tu perfil y el mercado de cada rubro. Este manual te da el método; la constancia la ponés vos.</p>
  </div>
</section>

<a class="to-top" href="#indice" aria-label="Volver al índice">Índice</a>
<script>{js}</script>
'''
open(OUT, "w", encoding="utf-8").write(page)
print("ok", len(page))
