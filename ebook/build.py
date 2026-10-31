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
ED = sys.argv[3] if len(sys.argv) > 3 else "main"  # "main" = Conseguí trabajo en 30 días, "pro" = Secretos de reclutador, "sueldo" = Cuánto pedir de sueldo
# Guías cortas (Introducción + Capítulo N + Caja de herramientas): nombre e ilustración de cada apertura
GEN = {
    "sueldo": dict(book="Cuánto pedir de sueldo", illus=["s0", "s1", "s2", "s3", "s4", "s5", "s6"]),
    "psico": dict(book="Psicotécnico sin miedo", illus=["p0", "p1", "p2", "p3", "b3", 4, "p6"]),
    "entrevista": dict(book="Las preguntas de la entrevista", illus=[5, "b3", 1, 3, "s3", "b4", 4, "s4"]),
    "primer": dict(book="Tu primer trabajo", illus=[0, "b1", 2, 4, 3, 5, "b4", 7]),
    "linkedin": dict(book="LinkedIn que te encuentra", illus=[4, "b1", 3, 2, "b3", 1, "s3", 7]),
    "remoto": dict(book="Trabajo remoto para el exterior", illus=["b2", "p1", "s3", 2, 4, 5, 6, "b4"]),
    "senior": dict(book="Buscar trabajo después de los 45", illus=[7, "b1", 2, "p0", 4, 5, 1, "b4"]),
}
BOOK = GEN[ED]["book"] if ED in GEN else {"main": "Conseguí trabajo en 30 días", "pro": "Secretos de reclutador"}[ED]
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
    # con [corchetes] es una plantilla para completar; sin corchetes, un ejemplo de cómo decirlo
    h = re.sub(r"<blockquote>(.*?)</blockquote>", lambda m: '<blockquote><div class="bq-tag">' + ("Plantilla para copiar" if "[" in m.group(1) else "Ejemplo") + '</div>' + m.group(1) + '</blockquote>', h, flags=re.S)
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

