# Edita los creativos para publicarlos orgánicos en TikTok:
# corta el "Tocá el botón" del final, suma el texto del gancho arriba, agrega al final una parte nueva que pide un comentario,
# y en la parte del generador (fondo blanco) tapa los subtítulos quemados con un recuadro oscuro y los reescribe.
#   python3 instagram/tiktok/editar.py C=creativoC.mp4 B=creativoB.mp4 V1=... V2=... V3=... V4=... V5=...
# Solo se arman los videos cuyas fuentes se pasan.
# Los tiempos salen de la transcripción palabra por palabra y de los cambios de escena de cada video.
import os, subprocess, sys, json, tempfile

AQUI = os.path.dirname(os.path.abspath(__file__))
FUENTES = dict(a.split("=", 1) for a in sys.argv[1:] if "=" in a)
C_IN, B_IN = "C", "B"

# Recuadro que tapa los subtítulos quemados (zona abajo a la izquierda, al lado de Cami)
CAJA = dict(x=30, y=1395, w=600, h=330)

TRABAJOS = [
    dict(salida="tiktok-1-no-te-llaman.mp4", entrada=C_IN, desde=0.0, hasta=22.40,
         titulo=("POR ESTO NO TE LLAMAN 👇", 0.0, 2.8),
         cierre=dict(titulo="Comentá «CV»", sub="y te digo cómo arreglar el tuyo 👇", comentario="CV"),
         subs=[(12.933, 15.02, "*MIRÁ:* PONGO MIS DATOS, PEGO EL AVISO"),
               (15.02, 17.28, "Y ME DICE QUÉ *PALABRAS* ME FALTAN"),
               (17.28, 18.72, "EN *10 MINUTOS*, LISTO"),
               (18.72, 20.5, "VIENE INCLUIDO CON *MÉTODO 30*")]),
    dict(salida="tiktok-2-para-de-mandar-cv.mp4", entrada=B_IN, desde=0.0, hasta=23.60,
         titulo=("¿SEGUÍS MANDANDO EL MISMO CV? 😬", 0.0, 3.4),
         cierre=dict(titulo="¿Cuántos CV mandás por semana?", sub="Contalo en los comentarios 👇", comentario="Como 20 😩"),
         subs=[(12.467, 13.20, "*SIN LEERLO*"),
               (13.20, 14.78, "POR ESO ARMAMOS UN *GENERADOR*"),
               (14.78, 15.90, "*CONTESTÁS* UNAS PREGUNTAS"),
               (15.90, 18.44, "Y EN *10 MINUTOS* TENÉS TU CURRÍCULUM"),
               (18.44, 19.88, "HECHO PARA *CADA AVISO*"),
               (19.88, 21.767, "VIENE INCLUIDO CON *MÉTODO 30*")]),
    dict(salida="tiktok-3-generador.mp4", entrada=C_IN, desde=12.933, hasta=18.68,
         titulo=("Armé mi CV en 10 minutos con esto 🤯", 12.933, 14.933),
         cierre=dict(titulo="Comentá «CV»", sub="y te muestro cómo funciona 👇", comentario="CV"),
         subs=[(12.933, 15.02, "*MIRÁ:* PONGO MIS DATOS, PEGO EL AVISO"),
               (15.02, 17.28, "Y ME DICE QUÉ *PALABRAS* ME FALTAN"),
               (17.28, 18.68, "EN *10 MINUTOS*, LISTO")]),
    # Segunda tanda: solo se corrigen los subtítulos que estaban mal, se corta el «Tocá el botón» y se suma el cierre
    dict(salida="tiktok-4-sos-un-salame.mp4", entrada="V5", desde=0.0, hasta=28.15,
         cierre=dict(titulo="¿Cuál de los 3 no hacías?", sub="Comentá 1, 2 o 3 👇", comentario="El 2 😅"),
         subs=[(1.13, 2.83, "VER ESTO SEGUÍS MANDANDO EL MISMO *CV*", dict(x=265, y=1315, w=550, h=270))]),
    dict(salida="tiktok-5-entrevista.mp4", entrada="V4", desde=0.0, hasta=23.55,
         cierre=dict(titulo="¿Cuál es tu mayor debilidad?", sub="Comentala y te digo cómo decirla 👇", comentario="Soy impaciente 😅"),
         subs=[(22.27, 23.55, "*RESUELTAS* PASO A PASO", dict(x=95, y=1395, w=545, h=260))]),
    dict(salida="tiktok-6-asi-termina-tu-cv.mp4", entrada="V3", desde=0.0, hasta=27.80,
         cierre=dict(titulo="¿Cuántos CV mandaste este mes?", sub="Contalo en los comentarios 👇", comentario="Más de 50 😩"),
         subs=[(6.2, 7.77, "MANDASTE *40 CVS*", dict(x=110, y=1415, w=480, h=190))]),
    dict(salida="tiktok-7-isabela.mp4", entrada="V1", desde=0.0, hasta=27.03,
         cierre=dict(titulo="¿Hace cuánto estás buscando?", sub="Contalo en los comentarios 👇", comentario="8 meses 😩"),
         subs=[(0.0, 2.33, "UN AÑO Y MEDIO ESTUVO *ISABELA* MANDANDO"),
               (21.57, 24.40, "ESE ES *MÉTODO 30*, EL PLAN QUE USÓ ELLA"),
               (24.40, 27.03, "AHORA CON *GENERADOR DE CURRÍCULUM* INCLUIDO")]),
    dict(salida="tiktok-8-tres-errores.mp4", entrada="V2", desde=0.0, hasta=26.97,
         cierre=dict(titulo="Comentá «CV»", sub="y te digo cómo arreglar el tuyo 👇", comentario="CV"),
         subs=[]),
]

