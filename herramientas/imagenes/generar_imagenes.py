"""Genera las imágenes de las marcas (galería, carruseles y conceptos) como PNG.

Uso:  python3 herramientas/imagenes/generar_imagenes.py
      node herramientas/imagenes/render.js /tmp/jobs.json
(o directamente: bash herramientas/imagenes/generar.sh)

Los precios y textos se toman de este archivo: si cambian, editalos acá y volvé a generar.
"""
import json, os, sys, urllib.request, base64
sys.path.insert(0, os.path.dirname(__file__))
from ilustraciones import (caja, estante_desordenado, estante_ordenado, zapatilla, pie_midiendo,
                           estacion, tubo_solo, pila_caida, etiqueta_caja)

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
BUILD = os.environ.get("BUILD_DIR", "/tmp/imagenes-build")
os.makedirs(BUILD, exist_ok=True)
JOBS = []

BASE_CSS = """
*{box-sizing:border-box;margin:0;padding:0}
html,body{width:%(w)dpx;height:%(h)dpx;overflow:hidden}
body{background:%(bg)s;color:%(ink)s;font-family:%(body)s;-webkit-font-smoothing:antialiased}
.t{font-family:%(title)s}
.c{display:flex;flex-direction:column;align-items:center;text-align:center}
.row{display:flex;align-items:flex-end;justify-content:center}
"""

FONTS = {
    "verdea": ("'Poppins',sans-serif", "'Open Sans',sans-serif", "family=Poppins:wght@500;600;700;800&family=Open+Sans:wght@400;600;700"),
    "ordi": ("'Fraunces',Georgia,serif", "'DM Sans',sans-serif", "family=Fraunces:opsz,wght@9..144,500;9..144,600;9..144,700&family=DM+Sans:wght@400;500;600;700"),
    "vanta": ("'Archivo',sans-serif", "'Inter',sans-serif", "family=Archivo:wght@600;700;800;900&family=Inter:wght@400;500;600;700"),
}


def page(brand, name, out_rel, w, h, bg, ink, body_html, extra_css=""):
    title, bodyf, fam = FONTS[brand]
    css = BASE_CSS % dict(w=w, h=h, bg=bg, ink=ink, body=bodyf, title=title) + extra_css
    html = ('<!doctype html><html><head><meta charset="utf-8">'
            '<link href="https://fonts.googleapis.com/css2?%s&display=block" rel="stylesheet">'
            '<style>%s</style></head><body>%s</body></html>' % (fam, css, body_html))
    path = os.path.join(BUILD, name + ".html")
    open(path, "w", encoding="utf-8").write(html)
    out = os.path.join(ROOT, out_rel)
    os.makedirs(os.path.dirname(out), exist_ok=True)
    JOBS.append({"html": path, "out": out, "w": w, "h": h})


def data_uri(url, cache_name):
    p = os.path.join(BUILD, cache_name)
    if not os.path.exists(p):
        urllib.request.urlretrieve(url, p)
    return "data:image/png;base64," + base64.b64encode(open(p, "rb").read()).decode()


# =================================================================== ORDI
O = dict(bg="#F5F0E8", ink="#2F2A26", accent="#C65D3B", sand="#A8896B", earth="#3B342F")
ORDI_DIR = "ORDI-organizacion-hogar/creativos/imagenes/"
ORDI_PRECIOS = [("1 set", "$34.900", "", "", "3 cajas"),
                ("2 sets", "$59.900", "$69.800", "AHORRÁS 14% + GUÍA", "6 cajas"),
                ("3 sets", "$79.900", "$104.700", "AHORRÁS 24% + ENVÍO GRATIS", "9 cajas")]
ordi_css = """
.kick{font-size:20px;letter-spacing:.18em;font-weight:700;color:%(sand)s;text-transform:uppercase}
h1{font-family:'Fraunces',Georgia,serif;font-weight:600;font-size:66px;line-height:1.05;letter-spacing:-.01em;color:%(ink)s}
.sub{font-size:27px;color:#6E6157;margin-top:12px}
.pill{display:inline-block;background:%(ink)s;color:#fff;border-radius:999px;padding:16px 34px;font-size:24px;font-weight:600}
.tag{display:inline-block;background:%(accent)s;color:#fff;border-radius:999px;padding:9px 16px;font-size:17px;font-weight:700;letter-spacing:.01em;white-space:nowrap}
.pop{display:inline-block;background:%(sand)s;color:#fff;border-radius:8px;padding:7px 14px;font-size:17px;font-weight:700;letter-spacing:.06em}
.brand{font-family:'Fraunces',Georgia,serif;font-weight:700;font-size:30px;letter-spacing:.06em}
""" % O

