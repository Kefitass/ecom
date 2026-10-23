import re, sys, markdown, html, os, base64
FOTOS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fotos")
def foto(name):
    for ext in ("jpg","jpeg","png","webp"):
        f = os.path.join(FOTOS, f"{name}.{ext}")
        if os.path.exists(f):
            mime = "jpeg" if ext in ("jpg","jpeg") else ext
            return f"data:image/{mime};base64," + base64.b64encode(open(f,"rb").read()).decode()
    return None

SRC = sys.argv[1]
OUT = sys.argv[2]
ED = sys.argv[3] if len(sys.argv) > 3 else "main"  # "main" = Conseguí trabajo en 30 días, "pro" = Secretos de reclutador
md = open(SRC, encoding="utf-8").read()

# --- split into chapters -------------------------------------------------
parts = re.split(r"^## ", md, flags=re.M)
chapters = []
for p in parts[1:]:
    title, _, body = p.partition("\n")
    chapters.append((title.strip(), body.strip()))
# drop the author-only annex from the reader's ebook
chapters = [c for c in chapters if not c[0].startswith("Anexo para el autor")]

INK = "#14213D"
ACC = "#FF7A45"
ACC2 = "#FFC857"
SKY = "#5B8DEF"
MINT = "#3DDC97"

def svg(inner, w=520, h=420):
    return f'<svg viewBox="0 0 {w} {h}" xmlns="http://www.w3.org/2000/svg" class="illu">{inner}</svg>'

def blob(cx, cy, r, c, o=0.18):
    return f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{c}" opacity="{o}"/>'

