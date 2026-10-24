"""Carruseles de Método 30 (1080x1350, 4:5).

Uso: python3 instagram/build_carruseles.py && node instagram/render_historias.js carruseles
Escribe instagram/carruseles/<carrusel>/<n>.png
"""
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "instagram", "carruseles")


def img(rel):
    return "file://" + os.path.join(ROOT, rel)


ICON = img("marca/icono-metodo30.png")
TAPA1 = img("ebook/tapas/tapa-consegui-trabajo.png")
TAPA2 = img("ebook/tapas/tapa-secretos-de-reclutador.png")

C = {}  # carrusel -> lista de placas


def add(car, kind, **d):
    C.setdefault(car, []).append({"kind": kind, **d})


# ---------- 1. Errores del CV ----------
K = "1-errores-cv"
add(K, "cover", kicker="CV", title="¿Mandás CV y<br>nadie te <em>llama</em>?",
    sub="5 errores que te dejan afuera (y cómo arreglarlos hoy)")
for n, (err, fix) in enumerate([
    ("Un CV genérico para todo", "Adaptalo a cada aviso: usá las mismas palabras clave que aparecen en la publicación."),
    ("Tareas en vez de logros", "Cambiá «Atención al cliente» por «Resolví 45 consultas diarias con 96 % de satisfacción»."),
    ("Diseños recargados", "Los filtros automáticos leen texto. Una columna, sin tablas ni íconos con información."),
    ("«Busco crecer en una empresa…»", "Eso habla de vos. Un perfil de 3 líneas tiene que decir qué le resolvés a la empresa."),
    ("No poner el link de LinkedIn", "Es lo primero que van a buscar. Personalizá la URL y sumala al encabezado."),
], 1):
    add(K, "error", n=n, err=err, fix=fix)
add(K, "close", title="Son 12 los errores<br>que te dejan <em>afuera</em>",
    sub="En «Conseguí trabajo en 30 días» están todos, con la plantilla de CV y el paso a paso para corregirlo en una tarde.")

# ---------- 2. De tarea a logro ----------
K = "2-tarea-a-logro"
add(K, "cover", kicker="CV", title="Tu CV dice lo que<br>hacías. Tiene que<br>decir lo que <em>lograste</em>",
    sub="Antes y después de 4 viñetas reales")
add(K, "formula", title="La fórmula", parts=["Verbo de acción", "Qué hiciste", "Resultado medible"],
    note="Borrá «responsable de», «encargado de» y «tareas de»: describen obligaciones, no resultados.")
for antes, despues in [
    ("Atención al cliente", "Resolví un promedio de 45 consultas diarias con 96 % de satisfacción, el puntaje más alto del equipo."),
    ("Encargado de redes sociales", "Aumenté los seguidores de Instagram de 2.000 a 11.500 en 8 meses y generé el 30 % de las ventas online."),
    ("Tareas administrativas", "Reorganicé el archivo de facturación y reduje de 3 días a 1 el cierre mensual."),
    ("Ventas", "Superé la cuota anual en un 22 % y abrí 14 cuentas nuevas en la zona norte."),
]:
    add(K, "beforeafter", antes=antes, despues=despues)
add(K, "words", title="Verbos que <em>suman</em>",
    words=["Lideré", "Implementé", "Aumenté", "Reduje", "Optimicé", "Negocié", "Lancé", "Automaticé",
           "Coordiné", "Diseñé", "Generé", "Ahorré", "Resolví", "Conseguí"])
add(K, "close", title="Guardalo para cuando<br>actualices tu <em>CV</em>",
    sub="El paso a paso completo, con más ejemplos por rubro, está en «Conseguí trabajo en 30 días».")

# ---------- 3. Titular de LinkedIn ----------
K = "3-titular-linkedin"
add(K, "cover", kicker="LinkedIn", title="El titular que hace<br>que los reclutadores<br>te <em>encuentren</em>",
    sub="Es lo que más pesa en las búsquedas de LinkedIn")
add(K, "bad", title="Esto no te hace aparecer",
    items=["Buscando nuevas oportunidades", "Estudiante", "Persona proactiva con ganas de aprender"],
    note="Nadie busca esas palabras. Los reclutadores buscan puestos y herramientas.")