# --- O1 · Medidas
cajas = [("Grande", "40 × 30 × 25 cm", "Sábanas, toallas, abrigos", 330),
         ("Mediana", "35 × 25 × 20 cm", "Remeras, jeans, buzos", 282),
         ("Chica", "30 × 20 × 15 cm", "Ropa interior, medias", 236)]
ilus = "".join('<div class="c" style="width:330px;justify-content:flex-end">%s</div>' % caja(w, seed=i) for i, (n, m, d, w) in enumerate(cajas))
textos = "".join('<div class="c" style="width:330px"><div class="t" style="font-weight:700;font-size:36px">%s</div>'
                 '<div style="font-size:27px;font-weight:700;color:%s;margin-top:6px">%s</div>'
                 '<div style="font-size:22px;color:#6E6157;margin-top:6px;line-height:1.3">%s</div></div>'
                 % (n, O["accent"], m, d) for (n, m, d, w) in cajas)
page("ordi", "ordi-medidas", ORDI_DIR + "galeria-medidas-1080.png", 1080, 1080, O["bg"], O["ink"],
     '<div class="c" style="padding:76px 30px 0">'
     '<div class="kick">Set x3 · tela símil lino</div>'
     '<h1 style="margin-top:14px">3 medidas para<br>aprovechar cada estante</h1>'
     '<div class="row" style="gap:8px;margin-top:58px;height:270px;align-items:flex-end">%s</div>'
     '<div style="width:1010px;height:16px;border-radius:8px;background:#D9C7AC;margin-top:-10px"></div>'
     '<div class="row" style="gap:8px;margin-top:30px;align-items:flex-start">%s</div>'
     '<div style="margin-top:44px"><span class="pill">Plegables · base rígida · manijas reforzadas</span></div>'
     '<div style="font-size:18px;color:#8C7F72;margin-top:16px">Medidas: largo × ancho × alto</div>'
     '</div>' % (ilus, textos), ordi_css)

# --- O2 · Packs
def pila(n_sets, w):
    sets = []
    for s in range(n_sets):
        stack = ('<div class="c" style="gap:0">%s%s%s</div>'
                 % (caja(int(w * .62), seed=s + 2), caja(int(w * .8), seed=s + 1), caja(w, seed=s)))
        sets.append(stack)
    return '<div class="row" style="gap:6px">%s</div>' % "".join(sets)

pack_cols = []
for i, (nom, precio, viejo, tag, cont) in enumerate(ORDI_PRECIOS):
    w = [190, 128, 88][i]
    pack_cols.append(
        '<div class="c" style="width:330px;justify-content:flex-end">'
        '<div style="height:40px">%s</div>'
        '<div class="t" style="font-weight:600;font-size:36px;margin-top:6px">%s</div>'
        '<div style="font-size:22px;color:#6E6157">%s</div>'
        '<div style="font-size:52px;font-weight:700;color:%s;margin-top:4px">%s</div>'
        '<div style="font-size:24px;color:#9A8F86;text-decoration:line-through;height:30px">%s</div>'
        '<div style="height:52px;margin-top:8px">%s</div>'
        '<div style="height:430px;display:flex;align-items:flex-end;margin-top:10px">%s</div></div>'
        % ('<span class="pop">MÁS POPULAR</span>' if i == 1 else '', nom, cont, O["ink"], precio, viejo,
           '<span class="tag">%s</span>' % tag if tag else '', pila(i + 1, w)))
page("ordi", "ordi-packs", ORDI_DIR + "galeria-packs-1080.png", 1080, 1080, O["bg"], O["ink"],
     '<div class="c" style="padding:60px 30px 0">'
     '<h1>Elegí tu pack ✨</h1><div class="sub">Cada set trae 3 cajas. Cuantos más llevás, menos pagás por set.</div>'
     '<div class="row" style="gap:6px;margin-top:34px">%s</div>'
     '<div style="width:1000px;height:3px;background:#E2D6C3;margin-top:-2px"></div>'
     '<div style="font-size:23px;font-weight:600;margin-top:26px;color:%s">3 cuotas sin interés · Envío a todo el país · Guía de regalo en 2 y 3 sets</div>'
     '</div>' % ("".join(pack_cols), O["earth"]), ordi_css)