ILLU = {}
# 0 intro: rising staircase to a flag
ILLU[0] = svg(
    blob(260, 210, 190, "#fff", .06) +
    "".join(f'<rect x="{80+i*60}" y="{330-i*40}" width="60" height="{20+i*40}" rx="6" fill="#fff" opacity="{.15+i*.1}"/>' for i in range(6)) +
    f'<line x1="410" y1="110" x2="410" y2="40" stroke="#fff" stroke-width="5" stroke-linecap="round"/>'
    f'<path d="M410 42 L470 58 L410 76 Z" fill="{ACC}"/>'
    f'<circle cx="372" cy="118" r="14" fill="{ACC2}"/><rect x="362" y="134" width="20" height="36" rx="8" fill="{ACC2}"/>'
    f'<rect x="384" y="146" width="22" height="16" rx="3" fill="#fff"/>'
)
# 1 target
ILLU[1] = svg(
    blob(260, 210, 190, "#fff", .06) +
    "".join(f'<circle cx="250" cy="220" r="{r}" fill="{c}"/>' for r, c in [(150, "rgba(255,255,255,.14)"), (112, "rgba(255,255,255,.22)"), (74, "rgba(255,255,255,.32)"), (36, ACC)]) +
    f'<line x1="430" y1="60" x2="262" y2="210" stroke="#fff" stroke-width="7" stroke-linecap="round"/>'
    f'<path d="M430 60 l30 -14 l-6 30 z" fill="{ACC2}"/><path d="M262 210 l22 -4 l-8 14 z" fill="#fff"/>'
)
# 2 CV document
ILLU[2] = svg(
    blob(260, 210, 190, "#fff", .06) +
    '<rect x="140" y="50" width="240" height="320" rx="18" fill="#fff"/>'
    f'<circle cx="190" cy="105" r="26" fill="{ACC2}"/>'
    f'<rect x="230" y="88" width="120" height="12" rx="6" fill="{INK}"/><rect x="230" y="110" width="80" height="10" rx="5" fill="#C9D3E6"/>'
    + "".join(f'<rect x="200" y="{160+i*40}" width="{150-(i%2)*40}" height="10" rx="5" fill="#C9D3E6"/>'
              f'<circle cx="176" cy="{165+i*40}" r="11" fill="{MINT}"/><path d="M170 {165+i*40} l5 5 l9 -10" stroke="#fff" stroke-width="3" fill="none" stroke-linecap="round"/>' for i in range(5))
    + f'<g transform="rotate(-12 400 330)"><rect x="350" y="300" width="110" height="44" rx="22" fill="{ACC}"/><text x="405" y="329" text-anchor="middle" font-size="20" font-weight="800" fill="#fff" font-family="Inter">ATS OK</text></g>'
)
# 3 profile card
ILLU[3] = svg(
    blob(260, 210, 190, "#fff", .06) +
    '<rect x="100" y="70" width="320" height="280" rx="22" fill="#fff"/>'
    f'<rect x="100" y="70" width="320" height="80" rx="22" fill="{SKY}"/><rect x="100" y="120" width="320" height="30" fill="{SKY}"/>'
    f'<circle cx="170" cy="150" r="42" fill="{ACC2}" stroke="#fff" stroke-width="6"/>'
    f'<circle cx="170" cy="140" r="14" fill="{INK}"/><path d="M146 176 q24 -26 48 0" fill="{INK}"/>'
    f'<rect x="130" y="210" width="190" height="14" rx="7" fill="{INK}"/><rect x="130" y="236" width="240" height="10" rx="5" fill="#C9D3E6"/>'
    f'<rect x="130" y="256" width="200" height="10" rx="5" fill="#C9D3E6"/>'
    f'<rect x="130" y="290" width="120" height="34" rx="17" fill="{MINT}"/><text x="190" y="312" text-anchor="middle" font-size="14" font-weight="700" fill="#fff" font-family="Inter">Open to work</text>'
    + "".join(f'<path d="M{380+i*28} 60 l6 14 l15 1 l-12 9 l4 15 l-13 -8 l-13 8 l4 -15 l-12 -9 l15 -1 z" fill="{ACC2}"/>' for i in range(3))
)
# 4 network
nodes = [(260, 210, 34, ACC), (120, 110, 22, "#fff"), (400, 100, 24, "#fff"), (100, 300, 20, "#fff"), (420, 300, 26, "#fff"), (260, 60, 16, ACC2), (260, 360, 18, ACC2), (180, 210, 12, MINT), (340, 210, 12, MINT)]
ILLU[4] = svg(
    blob(260, 210, 190, "#fff", .06) +
    "".join(f'<line x1="260" y1="210" x2="{x}" y2="{y}" stroke="rgba(255,255,255,.45)" stroke-width="3"/>' for x, y, r, c in nodes[1:]) +
    '<line x1="120" y1="110" x2="260" y2="60" stroke="rgba(255,255,255,.25)" stroke-width="2"/><line x1="400" y1="100" x2="420" y2="300" stroke="rgba(255,255,255,.25)" stroke-width="2"/><line x1="100" y1="300" x2="260" y2="360" stroke="rgba(255,255,255,.25)" stroke-width="2"/>'
    + "".join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{c}"/>' for x, y, r, c in nodes)
)
# 5 interview: video call + speech bubbles
ILLU[5] = svg(
    blob(260, 210, 190, "#fff", .06) +
    '<rect x="80" y="90" width="300" height="200" rx="18" fill="#fff"/>'
    f'<rect x="96" y="106" width="268" height="150" rx="10" fill="{SKY}" opacity=".35"/>'
    f'<circle cx="230" cy="160" r="28" fill="{ACC2}"/><path d="M180 256 q50 -70 100 0" fill="{ACC2}"/>'
    f'<rect x="200" y="300" width="60" height="18" fill="#fff"/><rect x="160" y="316" width="140" height="10" rx="5" fill="#fff"/>'
    f'<rect x="330" y="40" width="150" height="70" rx="20" fill="{ACC}"/><path d="M360 108 l-6 24 l26 -24 z" fill="{ACC}"/>'
    f'<circle cx="372" cy="75" r="7" fill="#fff"/><circle cx="405" cy="75" r="7" fill="#fff"/><circle cx="438" cy="75" r="7" fill="#fff"/>'
    f'<rect x="380" y="230" width="120" height="56" rx="18" fill="{MINT}"/><path d="M480 284 l8 20 l-24 -20 z" fill="{MINT}"/>'
    f'<path d="M418 258 l10 10 l20 -20" stroke="#fff" stroke-width="6" fill="none" stroke-linecap="round"/>'
)
# 6 negotiation: coins + rising chart
ILLU[6] = svg(
    blob(260, 210, 190, "#fff", .06) +
    "".join(f'<rect x="{110+i*80}" y="{330-h}" width="54" height="{h}" rx="8" fill="#fff" opacity="{.25+i*.18}"/>' for i, h in enumerate([80, 130, 180, 240])) +
    f'<path d="M110 240 L190 200 L270 150 L350 80" stroke="{ACC}" stroke-width="7" fill="none" stroke-linecap="round"/>'
    f'<path d="M350 80 l-26 2 l14 20 z" fill="{ACC}"/>'
    + "".join(f'<ellipse cx="430" cy="{330-i*18}" rx="44" ry="14" fill="{ACC2}" stroke="#E0A800" stroke-width="2"/>' for i in range(6))
    + f'<text x="430" y="245" text-anchor="middle" font-size="28" font-weight="800" fill="{INK}" font-family="Inter">$</text>'
)
# 7 summit flag
ILLU[7] = svg(
    blob(260, 210, 190, "#fff", .06) +
    '<path d="M40 370 L200 140 L270 230 L330 160 L480 370 Z" fill="rgba(255,255,255,.22)"/>'
    '<path d="M200 140 L230 183 L215 178 L200 195 L185 180 L172 182 Z" fill="#fff"/>'
    f'<line x1="200" y1="140" x2="200" y2="50" stroke="#fff" stroke-width="5" stroke-linecap="round"/>'
    f'<path d="M200 52 L270 70 L200 92 Z" fill="{ACC}"/>'
    f'<circle cx="400" cy="90" r="34" fill="{ACC2}"/>'
)
# 8 toolbox
ILLU[8] = svg(
    blob(260, 210, 190, "#fff", .06) +
    f'<rect x="200" y="100" width="120" height="50" rx="14" fill="none" stroke="#fff" stroke-width="12"/>'
    f'<rect x="110" y="140" width="300" height="190" rx="22" fill="{ACC}"/>'
    f'<rect x="110" y="200" width="300" height="18" fill="#E5602E"/><rect x="235" y="190" width="50" height="38" rx="8" fill="{ACC2}"/>'
    f'<rect x="150" y="60" width="16" height="110" rx="8" fill="#fff" transform="rotate(-20 158 115)"/>'
    f'<rect x="350" y="70" width="18" height="100" rx="6" fill="{MINT}" transform="rotate(18 359 120)"/>'
)

