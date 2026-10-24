"""Genera las historias (1080x1920) de cada destacada de Método 30.

Uso: python3 instagram/build_historias.py  →  escribe instagram/historias/_historias.html
Después: node instagram/render_historias.js  →  un PNG por historia.
"""
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "instagram", "historias")


def img(rel):
    return "file://" + os.path.join(ROOT, rel)


ICON = img("marca/icono-metodo30.png")
TAPA1 = img("ebook/tapas/tapa-consegui-trabajo.png")
TAPA2 = img("ebook/tapas/tapa-secretos-de-reclutador.png")
COMBO = img("landing/producto/producto-1-combo.jpg")
CEL = img("landing/muestras/version-web-celular.jpg")
LINK = "somosmetodo30.myshopify.com"

# Cada historia: (carpeta, archivo, tipo, datos)
H = []


def add(folder, name, kind, **d):
    H.append({"folder": folder, "name": name, "kind": kind, **d})


# ---------- 1. CÓMO FUNCIONA ----------
F = "1-como-funciona"
add(F, "1", "cover", tag="Cómo funciona", title="Así funciona<br><em>Método 30</em>",
    sub="Un plan de 30 días para conseguir trabajo: CV, LinkedIn y entrevistas.",
    pic=f'<div class="tapas"><img src="{TAPA1}"><img src="{TAPA2}"></div>')
add(F, "2", "step", tag="Cómo funciona", n="1", title="Elegís tu opción",
    text="<b>Ebook:</b> el plan completo de 30 días.<br><b>Combo:</b> el plan + <i>Secretos de reclutador</i>, el manual avanzado.",
    pic=f'<img class="sq" src="{COMBO}">')
add(F, "3", "step", tag="Cómo funciona", n="2", title="Pagás y te llega al mail",
    text="Hasta 3 cuotas sin interés. Apenas se acredita el pago recibís un mail con los PDF para descargar.",
    pic='<div class="mail"><div class="mh"><span class="dot"></span><b>Método 30</b><small>ahora</small></div>'
        '<div class="ms">Tus ebooks están listos</div><div class="mf"><span>PDF</span>Consegui-trabajo-en-30-dias.pdf</div>'
        '<div class="mf"><span>PDF</span>Secretos-de-reclutador.pdf</div></div>')
add(F, "4", "step", tag="Cómo funciona", n="3", title="Lo usás desde el celu",
    text="En <b>Mis ebooks</b> tenés la versión web: tildás las tareas de cada día y copiás las plantillas con un toque.",
    pic=f'<img class="phone" src="{CEL}">')
add(F, "5", "link", tag="Cómo funciona", title="Empezá hoy",
    sub="Tu plan de 30 días, en hasta 3 cuotas sin interés.")

# ---------- 2. RESEÑAS ----------
F = "2-resenas"
add(F, "1-pedi-resenas", "ask", tag="Reseñas", title="¿Ya leíste<br><em>Método 30</em>?",
    sub="Contanos cómo te fue con tu búsqueda. Con tu permiso, compartimos tu mensaje acá.",
    cta="Mandanos un mensaje", note="o escribinos a somosmetodo30@gmail.com")
add(F, "2-como-contarnos", "list", tag="Reseñas", title="Contanos<br>tu experiencia",
    items=["Aplicá el plan en tu búsqueda", "Mandanos un mensaje directo contando cómo te fue",
           "Si querés, sumá una captura de tu CV o tu LinkedIn nuevo", "Con tu permiso, lo compartimos en esta destacada"],
    foot="Tu historia puede ayudar a otra persona a animarse.")

# ---------- 3. PAGOS ----------
F = "3-pagos"
add(F, "1", "big", tag="Pagos", big="3", bigsub="cuotas<br>sin interés",
    text="Con todas las tarjetas de crédito, a través de Mercado Pago.")
add(F, "2", "list", tag="Pagos", title="Pagá como quieras",
    items=["Tarjeta de crédito, hasta 3 cuotas sin interés", "Tarjeta de débito",
           "Dinero en cuenta de Mercado Pago", "Pago 100 % seguro: tus datos no pasan por nosotros"])
add(F, "3", "prices", tag="Pagos", title="Elegí tu opción")

# ---------- 4. MIS EBOOKS ----------
F = "4-mis-ebooks"
add(F, "1", "cover", tag="Mis ebooks", title="Cómo entrar a<br><em>Mis ebooks</em>",
    sub="La versión web interactiva de tus ebooks. Sin contraseña: entrás con tu mail en 3 pasos.",
    pic=f'<img class="phone" src="{CEL}">')
