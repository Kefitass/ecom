# Prompts de fotos para el ebook (ChatGPT / DALL·E, Midjourney, etc.)

Guardá cada imagen en `ebook/fotos/` con el nombre indicado (`.jpg` o `.png`) y volvé a generar el PDF.
Las fotos reemplazan solas a las ilustraciones. Las aperturas de los capítulos bonus son negras con dorado: pedí esas fotos con tonos oscuros y dorados.

**Estilo común (pegalo al final de cada prompt para que todas combinen):**
> Fotografía editorial realista, luz natural cálida, paleta de azul marino profundo con acentos naranja y dorado, profundidad de campo baja, estética premium y aspiracional, personas latinoamericanas diversas de 25 a 40 años, sin texto, sin logos, sin marcas de agua.

| Archivo | Formato | Prompt |
| --- | --- | --- |
| `portada.jpg` | Vertical 2:3 (1024×1536) | Persona joven profesional sonriendo con confianza, caminando por una oficina moderna luminosa con ventanales, sosteniendo una laptop, mirando hacia adelante. La mitad superior de la imagen con fondo despejado y oscuro para poner el título encima. |
| `cap0.jpg` (Introducción) | Horizontal 3:2 (1536×1024) | Persona sentada en un escritorio de casa ordenado a primera hora de la mañana, con café, cuaderno con un calendario de 30 días marcado y laptop abierta, actitud decidida. |
| `cap1.jpg` (Objetivo) | Horizontal 3:2 | Primer plano de manos escribiendo metas en un cuaderno con un pizarrón de notas adhesivas de fondo, ambiente de planificación y claridad. |
| `cap2.jpg` (CV) | Horizontal 3:2 | Currículum impreso moderno y prolijo sobre un escritorio de madera, junto a una lapicera y una laptop, una mano marcando con resaltador naranja. Sin texto legible. |
| `cap3.jpg` (LinkedIn) | Horizontal 3:2 | Persona tomándose una foto de perfil profesional con el celular frente a una pared clara, con luz natural de ventana, ropa de trabajo casual elegante. |
| `cap4.jpg` (Búsqueda y networking) | Horizontal 3:2 | Dos profesionales conversando de forma distendida con café en un evento de networking en un coworking moderno, se dan la mano y sonríen. |
| `cap5.jpg` (Entrevistas) | Horizontal 3:2 | Entrevista de trabajo en una sala de reuniones luminosa: candidata segura hablando y una entrevistadora escuchando con interés, ambiente positivo. |
| `cap6.jpg` (Negociación) | Horizontal 3:2 | Apretón de manos firme sobre una mesa de reunión con una carpeta de contrato y una lapicera, en una oficina elegante, sensación de acuerdo y éxito. |
| `cap7.jpg` (Cierre y primeros 90 días) | Horizontal 3:2 | Persona en su primer día de trabajo recibiendo una bienvenida de su nuevo equipo en una oficina moderna, todos sonriendo, con una credencial colgando del cuello. |
| `cap8.jpg` (Caja de herramientas) | Horizontal 3:2 | Vista cenital de un escritorio organizado con laptop mostrando una planilla, checklist en papel, lapiceras, notas adhesivas naranjas y una taza de café. |
| `bonus1.jpg` (Detrás de escena) | Horizontal 3:2 | Reclutadora revisando varios perfiles de candidatos en dos monitores en una oficina de recursos humanos de noche, luz cálida de escritorio, tonos oscuros y dorados. |
| `bonus2.jpg` (Estrategias avanzadas) | Horizontal 3:2 | Persona joven caminando con paso decidido por delante de una fila de personas que esperan, en un hall corporativo elegante, tonos oscuros y dorados, sensación de ventaja. |
| `bonus3.jpg` (Evaluaciones y referencias) | Horizontal 3:2 | Primer plano de una planilla de evaluación de entrevista con puntajes marcados sobre una mesa de reunión, una lapicera dorada y una taza de café, tonos oscuros y dorados. Sin texto legible. |
| `bonus4.jpg` (Situaciones especiales y estafas) | Horizontal 3:2 | Persona de unos 45 años revisando con atención un mensaje sospechoso en su celular, gesto pensativo, ambiente de casa con luz tenue y acentos dorados. |

**Consejos:**
- En las fotos de capítulo, lo importante tiene que quedar en la mitad de abajo: la parte de arriba se funde con el color del capítulo y ahí va el título.
- Si una foto sale con texto o con manos raras, pedí: "regenerá sin texto y con manos naturales".

## Cómo regenerar el PDF

```bash
cd ebook
python3 split.py ebook.md   # genera ebook1.md y ebook2.md
python3 build.py ebook1.md e1.html main && python3 build.py ebook2.md e2.html pro
NODE_PATH=$(npm root -g) node render.js "$PWD/e1.html" "$PWD/Consegui-trabajo-en-30-dias.pdf"
NODE_PATH=$(npm root -g) node render.js "$PWD/e2.html" "$PWD/Secretos-de-reclutador.pdf"
```
