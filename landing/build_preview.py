"""Genera las vistas previas de la landing a partir del snippet.

  vista-previa.html   → abrir con doble clic (usa las fotos de la carpeta)
  ../.preview/landing-artifact.html (opcional, con --embed) → imágenes embebidas, para compartir

Uso: python3 build_preview.py [--embed SALIDA.html]
"""
import base64, io, os, re, sys
from PIL import Image

here = os.path.dirname(os.path.abspath(__file__))
snip = open(os.path.join(here, "ebooks-landing-snippet.txt"), encoding="utf-8").read()
open(os.path.join(here, "vista-previa.html"), "w", encoding="utf-8").write(
    "<!doctype html><html lang='es'><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'>"
    "<title>Vista previa · Landing ebooks</title></head><body>" + snip + "</body></html>")

if "--embed" in sys.argv:
    out = sys.argv[sys.argv.index("--embed") + 1]
    def uri(rel, width):
        im = Image.open(os.path.join(here, rel)).convert("RGB")
        if im.width > width:
            im = im.resize((width, round(im.height * width / im.width)), Image.LANCZOS)
        b = io.BytesIO(); im.save(b, "JPEG", quality=74, optimize=True)
        return "data:image/jpeg;base64," + base64.b64encode(b.getvalue()).decode()
    page = snip.replace("modoPrueba: false", "modoPrueba: true")
    for rel in sorted(set(re.findall(r'"((?:\.\./)?[\w/.-]+\.(?:jpg|png))"', page))):
        page = page.replace('"' + rel + '"', '"' + uri(rel, 700 if "tapa" in rel else 1400) + '"')
    page = ("<title>Landing Conseguí trabajo</title>\n<meta name=\"claude:viewport-fit-sides\" content=\"cover\">\n"
            "<style>body{background:#fff}</style>\n") + page
    open(out, "w", encoding="utf-8").write(page)
    print("embed", os.path.getsize(out))
print("ok")
