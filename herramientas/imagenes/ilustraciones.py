"""Ilustraciones SVG reutilizables para las imágenes de las marcas (cajas ORDI,
zapatillas VANTA, estación de propagación VERDEA, pie para la guía de talles)."""
import math

_uid = [0]
def uid(p):
    _uid[0] += 1
    return "%s%d" % (p, _uid[0])


# ------------------------------------------------------------------ ORDI
ROLL_COLORS = ["#F4F0E8", "#9FAAA3", "#CDB89C", "#6F7E8F", "#D8AFA2", "#E9E1D2", "#8E9A86"]

def caja(width=300, rolls=True, seed=0, handle="#8A5A3B"):
    """Caja de lino vista de frente y un poco desde arriba (se ve la boca)."""
    g, tex, clip, sh = uid("lin"), uid("tex"), uid("clp"), uid("sh")
    h = width * 240 / 300
    parts = []
    parts.append('<svg viewBox="0 0 300 240" width="%d" height="%d" xmlns="http://www.w3.org/2000/svg">' % (width, h))
    parts.append('<defs>'
                 '<linearGradient id="%s" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#EADFCD"/><stop offset="1" stop-color="#D9C8AE"/></linearGradient>'
                 '<pattern id="%s" width="6" height="6" patternUnits="userSpaceOnUse"><path d="M0 1.5H6M0 4.5H6" stroke="#8C7556" stroke-opacity=".10" stroke-width=".8"/><path d="M1.5 0V6M4.5 0V6" stroke="#8C7556" stroke-opacity=".06" stroke-width=".8"/></pattern>'
                 '<clipPath id="%s"><polygon points="24,16 276,16 290,58 10,58"/></clipPath>'
                 '<filter id="%s" x="-20%%" y="-50%%" width="140%%" height="200%%"><feGaussianBlur stdDeviation="5"/></filter>'
                 '</defs>' % (g, tex, clip, sh))
    parts.append('<ellipse cx="150" cy="230" rx="138" ry="8" fill="#000" opacity=".16" filter="url(#%s)"/>' % sh)
    # boca de la caja (interior)
    parts.append('<polygon points="24,16 276,16 290,58 10,58" fill="#B9A281"/>')
    parts.append('<polygon points="24,16 276,16 278,26 22,26" fill="#A88F6D"/>')
    if rolls:
        parts.append('<g clip-path="url(#%s)">' % clip)
        n = 6
        for i in range(n):
            cx = 36 + i * 45.5
            col = ROLL_COLORS[(i + seed) % len(ROLL_COLORS)]
            parts.append('<circle cx="%.1f" cy="56" r="21" fill="%s" stroke="#000" stroke-opacity=".08"/>' % (cx, col))
            parts.append('<path d="M%.1f 56 m-11 0 a11 11 0 1 1 11 11 a6 6 0 1 1 -6 -6" fill="none" stroke="#000" stroke-opacity=".14" stroke-width="1.6"/>' % cx)
        parts.append('</g>')
    # borde de la boca (espesor de la tela)
    parts.append('<polyline points="10,58 24,16 276,16 290,58" fill="none" stroke="#E2D5BF" stroke-width="3" stroke-linejoin="round"/>')
    # frente
    front = "M10 58H290V214Q290 226 278 226H22Q10 226 10 214Z"
    parts.append('<path d="%s" fill="url(#%s)"/>' % (front, g))
    parts.append('<path d="%s" fill="url(#%s)"/>' % (front, tex))
    parts.append('<rect x="10" y="56" width="280" height="8" rx="2" fill="#C9B394"/>')
    parts.append('<path d="M14 220H286" stroke="#BFA785" stroke-width="2" stroke-opacity=".5"/>')
    # manija de cuero
    parts.append('<rect x="118" y="94" width="64" height="20" rx="10" fill="%s"/>' % handle)
    parts.append('<rect x="122" y="98" width="56" height="12" rx="6" fill="none" stroke="#F3E3CF" stroke-opacity=".7" stroke-width="1.2" stroke-dasharray="2.5 2.5"/>')
    parts.append('<circle cx="126" cy="104" r="3" fill="#5E3B26"/><circle cx="174" cy="104" r="3" fill="#5E3B26"/>')
    parts.append('</svg>')
    return "".join(parts)


