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


FOTO_PROBLEMA = img("landing/fotos/problema.jpg")
FOTO_RESULTADO = img("landing/fotos/resultado.jpg")

# ---------- 6. ¿Cuánto pretendés? (portada naranja) ----------
K = "6-cuanto-pretendes"
add(K, "cv_orange", big="$?", title="«¿Cuánto<br>pretendés?»", sub="Cómo responder sin quedarte corto")
add(K, "quote", label="Primero, que lo digan ellos",
    text="«Me interesa mucho entender bien el puesto antes de hablar de números. ¿Cuál es la banda que tienen prevista para esta posición?»")
add(K, "quote", label="Si insisten, da un rango",
    text="«Por lo que vi en el mercado para este rol y mi experiencia, estoy en un rango de [X] a [Y] brutos mensuales, abierto a conversar según el paquete completo.»",
    note="El mínimo del rango es tu número objetivo, no tu piso.")
add(K, "bad", title="Los 3 errores<br>más caros",
    items=["Decir tu sueldo actual (no estás obligado)", "Dar un número sin investigar el mercado", "Pedir de menos «para no asustar»"],
    note="Hablá de lo que vale el nuevo puesto, no de lo que ganás hoy.")
add(K, "close", title="Negociá sin <em>miedo</em>",
    sub="Cómo investigar tu valor, negociar la oferta y comparar propuestas: días 25 a 28 del plan.")

# ---------- 7. Te dejaron en visto (portada foto oscura) ----------
K = "7-sin-respuesta"
add(K, "cv_photo", photo=FOTO_PROBLEMA, chat="Te postulaste hace una semana…", title="¿Y si nadie<br>te <em>responde</em>?",
    sub="El mensaje de seguimiento que casi nadie manda")
add(K, "msg", label="A la semana de postularte", to="Seguimiento · Postulación [puesto]",
    text="Hola, [nombre]: hace una semana me postulé a [puesto] y quería reiterar mi interés. Desde entonces [dato nuevo: terminé un curso / leí sobre su lanzamiento de X], y me entusiasma todavía más la posibilidad de aportar en [área]. Quedo a disposición para conversar. ¡Gracias!")
add(K, "msg", label="Si pasó el plazo de respuesta", to="Mensaje directo",
    text="Hola, [nombre]: espero que estés bien. Quería consultar si hay novedades sobre el proceso de [puesto]. Sigo muy interesado y, si necesitan algo más de mi parte, con gusto lo envío. ¡Saludos!")
add(K, "list", title="Para que lo lean",
    items=["Corto: menos de 100 palabras", "Con un dato concreto o algo nuevo", "Sin rogar", "Sin pegar el CV entero en el mensaje"])
add(K, "close", title="8 plantillas listas<br>para <em>copiar</em>",
    sub="Seguimientos, pedidos de referido, respuesta a un rechazo y más: todas en «Conseguí trabajo en 30 días».")

# ---------- 8. Preguntas que hacés vos (portada foto luminosa) ----------
K = "8-preguntas-que-haces-vos"
add(K, "cv_photo2", photo=FOTO_RESULTADO, title="«¿Tenés alguna<br>pregunta?»",
    sub="Nunca digas que no. Llevá estas 👇")
add(K, "numlist", title="Preguntas que<br>suman <em>puntos</em>", start=1,
    items=["¿Cómo sería un éxito en este puesto a los 90 días y al año?", "¿Cuál es el mayor desafío que tiene hoy el equipo?",
           "¿Por qué se abrió esta posición?", "¿Qué diferencia a las personas que mejor rinden acá?"])
add(K, "numlist", title="Y las que te<br>dan <em>ventaja</em>", start=5,
    items=["¿Hay algo de mi perfil que te genere dudas para el puesto?", "¿Cuáles son los próximos pasos del proceso?"],
    note="La 5 te da la chance de responder una duda en el momento.")
add(K, "bad", title="En la primera<br>entrevista, no",
    items=["Vacaciones y licencias", "«¿Cuándo puedo pedir un aumento?»"],
    note="Eso llega con la oferta.")
add(K, "close", title="Llevá 5 preparadas<br>y hacé <em>2 o 3</em>",
    sub="La preparación completa de cada entrevista está en los días 18 a 24 del plan.")

# ---------- 9. Networking (portada dorada) ----------
K = "9-networking"
add(K, "cv_gold", title="Dejá de pedir<br>trabajo.<br><em>Pedí un consejo.</em>", sub="Así funciona el networking que sí da resultados")
add(K, "msg", label="Mensaje para conectar", to="LinkedIn",
    text="Hola, [nombre]. Vi tu trabajo en [empresa/posteo] y me interesa mucho [área]. Estoy dando mis próximos pasos en ese camino y me encantaría conectar para aprender de tu experiencia. ¡Gracias!")
