# Edita los creativos para publicarlos orgánicos en TikTok:
# corta el "Tocá el botón" del final, suma el texto del gancho arriba y el cartel "Más info en mi perfil",
# y en la parte del generador (fondo blanco) tapa los subtítulos quemados con un recuadro oscuro y los reescribe.
#   python3 instagram/tiktok/editar.py CREATIVO_C.mp4 CREATIVO_B.mp4
# Los tiempos salen de la transcripción palabra por palabra y de los cambios de escena de cada video.
import os, subprocess, sys, json, tempfile

AQUI = os.path.dirname(os.path.abspath(__file__))
C_IN, B_IN = sys.argv[1], sys.argv[2]

# Recuadro que tapa los subtítulos quemados (zona abajo a la izquierda, al lado de Cami)
CAJA = dict(x=30, y=1395, w=600, h=330)

TRABAJOS = [
    dict(salida="tiktok-1-no-te-llaman.mp4", entrada=C_IN, desde=0.0, hasta=22.40,
         titulo=("POR ESTO NO TE LLAMAN 👇", 0.0, 2.8),
         cartel=("MÁS INFO EN MI PERFIL 👆", 20.5, 22.40),
         subs=[(12.933, 15.02, "*MIRÁ:* PONGO MIS DATOS, PEGO EL AVISO"),
               (15.02, 17.28, "Y ME DICE QUÉ *PALABRAS* ME FALTAN"),
               (17.28, 18.72, "EN *10 MINUTOS*, LISTO"),
               (18.72, 20.5, "VIENE INCLUIDO CON *MÉTODO 30*")]),
    dict(salida="tiktok-2-para-de-mandar-cv.mp4", entrada=B_IN, desde=0.0, hasta=23.60,
         titulo=("¿SEGUÍS MANDANDO EL MISMO CV? 😬", 0.0, 3.4),
         cartel=("MÁS INFO EN MI PERFIL 👆", 21.767, 23.60),
         subs=[(12.467, 13.20, "*SIN LEERLO*"),
               (13.20, 14.78, "POR ESO ARMAMOS UN *GENERADOR*"),
               (14.78, 15.90, "*CONTESTÁS* UNAS PREGUNTAS"),
               (15.90, 18.44, "Y EN *10 MINUTOS* TENÉS TU CURRÍCULUM"),
               (18.44, 19.88, "HECHO PARA *CADA AVISO*"),
               (19.88, 21.767, "VIENE INCLUIDO CON *MÉTODO 30*")]),
    dict(salida="tiktok-3-generador.mp4", entrada=C_IN, desde=12.933, hasta=18.68,
         titulo=("Armé mi CV en 10 minutos con esto 🤯", 12.933, 14.933),
         cartel=("Comentá «CV» y te muestro cómo 👇", 16.88, 18.68),
         cartel_arriba=True,
         subs=[(12.933, 15.02, "*MIRÁ:* PONGO MIS DATOS, PEGO EL AVISO"),
               (15.02, 17.28, "Y ME DICE QUÉ *PALABRAS* ME FALTAN"),
               (17.28, 18.68, "EN *10 MINUTOS*, LISTO")]),
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
    d.textContent = text.replace(/ (\S+)$/, '\u00a0$1');
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
    t, ti, tf = job["titulo"]
    tareas.append(("t", t, dict(y=250), ti, tf, True))
    c, ci, cf = job["cartel"]
    tareas.append(("t" if job.get("cartel_arriba") else "c", c, dict(y=250 if job.get("cartel_arriba") else 940), ci, cf, True))
    for a, b, txt in job["subs"]:
        tareas.append(("s", txt, CAJA, a, b, False))
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


def editar(job):
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
    filtros.append(f"[0:a]afade=t=in:st=0:d=0.02,afade=t=out:st={fin_audio:.3f}:d=0.12[a]")
    salida = os.path.join(AQUI, job["salida"])
    args += ["-filter_complex", ";".join(filtros), "-map", ultimo, "-map", "[a]",
             "-c:v", "libx264", "-preset", "slow", "-crf", "16", "-profile:v", "high", "-pix_fmt", "yuv420p", "-r", "30",
             "-c:a", "aac", "-b:a", "192k", "-ar", "44100", "-movflags", "+faststart", "-t", f"{dur:.3f}", salida]
    subprocess.run(args, check=True)
    print(job["salida"], "listo")


if __name__ == "__main__":
    solo = sys.argv[3:]  # opcional: nombres de salida a rehacer
    for job in TRABAJOS:
        if not solo or job["salida"] in solo:
            editar(job)