def inline_md(s):
    return markdown.markdown(s, extensions=["tables"])

def body_html(text):
    # embed placeholder → roadmap
    text = re.sub(r"^&#91;embedded content:.*$", "%%ROADMAP%%", text, flags=re.M)
    # checklists: wrap consecutive "- [ ]" lines
    def cl(m):
        items = re.findall(r"^- \[ \] (.*)$", m.group(0), flags=re.M)
        lis = "".join(f'<li><span class="box"></span>{markdown.markdown(i)[3:-4]}</li>' for i in items)
        return f'\n\n<div class="checklist"><div class="cl-head">Checklist</div><ul>{lis}</ul></div>\n\n'
    text = re.sub(r"(?:^- \[ \] .*\n?)+", cl, text, flags=re.M)
    h = markdown.markdown(text, extensions=["tables", "md_in_html"])
    # formula / key paragraphs → callouts
    h = re.sub(r"<p><strong>(F[óo]rmula[^<]*|Meta:|Claves:|Regla de[^<]*|Extensi[óo]n:|Plan para[^<]*)</strong>(.*?)</p>",
               r'<div class="callout"><strong>\1</strong>\2</div>', h, flags=re.S)
    h = re.sub(r"<p><strong>(Secreto de reclutador:)</strong>(.*?)</p>",
               r'<div class="secret"><div class="secret-tag">Secreto de reclutador</div>\2</div>', h, flags=re.S)
    h = h.replace("<blockquote>", '<blockquote><div class="bq-tag">Plantilla para copiar</div>')
    h = h.replace("<p>%%ROADMAP%%</p>", ROADMAP)
    h = h.replace("<table>", '<div class="tbl"><table>').replace("</table>", "</table></div>")
    return h

steps = [("1–3", "Objetivo"), ("4–8", "CV"), ("9–12", "LinkedIn"), ("13–17", "Búsqueda"), ("18–24", "Entrevistas"), ("25–28", "Negociación"), ("29–30", "Cierre")]
ROADMAP = '<div class="roadmap">' + "".join(
    f'<div class="rm-step"><div class="rm-dot">{i+1}</div><div class="rm-days">Días {d}</div><div class="rm-name">{n}</div></div>'
    for i, (d, n) in enumerate(steps)) + '</div><div class="rm-bar">Desde el día 8: postulaciones, mensajes y seguimientos todos los días, hasta firmar</div>'