add(F, "2", "step", tag="Mis ebooks", n="1", title="Tocá «Iniciar sesión»",
    text="Entrá a la tienda desde el link de nuestro perfil o desde el mail de compra.",
    pic='<div class="ui"><div class="ui-btn">Iniciar sesión</div></div>')
add(F, "3", "step", tag="Mis ebooks", n="2", title="Poné el mismo mail de la compra",
    text="Tiene que ser el mail que usaste para pagar: así se habilitan tus ebooks.",
    pic='<div class="ui"><div class="ui-lbl">Correo electrónico</div><div class="ui-in">tunombre@gmail.com</div><div class="ui-btn">Continuar</div></div>')
add(F, "4", "step", tag="Mis ebooks", n="3", title="Escribí el código de 6 dígitos",
    text="Te llega por mail en segundos. Si no lo ves, revisá la carpeta de spam.",
    pic='<div class="ui"><div class="ui-lbl">Código</div><div class="code">' + "".join(f"<span>{c}</span>" for c in "······") + "</div></div>")
add(F, "5", "step", tag="Mis ebooks", n="✓", title="¡Listo!",
    text="Tildá las tareas de cada día y copiá las plantillas. Tu avance queda guardado.",
    pic=f'<img class="phone" src="{CEL}">')

# ---------- 5. TIPS ----------
F = "5-tips"
add(F, "1-cv", "list", tag="Tip de CV", title="5 errores que dejan<br>tu CV afuera",
    items=["Faltas de ortografía", "Un CV genérico para todo", "Tareas en vez de logros",
           "Diseños recargados que el sistema no lee", "«Busco crecer» en vez de un perfil"],
    foot="Los 12 errores y cómo arreglarlos están en el ebook.")
add(F, "2-linkedin", "formula", tag="Tip de LinkedIn", title="El titular que<br>te hace aparecer",
    formula=["Puesto objetivo", "Especialidad o herramientas", "Resultado o diferencial"],
    example="Analista Contable | Impuestos, cierres mensuales y SAP | Ayudo a pymes a ordenar sus números",
    foot="Nunca pongas «Buscando nuevas oportunidades».")
add(F, "3-entrevista", "star", tag="Tip de entrevista", title="Respondé con<br>el método STAR",
    items=[("S", "Situación", "El contexto en una o dos frases."),
           ("T", "Tarea", "Cuál era tu responsabilidad."),
           ("A", "Acción", "Qué hiciste vos. Decí «yo», no «nosotros»."),
           ("R", "Resultado", "Qué lograste, con números.")],
    foot="Ideal: 1,5 a 2 minutos por respuesta.")
add(F, "4-debilidad", "qa", tag="Tip de entrevista", q="«¿Cuál es tu mayor debilidad?»",
    a="Algo real pero que no sea central para el puesto, y qué estás haciendo para mejorarlo.<br><br>"
      "<span class='no'>Evitá el clásico «soy muy perfeccionista».</span>")

# ---------- 6. PREGUNTAS ----------
F = "6-preguntas"
QA = [
    ("¿Cómo recibo los ebooks?", "Por mail, apenas se acredita el pago: los PDF y el acceso a la versión web interactiva."),
    ("¿Sirve si no tengo experiencia?", "Sí. Hay consejos para el primer empleo y estrategias para mostrar lo que sabés hacer."),
    ("¿Sirve para mi rubro?", "Sí. El método funciona en cualquier rubro e incluye consejos para 10 rubros distintos."),
    ("¿Es un curso con videos?", "No. Son ebooks en PDF con versión web. Los leés a tu ritmo y seguís el plan día por día."),
    ("¿Ebook o combo?", "El ebook tiene el plan completo. El combo suma el manual avanzado, ideal si tu rubro es competido."),
    ("¿Me garantiza conseguir trabajo?", "Nadie puede garantizarlo. Te da un método claro para hacer una búsqueda muy por encima del promedio."),
    ("¿Y si me arrepiento?", "Tenés 10 días para cancelar la compra. Escribinos a somosmetodo30@gmail.com."),
]
for i, (q, a) in enumerate(QA, 1):
    add(F, str(i), "qa", tag="Preguntas", q=q, a=a)
add(F, str(len(QA) + 1), "ask", tag="Preguntas", title="¿Tenés otra<br>pregunta?",
    sub="Mandanos un mensaje y te respondemos en una historia.",
    cta="Mandanos un mensaje", note="o escribinos a somosmetodo30@gmail.com")