# guía de sueldo: s0 ancla · s1 calculadora · s2 rango · s3 diálogo · s4 oferta · s5 ajuste · s6 aumento
ILLU["s0"] = svg(
    blob(260, 210, 190, "#fff", .06) +
    f'<line x1="260" y1="60" x2="260" y2="300" stroke="#fff" stroke-width="14" stroke-linecap="round"/>'
    f'<circle cx="260" cy="60" r="26" fill="none" stroke="#fff" stroke-width="12"/>'
    f'<path d="M150 250 Q160 340 260 345 Q360 340 370 250" fill="none" stroke="#fff" stroke-width="14" stroke-linecap="round"/>'
    f'<path d="M130 262 l30 -28 l12 40 z" fill="{ACC2}"/><path d="M390 262 l-30 -28 l-12 40 z" fill="{ACC2}"/>'
    f'<rect x="215" y="120" width="90" height="14" rx="7" fill="#fff"/>'
)
ILLU["s1"] = svg(
    blob(260, 210, 190, "#fff", .06) +
    '<rect x="160" y="50" width="200" height="320" rx="24" fill="#fff"/>'
    f'<rect x="185" y="78" width="150" height="62" rx="10" fill="{INK}"/><text x="320" y="122" text-anchor="end" font-family="Inter" font-weight="800" font-size="30" fill="{MINT}">−17%</text>'
    + "".join(f'<rect x="{185+c*52}" y="{165+r*48}" width="42" height="36" rx="8" fill="{ACC if (r, c) == (3, 2) else "#E5E7EB"}"/>' for r in range(4) for c in range(3))
)
ILLU["s2"] = svg(
    blob(260, 210, 190, "#fff", .06) +
    f'<rect x="70" y="190" width="380" height="26" rx="13" fill="rgba(255,255,255,.25)"/>'
    f'<rect x="230" y="190" width="160" height="26" rx="13" fill="{MINT}"/>'
    + "".join(f'<line x1="{x}" y1="160" x2="{x}" y2="246" stroke="{c}" stroke-width="8" stroke-linecap="round"/><circle cx="{x}" cy="150" r="16" fill="{c}"/>' for x, c in [(130, "#fff"), (230, ACC2), (390, ACC)])
    + f'<text x="130" y="290" text-anchor="middle" font-family="Inter" font-weight="800" font-size="22" fill="#fff">PISO</text>'
      f'<text x="230" y="290" text-anchor="middle" font-family="Inter" font-weight="800" font-size="22" fill="{ACC2}">OBJETIVO</text>'
      f'<text x="390" y="290" text-anchor="middle" font-family="Inter" font-weight="800" font-size="22" fill="{ACC}">TECHO</text>'
)
ILLU["s3"] = svg(
    blob(260, 210, 190, "#fff", .06) +
    '<path d="M90 90 h220 a20 20 0 0 1 20 20 v90 a20 20 0 0 1 -20 20 h-150 l-40 36 v-36 h-30 a20 20 0 0 1 -20 -20 v-90 a20 20 0 0 1 20 -20 z" fill="#fff"/>'
    f'<text x="200" y="182" text-anchor="middle" font-family="Inter Display" font-weight="900" font-size="64" fill="{INK}">¿$?</text>'
    f'<path d="M430 210 h-180 a20 20 0 0 0 -20 20 v70 a20 20 0 0 0 20 20 h120 l40 32 v-32 h20 a20 20 0 0 0 20 -20 v-70 a20 20 0 0 0 -20 -20 z" fill="{ACC2}"/>'
    + "".join(f'<rect x="260" y="{240+i*26}" width="{140-i*40}" height="12" rx="6" fill="{INK}" opacity=".6"/>' for i in range(3))
)
ILLU["s4"] = svg(
    blob(260, 210, 190, "#fff", .06) +
    '<rect x="120" y="70" width="280" height="200" rx="16" fill="#fff"/>'
    f'<path d="M120 86 L260 190 L400 86" fill="none" stroke="#C9D3E6" stroke-width="10" stroke-linejoin="round"/>'
    f'<circle cx="380" cy="270" r="54" fill="{MINT}"/><path d="M352 270 l20 20 l38 -42" stroke="#fff" stroke-width="14" fill="none" stroke-linecap="round" stroke-linejoin="round"/>'
)
ILLU["s5"] = svg(
    blob(260, 210, 190, "#fff", .06) +
    "".join(f'<rect x="{90+i*58}" y="{300-h}" width="40" height="{h}" rx="8" fill="#fff" opacity="{.35+i*.1}"/>' for i, h in enumerate([90, 120, 150, 185, 220, 255]))
    + f'<polyline points="110,250 168,230 226,205 284,170 342,140 400,100" fill="none" stroke="{ACC2}" stroke-width="10" stroke-linecap="round" stroke-linejoin="round"/>'
      f'<circle cx="400" cy="100" r="16" fill="{ACC}"/>'
)
ILLU["s6"] = svg(
    blob(260, 210, 190, "#fff", .06) +
    f'<path d="M260 50 L380 190 H310 V340 H210 V190 H140 Z" fill="#fff"/>'
    f'<text x="260" y="290" text-anchor="middle" font-family="Inter Display" font-weight="900" font-size="58" fill="{ACC}">$</text>'
)