def estante_desordenado(width=820):
    """Estante con pilas de ropa caídas y revueltas."""
    h = width * 420 / 820
    out = ['<svg viewBox="0 0 820 420" width="%d" height="%d" xmlns="http://www.w3.org/2000/svg">' % (width, h)]
    out.append('<rect x="0" y="0" width="820" height="420" rx="18" fill="#E7DCCB"/>')
    out.append('<rect x="20" y="20" width="780" height="380" rx="10" fill="#F2EADD"/>')
    for y in (205, 385):
        out.append('<rect x="20" y="%d" width="780" height="16" fill="#C7A983"/>' % y)
    import random
    rnd = random.Random(7)
    cols = ROLL_COLORS + ["#B9C4CF", "#E3C9A5", "#A7B39B"]
    for shelf_y in (205, 385):
        x = 40
        while x < 760:
            pile_h = rnd.randint(3, 7)
            y = shelf_y
            for k in range(pile_h):
                w = rnd.randint(70, 120)
                hh = rnd.randint(14, 22)
                ang = rnd.uniform(-14, 14) * (1 + k * 0.25)
                dx = rnd.uniform(-10, 10) * k * 0.5
                y -= hh - 2
                out.append('<rect x="%.0f" y="%.0f" width="%d" height="%d" rx="5" fill="%s" stroke="#000" stroke-opacity=".08" transform="rotate(%.1f %.0f %.0f)"/>'
                           % (x + dx, y, w, hh, rnd.choice(cols), ang, x + w / 2, y + hh / 2))
            # prenda colgando del estante
            if rnd.random() < .5:
                out.append('<path d="M%.0f %d q20 40 -6 80" stroke="%s" stroke-width="16" fill="none" stroke-linecap="round"/>' % (x + 40, shelf_y + 14, rnd.choice(cols)))
            x += rnd.randint(110, 150)
    out.append('</svg>')
    return "".join(out)


def estante_ordenado(width=820):
    h = width * 420 / 820
    out = ['<svg viewBox="0 0 820 420" width="%d" height="%d" xmlns="http://www.w3.org/2000/svg">' % (width, h)]
    out.append('<rect x="0" y="0" width="820" height="420" rx="18" fill="#E7DCCB"/>')
    out.append('<rect x="20" y="20" width="780" height="380" rx="10" fill="#F2EADD"/>')
    for y in (205, 385):
        out.append('<rect x="20" y="%d" width="780" height="16" fill="#C7A983"/>' % y)
    # estante de arriba: 3 cajas
    xs = [(60, 230), (300, 230), (540, 230)]
    for i, (x, w) in enumerate(xs):
        svg = caja(w, rolls=True, seed=i * 2)
        out.append('<g transform="translate(%d %d)">%s</g>' % (x, 205 - w * 240 / 300 + 6, svg))
    # estante de abajo: toallas prolijas + 2 cajas
    for i in range(4):
        out.append('<rect x="70" y="%d" width="150" height="34" rx="10" fill="%s" stroke="#000" stroke-opacity=".06"/>' % (385 - 34 * (i + 1) - 2 * i, ["#F4F0E8", "#CDB89C", "#9FAAA3", "#E9E1D2"][i]))
    for i, x in enumerate((300, 540)):
        svg = caja(220, rolls=True, seed=i + 3)
        out.append('<g transform="translate(%d %d)">%s</g>' % (x, 385 - 220 * 240 / 300 + 6, svg))
    out.append('</svg>')
    return "".join(out)