HTML = """<!doctype html><meta charset="utf-8"><style>
*{margin:0;padding:0;box-sizing:border-box}
html,body{width:1080px;height:1920px;background:transparent;overflow:hidden}
.t{position:absolute;left:50%;transform:translateX(-50%);max-width:940px;padding:22px 34px;border-radius:26px;background:#fff;color:#0B0B0B;
  font:900 64px/1.12 "Inter Display","Noto Color Emoji",sans-serif;text-align:center;box-shadow:0 10px 30px rgba(0,0,0,.35);width:max-content}
.c{position:absolute;left:50%;transform:translateX(-50%);padding:22px 38px;border-radius:60px;background:#E8632E;color:#fff;
  font:900 54px/1.1 "Inter Display","Noto Color Emoji",sans-serif;text-align:center;box-shadow:0 12px 30px rgba(0,0,0,.4);width:max-content;max-width:960px}
.s{position:absolute;display:flex;align-items:center;justify-content:center;border-radius:30px;background:#0B1226;
  border:2px solid rgba(255,255,255,.10);padding:24px 30px}
.s p{font:400 76px/1.04 Anton,"Noto Color Emoji",sans-serif;color:#fff;text-align:center;letter-spacing:.01em;text-transform:uppercase}
.s em{font-style:normal;color:#FFD84D}
</style><body><div id="r"></div></body>"""

JS_RENDER = """([kind, text, box]) => {
  const r = document.getElementById('r'); r.innerHTML = '';
  const esc = s => s.replace(/&/g,'&amp;').replace(/</g,'&lt;');
  if (kind === 's') {
    const d = document.createElement('div'); d.className = 's';
    Object.assign(d.style, {left: box.x+'px', top: box.y+'px', width: box.w+'px', height: box.h+'px'});
    const p = document.createElement('p');
    p.innerHTML = esc(text).replace(/\\*(.+?)\\*/g, '<em>$1</em>');
    d.appendChild(p); r.appendChild(d);
    let fs = 76; while ((p.scrollHeight > box.h - 40 || p.scrollWidth > box.w - 50) && fs > 40) { fs -= 2; p.style.fontSize = fs + 'px'; }
  } else {
    const d = document.createElement('div'); d.className = kind;
    d.textContent = text.replace(/ (\\S+)$/, '\\u00a0$1');
    d.style.top = box.y + 'px'; d.style.whiteSpace = 'nowrap'; r.appendChild(d);
    const base = parseFloat(getComputedStyle(d).fontSize); let fs = base;
    while (d.scrollWidth > 1000 && fs > base * 0.84) { fs -= 2; d.style.fontSize = fs + 'px'; }
    if (d.scrollWidth > 1000) { d.style.whiteSpace = 'normal'; d.style.fontSize = base + 'px'; }
  }
}"""


