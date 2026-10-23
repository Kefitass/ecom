"""Splits the full manuscript (ebook.md) into two books.

ebook1.md  "Conseguí trabajo en 30 días"   → the 30-day plan (core chapters + toolbox)
ebook2.md  "Secretos de reclutador"        → the 4 bonus chapters + every "expert" subsection,
                                              with its own intro and closing checklist (ebook2_extra.md)

Usage: python3 split.py ebook.md
"""
import re, sys, os

here = os.path.dirname(os.path.abspath(__file__))
md = open(sys.argv[1], encoding="utf-8").read()
head, *chunks = re.split(r"^(?=## )", md, flags=re.M)
chapters = {c.split("\n", 1)[0][3:].strip(): c for c in chunks}


def find(prefix):
    return next(k for k in chapters if k.startswith(prefix))


def cut(text, start_heading, stop_heading):
    """Remove the run of ### subsections from start_heading up to (not incl.) stop_heading; return (rest, removed)."""
    i = text.index(start_heading)
    j = text.index(stop_heading, i)
    return text[:i] + text[j:], text[i:j]


cv_t, li_t, neg_t = find("Días 4–8"), find("Días 9–12"), find("Días 25–28")
cv, cv_x = cut(chapters[cv_t], "### Nivel experto: el CV", "### Los 12 errores")
li, li_x = cut(chapters[li_t], "### Nivel experto: cómo te busca", "### Tareas de los días 9–12")
neg, neg_x = cut(chapters[neg_t], "### Nivel experto: cómo funciona una banda", "### Día 28")
chapters[cv_t], chapters[li_t], chapters[neg_t] = cv, li, neg

# ---------- book 1 ----------
order1 = [k for k in chapters if not k.startswith(("Bonus", "Anexo"))]
book1 = "# Conseguí trabajo en 30 días\n\n" + "".join(chapters[k] for k in order1)

# ---------- book 2 ----------
extra = open(os.path.join(here, "ebook2_extra.md"), encoding="utf-8").read()
blocks = dict(re.findall(r"^%%(\w+)%%\n(.*?)(?=^%%\w+%%\n|\Z)", extra, flags=re.M | re.S))


def body(k):
    return chapters[k].split("\n", 1)[1].strip()


def retitle(title, text):
    return f"## {title}\n\n{text.strip()}\n\n"


b1, b2, b3, b4 = (find(f"Bonus {n}") for n in range(1, 5))
b4_body = body(b4).replace("La prueba de trabajo (Bonus 2)", "La prueba de trabajo (capítulo 4)")
book2 = "# Secretos de reclutador\n\n" + "".join([
    retitle("Introducción: lo que pasa del otro lado de la mesa", blocks["intro"]),
    retitle("Capítulo 1: Detrás de escena, cómo se decide realmente una contratación", body(b1)),
    retitle("Capítulo 2: El CV de nivel experto", blocks["cv_lead"] + "\n\n" + cv_x),
    retitle("Capítulo 3: LinkedIn por dentro, cómo te busca un reclutador", blocks["li_lead"] + "\n\n" + li_x.replace("### Nivel experto: cómo te busca un reclutador (y cómo aparecer primero)", "### Cómo te busca un reclutador (y cómo aparecer primero)")),
    retitle("Capítulo 4: Estrategias avanzadas para pasar primero en la fila", body(b2)),
    retitle("Capítulo 5: Entrevistas, evaluaciones y referencias de nivel experto", body(b3)),
    retitle("Capítulo 6: Negociación avanzada", blocks["neg_lead"] + "\n\n" + neg_x.replace("### Nivel experto: cómo funciona una banda salarial por dentro", "### Cómo funciona una banda salarial por dentro")),
    retitle("Capítulo 7: Situaciones especiales y cómo protegerte de estafas", b4_body),
    retitle("Caja de herramientas: el checklist del candidato experto", blocks["tools"]),
])
book2 = book2.replace("### Nivel experto: el CV como respuesta", "### El CV como respuesta")

open(os.path.join(here, "ebook1.md"), "w", encoding="utf-8").write(book1)
open(os.path.join(here, "ebook2.md"), "w", encoding="utf-8").write(book2)
print("ok", len(book1), len(book2))
