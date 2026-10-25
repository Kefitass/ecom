"""Historias de venta para una semana (1080x1920), con el código de descuento para las primeras 3 compras.

Uso: python3 instagram/build_semana.py && node instagram/render_historias.js semana
Escribe instagram/semana/<día>/<n>.png
"""
import json
import os

import build_historias as bh

OUT = os.path.join(bh.ROOT, "instagram", "semana")

CODIGO = "METODO30"
DESC = 30
PRECIOS = {"Ebook": 18000, "Combo": 27000}


def pesos(n):
    return "$" + f"{n:,.0f}".replace(",", ".")


def off(n):
    return round(n * (100 - DESC) / 100)


H = []


def add(folder, name, kind, **d):
    H.append({"folder": folder, "name": name, "kind": kind, **d})


CTA_CODIGO = dict(kind="cta_code")
CTA_SIN = dict(kind="cta_plain")

# ---------- Lunes · lanzamiento de la oferta ----------
F = "1-lunes"
add(F, "1", "offer_big", tag="Solo 3 lugares")
add(F, "2", "offer_prices", tag="Solo 3 lugares")
add(F, "3", **CTA_CODIGO, tag="Cómo usarlo")

# ---------- Martes · el problema ----------
F = "2-martes"
add(F, "1", "cover", tag="¿Te pasa?", title="Mandás CVs<br>y nadie te<br><em>responde</em>",
    sub="No es falta de talento. Es falta de método.",
    pic='<div class="chatx"><div class="b">Hola, me postulé al puesto de…</div><div class="seen">Visto ✓✓</div></div>')
add(F, "2", "list", tag="Método 30", title="En 30 días<br>dejás de buscar<br>a ciegas",
    items=["Un CV que pasa los filtros automáticos", "Un LinkedIn que hace que te encuentren",
           "Mensajes para llegar a quien decide", "Respuestas para cada entrevista"],
    foot="Un plan día por día, desde el celular.")
add(F, "3", **CTA_CODIGO, tag="30% OFF")

# ---------- Miércoles · reseñas reales ----------
F = "3-miercoles"
add(F, "1", "review", tag="Reseñas", stars=5, titulo="Revelador para pasar los filtros de RR. HH.",
    texto="El manual 'Secretos de Reclutador' te abre los ojos por completo. Entender cómo funcionan los ATS y cómo piensa el evaluador me dio una ventaja enorme.",
    nombre="Camila R.")
add(F, "2", "review", tag="Reseñas", stars=5, titulo="Práctico, directo y sin relleno",
    texto="Lo que más me gustó es que no es teoría vacía; son checklists, plantillas de mensajes para copiar y un tracker diario.",
    nombre="Sofía L.")
add(F, "3", **CTA_CODIGO, tag="30% OFF")

# ---------- Jueves · qué incluye ----------
F = "4-jueves"
add(F, "1", "cover", tag="Qué incluye", title="Todo lo que<br>necesitás para<br><em>conseguir trabajo</em>",
    sub="Dos ebooks en PDF y la versión web para usar desde el celular.",
    pic=f'<div class="tapas"><img src="{bh.TAPA1}"><img src="{bh.TAPA2}"></div>')
add(F, "2", "list", tag="Qué incluye", title="Adentro<br>vas a encontrar",
    items=["Plan de 30 días con tareas para tildar", "8 plantillas de mensajes listas para copiar",
           "Las 15 preguntas de entrevista resueltas", "Cómo negociar tu sueldo"],
    foot="Te llega al mail apenas pagás.")
add(F, "3", **CTA_CODIGO, tag="30% OFF")

# ---------- Viernes · sin riesgo ----------
F = "5-viernes"
add(F, "1", "big", tag="Sin riesgo", big="10", bigsub="días para<br>arrepentirte",
    text="Si no es para vos, escribinos dentro de los 10 días y te devolvemos el dinero.")
add(F, "2", "big", tag="Sin riesgo", big="3", bigsub="cuotas<br>sin interés",
    text="Con todas las tarjetas de crédito, a través de Mercado Pago.")
add(F, "3", **CTA_CODIGO, tag="30% OFF")

# ---------- Sábado · entrevistas ----------
F = "6-sabado"
add(F, "1", "review", tag="Reseñas", stars=5, titulo="Dejé de sufrir las entrevistas",
    texto="me daba pánico que me pregunten 'hablame de vos' o 'cuales son tus debilidades'. practiqué las respuestas del ebook frente al espejo y fui mil veces mas tranquila.",
    nombre="Valen D.")