# ---------- RENDER ----------
ARROW = '<svg viewBox="0 0 24 24"><path d="M5 12h14M13 6l6 6-6 6" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"/></svg>'
PLANE = '<svg viewBox="0 0 24 24"><path d="M21 3 10 14M21 3l-7 18-4-7-7-4 18-7Z" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linejoin="round"/></svg>'


def cta(label, note, small, icon=ARROW):
    sm = f"<small>{small}</small>" if small else ""
    return f'<div class="cta"><div class="btn"><span>{label}</span>{icon}</div><p>{note}{sm}</p></div>'


def head(h, i, total):
    dots = "".join(f'<i class="{"on" if k == i else ""}"></i>' for k in range(total))
    return (f'<div class="top"><img src="{ICON}"><span>Método 30</span><b>{h["tag"]}</b></div>'
            f'<div class="dots">{dots}</div>')


def body(h):
    k = h["kind"]
    if k == "cover":
        return f'<div class="cover"><h1>{h["title"]}</h1><p class="sub">{h["sub"]}</p><div class="pic">{h["pic"]}</div></div>'
    if k == "step":
        return (f'<div class="step"><div class="num">{h["n"]}</div><h2>{h["title"]}</h2>'
                f'<p>{h["text"]}</p><div class="pic">{h["pic"]}</div></div>')
    if k == "link":
        return (f'<div class="cover center"><img class="tp" src="{COMBO}"><h1>{h["title"]}</h1><p class="sub">{h["sub"]}</p>' +
                cta("Ver los ebooks", "Tocá el link de nuestro perfil", LINK) + "</div>")
    if k == "ask":
        return (f'<div class="cover center"><img class="av" src="{ICON}"><h1>{h["title"]}</h1><p class="sub">{h["sub"]}</p>'
                + cta(h["cta"], h["note"], "", icon=PLANE) + "</div>")
    if k == "big":
        return f'<div class="cover center"><div class="bign">{h["big"]}</div><div class="bigsub">{h["bigsub"]}</div><p class="sub">{h["text"]}</p></div>'
    if k == "list":
        lis = "".join(f'<li><span>{j}</span>{t}</li>' for j, t in enumerate(h["items"], 1))
        foot = f'<p class="foot">{h["foot"]}</p>' if h.get("foot") else ""
        return f'<div class="lst"><h2>{h["title"]}</h2><ul>{lis}</ul>{foot}</div>'
    if k == "prices":
        return (f'<div class="lst"><h2>{h["title"]}</h2>'
                f'<div class="price"><img src="{TAPA1}"><div><small>Ebook</small><b>Conseguí trabajo en 30 días</b><strong>$18.000</strong><em>o 3 cuotas de $6.000</em></div></div>'
                f'<div class="price best"><span class="badge">Más elegido</span><div class="two"><img src="{TAPA1}"><img src="{TAPA2}"></div><div><small>Combo 2 ebooks</small><b>+ Secretos de reclutador</b><strong>$27.000 <s>$33.000</s></strong><em>o 3 cuotas de $9.000</em></div></div>'
                f'<p class="foot">Link en el perfil</p></div>')
    if k == "formula":
        f_ = '<span class="plus">|</span>'.join(f"<div>{x}</div>" for x in h["formula"])
        return (f'<div class="lst"><h2>{h["title"]}</h2><div class="formula">{f_}</div>'
                f'<div class="ex"><small>Ejemplo</small>{h["example"]}</div><p class="foot no">{h["foot"]}</p></div>')
    if k == "star":
        lis = "".join(f'<li><span class="l">{l}</span><div><b>{t}</b>{d}</div></li>' for l, t, d in h["items"])
        return f'<div class="lst"><h2>{h["title"]}</h2><ul class="st">{lis}</ul><p class="foot">{h["foot"]}</p></div>'
    if k == "qa":
        return f'<div class="qa"><div class="bubble">{h["q"]}</div><p>{h["a"]}</p></div>'
    raise ValueError(k)


THEME = {"cover": "dark", "link": "dark", "ask": "dark", "big": "dark",
         "step": "light", "list": "light", "prices": "light", "formula": "light", "star": "light", "qa": "dark"}