THEMES = [
    ("#14213D", "#2B4C8C"), ("#1B2A4A", "#3A3F9E"), ("#0F3D3E", "#1F7A6D"), ("#1E3A8A", "#2563EB"),
    ("#3B1F5C", "#6D3FB0"), ("#7A2E1F", "#D9572B"), ("#0B4F3C", "#14A06F"), ("#2A1E5C", "#C2410C"), ("#14213D", "#FF7A45"),
]
BONUS_THEME = ("#111111", "#8A6A1F")

# bonus illustrations
ILLU["b1"] = svg(
    blob(260, 210, 190, "#fff", .06) +
    "".join(f'<rect x="{90+i*120}" y="120" width="100" height="140" rx="14" fill="#fff" opacity="{.9 if i==1 else .35}"/>'
            f'<circle cx="{140+i*120}" cy="165" r="22" fill="{ACC2 if i==1 else "#C9D3E6"}"/>'
            f'<rect x="{110+i*120}" y="205" width="60" height="9" rx="4" fill="#C9D3E6"/><rect x="{110+i*120}" y="224" width="44" height="9" rx="4" fill="#C9D3E6"/>' for i in range(3)) +
    f'<circle cx="300" cy="190" r="70" fill="none" stroke="{ACC}" stroke-width="12"/><line x1="350" y1="240" x2="420" y2="310" stroke="{ACC}" stroke-width="18" stroke-linecap="round"/>'
)
ILLU["b2"] = svg(
    blob(260, 210, 190, "#fff", .06) +
    f'<g transform="rotate(35 260 210)"><path d="M260 50 C310 100 320 200 300 290 L220 290 C200 200 210 100 260 50 Z" fill="#fff"/>'
    f'<circle cx="260" cy="160" r="26" fill="{SKY}"/><path d="M220 250 L170 310 L220 295 Z" fill="{ACC}"/><path d="M300 250 L350 310 L300 295 Z" fill="{ACC}"/>'
    f'<path d="M230 295 Q260 380 290 295 Z" fill="{ACC2}"/></g>'
    + "".join(f'<circle cx="{x}" cy="{y}" r="4" fill="#fff" opacity=".7"/>' for x, y in [(80,80),(450,60),(470,200),(60,240),(120,370)])
)
ILLU["b3"] = svg(
    blob(260, 210, 190, "#fff", .06) +
    '<rect x="140" y="60" width="240" height="310" rx="18" fill="#fff"/>'
    f'<rect x="210" y="44" width="100" height="36" rx="10" fill="{ACC2}"/>'
    + "".join(f'<rect x="170" y="{120+i*55}" width="90" height="10" rx="5" fill="#C9D3E6"/>' + "".join(f'<circle cx="{280+j*22}" cy="{125+i*55}" r="8" fill="{ACC if j<=(3-i%3) else "#E5E7EB"}"/>' for j in range(4)) for i in range(4))
)
ILLU["b4"] = svg(
    blob(260, 210, 190, "#fff", .06) +
    f'<path d="M260 50 L390 100 L390 210 C390 290 330 340 260 370 C190 340 130 290 130 210 L130 100 Z" fill="#fff" opacity=".9"/>'
    f'<path d="M260 80 L365 120 L365 210 C365 275 318 318 260 343 Z" fill="{MINT}" opacity=".35"/>'
    f'<path d="M205 210 l38 38 l75 -80" stroke="{INK}" stroke-width="18" fill="none" stroke-linecap="round" stroke-linejoin="round"/>'
)