# --- O3 · Beneficios
ICON = {
    "grid": '<path d="M4 4h7v7H4zM13 4h7v7h-7zM4 13h7v7H4zM13 13h7v7h-7z"/>',
    "shield": '<path d="M12 2.5 4 6v6c0 5 3.4 8.6 8 9.5 4.6-.9 8-4.5 8-9.5V6z"/><path d="m8.5 12 2.5 2.5 4.5-5"/>',
    "fold": '<path d="M3 7l9-4 9 4-9 4z"/><path d="M3 12l9 4 9-4"/><path d="M3 17l9 4 9-4"/>',
    "heart": '<path d="M12 20s-7-4.4-7-10a4 4 0 0 1 7-2.6A4 4 0 0 1 19 10c0 5.6-7 10-7 10z"/>',
}
def ben(icon, t, d, align):
    return ('<div style="display:flex;flex-direction:column;align-items:%s;text-align:%s;width:270px">'
            '<div style="width:74px;height:74px;border-radius:20px;background:#fff;display:flex;align-items:center;justify-content:center;box-shadow:0 8px 20px rgba(47,42,38,.08)">'
            '<svg viewBox="0 0 24 24" width="36" height="36" fill="none" stroke="%s" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">%s</svg></div>'
            '<div class="t" style="font-weight:600;font-size:31px;margin-top:18px;line-height:1.15">%s</div>'
            '<div style="font-size:21px;color:#6E6157;margin-top:8px;line-height:1.35">%s</div></div>'
            % (align, "right" if align == "flex-end" else "left", O["ink"], ICON[icon], t, d))
page("ordi", "ordi-beneficios", ORDI_DIR + "galeria-beneficios-1080.png", 1080, 1080, O["bg"], O["ink"],
     '<div class="c" style="padding:80px 40px 0">'
     '<div class="kick">Cajas organizadoras ORDI</div><h1 style="margin-top:12px">¿Por qué ORDI? ✨</h1>'
     '<div style="display:grid;grid-template-columns:270px 380px 270px;gap:24px;align-items:center;margin-top:54px">'
     '<div style="display:flex;flex-direction:column;gap:96px">%s%s</div>'
     '<div style="background:#fff;border-radius:34px;height:640px;display:flex;align-items:center;justify-content:center;box-shadow:0 24px 50px rgba(47,42,38,.10)">%s</div>'
     '<div style="display:flex;flex-direction:column;gap:96px">%s%s</div></div>'
     '<div style="margin-top:58px"><span class="pill">Placard · ropa de cama · juguetes · lavadero · baño</span></div></div>'
     % (ben("grid", "Un lugar para cada cosa", "Encontrás todo de un vistazo", "flex-end"),
        ben("shield", "Firmes de verdad", "Base rígida que no se deforma", "flex-end"),
        caja(330, seed=1),
        ben("fold", "Plegables", "Se guardan planas sin ocupar lugar", "flex-start"),
        ben("heart", "Lindas a la vista", "Lino natural y manijas de cuero", "flex-start")), ordi_css)

# --- O4 · Carrusel "5 errores" (1080x1350)
car_css = ordi_css + """
.slide{width:1080px;height:1350px;padding:90px 80px;display:flex;flex-direction:column}
.num{font-family:'Fraunces',Georgia,serif;font-size:170px;font-weight:600;color:%(accent)s;line-height:.9}
.h{font-family:'Fraunces',Georgia,serif;font-size:70px;font-weight:600;line-height:1.08;margin-top:24px}
.p{font-size:34px;line-height:1.45;color:#5E544C;margin-top:26px}
.tip{margin-top:auto;background:#fff;border-radius:28px;padding:38px 42px;box-shadow:0 16px 40px rgba(47,42,38,.08)}
.tip b{display:block;font-size:22px;letter-spacing:.14em;color:%(sand)s;text-transform:uppercase;margin-bottom:10px}
.tip span{font-size:34px;line-height:1.4}
.foot{display:flex;justify-content:space-between;align-items:center;margin-top:40px;font-size:22px;color:#8C7F72}
""" % O
def barra_80():
    return ('<div style="width:820px;background:#fff;border-radius:28px;padding:40px 44px;box-shadow:0 16px 40px rgba(47,42,38,.08)">'
            '<div style="display:flex;justify-content:space-between;font-size:28px;font-weight:600"><span>Placard</span><span style="color:%s">80%% lleno · 20%% aire</span></div>'
            '<div style="height:44px;border-radius:22px;background:#EFE7DA;margin-top:22px;overflow:hidden"><div style="width:80%%;height:100%%;background:%s;border-radius:22px"></div></div>'
            '<div style="font-size:24px;color:#6E6157;margin-top:18px">Ese 20%% es lo que te deja devolver cada cosa a su lugar.</div></div>' % (O["accent"], O["sand"]))