def render_pngs(job, carpeta):
    """Devuelve una lista de (png, inicio, fin, fundido) en segundos del video original."""
    piezas = []
    tareas = []
    if job.get("titulo"):
        t, ti, tf = job["titulo"]
        tareas.append(("t", t, dict(y=250), ti, tf, True))
    for sub in job["subs"]:
        a, b, txt = sub[:3]
        tareas.append(("s", txt, sub[3] if len(sub) > 3 else CAJA, a, b, False))
    script = os.path.join(carpeta, "render.js")
    html = os.path.join(carpeta, "o.html")
    open(html, "w", encoding="utf-8").write(HTML)
    lista = []
    for i, (kind, text, box, a, b, fade) in enumerate(tareas):
        png = os.path.join(carpeta, f"o{i:02d}.png")
        lista.append(dict(kind=kind, text=text, box=box, png=png))
        piezas.append((png, a, b, fade))
    open(os.path.join(carpeta, "lista.json"), "w").write(json.dumps(lista))
    open(script, "w").write("""
const { chromium } = require('playwright'); const fs = require('fs');
(async () => {
  const lista = JSON.parse(fs.readFileSync(process.argv[2] + '/lista.json'));
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1080, height: 1920 } });
  await p.goto('file://' + process.argv[2] + '/o.html'); await p.evaluate(() => document.fonts.ready);
  for (const it of lista) {
    await p.evaluate(""" + JS_RENDER + """, [it.kind, it.text, it.box]);
    await p.evaluate(() => document.fonts.ready);
    await p.screenshot({ path: it.png, omitBackground: true });
  }
  await b.close();
})();
""")
    subprocess.run(["node", script, carpeta], check=True)
    return piezas