def meta_for(chapters):
    out, n = [], 0
    for title, _ in chapters:
        if title.startswith("Introducci"):
            out.append(dict(num="00", kicker="Introducción", main=title.split(":", 1)[1], illu=0, photo="pro0" if ED == "pro" else "cap0", theme=BONUS_THEME if ED == "pro" else THEMES[0], bonus=ED == "pro"))
        elif title.startswith("Bonus"):
            k = re.match(r"Bonus (\d+)", title).group(1)
            out.append(dict(num=f"B{k}", kicker=f"Bonus {k} · Nivel experto", main=title.split(":", 1)[1], illu=f"b{k}", photo=f"bonus{k}", theme=BONUS_THEME, bonus=True))
        elif title.startswith("Capítulo"):
            k = int(re.match(r"Capítulo (\d+)", title).group(1))
            illu = {1: "b1", 2: 2, 3: 3, 4: "b2", 5: "b3", 6: 6, 7: "b4"}.get(k, 0)
            out.append(dict(num=f"{k:02d}", kicker=f"Capítulo {k}", main=title.split(":", 1)[1], illu=illu, photo=f"pro{k}", theme=BONUS_THEME, bonus=True))
        elif title.startswith("Caja"):
            main = title.split(":", 1)[1] if ED == "pro" else "Plantillas, checklist y tracker"
            out.append(dict(num="+", kicker="Caja de herramientas", main=main, illu=8, photo="pro8" if ED == "pro" else "cap8", theme=BONUS_THEME if ED == "pro" else THEMES[8], bonus=ED == "pro"))
        else:
            n += 1
            kick, main = title.split(":", 1)
            out.append(dict(num=f"{n:02d}", kicker=kick, main=main, illu=n, photo=f"cap{n}", theme=THEMES[n], bonus=False))
    for m in out:
        m["main"] = m["main"].strip()
        m["main"] = m["main"][0].upper() + m["main"][1:]
    return out

def chapter_open(m):
    a, b = m["theme"]
    ph = foto(m["photo"])
    photo_or_illu = f'<div class="op-photo" style="--bg:{a};background-image:url({ph})"></div>' if ph else f'<div class="op-illu">{ILLU[m["illu"]]}</div>'
    cls = "opener bonus" if m["bonus"] else "opener"
    return f'''
<section class="{cls}" style="--bg:{a};background: radial-gradient(circle at 85% 15%, {b} 0%, {a} 60%);">
  <div class="op-num">{m["num"]}</div>
  <div class="op-kicker">{html.escape(m["kicker"])}</div>
  <h2 class="op-title">{html.escape(m["main"])}</h2>
  {photo_or_illu}
  <div class="op-foot">Método 30 · {"Secretos de reclutador" if ED == "pro" else "Conseguí trabajo en 30 días"}</div>
</section>'''

metas = meta_for(chapters)
chap_html = []
for m, (title, body) in zip(metas, chapters):
    body = re.sub(r"^.*· @\S+\s*$", "", body, flags=re.M)
    chap_html.append(chapter_open(m) + f'<section class="content">{body_html(body)}</section>')

toc = "".join(
    f'<li class="{"toc-bonus" if m["bonus"] else ""}"><span class="toc-n">{m["num"]}</span><span class="toc-t">{html.escape(m["kicker"] + ": " + m["main"] if not m["num"] in ("00", "+") else m["main"])}</span></li>'
    for m in metas)

if ED == "pro":
    E = dict(
        doc_title="Secretos de reclutador", photo="pro_portada", cover_cls="cover pro",
        badge="Método 30 · Manual avanzado",
        title="Secretos<br>de<br><span>reclutador</span>",
        sub="Lo que pasa del otro lado de la mesa: el manual avanzado para ganarle a cualquier competencia",
        seal='<div class="cv-seal"><div class="cv-seal-star">★</div><div class="cv-seal-l">NIVEL<br>EXPERTO</div></div>',
        illu=ILLU["b1"],
        pills=["Cómo te puntúan", "LinkedIn por dentro", "Bandas salariales", "Tests y evaluaciones", "Estafas laborales"],
        wl_title="La ventaja que no ve el resto",
        wl_lead="Este manual te muestra el proceso de selección desde adentro: qué mide cada persona que decide, cómo te buscan y te puntúan, y qué hacen distinto los candidatos que siempre llegan a la final. Usalo junto al plan de 30 días: cada capítulo potencia una etapa.",
        stats=[("7", "capítulos de nivel experto"), ("10", "estrategias avanzadas para destacar"), ("6", "tipos de test explicados"), ("23", "puntos en el checklist del candidato experto")],
        cl_title="Ahora jugás con ventaja",
        cl_lead="Ya sabés lo que pasa del otro lado de la mesa. Usá cada capítulo en su etapa del plan y vas a dejar de competir como un candidato más.",
        steps=["Leé el capítulo de la etapa en la que estás", "Prepará una prueba de trabajo para tu empresa favorita", "Repasá el checklist experto antes de cada entrevista"],
    )