# ------------------------------------------------------------------ VANTA
def zapatilla(width=360, color="negro", flip=False):
    pal = {
        "negro": dict(upper="#151515", cap="#0B0B0B", heel="#232323", lace="#F2F2F2", sole="#FAFAF8", line="#DCDCD8", stitch="#5A5A5A", tongue="#222", outline="none"),
        "blanco": dict(upper="#F8F8F6", cap="#EEEEEA", heel="#0A0A0A", lace="#FFFFFF", sole="#FFFFFF", line="#D6D6D2", stitch="#BDBDB8", tongue="#F1F1EE", outline="#CFCFCA"),
    }[color]
    h = width * 190 / 360
    sh = uid("zs")
    t = ' transform="translate(360 0) scale(-1 1)"' if flip else ''
    o = ['<svg viewBox="0 0 360 190" width="%d" height="%d" xmlns="http://www.w3.org/2000/svg">' % (width, h)]
    o.append('<defs><filter id="%s" x="-20%%" y="-50%%" width="140%%" height="200%%"><feGaussianBlur stdDeviation="5"/></filter></defs>' % sh)
    o.append('<g%s>' % t)
    o.append('<ellipse cx="182" cy="178" rx="160" ry="7" fill="#000" opacity=".18" filter="url(#%s)"/>' % sh)
    st = ' stroke="%s" stroke-width="1.5"' % pal["outline"] if pal["outline"] != "none" else ''
    # lengüeta
    o.append('<path d="M150 50C150 36 160 25 173 26C183 27 188 35 186 45L180 60Z" fill="%s"%s/>' % (pal["tongue"], st))
    # capellada
    o.append('<path d="M32 134L36 86C37 68 46 60 60 58L86 57C96 72 112 75 128 66L158 42C165 35 174 33 182 37L206 52C234 68 270 88 306 102C328 110 342 120 340 134Z" fill="%s"%s/>' % (pal["upper"], st))
    # puntera
    o.append('<path d="M266 94C292 101 326 109 336 120C341 126 341 131 340 134L258 134C258 118 260 104 266 94Z" fill="%s"%s/>' % (pal["cap"], st))
    # talón
    o.append('<path d="M32 134L36 92C48 96 62 108 66 134Z" fill="%s"/>' % pal["heel"])
    o.append('<rect x="30" y="64" width="10" height="26" rx="4" fill="%s"/>' % pal["heel"])
    # acolchado del cuello
    o.append('<path d="M60 58L86 57C96 72 112 75 128 66" fill="none" stroke="%s" stroke-width="5" stroke-linecap="round" opacity=".55"/>' % pal["stitch"])
    # cordones
    sx, sy, ex, ey = 162, 50, 240, 84
    dx, dy = ex - sx, ey - sy
    L = math.hypot(dx, dy)
    px, py = -dy / L * 11, dx / L * 11
    for k in range(6):
        cx, cy = sx + dx * k / 5, sy + dy * k / 5
        o.append('<circle cx="%.1f" cy="%.1f" r="2.4" fill="%s"/>' % (cx - px, cy - py, pal["stitch"]))
        o.append('<circle cx="%.1f" cy="%.1f" r="2.4" fill="%s"/>' % (cx + px, cy + py, pal["stitch"]))
        o.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="3.2" stroke-linecap="round"/>' % (cx - px, cy - py, cx + px + 6, cy + py - 3, pal["lace"]))
    # costura
    o.append('<path d="M40 126C130 124 250 124 334 126" fill="none" stroke="%s" stroke-width="1.4" stroke-dasharray="4 4"/>' % pal["stitch"])
    # suela
    o.append('<path d="M18 147C18 167 34 172 52 172L318 172C336 172 348 164 348 151C348 139 340 133 326 132L36 132C24 133 18 139 18 147Z" fill="%s" stroke="%s" stroke-width="1.5"/>' % (pal["sole"], pal["line"]))
    o.append('<path d="M26 154H340" stroke="%s" stroke-width="2"/>' % pal["line"])
    o.append('<path d="M30 166H336" stroke="%s" stroke-width="3" stroke-linecap="round"/>' % ("#2A2A2A" if color == "negro" else "#D6D6D2"))
    o.append('</g></svg>')
    return "".join(o)