add(K, "formula", title="La fórmula", parts=["Puesto objetivo", "Especialidad o herramientas", "Resultado o diferencial"],
    note="Tenés 220 caracteres. Usalos.")
for ex in [
    "Analista Contable | Impuestos, cierres mensuales y SAP | Ayudo a pymes a ordenar sus números",
    "Ejecutivo Comercial B2B | SaaS y tecnología | +120 % de cumplimiento de cuota en 2025",
    "Diseñadora UX/UI | Figma, research y apps móviles | Productos simples que la gente usa",
]:
    add(K, "example", label="Ejemplo", text=ex)
add(K, "close", title="Cambialo hoy:<br>tarda <em>5 minutos</em>",
    sub="Foto, banner, «Acerca de» y cómo activar tu red: está todo en los días 9 a 12 del plan.")

# ---------- 4. Preguntas de entrevista ----------
K = "4-preguntas-entrevista"
add(K, "cover", kicker="Entrevistas", title="3 preguntas que te<br>van a hacer <em>seguro</em>",
    sub="Y cómo responderlas sin improvisar")
add(K, "qa", n=1, q="«Contame sobre vos»",
    a="No es tu biografía. Usá <b>presente, pasado y futuro</b> en 60 a 90 segundos: qué hacés hoy y tu fuerte, uno o dos logros que te trajeron hasta acá, y por qué este puesto es el paso lógico.")
add(K, "qa", n=2, q="«¿Por qué deberíamos contratarte?»",
    a="Resumí en <b>tres puntos</b> los requisitos del aviso que cumplís, con una prueba concreta de cada uno.")
add(K, "qa", n=3, q="«¿Cuál es tu mayor debilidad?»",
    a="Algo real pero que no sea central para el puesto, y <b>qué estás haciendo para mejorarlo</b>. Evitá el clásico «soy muy perfeccionista».")
add(K, "star", title="Para el resto: <em>STAR</em>",
    items=[("S", "Situación", "El contexto en una o dos frases."), ("T", "Tarea", "Cuál era tu responsabilidad."),
           ("A", "Acción", "Qué hiciste vos. Decí «yo», no «nosotros»."), ("R", "Resultado", "Qué lograste, con números.")])
add(K, "close", title="Son 15 las preguntas<br>que casi seguro<br>te van a <em>hacer</em>",
    sub="Las 15, con cómo responder cada una, están en «Conseguí trabajo en 30 días».")

# ---------- 5. Qué es Método 30 ----------
K = "5-que-es-metodo30"
add(K, "cover", kicker="Método 30", title="Buscar trabajo<br>es un trabajo.<br>Hacelo con <em>método</em>",
    sub="Qué es Método 30 y para quién es", pic=True)
add(K, "bad", title="Por qué la mayoría<br>no consigue",
    items=["Manda el mismo CV genérico a todo", "Espera que la llamen en vez de ir a buscar a quien decide",
           "Llega a la entrevista improvisando"],
    note="Método 30 ataca las tres, día por día.")
add(K, "plan", title="El plan en 30 días",
    items=[("1–3", "Objetivo y propuesta de valor"), ("4–8", "Un CV que pasa filtros"), ("9–12", "LinkedIn que atrae reclutadores"),
           ("13–17", "Búsqueda y networking"), ("18–24", "Entrevistas que terminan en oferta"), ("25–28", "Negociación de sueldo"),
           ("29–30", "Cierre y plan B")])
add(K, "list", title="Qué incluye",
    items=["Plan día por día con tareas para tildar", "Plantillas de CV, mensajes y seguimientos",
           "Respuestas para las 15 preguntas de entrevista", "Versión web para usar desde el celular"])
add(K, "close", title="Elegí tu opción", prices=True,
    sub="Hasta 3 cuotas sin interés<br><b class='gold'>Link en nuestro perfil</b>")