add(F, "2", "qa", tag="Entrevistas", q="«¿Cuál es tu mayor debilidad?»",
    a="Algo real que no sea central para el puesto, y qué estás haciendo para mejorarlo.<br><br>"
      "<span class='no'>Esta y otras 14 preguntas, resueltas en Método 30.</span>")
add(F, "3", **CTA_CODIGO, tag="30% OFF")

# ---------- Domingo · empezá el lunes ----------
F = "7-domingo"
add(F, "1", "cover", tag="Mañana es lunes", title="Mañana<br>arrancás<br>el <em>día 1</em>",
    sub="Treinta días con un plan claro: qué hacer cada día para dejar de mandar CVs al vacío.",
    pic=f'<img class="phone" src="{bh.CEL}">')
add(F, "2", **CTA_CODIGO, tag="Última chance")

# ---------- Cierre sin código (usar cuando se agote) ----------
add("cierre-sin-codigo", "1", **CTA_SIN, tag="Método 30")


# ---------- RENDER ----------
STAR = "★"


def body(h):
    k = h["kind"]
    if k == "offer_big":
        return ('<div class="cover center"><div class="pct">' + str(DESC) + '<span>%</span></div><div class="pctoff">OFF</div>'
                '<h1 class="oh">Para las primeras<br><em>3 compras</em></h1>'
                '<p class="sub">Solo 3 personas. Cuando se usa la tercera, se termina.</p></div>')
    if k == "offer_prices":
        e, c = PRECIOS["Ebook"], PRECIOS["Combo"]
        return ('<div class="lst"><h2>Con el código<br>te queda así</h2>'
                f'<div class="oprice"><img src="{bh.TAPA1}"><div><small>Ebook</small><s>{pesos(e)}</s><b>{pesos(off(e))}</b>'
                f'<em>o 3 cuotas de {pesos(off(e) / 3)}</em></div></div>'
                f'<div class="oprice best"><div class="two"><img src="{bh.TAPA1}"><img src="{bh.TAPA2}"></div><div><small>Combo 2 ebooks</small><s>{pesos(c)}</s><b>{pesos(off(c))}</b>'
                f'<em>o 3 cuotas de {pesos(off(c) / 3)}</em></div></div>'
                '<p class="foot">Solo para las primeras 3 compras</p></div>')
    if k == "cta_code":
        return ('<div class="cover center"><div class="kick2">' + str(DESC) + '% OFF · primeras 3 compras</div>'
                '<h1 class="oh">Usá el código</h1>'
                f'<div class="coupon"><small>Código</small>{CODIGO}</div>'
                '<ol class="how"><li>Entrá al link de nuestro perfil</li><li>Elegí Ebook o Combo</li>'
                f'<li>En el pago, escribí <b>{CODIGO}</b></li></ol>'
                '<p class="sub small">Se termina cuando lo usen 3 personas.</p></div>')
    if k == "cta_plain":
        return ('<div class="cover center"><img class="tp" src="' + bh.COMBO + '"><h1>Empezá hoy<br>el <em>día 1</em></h1>'
                '<p class="sub">Ebook $18.000 · Combo $27.000<br>Hasta 3 cuotas sin interés</p>'
                f'<div class="cta"><i></i><b>Link en nuestro perfil</b><p><small>{bh.LINK}</small></p></div></div>')
    if k == "review":
        st = STAR * h["stars"] + '<span class="off">' + STAR * (5 - h["stars"]) + "</span>"
        return (f'<div class="qa"><div class="rcard"><div class="rst">{st}</div><h3>{h["titulo"]}</h3>'
                f'<p>“{h["texto"]}”</p><div class="rwho"><i>{h["nombre"][0]}</i>{h["nombre"]}</div></div>'
                '<p class="rnote">Opinión real de una lectora</p></div>')
    return bh.body(h)


THEME = dict(bh.THEME, offer_big="orange", offer_prices="light", cta_code="dark", cta_plain="dark", review="dark")