def domingo():
    return ('<div style="display:flex;gap:30px;align-items:center">'
            '<div style="width:260px;background:#fff;border-radius:28px;overflow:hidden;box-shadow:0 16px 40px rgba(47,42,38,.08);text-align:center">'
            '<div style="background:%s;color:#fff;font-size:28px;font-weight:700;letter-spacing:.12em;padding:16px">DOMINGO</div>'
            '<div class="t" style="font-size:120px;font-weight:600;padding:18px 0 6px">5</div><div style="font-size:30px;color:#6E6157;padding-bottom:26px">minutos</div></div>'
            '<div style="font-size:30px;line-height:1.9;color:#3B342F;text-align:left">✔ Lo que quedó afuera, a su caja<br>✔ Lo que no usás, a donar<br>✔ Listo, una semana más</div></div>' % O["accent"])

ilus_err = [
    '<div class="row" style="gap:40px;align-items:center">'
    '<div class="c">%s<div style="font-size:28px;font-weight:700;color:%s;margin-top:10px">✗ Apilado</div></div>'
    '<div class="c">%s<div style="font-size:28px;font-weight:700;color:#5B7F4E;margin-top:10px">✓ En vertical</div></div></div>' % (pila_caida(300), O["accent"], caja(340, seed=2)),
    '<div class="row" style="gap:18px">%s%s%s</div>' % (etiqueta_caja("Remeras", 270, 0), etiqueta_caja("Jeans", 270, 3), etiqueta_caja("Medias", 270, 5)),
    barra_80(),
    estante_ordenado(860),
    domingo(),
]

errores = [
    ("Apilar en vez de guardar en vertical", "Cuando sacás la remera de abajo, se cae toda la pila. Y en dos días el placard está revuelto otra vez.", "Doblá en rollito o en vertical, como archivos: ves todo y sacás una prenda sin desarmar el resto."),
    ("Mezclar categorías", "Remeras con buzos, medias con pijamas… Si todo va a todos lados, nada tiene su lugar.", "Una categoría por caja. Grande para ropa de cama, mediana para remeras, chica para ropa interior."),
    ("Llenarlo al 100%", "Un placard sin aire se desordena en una semana: no hay dónde devolver las cosas.", "Apuntá al 80%. Lo que está en duda, a una caja aparte con fecha."),
    ("Desaprovechar la altura", "El espacio arriba de las pilas y el estante de arriba de todo quedan vacíos o con cosas sueltas.", "Cajas con manijas arriba, para lo de otra temporada: las bajás en un segundo."),
    ("No tener un momento para mantenerlo", "Ordenar una vez es fácil. Lo difícil es que dure.", "Cinco minutos los domingos: devolvé a su caja lo que quedó afuera. Listo."),
]
slides = []
slides.append(('car-ordi-1', '<div class="slide"><div class="kick">Guardá este post 📌</div>'
               '<div class="h" style="font-size:92px;margin-top:30px">Tu placard no se desordena solo.</div>'
               '<div class="p" style="font-size:40px">Estos <b style="color:%s">5 errores</b> lo desordenan 👉</div>'
               '<div style="margin-top:auto">%s</div>'
               '<div class="foot"><span class="brand">ORDI</span><span>Deslizá →</span></div></div>' % (O["accent"], estante_desordenado(920))))
for i, (t, p, tip) in enumerate(errores):
    slides.append(('car-ordi-%d' % (i + 2),
                   '<div class="slide"><div class="num">0%d</div><div class="h">%s</div><div class="p">%s</div>'
                   '<div class="c" style="margin:auto 0">%s</div>'
                   '<div class="tip" style="margin-top:0"><b>Hacé esto</b><span>%s</span></div>'
                   '<div class="foot"><span class="brand">ORDI</span><span>%d / 7</span></div></div>' % (i + 1, t, p, ilus_err[i], tip, i + 2)))