# psicotécnicos: p0 cabeza con engranaje · p1 cartas de tests · p2 dibujo casa-árbol-persona · p3 matriz · p6 reloj
ILLU["p0"] = svg(
    blob(260, 210, 190, "#fff", .06) +
    '<path d="M300 360 v-50 c60 -10 90 -60 90 -110 c0 -80 -60 -140 -140 -140 c-80 0 -130 60 -130 130 c0 30 -20 50 -30 70 h40 v50 c0 20 20 30 40 30 h30 v20 z" fill="#fff"/>'
    f'<circle cx="250" cy="180" r="52" fill="{ACC2}"/>'
    + "".join(f'<rect x="242" y="112" width="16" height="22" rx="4" fill="{ACC2}" transform="rotate({a} 250 180)"/>' for a in range(0, 360, 45))
    + f'<circle cx="250" cy="180" r="20" fill="#fff"/>'
)
ILLU["p1"] = svg(
    blob(260, 210, 190, "#fff", .06) +
    "".join(f'<g transform="rotate({r} {x+60} {y+80})"><rect x="{x}" y="{y}" width="120" height="160" rx="14" fill="#fff" opacity="{o}"/></g>' for x, y, r, o in [(90, 130, -14, .5), (200, 110, 0, .7), (310, 130, 14, .95)])
    + f'<circle cx="370" cy="200" r="22" fill="none" stroke="{ACC}" stroke-width="8"/><path d="M335 250 h70" stroke="{INK}" stroke-width="8" stroke-linecap="round"/>'
      f'<path d="M340 270 h50" stroke="#C9D3E6" stroke-width="8" stroke-linecap="round"/>'
)
ILLU["p2"] = svg(
    blob(260, 210, 190, "#fff", .06) +
    '<rect x="80" y="60" width="360" height="300" rx="10" fill="#fff"/>'
    f'<path d="M120 250 l50 -45 l50 45 v60 h-100 z" fill="none" stroke="{INK}" stroke-width="6" stroke-linejoin="round"/><rect x="155" y="275" width="26" height="35" fill="none" stroke="{INK}" stroke-width="5"/>'
    f'<rect x="250" y="250" width="14" height="60" fill="{INK}"/><circle cx="257" cy="225" r="38" fill="none" stroke="{MINT}" stroke-width="7"/>'
    f'<circle cx="350" cy="205" r="16" fill="none" stroke="{INK}" stroke-width="5"/><path d="M350 222 v48 M330 240 h40 M350 270 l-16 38 M350 270 l16 38" stroke="{INK}" stroke-width="5" stroke-linecap="round"/>'
    + "".join(f'<path d="M{x} {y} l-8 22" stroke="{SKY}" stroke-width="4" stroke-linecap="round"/>' for x, y in [(320, 90), (350, 110), (380, 85), (410, 115), (335, 140), (395, 150)])
    + f'<rect x="400" y="300" width="80" height="14" rx="7" fill="{ACC}" transform="rotate(-35 440 307)"/>'
)
ILLU["p3"] = svg(
    blob(260, 210, 190, "#fff", .06) +
    '<rect x="130" y="70" width="260" height="260" rx="16" fill="#fff"/>'
    + "".join(f'<line x1="{130+i*87}" y1="70" x2="{130+i*87}" y2="330" stroke="#E5E7EB" stroke-width="4"/><line x1="130" y1="{70+i*87}" x2="390" y2="{70+i*87}" stroke="#E5E7EB" stroke-width="4"/>' for i in (1, 2))
    + "".join(f'<circle cx="{173+c*87}" cy="{113+r*87}" r="{10+c*8}" fill="{[ACC, SKY, MINT][r]}"/>' for r in range(3) for c in range(3) if (r, c) != (2, 2))
    + f'<text x="347" y="320" text-anchor="middle" font-family="Inter Display" font-weight="900" font-size="64" fill="{ACC2}">?</text>'
)
ILLU["p6"] = svg(
    blob(260, 210, 190, "#fff", .06) +
    '<circle cx="260" cy="215" r="130" fill="#fff"/>'
    f'<circle cx="260" cy="215" r="112" fill="none" stroke="#E5E7EB" stroke-width="6"/>'
    + "".join(f'<rect x="256" y="112" width="8" height="18" rx="4" fill="{INK}" transform="rotate({a} 260 215)"/>' for a in range(0, 360, 30))
    + f'<line x1="260" y1="215" x2="260" y2="140" stroke="{INK}" stroke-width="10" stroke-linecap="round"/><line x1="260" y1="215" x2="320" y2="245" stroke="{ACC}" stroke-width="8" stroke-linecap="round"/>'
      f'<circle cx="260" cy="215" r="12" fill="{ACC2}"/><rect x="235" y="62" width="50" height="22" rx="8" fill="#fff"/>'
)