add(K, "numlist", title="En la charla<br>de 15 minutos", start=1,
    items=["¿Cómo es un día típico en tu rol?", "¿Qué valora más tu empresa en alguien que entra en esta área?",
           "¿Qué me recomendarías para destacarme?", "¿Hay alguien más con quien me recomendarías hablar?"])
add(K, "split", title="Cómo repartir<br>tu tiempo",
    items=[("50 %", "Networking y contacto directo"), ("30 %", "Postulaciones adaptadas"), ("20 %", "Seguimientos y visibilidad")],
    note="La mayoría lo hace al revés.")
add(K, "close", title="2 o 3 charlas<br>por <em>semana</em>",
    sub="Cada una abre, en promedio, otro contacto. El método completo está en los días 13 a 17 del plan.")

# ---------- 10. Diagnóstico (portada negra con embudo) ----------
K = "10-donde-se-corta"
add(K, "cv_funnel", title="¿Dónde se corta<br>tu <em>búsqueda</em>?",
    stages=["Postulaciones", "Respuestas", "Entrevistas", "Final", "Oferta"])
for sint, fix in [
    ("Casi no te responden", "Reescribí perfil y viñetas, revisá el nivel al que apuntás y subí el networking al 50 % de tu tiempo."),
    ("Te responden pero no pasás RR. HH.", "Practicá el «contame sobre vos» y el «por qué acá». Revisá tu rango de sueldo."),
    ("Llegás a la final y eligen a otro", "Historias STAR más fuertes, preguntas de cierre y un mail de seguimiento con valor."),
    ("Ofertas por debajo de lo esperado", "Investigá el mercado y practicá la contraoferta."),
]:
    add(K, "beforeafter", antes=sint, despues=fix, la="Si te pasa esto", lb="Hacé esto")
add(K, "close", title="Medí todo.<br>Ajustá cada <em>semana</em>",
    sub="El tracker y el diagnóstico completo están en «Conseguí trabajo en 30 días».")


# ---------- RENDER ----------
def body(p):
    k = p["kind"]
    if k == "cv_orange":
        return (f'<div class="bigsym">{p["big"]}</div><h1>{p["title"]}</h1><p class="sub">{p["sub"]}</p>'
                '<div class="swipe">Deslizá <span>→</span></div>')
    if k == "cv_photo":
        return (f'<div class="bg" style="background-image:url({p["photo"]})"></div><div class="shade"></div>'
                f'<div class="chat">{p["chat"]}<span>Visto ✓✓</span></div>'
                f'<div class="ph-text"><h1>{p["title"]}</h1><p class="sub">{p["sub"]}</p></div>')
    if k == "cv_photo2":
        return (f'<div class="bg" style="background-image:url({p["photo"]})"></div><div class="shade2"></div>'
                f'<div class="ph-text"><h1>{p["title"]}</h1><p class="sub">{p["sub"]}</p></div>')
    if k == "cv_gold":
        return (f'<div class="kick">Networking</div><h1>{p["title"]}</h1><p class="sub">{p["sub"]}</p>'
                '<div class="swipe">Deslizá <span>→</span></div>')
    if k == "cv_funnel":
        n = len(p["stages"])
        st = "".join(f'<div class="fs" style="width:{100 - i * 15}%;--o:{1 - i * .15}">{x}</div>' for i, x in enumerate(p["stages"]))
        return f'<h1>{p["title"]}</h1><div class="funnel">{st}</div><div class="swipe">Deslizá <span>→</span></div>'
    if k == "quote":
        note = f'<p class="note strong">{p["note"]}</p>' if p.get("note") else ""
        return f'<div class="mid"><div class="qn">{p["label"]}</div><div class="quote">{p["text"]}</div></div>{note}'
    if k == "msg":
        return (f'<div class="mid"><div class="qn">{p["label"]}</div><div class="msgcard"><div class="mto">{p["to"]}</div>'
                f'<div class="mtx">{p["text"]}</div></div></div>')
    if k == "numlist":
        li = "".join(f'<li><span>{j}</span>{x}</li>' for j, x in enumerate(p["items"], p["start"]))
        note = f'<p class="note strong">{p["note"]}</p>' if p.get("note") else ""
        return f'<h2>{p["title"]}</h2><ul class="ok num">{li}</ul>{note}'
    if k == "split":
        li = "".join(f'<div class="sp"><b>{a}</b><span>{b}</span></div>' for a, b in p["items"])
        return f'<h2>{p["title"]}</h2><div class="splits">{li}</div><p class="note strong">{p["note"]}</p>'
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
        return (f'<div class="ba"><div class="antes"><small>{p.get("la", "Antes")}</small>{p["antes"]}</div>'
                f'<div class="arrow">↓</div><div class="despues"><small>{p.get("lb", "Después")}</small>{p["despues"]}</div></div>')
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