slides.append(('car-ordi-7', '<div class="slide"><div class="kick">Cada cosa en su lugar</div>'
               '<div class="h" style="font-size:78px">Te armamos una guía paso a paso ✨</div>'
               '<div class="p">"Placard ordenado en 1 tarde" viene de regalo con los packs de 2 y 3 sets de cajas ORDI.</div>'
               '<div style="margin-top:auto">%s</div>'
               '<div class="foot"><span class="brand">ORDI</span><span>Link en la bio</span></div></div>' % estante_ordenado(920)))
for name, html in slides:
    page("ordi", name, ORDI_DIR + "carrusel-5-errores/" + name.replace("car-ordi-", "slide-") + ".png", 1080, 1350, O["bg"], O["ink"], html, car_css)


# =================================================================== VANTA
V = dict(bg="#F4F4F2", ink="#0A0A0A", accent="#E10600", grey="#4A4A4A")
VANTA_DIR = "VANTA-zapatillas/creativos/imagenes/"
vanta_css = """
h1{font-family:'Archivo',sans-serif;font-weight:900;font-size:78px;line-height:1;text-transform:uppercase;letter-spacing:-.02em}
.kick{font-size:20px;letter-spacing:.2em;font-weight:700;color:%(grey)s;text-transform:uppercase}
.sub{font-size:27px;color:#555;margin-top:14px}
.tag{display:inline-block;background:%(accent)s;color:#fff;border-radius:6px;padding:9px 16px;font-family:'Archivo';font-weight:800;font-size:19px;letter-spacing:.04em}
.pop{display:inline-block;background:%(ink)s;color:#fff;border-radius:6px;padding:8px 14px;font-family:'Archivo';font-weight:800;font-size:17px;letter-spacing:.08em}
.bar{display:inline-block;background:%(ink)s;color:#fff;border-radius:999px;padding:16px 34px;font-size:23px;font-weight:600}
""" % V
VANTA_PRECIOS = [("1 par", "$40.000", "", "", ["negro"]),
                 ("2 pares", "$60.000", "$80.000", "25% OFF", ["negro", "blanco"]),
                 ("3 pares", "$95.000", "$120.000", "21% OFF + ENVÍO GRATIS", ["negro", "blanco", "negro"])]
vcols = []
for i, (nom, precio, viejo, tag, colores) in enumerate(VANTA_PRECIOS):
    shoes = "".join('<div style="margin-top:-28px">%s</div>' % zapatilla(270, c) for c in colores)
    vcols.append('<div class="c" style="width:330px">'
                 '<div style="height:40px">%s</div>'
                 '<div style="font-family:Archivo;font-weight:900;font-size:36px;text-transform:uppercase">%s</div>'
                 '<div style="font-family:Archivo;font-weight:900;font-size:54px;margin-top:2px">%s</div>'
                 '<div style="font-size:24px;color:#999;text-decoration:line-through;height:30px">%s</div>'
                 '<div style="height:52px;margin-top:8px">%s</div>'
                 '<div class="c" style="height:470px;justify-content:flex-end;padding-top:30px">%s</div></div>'
                 % ('<span class="pop">MÁS POPULAR</span>' if i == 1 else '', nom, precio, viejo,
                    '<span class="tag">%s</span>' % tag if tag else '', shoes))
page("vanta", "vanta-packs", VANTA_DIR + "galeria-packs-1080.png", 1080, 1080, V["bg"], V["ink"],
     '<div class="c" style="padding:62px 30px 0"><h1>Elegí tu pack</h1>'
     '<div class="sub">Combiná talles y colores · talles 35 al 45</div>'
     '<div class="row" style="gap:8px;margin-top:30px;align-items:flex-start">%s</div>'
     '<div style="margin-top:22px"><span class="bar">3 cuotas sin interés · Cambio de talle gratis</span></div></div>' % "".join(vcols), vanta_css)