def meta_for(chapters):
    out, n = [], 0
    for title, _ in chapters:
        if ED in GEN:
            il = GEN[ED]["illus"]
            if title.startswith("Introducci"):
                out.append(dict(num="00", kicker="Introducción", main=title.split(":", 1)[1], illu=il[0], photo=ED + "0", theme=THEMES[0], bonus=False))
            elif title.startswith("Capítulo"):
                k = int(re.match(r"Capítulo (\d+)", title).group(1))
                out.append(dict(num=f"{k:02d}", kicker=f"Capítulo {k}", main=title.split(":", 1)[1], illu=il[k] if k < len(il) else 7, photo=f"{ED}{k}", theme=THEMES[(k + 1) % 8], bonus=False))
            else:
                out.append(dict(num="+", kicker="Caja de herramientas", main=title.split(":", 1)[1], illu=8, photo=ED + "8", theme=THEMES[8], bonus=False))
            continue
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
  <div class="op-foot">Método 30 · {BOOK}</div>
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
elif ED == "sueldo":
    E = dict(
        doc_title="Cuánto pedir de sueldo", photo="sueldo_portada", cover_cls="cover sueldo",
        badge="Método 30 · Guía 2026",
        title="Cuánto<br>pedir de<br><span>sueldo</span>",
        sub="El número, las frases exactas y la negociación: para no quedarte corto ni quedar afuera",
        seal='<div class="cv-seal"><div class="cv-seal-star">$</div><div class="cv-seal-l">GUÍA<br>2026</div></div>',
        illu=ILLU["s2"],
        pills=["Bruto y neto", "Tu número", "¿Cuánto pretendés?", "Negociar la oferta", "Pedir un aumento"],
        wl_title="El número que decís cambia todo",
        wl_lead="Esta guía te acompaña desde que armás tu número hasta que firmás la oferta, o hasta que pedís tu próximo aumento. Cada técnica está respaldada por estudios sobre negociación o por la ley argentina. Usala como manual de consulta: abrí el capítulo de la etapa en la que estás.",
        stats=[("3", "números para llegar preparado: piso, objetivo y techo"), ("10", "frases listas para usar en cada momento"), ("6", "capítulos, de la postulación al aumento"), ("2", "checklists: antes de decir un número y antes de aceptar")],
        cl_title="Ahora sabés cuánto pedir",
        cl_lead="Tenés tu número, las frases y el paso a paso. La próxima vez que te pregunten cuánto pretendés, vas a responder con datos y con seguridad.",
        steps=["Armá tus tres números con la tabla de la Caja de herramientas", "Practicá en voz alta las frases del capítulo 3", "Antes de aceptar cualquier oferta, repasá el checklist final"],
    )
elif ED == "psico":
    E = dict(
        doc_title="Psicotécnico sin miedo", photo="psico_portada", cover_cls="cover psico",
        badge="Método 30 · Guía práctica",
        title="Psicotécnico<br>sin<br><span>miedo</span>",
        sub="Qué te van a tomar, cómo prepararte de verdad y qué hacer el día de la evaluación",
        seal='<div class="cv-seal"><div class="cv-seal-star">✓</div><div class="cv-seal-l">23<br>EJERCICIOS</div></div>',
        illu=ILLU["p2"],
        pills=["Tests de dibujo", "Raven y Dominó", "Cuestionarios", "Dinámicas grupales", "El día de la evaluación"],
        wl_title="La etapa que más nervios da, explicada",
        wl_lead="El psicotécnico no es un examen para aprobar: es una forma de conocer cómo sos para ver si encajás con un puesto. Esta guía te cuenta qué pruebas se usan en Argentina, qué se observa en cada una, cuáles se pueden practicar y cómo llegar tranquilo. Al final tenés ejercicios de razonamiento con las respuestas explicadas.",
        stats=[("7", "pruebas de dibujo y de láminas explicadas"), ("3", "tipos de pruebas de razonamiento"), ("23", "ejercicios de práctica con respuestas"), ("2", "checklists: el día anterior y el día de la evaluación")],
        cl_title="Ahora sabés qué esperar",
        cl_lead="Ya sabés qué te pueden tomar, qué se observa y cómo prepararte. Lo demás es ser vos, con calma y siguiendo cada consigna.",
        steps=["Hacé los ejercicios de práctica de la Caja de herramientas", "Prepará tus ejemplos para la entrevista psicológica", "Repasá el checklist la noche anterior"],
    )