def pie_midiendo(width=320, ink="#0A0A0A", marca=True, flecha=True):
    h = width * 420 / 320
    o = ['<svg viewBox="0 0 320 420" width="%d" height="%d" xmlns="http://www.w3.org/2000/svg">' % (width, h)]
    o.append('<rect x="0" y="0" width="320" height="34" fill="#DADAD6"/>')
    o.append('<rect x="0" y="30" width="320" height="6" fill="#BDBDB8"/>')
    o.append('<rect x="58" y="36" width="190" height="368" fill="#FFFFFF" stroke="#E2E2DE"/>')
    # pie (vista de arriba)
    o.append('<path d="M152 392C118 392 106 360 108 314C110 268 100 214 106 166C110 136 126 122 150 122C178 122 198 140 198 172C198 220 192 270 194 316C196 362 184 392 152 392Z" fill="%s" fill-opacity=".07" stroke="%s" stroke-width="2.2"/>' % (ink, ink))
    for cx, cy, r in ((124, 100, 15), (149, 90, 11), (170, 95, 10), (186, 106, 9), (198, 121, 8)):
        o.append('<circle cx="%d" cy="%d" r="%d" fill="%s" fill-opacity=".07" stroke="%s" stroke-width="2.2"/>' % (cx, cy, r, ink, ink))
    if marca:
        # marca del dedo más largo + lápiz
        o.append('<path d="M70 74H236" stroke="#E10600" stroke-width="2.5" stroke-dasharray="7 5"/>')
        o.append('<g transform="rotate(-30 250 64)"><rect x="236" y="58" width="70" height="12" rx="2" fill="#F2C94C"/><path d="M236 58L222 64L236 70Z" fill="#E8C9A0"/><path d="M226 62L222 64L226 66Z" fill="#333"/></g>')
    if flecha:
        o.append('<path d="M272 40V392" stroke="%s" stroke-width="2"/>' % ink)
        o.append('<path d="M266 50L272 40L278 50M266 382L272 392L278 382" fill="none" stroke="%s" stroke-width="2"/>' % ink)
        o.append('<rect x="252" y="200" width="40" height="26" rx="6" fill="%s"/><text x="272" y="218" font-family="Archivo,Arial" font-weight="800" font-size="13" fill="#fff" text-anchor="middle">cm</text>' % ink)
    o.append('</svg>')
    return "".join(o)


# ------------------------------------------------------------------ VERDEA
def hoja(x, y, s, ang, color="#5A9C48", vena="#8CC27A"):
    return ('<g transform="translate(%.1f %.1f) rotate(%.1f) scale(%.2f)">'
            '<path d="M0 0C-12 -1 -19 -12 -16 -23C-13 -32 -5 -36 0 -46C5 -36 13 -32 16 -23C19 -12 12 -1 0 0Z" fill="%s"/>'
            '<path d="M0 -2V-40" stroke="%s" stroke-width="1.6" stroke-linecap="round"/>'
            '</g>' % (x, y, ang, s, color, vena))


def raices(cx, top, nivel, color="#F1E6CF"):
    """nivel 0: sin raíces · 1: primeras raíces · 2: raíces largas con ramificaciones."""
    o = []
    if nivel == 0:
        o.append('<circle cx="%.1f" cy="%.1f" r="3" fill="#7A9B5E"/>' % (cx, top))
        return "".join(o)
    specs = {1: [(-8, 18), (0, 24), (7, 16), (12, 10)], 2: [(-14, 46), (-6, 56), (2, 62), (9, 52), (15, 40), (-18, 30)]}[nivel]
    for dx, ln in specs:
        x2, y2 = cx + dx, top + ln
        o.append('<path d="M%.1f %.1f Q%.1f %.1f %.1f %.1f" stroke="%s" stroke-width="2.3" fill="none" stroke-linecap="round"/>' % (cx, top, cx + dx * .3, top + ln * .6, x2, y2, color))
        if nivel == 2:
            o.append('<path d="M%.1f %.1f q%.1f 6 %.1f 14" stroke="%s" stroke-width="1.4" fill="none" stroke-linecap="round"/>' % (cx + dx * .55, top + ln * .55, dx * .4 + 4, dx * .2 + 6, color))
    return "".join(o)