TALLES = [(35, "22,5"), (36, "23"), (37, "24"), (38, "24,5"), (39, "25,5"), (40, "26"), (41, "26,5"), (42, "27,5"), (43, "28"), (44, "29"), (45, "29,5")]
tabla = ('<table style="border-collapse:collapse;width:420px;font-size:25px">'
         '<tr><th style="background:#0A0A0A;color:#fff;padding:14px;font-family:Archivo;letter-spacing:.06em;text-align:left">TALLE AR</th>'
         '<th style="background:#0A0A0A;color:#fff;padding:14px;font-family:Archivo;letter-spacing:.06em;text-align:left">LARGO DEL PIE</th></tr>'
         + "".join('<tr style="background:%s"><td style="padding:11px 14px;font-weight:700">%d</td><td style="padding:11px 14px">%s cm</td></tr>' % ("#fff" if k % 2 == 0 else "#EBEBE8", t, cm) for k, (t, cm) in enumerate(TALLES))
         + '</table>')
page("vanta", "vanta-guia-talles", VANTA_DIR + "galeria-guia-de-talles-1080x1350.png", 1080, 1350, V["bg"], V["ink"],
     '<div class="c" style="padding:70px 60px 0"><div class="kick">Guía de talles</div><h1 style="margin-top:12px">¿Qué talle soy?</h1>'
     '<div class="sub">Calzan talle normal. Medilo en 30 segundos:</div>'
     '<div style="display:flex;gap:50px;align-items:center;margin-top:40px">'
     '<div class="c">%s</div><div style="text-align:left">%s'
     '<div style="font-size:22px;color:#555;margin-top:16px;line-height:1.4;width:420px">1. Apoyá el pie sobre una hoja contra la pared.<br>2. Marcá el dedo más largo.<br>3. Medí en cm y buscá tu talle.</div></div></div>'
     '<div style="margin-top:34px"><span class="bar">¿Entre dos talles? Elegí el más grande · Cambio gratis</span></div>'
     '<div style="font-size:16px;color:#999;margin-top:14px">Medidas de referencia</div></div>' % (pie_midiendo(330), tabla), vanta_css)

vslide_css = vanta_css + """
.slide{width:1080px;height:1350px;padding:90px 80px;display:flex;flex-direction:column}
.n{font-family:'Archivo';font-weight:900;font-size:150px;color:%(accent)s;line-height:.9}
.h{font-family:'Archivo';font-weight:900;font-size:76px;line-height:1.02;text-transform:uppercase;letter-spacing:-.02em;margin-top:20px}
.p{font-size:34px;line-height:1.45;color:#444;margin-top:24px}
.foot{display:flex;justify-content:space-between;align-items:center;margin-top:auto;font-size:22px;color:#777}
.logo{font-family:'Archivo';font-weight:900;font-size:32px;letter-spacing:.08em;color:#0A0A0A}
""" % V
vs = [
    ("car-vanta-1", '<div class="slide"><div class="kick">Guardá este post 📌</div><div class="h" style="font-size:104px;margin-top:30px">¿Miedo a errarle al talle?</div>'
     '<div class="p" style="font-size:40px">Medí tu pie en 30 segundos, con una hoja y un lápiz 👉</div>'
     '<div class="c" style="margin-top:auto">%s</div><div class="foot" style="margin-top:40px"><span class="logo">VANTA</span><span>Deslizá →</span></div></div>' % zapatilla(760, "negro")),
    ("car-vanta-2", '<div class="slide"><div class="n">01</div><div class="h">Pie sobre una hoja, contra la pared</div>'
     '<div class="p">Talón apoyado en la pared, de pie y con el peso repartido. Mejor a la tarde: el pie está un poco más hinchado.</div>'
     '<div class="c" style="margin-top:auto">%s</div><div class="foot" style="margin-top:30px"><span class="logo">VANTA</span><span>2 / 6</span></div></div>' % pie_midiendo(420, marca=False, flecha=False)),
    ("car-vanta-3", '<div class="slide"><div class="n">02</div><div class="h">Marcá el dedo más largo</div>'
     '<div class="p">No siempre es el dedo gordo. Hacé una línea recta en la punta del dedo que llegue más lejos.</div>'
     '<div class="c" style="margin-top:auto">%s</div><div class="foot" style="margin-top:30px"><span class="logo">VANTA</span><span>3 / 6</span></div></div>' % pie_midiendo(420, flecha=False)),
    ("car-vanta-4", '<div class="slide"><div class="n">03</div><div class="h">Medí en centímetros</div>'
     '<div class="p">Desde el borde de la hoja hasta la línea. Medí los dos pies y quedate con el más largo.</div>'
     '<div style="margin-top:auto;background:#fff;border-radius:22px;padding:60px;text-align:center;box-shadow:0 16px 40px rgba(0,0,0,.06)">'
     '<div style="font-family:Archivo;font-weight:900;font-size:150px">26 cm</div><div style="font-size:34px;color:#555;margin-top:8px">= talle 40 en la tabla →</div></div>'
     '<div class="foot" style="margin-top:40px"><span class="logo">VANTA</span><span>4 / 6</span></div></div>'),
    ("car-vanta-5", '<div class="slide"><div class="n">04</div><div class="h">Buscá tu talle</div>'
     '<div class="c" style="margin-top:40px">%s</div>'
     '<div class="foot" style="margin-top:40px"><span class="logo">VANTA</span><span>5 / 6</span></div></div>' % tabla.replace("width:420px;font-size:25px", "width:820px;font-size:30px")),
    ("car-vanta-6", '<div class="slide" style="background:#0A0A0A;color:#fff"><div class="kick" style="color:#aaa">Comprá sin miedo</div>'
     '<div class="h" style="font-size:96px;margin-top:30px">¿Igual no te quedó?</div>'
     '<div class="p" style="color:#ddd;font-size:42px">El cambio de talle es <b style="color:#fff">gratis</b>. Nos escribís por WhatsApp y lo coordinamos.</div>'
     '<div class="c" style="margin-top:auto">%s</div><div class="foot" style="margin-top:30px;color:#aaa"><span class="logo" style="color:#fff">VANTA</span><span>Link en la bio</span></div></div>' % zapatilla(760, "blanco")),
]
for name, html in vs:
    page("vanta", name, VANTA_DIR + "carrusel-guia-de-talles/" + name.replace("car-vanta-", "slide-") + ".png", 1080, 1350, V["bg"], V["ink"], html, vslide_css)