CSS = """
*{box-sizing:border-box;margin:0;padding:0}
body{background:#222}
.s{width:1080px;height:1920px;position:relative;overflow:hidden;font-family:Inter,sans-serif;padding:250px 90px 260px;display:flex;flex-direction:column}
.dark{background:radial-gradient(circle at 85% 0%,#3B3F9A 0%,#14213D 45%,#0B1226 100%);color:#fff}
.light{background:#F6F7FB;color:#14213D}
.top{display:flex;align-items:center;gap:16px;font-weight:800;font-size:32px}
.top img{width:64px;height:64px;border-radius:16px}
.top b{margin-left:auto;font-size:24px;letter-spacing:.12em;text-transform:uppercase;color:#E8632E;border:3px solid #E8632E;border-radius:99px;padding:8px 22px}
.dots{display:flex;gap:10px;margin:34px 0 60px}
.dots i{height:8px;flex:1;border-radius:9px;background:currentColor;opacity:.18}.dots i.on{background:#E8632E;opacity:1}
h1,h2,.bign{font-family:"Inter Display",Inter,sans-serif;letter-spacing:-.03em}
h1{font-size:116px;font-weight:900;line-height:.98}
h1 em,h2 em{font-style:normal;color:#E8632E}
.dark h1 em{color:#F5D27A}
h2{font-size:84px;font-weight:900;line-height:1.02;margin-bottom:34px}
.sub{font-size:44px;line-height:1.35;margin-top:36px;opacity:.88}
.cover{flex:1;display:flex;flex-direction:column}
.cover .pic{flex:1;display:flex;align-items:center;justify-content:center;margin-top:50px}
.center{align-items:center;text-align:center;justify-content:center}
.tapas{position:relative;width:820px;height:640px}
.tapas img{position:absolute;width:420px;border-radius:10px;box-shadow:0 30px 70px rgba(0,0,0,.5)}
.tapas img:first-child{left:40px;top:20px;transform:rotate(-6deg);z-index:2}
.tapas img:last-child{right:40px;top:40px;transform:rotate(6deg)}
.phone{height:900px;border-radius:52px;border:14px solid #0E0C09;box-shadow:0 40px 80px rgba(0,0,0,.4)}
.step .phone{height:780px}
.sq{width:820px;border-radius:36px;box-shadow:0 30px 60px rgba(20,33,61,.18)}
.step{flex:1;display:flex;flex-direction:column}
.step .num{width:130px;height:130px;border-radius:50%;background:#E8632E;color:#fff;font:900 76px/130px "Inter Display";text-align:center;margin-bottom:40px}
.step p{font-size:44px;line-height:1.4;color:#334155}
.step .pic{flex:1;display:flex;align-items:center;justify-content:center;margin-top:40px}
.mail{width:860px;background:#fff;border-radius:36px;padding:44px;box-shadow:0 30px 60px rgba(20,33,61,.15);font-size:34px}
.mh{display:flex;align-items:center;gap:16px}.mh .dot{width:56px;height:56px;border-radius:14px;background:#14213D url(ICON) center/cover}
.mh small{margin-left:auto;color:#94A3B8}
.ms{font-weight:800;font-size:42px;margin:28px 0}
.mf{display:flex;align-items:center;gap:20px;border:2px solid #E2E8F0;border-radius:20px;padding:22px;margin-top:16px;font-size:30px}
.mf span{background:#E8632E;color:#fff;font-weight:800;font-size:24px;border-radius:10px;padding:8px 12px}
.ui{width:820px;background:#fff;border-radius:36px;padding:56px;box-shadow:0 30px 60px rgba(20,33,61,.15)}
.ui-lbl{font-size:30px;color:#64748B;margin-bottom:14px}
.ui-in{border:3px solid #14213D;border-radius:18px;padding:28px;font-size:38px;color:#94A3B8;margin-bottom:30px}
.ui-btn{background:#14213D;color:#fff;border-radius:18px;padding:32px;text-align:center;font-weight:800;font-size:40px;outline:6px solid rgba(232,99,46,.5);outline-offset:6px}
.code{display:flex;gap:14px}.code span{flex:1;height:130px;border:3px solid #14213D;border-radius:18px;font:900 70px/120px Inter;text-align:center;color:#E8632E}
.cta{margin-top:80px;width:100%;display:flex;flex-direction:column;align-items:center}
.btn{display:flex;align-items:center;justify-content:center;gap:24px;width:100%;background:#E8632E;color:#fff;border-radius:999px;padding:44px 50px;font:800 50px/1 Inter;box-shadow:0 24px 50px rgba(232,99,46,.38)}
.btn svg{width:56px;height:56px;flex:none}
.cta p{margin-top:36px;font-size:36px;opacity:.8;line-height:1.4}
.cta small{display:block;font-size:32px;color:#F5D27A;font-weight:600;margin-top:6px;opacity:1}
.av{width:180px;height:180px;border-radius:44px;margin-bottom:60px;box-shadow:0 0 0 8px rgba(245,210,122,.6),0 30px 60px rgba(0,0,0,.4)}
.tp{width:520px;border-radius:30px;margin-bottom:60px;box-shadow:0 30px 70px rgba(0,0,0,.45)}
.bign{font-size:520px;font-weight:900;line-height:.8;color:#F5D27A}
.bigsub{font:900 110px/1 "Inter Display";margin-top:20px}
.lst{flex:1;display:flex;flex-direction:column}
.lst ul{list-style:none;display:flex;flex-direction:column;gap:26px}
.lst li{display:flex;align-items:center;gap:30px;background:#fff;border-radius:28px;padding:36px;font-size:42px;font-weight:600;line-height:1.25;box-shadow:0 12px 30px rgba(20,33,61,.08)}
.lst li span{flex:none;width:76px;height:76px;border-radius:50%;background:#14213D;color:#F5D27A;font:900 40px/76px Inter;text-align:center}
.foot{margin-top:auto;font-size:38px;font-weight:700;color:#E8632E;text-align:center}
.foot.no{color:#B42318}
.st li{align-items:flex-start}.st li div{font-weight:500;color:#334155}.st li b{display:block;font-size:46px;color:#14213D;margin-bottom:6px}
.st .l{background:#E8632E!important;color:#fff!important}
.formula{display:flex;flex-direction:column;gap:14px;align-items:stretch}
.formula div{background:#14213D;color:#fff;border-radius:24px;padding:34px;font-size:44px;font-weight:800;text-align:center}
.formula .plus{text-align:center;font:900 50px/1 Inter;color:#E8632E}
.ex{margin-top:50px;background:#fff;border-left:12px solid #E8632E;border-radius:20px;padding:40px;font-size:40px;line-height:1.4;font-weight:600}
.ex small{display:block;font-size:26px;letter-spacing:.14em;text-transform:uppercase;color:#E8632E;margin-bottom:12px}
.price{position:relative;display:flex;gap:40px;align-items:center;background:#fff;border-radius:36px;padding:44px;margin-bottom:40px;box-shadow:0 14px 34px rgba(20,33,61,.1)}
.price img{width:190px;border-radius:8px;box-shadow:0 10px 24px rgba(0,0,0,.25)}
.price .two{position:relative;width:250px;height:290px;flex:none}.price .two img{position:absolute;width:170px}.price .two img:first-child{left:0;top:0;z-index:2}.price .two img:last-child{right:0;top:30px}
.price small{display:block;font-size:28px;letter-spacing:.12em;text-transform:uppercase;color:#64748B}
.price b{display:block;font-size:40px;margin:8px 0 18px;line-height:1.2}
.price strong{display:block;font:900 76px/1 "Inter Display";color:#14213D}
.price s{font-size:40px;color:#94A3B8;font-weight:600}
.price em{display:block;font-style:normal;font-size:32px;color:#E8632E;font-weight:700;margin-top:10px}
.price.best{border:5px solid #E8632E}
.badge{position:absolute;top:-28px;right:40px;background:#E8632E;color:#fff;font-weight:800;font-size:28px;border-radius:99px;padding:12px 28px}
.qa{flex:1;display:flex;flex-direction:column;justify-content:center}
.bubble{background:#F6F1E4;color:#14213D;border-radius:44px;padding:60px 56px;font:900 70px/1.12 "Inter Display";letter-spacing:-.02em;box-shadow:0 0 0 8px #F5D27A}
.qa p{font-size:52px;line-height:1.38;margin-top:80px}
.qa .no{color:#F5D27A;font-weight:700}
"""


def build():
    os.makedirs(OUT, exist_ok=True)
    folders = {}
    for h in H:
        folders.setdefault(h["folder"], []).append(h)
    slides = []
    for f, items in folders.items():
        for i, h in enumerate(items):
            sid = f'{f}--{h["name"]}'
            slides.append(sid)
            h["html"] = (f'<div class="s {THEME[h["kind"]]}" id="{sid}">'
                         + head(h, i, len(items)) + body(h) + "</div>")
    html = ("<!doctype html><meta charset='utf-8'><style>" + CSS.replace("url(ICON)", f"url({ICON})")
            + "</style><body>" + "".join(h["html"] for h in H) + "</body>")
    open(os.path.join(OUT, "_historias.html"), "w").write(html)
    open(os.path.join(OUT, "_ids.json"), "w").write(json.dumps(slides))
    print(len(slides), "historias")


if __name__ == "__main__":
    build()