elif ED == "entrevista":
    E = dict(
        doc_title="Las preguntas de la entrevista", photo="entrevista_portada", cover_cls="cover entrevista",
        badge="Método 30 · Guía práctica",
        title="Las preguntas<br>de la<br><span>entrevista</span>",
        sub="Qué te van a preguntar, qué buscan con cada pregunta y cómo responder con ejemplos reales",
        seal='<div class="cv-seal"><div class="cv-seal-star">?</div><div class="cv-seal-l">28<br>PREGUNTAS</div></div>',
        illu=ILLU[5],
        pills=["Método STAR", "Preguntas difíciles", "Entrevista virtual", "Tus preguntas", "Después de la entrevista"],
        wl_title="Llegá sabiendo qué te van a preguntar",
        wl_lead="Casi todas las entrevistas se arman con las mismas preguntas, dichas de distintas formas. Esta guía te muestra qué evalúa cada una y cómo responderla con tus propios ejemplos, para que dejes de improvisar y llegues con tus historias preparadas.",
        stats=[("28", "preguntas frecuentes con cómo responderlas"), ("4", "pasos del método STAR"), ("8", "historias para preparar antes de cualquier entrevista"), ("10", "preguntas para hacer vos al final")],
        cl_title="Ahora te toca practicar",
        cl_lead="Las respuestas que funcionan no se improvisan: se preparan y se practican en voz alta. Armá tus historias y ensayalas hasta que te salgan naturales.",
        steps=["Completá tu banco de 8 historias STAR", "Practicá en voz alta las preguntas de la Caja de herramientas", "Prepará 3 preguntas para hacer al final"],
    )
elif ED == "primer":
    E = dict(
        doc_title="Tu primer trabajo", photo="primer_portada", cover_cls="cover primer",
        badge="Método 30 · Guía práctica",
        title="Tu<br>primer<br><span>trabajo</span>",
        sub="Cómo armar tu CV sin experiencia, dónde buscar y cómo pasar tu primera entrevista",
        seal='<div class="cv-seal"><div class="cv-seal-star">★</div><div class="cv-seal-l">SIN<br>EXPERIENCIA</div></div>',
        illu=ILLU[0],
        pills=["CV sin experiencia", "Dónde buscar", "LinkedIn desde cero", "Primera entrevista", "Tus derechos"],
        wl_title="Todos empezamos sin experiencia",
        wl_lead="Conseguir el primer trabajo es difícil porque te piden experiencia que todavía no tuviste. Esta guía te muestra cómo mostrar lo que sí tenés, dónde buscar las oportunidades que de verdad contratan sin experiencia y cómo prepararte para tu primera entrevista.",
        stats=[("12", "fuentes de experiencia que sí cuentan"), ("1", "modelo de CV para primer empleo"), ("10", "preguntas de primera entrevista con respuesta"), ("5", "derechos que tenés que conocer")],
        cl_title="Tu primer trabajo empieza hoy",
        cl_lead="No necesitás experiencia para empezar: necesitás mostrar bien lo que ya hiciste y postularte con constancia. Elegí tus primeras diez búsquedas y arrancá esta semana.",
        steps=["Armá tu CV con el modelo de la Caja de herramientas", "Abrí o completá tu perfil de LinkedIn", "Postulate a 10 búsquedas esta semana"],
    )
elif ED == "linkedin":
    E = dict(
        doc_title="LinkedIn que te encuentra", photo="linkedin_portada", cover_cls="cover linkedin",
        badge="Método 30 · Guía práctica",
        title="LinkedIn<br>que te<br><span>encuentra</span>",
        sub="Cómo armar un perfil que aparezca en las búsquedas de los reclutadores y usarlo para conseguir trabajo",
        seal='<div class="cv-seal"><div class="cv-seal-star">in</div><div class="cv-seal-l">PLAN DE<br>7 DÍAS</div></div>',
        illu=ILLU[3],
        pills=["Titular", "Acerca de", "Búsquedas", "Mensajes", "Plan de 7 días"],
        wl_title="Que te encuentren a vos",
        wl_lead="Los reclutadores buscan candidatos en LinkedIn todos los días, escribiendo palabras clave como en un buscador. Esta guía te muestra cómo funcionan esas búsquedas, cómo armar cada parte de tu perfil para aparecer y cómo usar la red para encontrar búsquedas y contactos, con ejemplos y mensajes listos para copiar.",
        stats=[("12", "titulares de ejemplo por rubro"), ("6", "mensajes listos para copiar"), ("7", "días para dejar tu perfil listo"), ("1", "checklist completo del perfil")],
        cl_title="Tu perfil ya trabaja para vos",
        cl_lead="Un perfil completo y con las palabras correctas te hace visible las 24 horas. Sumale constancia (conectar, comentar, escribir) y LinkedIn se convierte en tu mejor canal de búsqueda.",
        steps=["Seguí el plan de 7 días del capítulo 7", "Escribí 3 mensajes por semana con las plantillas", "Revisá el checklist del perfil una vez por mes"],
    )