# =================================================================== VERDEA · nuevo producto (concepto)
G = dict(bg="#F5F4EE", ink="#2A5F35", sprout="#6BA342", earth="#4E382A", orange="#E88031")
VERDEA_DIR = "VERDEA-huerta/productos-nuevos/imagenes/"
verdea_css = """
h1{font-family:'Poppins',sans-serif;font-weight:800;font-size:68px;line-height:1.06;color:%(earth)s;letter-spacing:-.01em}
.kick{font-family:'Poppins';font-size:20px;letter-spacing:.18em;font-weight:600;color:%(sprout)s;text-transform:uppercase}
.sub{font-size:28px;color:#6E6157;margin-top:12px}
.chip{display:inline-flex;align-items:center;gap:10px;background:#fff;border:1px solid #E5E2D6;border-radius:999px;padding:12px 22px;font-size:22px;font-weight:600;color:%(ink)s}
.pill{display:inline-block;background:%(ink)s;color:#fff;border-radius:999px;padding:16px 34px;font-family:'Poppins';font-size:24px;font-weight:600}
.badge{display:inline-block;background:%(orange)s;color:#fff;border-radius:999px;padding:9px 18px;font-family:'Poppins';font-size:19px;font-weight:700}
.concept{position:absolute;top:34px;right:34px;background:#fff;border:1px dashed #BFD3AE;color:%(ink)s;border-radius:10px;padding:8px 14px;font-size:16px;font-weight:700;letter-spacing:.06em}
""" % G
CHK = '<svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="#6BA342" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"><path d="M20 6 9 17l-5-5"/></svg>'
page("verdea", "verdea-estacion", VERDEA_DIR + "estacion-propagacion-concepto-1080.png", 1080, 1080, G["bg"], G["ink"],
     '<div class="concept">CONCEPTO · PRÓXIMO LANZAMIENTO</div>'
     '<div class="c" style="padding:70px 40px 0"><div class="kick">Para tu rincón verde</div>'
     '<h1 style="margin-top:12px">Estación de Propagación<br>VERDEA 🌱</h1><div class="sub">Mirá crecer tus raíces, a la vista.</div>'
     '<div style="margin-top:26px">%s</div>'
     '<div class="row" style="gap:12px;margin-top:22px"><span class="chip">%s Madera natural</span><span class="chip">%s 3 tubos de vidrio</span><span class="chip">%s Logo grabado</span></div>'
     '</div>' % (estacion(760), CHK, CHK, CHK), verdea_css)