# ---------- RENDER ----------
def body(p):
    k = p["kind"]
    if k == "cover":
        pic = (f'<div class="covpic"><img src="{TAPA1}"><img src="{TAPA2}"></div>' if p.get("pic") else "")
        return (f'<div class="kick">{p["kicker"]}</div><h1>{p["title"]}</h1><p class="sub">{p["sub"]}</p>{pic}'
                '<div class="swipe">Deslizá <span>→</span></div>')
    if k == "error":
        return (f'<div class="mid"><div class="big">{p["n"]}</div><div class="err"><small>Error</small>{p["err"]}</div>'
                f'<div class="fix"><small>Cómo arreglarlo</small>{p["fix"]}</div></div>')
    if k == "formula":
        parts = "".join(f"<div class='part'><span>{j}</span>{x}</div>" for j, x in enumerate(p["parts"], 1))
        return f'<h2>{p["title"]}</h2><div class="formula">{parts}</div><p class="note">{p["note"]}</p>'
    if k == "beforeafter":
        return (f'<div class="ba"><div class="antes"><small>Antes</small>{p["antes"]}</div>'
                f'<div class="arrow">↓</div><div class="despues"><small>Después</small>{p["despues"]}</div></div>')
    if k == "words":
        w = "".join(f"<div>{x}</div>" for x in p["words"])
        return f'<h2>{p["title"]}</h2><div class="words">{w}</div>'
    if k == "bad":
        li = "".join(f"<li><i>✕</i>{x}</li>" for x in p["items"])
        return f'<h2>{p["title"]}</h2><ul class="bad">{li}</ul><p class="note strong">{p["note"]}</p>'
    if k == "example":
        parts = p["text"].split(" | ")
        lines = "".join(f"<div class='ln'>{x}</div>" for x in parts)
        return (f'<div class="exwrap"><div class="li-card"><div class="li-top"><div class="li-av"></div><div class="li-name">Tu nombre</div></div>'
                f'<div class="li-head">{p["text"]}</div></div><div class="ex-parts">{lines}</div></div>')
    if k == "qa":
        return f'<div class="qn">Pregunta {p["n"]}</div><div class="bubble">{p["q"]}</div><p class="ans">{p["a"]}</p>'
    if k == "star":
        li = "".join(f'<li><span class="l">{l}</span><div><b>{t}</b>{d}</div></li>' for l, t, d in p["items"])
        return f'<h2>{p["title"]}</h2><ul class="st">{li}</ul>'
    if k == "plan":
        li = "".join(f'<li><span class="d">{d}</span>{t}</li>' for d, t in p["items"])
        return f'<h2>{p["title"]}</h2><ul class="plan">{li}</ul>'
    if k == "list":
        li = "".join(f'<li><span>✓</span>{x}</li>' for x in p["items"])
        return f'<h2>{p["title"]}</h2><ul class="ok">{li}</ul>'
    if k == "close":
        if p.get("prices"):
            return (f'<h2 class="c">{p["title"]}</h2><div class="prices">'
                    f'<div class="pr"><img src="{TAPA1}"><small>Ebook</small><b>$18.000</b><em>o 3 cuotas de $6.000</em></div>'
                    f'<div class="pr best"><div class="two"><img src="{TAPA1}"><img src="{TAPA2}"></div><small>Combo 2 ebooks</small><b>$27.000</b><em>o 3 cuotas de $9.000</em></div>'
                    f'</div><p class="sub c">{p["sub"]}</p>')
        return (f'<div class="closewrap"><img class="tapa" src="{TAPA1}"><h2 class="c">{p["title"]}</h2><p class="sub c">{p["sub"]}</p>'
                '<div class="linkline"><i></i>Link en nuestro perfil</div></div>')
    raise ValueError(k)


DARK = {"cover", "close", "qa"}