DARK = {"cover", "close", "qa", "cv_photo", "cv_photo2"}
THEMES = {"cv_orange": "orange", "cv_gold": "goldbg", "cv_funnel": "black"}

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
.orange{background:#E8632E;color:#fff}
.orange h1{font-size:120px}.orange .sub{opacity:.95}.orange .swipe{color:#14213D}
.bigsym{font:900 400px/.85 "Inter Display";letter-spacing:-.06em;color:#14213D;margin:20px 0 50px}
.goldbg{background:#F5D27A;color:#14213D}
.goldbg h1{font-size:118px}.goldbg h1 em{color:#E8632E}.goldbg .kick{color:#14213D}.goldbg .swipe{color:#14213D}
.goldbg .sub{opacity:1}
.black{background:#0E0C09;color:#fff}
.black h1 em{color:#E8632E}.black .swipe{color:#F5D27A}
.funnel{margin:80px auto 0;width:100%;display:flex;flex-direction:column;align-items:center;gap:6px}
.fs{position:relative;text-align:center;padding:30px 0;font-size:38px;font-weight:800;color:#fff;clip-path:polygon(0 0,100% 0,93% 100%,7% 100%);background:rgba(232,99,46,var(--o))}
.fs:nth-child(3){background:#F5D27A;color:#14213D}
.bg{position:absolute;inset:0;background-size:cover;background-position:center}
.shade{position:absolute;inset:0;background:linear-gradient(180deg,rgba(11,18,38,.35) 0%,rgba(11,18,38,.55) 45%,rgba(11,18,38,.97) 78%)}
.shade2{position:absolute;inset:0;background:linear-gradient(180deg,rgba(11,18,38,0) 30%,rgba(11,18,38,.75) 60%,rgba(11,18,38,.97) 82%)}
.ph-text{position:relative;margin-top:auto;margin-bottom:70px}
.ph-text h1{font-size:112px}
.chat{position:relative;align-self:flex-start;background:#fff;color:#14213D;border-radius:30px 30px 30px 8px;padding:30px 38px;font-size:38px;font-weight:600;max-width:760px;box-shadow:0 20px 50px rgba(0,0,0,.4);margin-top:30px}
.chat b{display:block;font-size:26px;color:#64748B;margin-bottom:8px}
.chat span{display:block;text-align:right;font-size:26px;color:#3B82F6;font-weight:700;margin-top:10px}
.quote{background:#fff;border-left:14px solid #E8632E;border-radius:28px;padding:56px;font-size:50px;font-weight:700;line-height:1.35;box-shadow:0 14px 34px rgba(20,33,61,.08)}
.msgcard{background:#fff;border-radius:32px;padding:50px;box-shadow:0 20px 40px rgba(20,33,61,.12)}
.mto{font-size:28px;font-weight:800;color:#64748B;padding-bottom:24px;margin-bottom:28px;border-bottom:2px solid #E2E8F0}
.mtx{font-size:40px;line-height:1.45;color:#1F2937}
.num li span{font-size:38px}
.splits{display:flex;flex-direction:column;gap:22px}
.sp{display:flex;align-items:center;gap:40px;background:#fff;border-radius:28px;padding:36px 44px;box-shadow:0 12px 30px rgba(20,33,61,.08)}
.sp b{flex:none;width:250px;font:900 96px/1 "Inter Display";color:#E8632E;letter-spacing:-.03em}
.sp span{font-size:44px;font-weight:700;line-height:1.25}
.pr.best{box-shadow:0 0 0 8px #E8632E}
"""


def build():
    os.makedirs(OUT, exist_ok=True)
    ids, html = [], []
    for car, placas in C.items():
        for i, p in enumerate(placas, 1):
            sid = f"{car}--{i}"
            ids.append(sid)
            theme = THEMES.get(p["kind"]) or ("dark" if p["kind"] in DARK else "light")
            html.append(f'<div class="s {theme}" id="{sid}">{body(p)}'
                        f'<div class="brand"><img src="{ICON}">Método 30</div>'
                        f'<div class="count">{i}/{len(placas)}</div></div>')
    open(os.path.join(OUT, "_historias.html"), "w").write(
        "<!doctype html><meta charset='utf-8'><style>" + CSS + "</style><body>" + "".join(html) + "</body>")
    open(os.path.join(OUT, "_ids.json"), "w").write(json.dumps(ids))
    print(len(ids), "placas")


if __name__ == "__main__":
    build()
