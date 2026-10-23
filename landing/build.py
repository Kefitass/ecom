"""Builds the landing from template.html.

  preview.html                       → static preview with images embedded (for viewing)
  shopify/sections/landing-ebooks.liquid → Shopify section: images, prices and links editable in the theme editor

Usage: python3 build.py
"""
import base64, io, json, os
from PIL import Image

here = os.path.dirname(os.path.abspath(__file__))
tpl = open(os.path.join(here, "template.html"), encoding="utf-8").read()

IMAGES = {
    "IMG_HERO": ("fotos/hero.jpg", "img_hero", "Foto del hero", 1600),
    "IMG_PROBLEMA": ("fotos/problema.jpg", "img_problema", "Foto: el problema", 1200),
    "IMG_RESULTADO": ("fotos/resultado.jpg", "img_resultado", "Foto: el resultado", 1200),
    "IMG_COMBO": ("fotos/combo-fondo.jpg", "img_combo", "Fondo de la sección Secretos de reclutador", 1600),
    "IMG_TAPA1": ("../ebook/tapas/tapa-consegui-trabajo.png", "img_tapa1", "Tapa del ebook 1", 700),
    "IMG_TAPA2": ("../ebook/tapas/tapa-secretos-de-reclutador.png", "img_tapa2", "Tapa del ebook 2", 700),
}
TEXTS = {
    "PRECIO_SOLO": ("precio_solo", "Precio del ebook 1", "$18.000", "text"),
    "PRECIO_COMBO": ("precio_combo", "Precio del combo", "$27.000", "text"),
    "PRECIO_TACHADO": ("precio_tachado", "Precio tachado del combo (suma de los dos)", "$33.000", "text"),
    "AHORRO": ("ahorro", "Etiqueta de ahorro", "Ahorrás $6.000", "text"),
    "LINK_SOLO": ("link_solo", "Link del botón del ebook 1 (ej: /cart/ID_VARIANTE:1)", "#", "text"),
    "LINK_COMBO": ("link_combo", "Link del botón del combo (ej: /cart/ID_VARIANTE:1)", "#", "text"),
    "NOTA_PAGO": ("nota_pago", "Nota debajo de los precios", "Pago seguro con Mercado Pago · Acceso inmediato por mail", "text"),
    "FAQ_PAGO": ("faq_pago", "Respuesta de la pregunta de medios de pago", "Podés pagar con tarjeta de crédito, débito y dinero en cuenta de Mercado Pago. Las cuotas disponibles dependen de tu banco y se ven al pagar.", "textarea"),
}


def data_uri(path, width):
    im = Image.open(os.path.join(here, path)).convert("RGB")
    if im.width > width:
        im = im.resize((width, round(im.height * width / im.width)), Image.LANCZOS)
    buf = io.BytesIO()
    im.save(buf, "JPEG", quality=74, optimize=True)
    return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()


# ---------- preview ----------
prev = tpl
for key, (path, _, _, w) in IMAGES.items():
    prev = prev.replace("{{" + key + "}}", data_uri(path, w))
for key, (_, _, default, _) in TEXTS.items():
    prev = prev.replace("{{" + key + "}}", default)
prev = ('<title>Landing Conseguí trabajo</title>\n<meta name="claude:viewport-fit-sides" content="cover">\n'
        '<style>body{background:#fff;margin:0}</style>\n') + prev
open(os.path.join(here, "preview.html"), "w", encoding="utf-8").write(prev)

# ---------- shopify section ----------
liq = tpl
for key, (_, setting, _, w) in IMAGES.items():
    liq = liq.replace("{{" + key + "}}", "{%% if section.settings.%s != blank %%}{{ section.settings.%s | image_url: width: %d }}{%% endif %%}" % (setting, setting, w * 2 if w < 1000 else w))
for key, (setting, _, default, _) in TEXTS.items():
    liq = liq.replace("{{" + key + "}}", "{{ section.settings.%s | default: %s }}" % (setting, json.dumps(default, ensure_ascii=False)))
schema = {
    "name": "Landing ebooks empleo",
    "tag": "section",
    "settings": (
        [{"type": "header", "content": "Imágenes"}]
        + [{"type": "image_picker", "id": s, "label": label} for (_, s, label, _) in IMAGES.values()]
        + [{"type": "header", "content": "Precios y links"}]
        + [{"type": t, "id": s, "label": label, "default": d} for (s, label, d, t) in TEXTS.values()]
    ),
    "presets": [{"name": "Landing ebooks empleo"}],
}
out = os.path.join(here, "shopify", "sections")
os.makedirs(out, exist_ok=True)
open(os.path.join(out, "landing-ebooks.liquid"), "w", encoding="utf-8").write(
    liq + "\n{% schema %}\n" + json.dumps(schema, ensure_ascii=False, indent=2) + "\n{% endschema %}\n")
print("ok", os.path.getsize(os.path.join(here, "preview.html")))