CSS = """
*{box-sizing:border-box;margin:0;padding:0}
body{background:#222}
.s{width:1080px;height:1350px;position:relative;overflow:hidden;font-family:Inter,sans-serif;padding:110px 96px 120px;display:flex;flex-direction:column}
.dark{background:radial-gradient(circle at 85% 0%,#3B3F9A 0%,#14213D 45%,#0B1226 100%);color:#fff}
.light{background:#F6F7FB;color:#14213D}
.brand{position:absolute;left:96px;bottom:52px;display:flex;align-items:center;gap:14px;font-weight:800;font-size:28px;opacity:.9}
.brand img{width:48px;height:48px;border-radius:12px}
.count{position:absolute;right:96px;bottom:60px;font-size:26px;font-weight:700;opacity:.5}
h1,h2,.big{font-family:"Inter Display",Inter,sans-serif;letter-spacing:-.03em}
h1{font-size:104px;font-weight:900;line-height:1}
h2{font-size:80px;font-weight:900;line-height:1.04;margin-bottom:50px}
h1 em,h2 em{font-style:normal;color:#E8632E}
.dark h1 em,.dark h2 em{color:#F5D27A}
.c{text-align:center}
.kick{font-size:28px;font-weight:800;letter-spacing:.16em;text-transform:uppercase;color:#E8632E;margin-bottom:40px}
.sub{font-size:42px;line-height:1.35;margin-top:40px;opacity:.85}
.swipe{margin-top:auto;font-size:32px;font-weight:700;color:#F5D27A;margin-bottom:60px}
.swipe span{display:inline-block;margin-left:8px}
.covpic{position:absolute;right:-30px;bottom:80px;width:520px;height:440px}
.covpic img{position:absolute;width:250px;border-radius:8px;box-shadow:0 30px 60px rgba(0,0,0,.5)}
.covpic img:first-child{left:40px;top:30px;transform:rotate(-8deg);z-index:2}
.covpic img:last-child{left:230px;top:10px;transform:rotate(6deg)}
.big{font-size:260px;font-weight:900;line-height:.8;color:#E8632E;margin-bottom:50px}
.err,.fix{border-radius:32px;padding:46px 50px;font-size:50px;font-weight:800;line-height:1.2}
.err{background:#fff;box-shadow:0 14px 34px rgba(20,33,61,.08);text-decoration:line-through;text-decoration-color:#E8632E;text-decoration-thickness:5px}
.fix{margin-top:30px;background:#14213D;color:#fff;font-size:42px;font-weight:600;line-height:1.4}
.err small,.fix small,.antes small,.despues small{display:block;font-size:26px;font-weight:800;letter-spacing:.14em;text-transform:uppercase;margin-bottom:16px;text-decoration:none}
.err small{color:#E8632E}.fix small{color:#F5D27A}
.formula{display:flex;flex-direction:column;gap:12px}
.part{display:flex;align-items:center;gap:34px;padding:40px 0;border-bottom:3px solid #E2E8F0;font:900 64px/1.1 "Inter Display";letter-spacing:-.02em}
.part span{flex:none;width:100px;font:900 90px/1 "Inter Display";color:#E8632E}
.note{margin-top:auto;margin-bottom:70px;font-size:38px;line-height:1.4;color:#475569}
.note.strong{color:#E8632E;font-weight:800}
.ba{flex:1;display:flex;flex-direction:column;justify-content:center}
.antes{background:#fff;border-radius:32px;padding:46px;font-size:56px;font-weight:800;color:#94A3B8;box-shadow:0 14px 34px rgba(20,33,61,.08)}
.antes small{color:#94A3B8}
.arrow{text-align:center;font:900 90px/1.2 Inter;color:#E8632E}
.despues{background:#14213D;color:#fff;border-radius:32px;padding:50px;font-size:48px;font-weight:700;line-height:1.35;box-shadow:0 0 0 8px #F5D27A}
.despues small{color:#F5D27A}
.words{display:grid;grid-template-columns:1fr 1fr;column-gap:60px}
.words div{display:flex;align-items:center;gap:24px;padding:22px 0;border-bottom:2px solid #E2E8F0;font-size:48px;font-weight:800}
.words div::before{content:"";flex:none;width:18px;height:18px;border-radius:50%;background:#E8632E}
.mid{flex:1;display:flex;flex-direction:column;justify-content:center;padding-bottom:60px}
.bad,.ok,.plan,.st{list-style:none;display:flex;flex-direction:column;gap:24px}
.bad li,.ok li,.st li{display:flex;align-items:center;gap:30px;background:#fff;border-radius:28px;padding:40px;font-size:44px;font-weight:700;line-height:1.25;box-shadow:0 12px 30px rgba(20,33,61,.08)}
.bad i{flex:none;width:76px;height:76px;border-radius:50%;background:#FDE8E0;color:#E8632E;font:900 40px/76px Inter;text-align:center;font-style:normal}
.ok li span{flex:none;width:76px;height:76px;border-radius:50%;background:#14213D;color:#F5D27A;font:900 40px/76px Inter;text-align:center}
.st li{align-items:flex-start}.st li div{font-weight:500;color:#334155}.st li b{display:block;font-size:48px;color:#14213D;margin-bottom:6px}
.st .l{flex:none;width:80px;height:80px;border-radius:50%;background:#E8632E;color:#fff;font:900 44px/80px Inter;text-align:center}
.plan{gap:14px}
.plan li{display:flex;align-items:center;gap:30px;font-size:40px;font-weight:700;padding:22px 0;border-bottom:2px solid #E2E8F0}
.plan .d{flex:none;width:200px;font:900 46px/1 "Inter Display";color:#E8632E}
.exwrap{flex:1;display:flex;flex-direction:column;justify-content:center}
.li-card{background:#fff;border-radius:32px;padding:50px;box-shadow:0 20px 40px rgba(20,33,61,.12)}
.li-top{display:flex;align-items:center;gap:26px;margin-bottom:28px}
.li-av{width:110px;height:110px;border-radius:50%;background:#CBD5E1}
.li-name{font-size:44px;font-weight:800}
.li-head{font-size:40px;line-height:1.4;color:#334155}
.ex-parts{margin-top:50px;display:flex;flex-direction:column;gap:16px}
.ln{border-left:10px solid #E8632E;padding:10px 0 10px 28px;font-size:38px;font-weight:700}
.ln:nth-child(2){border-color:#14213D}.ln:nth-child(3){border-color:#B8892B}
.qn{font-size:30px;font-weight:800;letter-spacing:.16em;text-transform:uppercase;color:#E8632E;margin-bottom:34px}
.bubble{background:#F6F1E4;color:#14213D;border-radius:44px;padding:56px;font:900 70px/1.12 "Inter Display";letter-spacing:-.02em;box-shadow:0 0 0 8px #F5D27A}
.ans{font-size:46px;line-height:1.42;margin-top:60px}
.ans b{color:#F5D27A}
.closewrap{flex:1;display:flex;flex-direction:column;align-items:center;justify-content:center;padding-bottom:40px}
.tapa{width:300px;border-radius:10px;box-shadow:0 30px 60px rgba(0,0,0,.5);margin-bottom:56px}
.linkline{margin-top:50px;font:900 50px/1 "Inter Display";color:#F5D27A;display:flex;flex-direction:column;align-items:center}
.linkline i{width:120px;height:6px;border-radius:6px;background:#E8632E;margin-bottom:36px}
.prices{display:flex;gap:40px;margin-top:10px}
.pr{flex:1;background:#fff;color:#14213D;border-radius:36px;padding:44px 30px;text-align:center}
.pr img{width:190px;border-radius:8px;box-shadow:0 12px 26px rgba(0,0,0,.3);margin-bottom:30px}
.pr .two{position:relative;height:300px;margin-bottom:30px}.pr .two img{position:absolute;width:170px;margin:0}.pr .two img:first-child{left:40px;top:0;z-index:2}.pr .two img:last-child{right:40px;top:30px}
.pr small{display:block;font-size:28px;font-weight:800;letter-spacing:.12em;text-transform:uppercase;color:#64748B}
.pr b{display:block;font:900 80px/1.1 "Inter Display";margin:14px 0 8px}
.pr em{font-style:normal;font-size:30px;font-weight:700;color:#E8632E}
.gold{color:#F5D27A;font-weight:900}
.pr.best{box-shadow:0 0 0 8px #E8632E}
"""


def build():
    os.makedirs(OUT, exist_ok=True)
    ids, html = [], []
    for car, placas in C.items():
        for i, p in enumerate(placas, 1):
            sid = f"{car}--{i}"
            ids.append(sid)
            theme = "dark" if p["kind"] in DARK else "light"
            html.append(f'<div class="s {theme}" id="{sid}">{body(p)}'
                        f'<div class="brand"><img src="{ICON}">Método 30</div>'
                        f'<div class="count">{i}/{len(placas)}</div></div>')
    open(os.path.join(OUT, "_historias.html"), "w").write(
        "<!doctype html><meta charset='utf-8'><style>" + CSS + "</style><body>" + "".join(html) + "</body>")
    open(os.path.join(OUT, "_ids.json"), "w").write(json.dumps(ids))
    print(len(ids), "placas")


if __name__ == "__main__":
    build()