else:
    E = dict(
        doc_title="Conseguí trabajo en 30 días", photo="portada", cover_cls="cover",
        badge="Método 30 · Guía práctica",
        title="Conseguí<br>trabajo<br><span>en 30 días</span>",
        sub="CV, LinkedIn y entrevistas: el sistema paso a paso para ser el mejor postulante en cualquier rubro",
        seal='<div class="cv-cal"><div class="cv-cal-top"></div><div class="cv-cal-n">30</div><div class="cv-cal-l">DÍAS</div></div>',
        illu=ILLU[0],
        pills=["CV que pasa filtros", "LinkedIn magnético", "Entrevistas ganadoras", "Negociación"],
        wl_title="Tu próximo trabajo empieza hoy",
        wl_lead="Este no es un libro para leer y guardar. Es un plan de acción: cada día tiene tareas concretas, plantillas listas para copiar y checklists para tildar. Si lo seguís, en 30 días vas a tener un CV que consigue entrevistas, un perfil que atrae reclutadores y las respuestas que hacen que te elijan.",
        stats=[("7", "etapas con tareas día por día"), ("15", "preguntas de entrevista con respuesta"), ("8", "plantillas de mensajes listas para usar"), ("10", "rubros con consejos específicos")],
        cl_title="Ahora te toca a vos",
        cl_lead="Ya tenés el mapa completo. La diferencia entre quien consigue trabajo y quien sigue buscando no es el talento: es la ejecución constante. Abrí el checklist del día 1 y empezá hoy.",
        steps=["Abrí el checklist del día 1", "Bloqueá tu horario fijo de búsqueda", "Cargá tu primera empresa en el tracker"],
    )

_cp = foto(E["photo"])
COVER_BG = f'<div class="cv-photo" style="background-image:url({_cp})"></div>' if _cp else ""
COVER_ILLU = "" if _cp else f'<div class="cv-illu">{E["illu"]}</div>'
COVER = f"""
<section class="{E['cover_cls']}{' has-photo' if _cp else ''}">{COVER_BG}
  <div class="cv-glow"></div>
  <div class="cv-badge">{E['badge']}</div>
  <h1 class="cv-title">{E['title']}</h1>
  <p class="cv-sub">{E['sub']}</p>
  {E['seal']}
  {COVER_ILLU}
  <div class="cv-pills">{''.join(f'<span>{x}</span>' for x in E['pills'])}</div>
</section>"""

WELCOME = f"""
<section class="welcome{' pro' if ED == 'pro' else ''}">
  <div class="wl-kicker">Antes de empezar</div>
  <h2 class="wl-title">{E['wl_title']}</h2>
  <p class="wl-lead">{E['wl_lead']}</p>
  <div class="wl-grid">{''.join(f'<div class="wl-card"><div class="wl-n">{n}</div><div>{t}</div></div>' for n, t in E['stats'])}</div>
  <h3 class="toc-h">Contenido</h3>
  <ol class="toc">{toc}</ol>
</section>"""

CLOSING = f"""
<section class="closing{' pro' if ED == 'pro' else ''}">
  <div class="cl-kicker">Último paso</div>
  <h2 class="cl-title">{E['cl_title']}</h2>
  <p>{E['cl_lead']}</p>
  <div class="cl-steps">{''.join(f'<div><b>{i + 1}</b>{t}</div>' for i, t in enumerate(E['steps']))}</div>
  <p class="cl-small">El resultado depende de tu dedicación, tu perfil y el mercado de cada rubro. Este manual te da el método; la constancia la ponés vos.</p>
</section>"""

CSS = open(__file__.replace("build.py", "style.css"), encoding="utf-8").read()
doc = f'''<!doctype html><html lang="es"><head><meta charset="utf-8"><title>Método 30 · {E['doc_title']}</title><style>{CSS}</style></head>
<body>{COVER}{WELCOME}{"".join(chap_html)}{CLOSING}</body></html>'''
open(OUT, "w", encoding="utf-8").write(doc)
print("ok", len(doc))