CSS = bh.CSS + """
.orange{background:radial-gradient(circle at 80% 10%,#F08A5D 0%,#E8632E 45%,#C94E1E 100%);color:#fff}
.orange .top b{color:#fff;border-color:#fff}
.orange .dots i.on{background:#14213D}
.pct{font:900 520px/.8 "Inter Display";letter-spacing:-.06em;color:#fff}
.pct span{font-size:260px}
.pctoff{font:900 150px/1 "Inter Display";color:#14213D;margin-top:-10px;letter-spacing:.05em}
.oh{font-size:104px;margin-top:60px}
.orange .oh em{color:#14213D}
.kick2{font-size:34px;font-weight:800;letter-spacing:.12em;text-transform:uppercase;color:#F5D27A;margin-bottom:40px}
.coupon{margin:60px 0 10px;border-radius:28px;padding:44px 80px;font:900 120px/1 "Inter Display";letter-spacing:.06em;color:#14213D;background:linear-gradient(135deg,#F5D27A,#E0B04F);border-radius:10px;-webkit-mask:radial-gradient(circle 34px at 0 50%,#0000 98%,#000) left/51% 100% no-repeat,radial-gradient(circle 34px at 100% 50%,#0000 98%,#000) right/51% 100% no-repeat;position:relative}
.coupon::after{content:"";position:absolute;left:70px;right:70px;bottom:18px;border-bottom:3px dashed rgba(20,33,61,.25)}
.coupon small{display:block;font:800 30px/1 Inter;letter-spacing:.2em;text-transform:uppercase;color:#7A5A12;margin-bottom:20px}
.how{list-style:none;counter-reset:n;text-align:left;margin-top:60px;display:flex;flex-direction:column;gap:26px;font-size:44px;font-weight:600}
.how li{counter-increment:n;display:flex;align-items:center;gap:26px}
.how li::before{content:counter(n);flex:none;width:76px;height:76px;border-radius:50%;background:#E8632E;color:#fff;font:900 40px/76px Inter;text-align:center}
.how b{color:#F5D27A}
.sub.small{font-size:34px;margin-top:60px}
.oprice{position:relative;display:flex;gap:40px;align-items:center;background:#fff;border-radius:36px;padding:44px;margin-bottom:40px;box-shadow:0 14px 34px rgba(20,33,61,.1)}
.oprice img{width:190px;border-radius:8px;box-shadow:0 10px 24px rgba(0,0,0,.25)}
.oprice .two{position:relative;width:250px;height:290px;flex:none}.oprice .two img{position:absolute;width:170px}.oprice .two img:first-child{left:0;top:0;z-index:2}.oprice .two img:last-child{right:0;top:30px}
.oprice small{display:block;font-size:30px;letter-spacing:.12em;text-transform:uppercase;color:#64748B;font-weight:800}
.oprice s{display:block;font-size:40px;color:#94A3B8;margin-top:10px}
.oprice b{display:block;font:900 96px/1 "Inter Display";color:#E8632E;margin:6px 0}
.oprice em{font-style:normal;font-size:32px;font-weight:700;color:#14213D}
.oprice.best{box-shadow:0 0 0 8px #E8632E}
.rcard{background:#fff;color:#14213D;border-radius:44px;padding:64px 56px;box-shadow:0 0 0 8px #F5D27A}
.rst{color:#E8A317;font-size:60px;letter-spacing:8px}.rst .off{color:#D5DAE3}
.rcard h3{font:900 64px/1.1 "Inter Display";letter-spacing:-.02em;margin:24px 0}
.rcard p{font-size:44px;line-height:1.45;color:#334155}
.rwho{display:flex;align-items:center;gap:24px;margin-top:44px;font-size:40px;font-weight:800}
.rwho i{width:90px;height:90px;border-radius:50%;background:#14213D;color:#fff;font:900 40px/90px Inter;text-align:center;font-style:normal}
.rnote{text-align:center;font-size:32px;opacity:.7;margin-top:44px}
.chatx{width:840px;display:flex;flex-direction:column;align-items:flex-end;gap:18px}
.chatx .b{background:#fff;color:#14213D;border-radius:36px 36px 8px 36px;padding:36px 44px;font-size:44px;font-weight:600}
.chatx .seen{font-size:34px;color:#93C5FD;font-weight:700}
"""


def build():
    os.makedirs(OUT, exist_ok=True)
    folders = {}
    for h in H:
        folders.setdefault(h["folder"], []).append(h)
    ids, html = [], []
    for f, items in folders.items():
        for i, h in enumerate(items):
            sid = f'{f}--{h["name"]}'
            ids.append(sid)
            html.append(f'<div class="s {THEME[h["kind"]]}" id="{sid}">' + bh.head(h, i, len(items)) + body(h) + "</div>")
    open(os.path.join(OUT, "_historias.html"), "w").write(
        "<!doctype html><meta charset='utf-8'><style>" + CSS.replace("url(ICON)", f"url({bh.ICON})") + "</style><body>" + "".join(html) + "</body>")
    open(os.path.join(OUT, "_ids.json"), "w").write(json.dumps(ids))
    print(len(ids), "historias")


if __name__ == "__main__":
    build()