elif ED == "remoto":
    E = dict(
        doc_title="Trabajo remoto para el exterior", photo="remoto_portada", cover_cls="cover remoto",
        badge="Método 30 · Guía práctica",
        title="Trabajo<br>remoto para<br>el <span>exterior</span>",
        sub="Cómo conseguir trabajo para empresas de afuera desde Argentina, y cómo cobrar sin sorpresas",
        seal='<div class="cv-seal"><div class="cv-seal-star">USD</div><div class="cv-seal-l">DESDE<br>ARGENTINA</div></div>',
        illu=ILLU["b2"],
        pills=["Qué trabajos", "Inglés", "CV en inglés", "Dónde buscar", "Cómo cobrar"],
        wl_title="Trabajar para afuera, con los pies en la tierra",
        wl_lead="Trabajar desde Argentina para una empresa del exterior es posible y cada vez más común, pero no es mágico: hay mucha competencia, el inglés pesa y las reglas para facturar y cobrar cambian seguido. Esta guía te muestra el camino completo, con información verificada y sin promesas exageradas.",
        stats=[("3", "formas de trabajar para el exterior"), ("1", "modelo de CV en inglés"), ("5", "respuestas en inglés para la entrevista"), ("8", "señales de estafa para detectar")],
        cl_title="Tu próximo cliente puede estar en otro país",
        cl_lead="Ya tenés el mapa: qué trabajos existen, cómo prepararte, dónde buscar y cómo cobrar. Lo que sigue es practicar inglés, adaptar tu perfil y postularte con constancia.",
        steps=["Pasá tu CV al inglés con el modelo de la Caja de herramientas", "Armá tu LinkedIn en inglés y activá las búsquedas remotas", "Consultá con un contador antes de tu primera factura"],
    )
elif ED == "senior":
    E = dict(
        doc_title="Buscar trabajo después de los 45", photo="senior_portada", cover_cls="cover senior",
        badge="Método 30 · Guía práctica",
        title="Buscar trabajo<br>después<br>de los <span>45</span>",
        sub="Cómo convertir tu experiencia en tu mayor ventaja y desarmar los prejuicios por la edad",
        seal='<div class="cv-seal"><div class="cv-seal-star">45+</div><div class="cv-seal-l">EXPERIENCIA<br>QUE SUMA</div></div>',
        illu=ILLU[7],
        pills=["Los prejuicios", "Un CV sin edad", "Actualizarte", "Tu red", "Otros caminos"],
        wl_title="Tu experiencia vale. Hay que saber mostrarla",
        wl_lead="Buscar trabajo después de los 45 tiene desafíos reales: los prejuicios por la edad existen. Pero la investigación muestra que la mayoría de esos prejuicios no tienen sustento, y vos tenés algo que nadie más tiene: años de experiencia y una red de contactos. Esta guía te muestra cómo usarlos a tu favor.",
        stats=[("6", "prejuicios frecuentes y cómo desarmarlos"), ("1", "estructura de CV que muestra experiencia, no edad"), ("6", "preguntas incómodas con respuesta"), ("7", "caminos posibles además del empleo tradicional")],
        cl_title="Tu experiencia es tu ventaja",
        cl_lead="Ya sabés cómo mostrarla, cómo desarmar los prejuicios y dónde buscar. Empezá por tu red: es el recurso más valioso que tenés.",
        steps=["Actualizá tu CV con la estructura de la Caja de herramientas", "Hacé tu lista de 50 contactos y escribile a 5 esta semana", "Elegí un curso corto para actualizar una herramienta clave"],
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