CIERRE_SEG = 4.0
CIERRE_HTML = """<!doctype html><meta charset="utf-8"><style>
*{margin:0;padding:0;box-sizing:border-box}
html,body{width:1080px;height:1920px;overflow:hidden;background:#0B1226}
#bg{position:absolute;inset:-40px;background:url(ultimo.png) center/cover;filter:blur(18px) brightness(.42)}
.card{position:absolute;left:80px;width:860px;top:560px;padding:44px 40px 40px;border-radius:36px;background:#fff;text-align:center;
  box-shadow:0 24px 60px rgba(0,0,0,.45)}
.card h1{font:900 92px/1.05 "Inter Display","Noto Color Emoji",sans-serif;color:#0B0B0B;letter-spacing:-.01em}
.card h1 em{font-style:normal;color:#E8632E}
.card p{margin-top:18px;font:800 46px/1.2 "Inter Display","Noto Color Emoji",sans-serif;color:#3A3F4B}
.com{position:absolute;left:80px;width:860px;padding:26px 30px;border-radius:28px;background:#fff;display:flex;align-items:center;gap:24px;
  box-shadow:0 18px 44px rgba(0,0,0,.4)}
.av{flex:none;width:84px;height:84px;border-radius:50%;background:linear-gradient(135deg,#F5D27A,#E8632E)}
.tx{flex:1;min-width:0}
.tx b{display:block;font:700 30px/1.2 Inter,sans-serif;color:#8A90A0}
.tx span{display:block;margin-top:6px;font:700 52px/1.15 Inter,"Noto Color Emoji",sans-serif;color:#0B0B0B;white-space:nowrap}
.cur{display:inline-block;width:4px;height:48px;background:#E8632E;margin-left:6px;vertical-align:-6px}
.hrt{flex:none;text-align:center;font:700 26px/1 Inter,sans-serif;color:#8A90A0}
.hrt svg{display:block;width:56px;height:56px;margin:0 auto 6px}
.pill{position:absolute;left:50%;padding:22px 40px;border-radius:60px;background:#E8632E;color:#fff;white-space:nowrap;
  font:900 50px/1.1 "Inter Display","Noto Color Emoji",sans-serif;box-shadow:0 14px 34px rgba(0,0,0,.4)}
</style><body><div id="bg"></div>
<div class="card" id="card"><h1 id="h1"></h1><p id="sub"></p></div>
<div class="com" id="com"><div class="av"></div><div class="tx"><b>Vos · ahora</b><span id="txt"></span></div>
  <div class="hrt"><svg viewBox="0 0 24 24"><path id="hp" d="M12 21s-7.5-4.6-9.6-9.2C.9 8.4 3.1 4.5 6.9 4.5c2.1 0 3.6 1.2 5.1 3 1.5-1.8 3-3 5.1-3 3.8 0 6 3.9 4.5 7.3C19.5 16.4 12 21 12 21z" fill="none" stroke="#8A90A0" stroke-width="2"/></svg><span id="cnt">0</span></div></div>
<div class="pill" id="pill">Más info en mi perfil 👆</div>
<script>
const clamp=(x,a=0,b=1)=>Math.max(a,Math.min(b,x)), span=(t,a,b)=>clamp((t-a)/(b-a));
const back=x=>{x=clamp(x);const c=1.7;return 1+(c+1)*Math.pow(x-1,3)+c*Math.pow(x-1,2)};
const $=id=>document.getElementById(id); let D;
function setup(d){D=d;$('h1').innerHTML=d.titulo.replace(/«(.+?)»/g,'<em>«$1»</em>');$('sub').textContent=d.sub;
  const cb=$('card').getBoundingClientRect(); $('com').style.top=(cb.bottom+40)+'px';
  const mb=$('com').getBoundingClientRect(); $('pill').style.top=(mb.bottom+44)+'px';}
function render(t){
  $('bg').style.transform=`scale(${1.04+0.04*t/4})`;
  const c=back(span(t,0,0.38)); $('card').style.opacity=span(t,0,0.12); $('card').style.transform=`scale(${0.7+0.3*c})`;
  const m=back(span(t,0.45,0.8)); $('com').style.opacity=span(t,0.45,0.55); $('com').style.transform=`translateY(${(1-m)*60}px)`;
  const chars=Array.from(D.comentario), k=Math.floor(clamp((t-0.8)/0.14,0,chars.length));
  const typed=chars.slice(0,k).join(''), done=k>=chars.length, blink=Math.floor(t*4)%2===0;
  $('txt').innerHTML=typed.replace(/&/g,'&amp;').replace(/</g,'&lt;')+((!done||blink)?'<i class="cur"></i>':'');
  const tl=0.8+chars.length*0.14+0.25, h=back(span(t,tl,tl+0.3));
  $('hp').setAttribute('fill',t>=tl?'#FE2C55':'none'); $('hp').setAttribute('stroke',t>=tl?'#FE2C55':'#8A90A0');
  $('hp').parentNode.style.transform=`scale(${t>=tl?0.6+0.4*h:1})`; $('cnt').textContent=t>=tl?'1':'0';
  const p=back(span(t,1.5,1.85)); $('pill').style.opacity=span(t,1.5,1.6); $('pill').style.transform=`translateX(-50%) scale(${0.6+0.4*p})`;
}
</script></body>"""