def tubo(cx, top=128, bottom=360, agua=222, nivel=2, tallo_alto=72, inclinacion=8, hojas=None, agujero=True):
    """Tubo de vidrio con agua, esqueje, raíces y hojas (coordenadas de la estación)."""
    o = []
    if agujero:
        o.append('<ellipse cx="%.1f" cy="%d" rx="29" ry="6" fill="#5C3A1E" opacity=".35"/>' % (cx, top + 24))
    r = 25
    o.append('<path d="M%.1f %dV%dA%d %d 0 0 0 %.1f %dV%dZ" fill="#E3F1F2" fill-opacity=".35" stroke="#FFFFFF" stroke-opacity=".9" stroke-width="2"/>' % (cx - r, top, bottom - r, r, r, cx + r, bottom - r, top))
    o.append('<path d="M%.1f %dV%dA%d %d 0 0 0 %.1f %dV%dZ" fill="#9FCBD2" fill-opacity=".42"/>' % (cx - r + 3, agua, bottom - r, r - 3, r - 3, cx + r - 3, bottom - r, agua))
    o.append('<ellipse cx="%.1f" cy="%d" rx="%d" ry="4" fill="#FFFFFF" opacity=".45"/>' % (cx, agua, r - 3))
    base = agua + 70
    o.append(raices(cx, base, nivel))
    tx = cx + inclinacion
    o.append('<path d="M%.1f %d Q%.1f %.1f %.1f %d" stroke="#4E8B3A" stroke-width="5" fill="none" stroke-linecap="round"/>' % (cx, base, cx - 4, (base + tallo_alto) / 2, tx, tallo_alto))
    for (dx, dy, s, a) in (hojas or [(-2, 0, 1.0, -35), (6, 18, .9, 40)]):
        o.append(hoja(tx + dx, tallo_alto + dy, s, a))
    o.append('<path d="M%.1f %dV%d" stroke="#FFFFFF" stroke-opacity=".55" stroke-width="4" stroke-linecap="round"/>' % (cx - 14, top + 14, bottom - 30))
    o.append('<ellipse cx="%.1f" cy="%d" rx="27" ry="6" fill="none" stroke="#FFFFFF" stroke-opacity=".95" stroke-width="2"/>' % (cx, top))
    return "".join(o)


def estacion(width=560, logo="VERDEA", niveles=(1, 2, 2)):
    h = width * 460 / 560
    wg, wv, sh = uid("wg"), uid("wv"), uid("ws")
    o = ['<svg viewBox="0 0 560 460" width="%d" height="%d" xmlns="http://www.w3.org/2000/svg">' % (width, h)]
    o.append('<defs><linearGradient id="%s" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#DDB386"/><stop offset="1" stop-color="#B9875B"/></linearGradient>'
             '<linearGradient id="%s" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#C69466"/><stop offset=".5" stop-color="#DCB184"/><stop offset="1" stop-color="#BE8B5E"/></linearGradient>'
             '<filter id="%s" x="-20%%" y="-50%%" width="140%%" height="200%%"><feGaussianBlur stdDeviation="7"/></filter></defs>' % (wg, wv, sh))
    o.append('<ellipse cx="280" cy="432" rx="250" ry="12" fill="#000" opacity=".2" filter="url(#%s)"/>' % sh)
    # postes
    o.append('<rect x="62" y="166" width="24" height="220" rx="5" fill="url(#%s)"/>' % wv)
    o.append('<rect x="474" y="166" width="24" height="220" rx="5" fill="url(#%s)"/>' % wv)
    # base
    o.append('<rect x="36" y="380" width="488" height="46" rx="10" fill="url(#%s)"/>' % wg)
    o.append('<rect x="36" y="380" width="488" height="8" rx="4" fill="#FFFFFF" opacity=".2"/>')
    for k, yy in enumerate((398, 410)):
        o.append('<path d="M60 %d C160 %d 240 %d 330 %d S470 %d 500 %d" stroke="#7A4E2A" stroke-opacity=".16" stroke-width="1.5" fill="none"/>' % (yy, yy - 4, yy + 4, yy, yy - 3, yy))
    if logo:
        o.append('<text x="280" y="414" font-family="Poppins,Arial" font-weight="700" font-size="17" letter-spacing="5" fill="#6E4524" fill-opacity=".55" text-anchor="middle">%s</text>' % logo)
    # travesaño
    o.append('<rect x="50" y="150" width="460" height="30" rx="7" fill="url(#%s)"/>' % wg)
    o.append('<rect x="50" y="150" width="460" height="6" rx="3" fill="#FFFFFF" opacity=".22"/>')
    # tubos
    conf = [
        (170, dict(tallo_alto=78, inclinacion=-6, hojas=[(-2, 0, 1.05, -30), (4, 22, .85, 38)])),
        (280, dict(tallo_alto=58, inclinacion=6, hojas=[(0, 0, 1.15, -12), (-6, 20, .95, -52), (6, 28, .9, 46)])),
        (390, dict(tallo_alto=70, inclinacion=10, hojas=[(2, 0, 1.1, 18), (-4, 22, .9, -40)])),
    ]
    for (cx, kw), niv in zip(conf, niveles):
        o.append(tubo(cx, nivel=niv, **kw))
    o.append('</svg>')
    return "".join(o)