bottle = data_uri("https://cdn.shopify.com/s/files/1/0815/0338/7880/files/verdea_enraizante_1024x1024_eabf64f8-9195-4e1d-b669-630989637b5a.png?v=1791546738", "verdea_bottle.png")
page("verdea", "verdea-kit", VERDEA_DIR + "kit-propagacion-concepto-1080.png", 1080, 1080, G["bg"], G["ink"],
     '<div class="concept">CONCEPTO · PRECIO SUGERIDO</div>'
     '<div class="c" style="padding:62px 40px 0"><div class="kick">Ideal para regalar 🎁</div>'
     '<h1 style="margin-top:12px">Kit Propagación VERDEA</h1><div class="sub">Estación de propagación + Enraizante Root Boost 250 ml</div>'
     '<div class="row" style="gap:20px;margin-top:40px;align-items:center">'
     '<div>%s</div>'
     '<div style="font-family:Poppins;font-size:70px;font-weight:300;color:#B5AB9C">+</div>'
     '<div style="width:300px;height:420px;border-radius:30px;overflow:hidden;border:6px solid #fff;box-shadow:0 20px 44px rgba(78,56,42,.16)">'
     '<img src="%s" style="width:100%%;height:100%%;object-fit:cover;object-position:50%% 40%%"></div></div>'
     '<div class="row" style="gap:18px;margin-top:40px;align-items:center">'
     '<span style="font-family:Poppins;font-size:66px;font-weight:800;color:%s">$79.900</span>'
     '<span style="display:flex;flex-direction:column;align-items:flex-start;gap:6px"><span style="font-size:24px;color:#9A8F86;text-decoration:line-through">Por separado $92.900</span>'
     '<span class="badge">AHORRÁS $13.000</span></span></div>'
     '<div class="row" style="gap:12px;margin-top:30px"><span class="chip">%s Madera natural</span><span class="chip">%s 3 tubos de vidrio</span><span class="chip">%s Enraizante 250 ml</span></div>'
     '<div style="font-size:21px;color:#6E6157;margin-top:20px">3 cuotas sin interés · Envío a todo el país</div></div>'
     % (estacion(520), bottle, G["earth"], CHK, CHK, CHK), verdea_css)

etapas = [("Recién cortado", "Nudo bajo el agua", 0), ("Primeras raíces", "Agua limpia y luz indirecta", 1), ("Listo para maceta", "Raíces de 3 a 5 cm", 2)]
ecols = "".join('<div class="c" style="width:300px">%s<div style="font-family:Poppins;font-weight:700;font-size:32px;color:%s;margin-top:18px">%s</div>'
                '<div style="font-size:22px;color:#6E6157;margin-top:6px">%s</div></div>'
                % (tubo_solo(250, nivel=n, hojas_n=2 + (n == 2)), G["earth"], t, d) for t, d, n in etapas)
arrow = '<svg viewBox="0 0 24 24" width="40" height="40" fill="none" stroke="#BFD3AE" stroke-width="2.4" stroke-linecap="round"><path d="M5 12h14M13 6l6 6-6 6"/></svg>'
page("verdea", "verdea-etapas", VERDEA_DIR + "etapas-propagacion-1080x1350.png", 1080, 1350, G["bg"], G["ink"],
     '<div class="concept">ILUSTRATIVO</div>'
     '<div class="c" style="padding:110px 40px 0"><div class="kick">Propagación en agua</div>'
     '<h1 style="margin-top:14px">Así se ve<br>crecer una raíz 🌱</h1>'
     '<div class="sub">Con la estación, cada etapa queda a la vista.</div>'
     '<div class="row" style="gap:0;margin-top:80px;align-items:center">%s</div>'
     '<div style="margin-top:84px"><span class="pill">Tip: cambiá el agua 1 vez por semana</span></div>'
     '<div style="font-family:Poppins;font-weight:700;font-size:26px;color:%s;margin-top:34px;letter-spacing:.12em">VERDEA · HUERTA DOMÉSTICA</div></div>'
     % (ecols.replace('</div><div class="c" style="width:300px">', '</div>' + arrow + '<div class="c" style="width:300px">'), G["ink"]), verdea_css)

json.dump(JOBS, open(os.path.join(BUILD, "jobs.json"), "w"), indent=1)
print("%d imágenes listas para renderizar" % len(JOBS))