def render_cierre(job, carpeta):
    """Renderiza la parte nueva del final (fondo: el último cuadro, desenfocado) como secuencia de PNG."""
    ultimo = os.path.join(carpeta, "ultimo.png")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{job['hasta'] - 0.04:.3f}", "-i", job["entrada"],
                    "-frames:v", "1", ultimo], check=True)
    open(os.path.join(carpeta, "cierre.html"), "w", encoding="utf-8").write(CIERRE_HTML)
    open(os.path.join(carpeta, "cierre.json"), "w").write(json.dumps(job["cierre"]))
    script = os.path.join(carpeta, "cierre.js")
    open(script, "w").write("""
const { chromium } = require('playwright'); const fs = require('fs'); const path = require('path');
(async () => {
  const dir = process.argv[2], n = Number(process.argv[3]);
  const d = JSON.parse(fs.readFileSync(path.join(dir, 'cierre.json')));
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1080, height: 1920 } });
  await p.goto('file://' + path.join(dir, 'cierre.html')); await p.evaluate(() => document.fonts.ready);
  await p.evaluate(d => setup(d), d);
  for (let f = 0; f < n; f++) {
    await p.evaluate(t => render(t), f / 30);
    await p.screenshot({ path: path.join(dir, 'cierre_' + String(f).padStart(3, '0') + '.png') });
  }
  await b.close();
})();
""")
    subprocess.run(["node", script, carpeta, str(round(CIERRE_SEG * 30))], check=True)
    return os.path.join(carpeta, "cierre_%03d.png")


def editar(job):
    job = dict(job, entrada=FUENTES[job["entrada"]])
    carpeta = tempfile.mkdtemp(prefix="tt-")
    piezas = render_pngs(job, carpeta)
    d0, d1 = job["desde"], job["hasta"]
    dur = d1 - d0
    args = ["ffmpeg", "-y", "-v", "error", "-ss", f"{d0:.3f}", "-t", f"{dur:.3f}", "-i", job["entrada"]]
    filtros, ultimo = [], "[0:v]"
    for i, (png, a, b, fade) in enumerate(piezas, start=1):
        a, b = max(a, d0) - d0, min(b, d1) - d0
        args += ["-loop", "1", "-t", f"{dur:.3f}", "-i", png]
        cadena = f"[{i}:v]format=rgba"
        if fade:
            cadena += f",fade=t=in:st={a:.3f}:d=0.18:alpha=1,fade=t=out:st={max(a, b - 0.18):.3f}:d=0.18:alpha=1"
        filtros.append(cadena + f"[p{i}]")
        filtros.append(f"{ultimo}[p{i}]overlay=0:0:enable='gte(t,{a:.3f})*lt(t,{b:.3f})'[v{i}]")
        ultimo = f"[v{i}]"
    fin_audio = max(0.0, dur - 0.12)
    filtros.append(f"[0:a]afade=t=in:st=0:d=0.02,afade=t=out:st={fin_audio:.3f}:d=0.12[am]")
    secuencia = render_cierre(job, carpeta)
    n = len(piezas) + 1
    args += ["-framerate", "30", "-i", secuencia,
             "-f", "lavfi", "-t", f"{CIERRE_SEG:.3f}", "-i", "anullsrc=channel_layout=stereo:sample_rate=44100"]
    filtros.append(f"{ultimo}format=yuv420p,setsar=1,fps=30[vm]")
    filtros.append(f"[{n}:v]format=yuv420p,setsar=1,fps=30[ve]")
    filtros.append(f"[vm][am][ve][{n + 1}:a]concat=n=2:v=1:a=1[vf][af]")
    salida = os.path.join(AQUI, job["salida"])
    args += ["-filter_complex", ";".join(filtros), "-map", "[vf]", "-map", "[af]",
             "-c:v", "libx264", "-preset", "slow", "-crf", "16", "-profile:v", "high", "-pix_fmt", "yuv420p", "-r", "30",
             "-c:a", "aac", "-b:a", "192k", "-ar", "44100", "-movflags", "+faststart", salida]
    subprocess.run(args, check=True)
    print(job["salida"], "listo")


if __name__ == "__main__":
    for job in TRABAJOS:
        if job["entrada"] in FUENTES:
            editar(job)