def tubo_solo(width=230, nivel=1, hojas_n=2):
    """Un tubo suelto con su base chica (para mostrar etapas)."""
    h = width * 460 / 230
    sh = uid("ts")
    hojas = [(-2, 0, 1.0, -28), (4, 20, .85, 40), (-6, 34, .8, -50)][:hojas_n]
    o = ['<svg viewBox="35 0 230 460" width="%d" height="%d" xmlns="http://www.w3.org/2000/svg">' % (width, h)]
    o.append('<defs><filter id="%s" x="-20%%" y="-50%%" width="140%%" height="200%%"><feGaussianBlur stdDeviation="5"/></filter></defs>' % sh)
    o.append('<ellipse cx="150" cy="420" rx="70" ry="8" fill="#000" opacity=".18" filter="url(#%s)"/>' % sh)
    o.append('<rect x="88" y="372" width="124" height="40" rx="9" fill="#C99A6B"/><rect x="88" y="372" width="124" height="7" rx="3" fill="#FFFFFF" opacity=".2"/>')
    o.append(tubo(150, top=110, bottom=372, agua=210, nivel=nivel, tallo_alto=66, inclinacion=4, hojas=hojas, agujero=False))
    o.append('</svg>')
    return "".join(o)


def pila_caida(width=300):
    """Pila de remeras torcida (lo que pasa al apilar)."""
    h = width * 300 / 300
    o = ['<svg viewBox="0 0 300 300" width="%d" height="%d" xmlns="http://www.w3.org/2000/svg">' % (width, h)]
    cols = ["#9FAAA3", "#F4F0E8", "#CDB89C", "#6F7E8F", "#D8AFA2", "#E9E1D2", "#8E9A86"]
    y = 270
    for k in range(7):
        ang = (-1) ** k * (3 + k * 2.2)
        y -= 30
        o.append('<rect x="%d" y="%d" width="190" height="30" rx="8" fill="%s" stroke="#000" stroke-opacity=".08" transform="rotate(%.1f 150 %d)"/>' % (55 + k * 4, y, cols[k], ang, y + 15))
    o.append('<path d="M60 286H250" stroke="#C7A983" stroke-width="10" stroke-linecap="round"/>')
    o.append('</svg>')
    return "".join(o)


def etiqueta_caja(texto, width=230, seed=0):
    return ('<div style="display:flex;flex-direction:column;align-items:center">%s'
            '<div style="margin-top:-118px;background:#fff;border-radius:6px;padding:6px 14px;font:600 20px DM Sans,sans-serif;color:#3B342F;box-shadow:0 2px 6px rgba(0,0,0,.08);position:relative">%s</div>'
            '<div style="height:88px"></div></div>' % (caja(width, seed=seed), texto))
