# Prompts para pedir nuevas skills de ecommerce

Cómo usarlos: copiá el prompt entero y pegámelo en un mensaje nuevo. Yo armo la skill con la skill
`skill-creator`, la pruebo con los casos de prueba y te paso el archivo `.skill` para que lo subas a tus
skills (como hiciste con `validar-producto-ar`).

## Qué skill conviene hacer (en orden)
| # | Skill | Para qué | Por qué ahora |
|---|---|---|---|
| 1 | **analizar-campanas-meta-ar** | Leer tus resultados de Meta Ads y decirte qué anuncio cortar, cuál escalar y qué probar después | Vas a testear VERDEA y ORDI: es donde más plata se gana o se pierde, todos los días |
| 2 | **creativos-ugc-ar** | Armar guiones de video UGC, prompts de Flow y textos de anuncio con tu formato (3 bloques de 8 s, avatar sobre verde) | Lo pedís seguido y hoy depende de que yo recuerde el formato |
| 3 | **auditar-landing-ar** | Revisar una página de producto y darte los 5 cambios que más suben la conversión | Antes de pautar, para no tirar tráfico a una página que no vende |

---

## 1 · analizar-campanas-meta-ar (prompt completo)

```
Quiero que crees una skill nueva, con la skill skill-creator, igual de completa que validar-producto-ar.

NOMBRE: analizar-campanas-meta-ar

OBJETIVO: que, con los números reales de mis campañas de Meta Ads, me digas en lenguaje simple qué anuncios
cortar, cuáles mantener, cuáles escalar y qué probar después, para no quemar plata. Vendo en Argentina con
Shopify, Kaching Bundles y Meta Ads, en pesos. Tiene que ser honesta: si hay que frenar todo, que lo diga.

CUÁNDO SE ACTIVA (ponelo en la descripción, con muchas frases de ejemplo): cuando pego o subo un export del
Administrador de anuncios (CSV o Excel), mando capturas de mis campañas, o pregunto cosas como "¿cómo va mi
campaña?", "¿corto este anuncio?", "¿escalo?", "gasté $X y no vendo", "¿por qué no compran?", o menciono CPA,
ROAS, CTR, CPM o frecuencia, aunque no diga "analizar".

QUÉ RECIBE:
1. El export del Administrador de anuncios a nivel anuncio (columnas en español o en inglés): importe gastado,
   impresiones, alcance, frecuencia, CPM, clics en el enlace, CTR del enlace, CPC, reproducciones de 3 segundos,
   ThruPlays, agregados al carrito, pagos iniciados, compras, valor de las compras, ROAS. Si solo hay capturas,
   que las lea.
2. Los números del producto: precio de cada pack y costo. Si existe la carpeta de la marca, que lea el CPA de
   equilibrio de <MARCA>/validacion/; si no, que lo calcule con el script economia.py de validar-producto-ar.
3. Opcional: ventas en Shopify del mismo período, para controlar que el píxel mida bien.

PASOS:
1. Ordenar los datos (fechas, campaña, conjunto, anuncio) y avisar si faltan columnas importantes.
2. Controlar el seguimiento: si Shopify tiene ventas que Meta no muestra, avisar que el píxel o la API de
   conversiones está mal antes de opinar sobre los anuncios.
3. Calcular por anuncio: CPM, CTR del enlace, CPC, gancho (reproducciones de 3 s / impresiones), retención
   (ThruPlays / reproducciones de 3 s), tasa de carrito, tasa de compra, CPA, ROAS y ticket promedio.
4. Comparar contra el CPA y el ROAS de equilibrio del producto y contra el promedio de la propia cuenta.
   Las referencias generales (CTR del enlace menor a 0,8% = gancho flojo; gancho menor a 25%; frecuencia mayor
   a 2,5 en 7 días = público cansado) son orientativas y tienen que decirlo.
5. Encontrar dónde se cae la venta: en el anuncio (poco CTR o gancho flojo), en la página (muchos clics y pocos
   carritos), en la oferta o el precio (carritos sin compra) o en el público (frecuencia alta, CPM en aumento).
6. Decidir por anuncio con reglas claras:
   - NO TOCAR: gastó menos de 1 CPA de equilibrio (salvo CTR muy bajo con más de 2.000 impresiones).
   - CORTAR: gastó entre 1,5 y 2 veces el CPA de equilibrio sin ventas, o tiene CPA mayor a 1,5 veces el de
     equilibrio con 3 o más ventas.
   - ESCALAR: CPA menor al de equilibrio con 3 o más ventas → subir 20% por día como máximo.
   - ITERAR: buen gancho pero no vende, o vende pero el gancho es flojo → qué cambiar exactamente.
7. Proponer los próximos pasos: presupuesto de los próximos 3-4 días, 3 ideas de anuncios nuevos basadas en el
   ganador (mismo ángulo, otro gancho en los primeros 3 segundos) y cambios en la página o la oferta si hacen falta.

REGLAS:
- Cada número con su origen: [Meta], [Shopify], [Usuario], [Calculado] o [Estimado]. Nunca inventar datos.
- Si hay pocos datos, decir "todavía no alcanza para decidir" en vez de adivinar.
- Español rioplatense, simple; explicar cada término (CPA, ROAS, CTR, CPM) la primera vez en media línea.
- Respetar las reglas de cada marca (por ejemplo, VERDEA-huerta/CLAUDE.md: solo las buyer personas del test y
  CTA suave en las ideas de anuncios).

FORMATO DE LA RESPUESTA:
# [Marca] · Diagnóstico de campaña ([fechas])
## Semáforo: VERDE / AMARILLO / ROJO · [una línea con el porqué]
Confianza en los datos: alta / media / baja · [qué faltó]
## Qué hacer mañana (checklist corto)
## Resultados por anuncio (tabla: anuncio, gasto, CTR, gancho, CPC, carritos, compras, CPA, ROAS, decisión)
## Dónde se cae la venta
## Próximos anuncios para probar (3 ideas)
## Datos que me faltaron (con instrucciones exactas para exportarlos)

SCRIPT: incluí scripts/metricas.py, que lea el CSV o Excel del Administrador de anuncios (nombres de columna en
español o inglés), calcule las métricas, aplique las reglas de decisión con el CPA de equilibrio como parámetro
e imprima la tabla en markdown. Explicá en la skill cómo exportar el informe desde Meta paso a paso.

CASOS DE PRUEBA (armá datos de ejemplo para cada uno y probá la skill con y sin ella):
1. Un anuncio ganador y dos perdedores después de 4 días.
2. Mucho clic y casi ningún carrito: el problema es la página.
3. Hay ventas en Shopify pero Meta muestra 0 compras: el píxel está mal.
4. Día 1, muy poco gasto: la respuesta correcta es "no toques nada todavía".

DÓNDE GUARDARLA: en herramientas-skills/analizar-campanas-meta-ar/ (con SKILL.md, references/ y scripts/) y
el archivo empaquetado herramientas-skills/analizar-campanas-meta-ar.skill. Al final, subí todo a la rama.
```

---

## 2 · creativos-ugc-ar (prompt)

```
Creá con skill-creator una skill llamada creativos-ugc-ar.

OBJETIVO: armar el paquete de creativos para Meta Ads de cualquiera de mis marcas con mi formato de siempre.

SE ACTIVA cuando pido guiones, videos UGC, ganchos, prompts de Flow o Hedra, fondos B-roll, textos de anuncios
o "creativos" para una marca o producto.

RECIBE: la marca (lee su carpeta y su CLAUDE.md si existen), el producto, la oferta y las buyer personas; si no
hay buyer personas, que las arme primero (dolor, deseo, objeciones, frase).

ENTREGA, para cada buyer persona:
- 3 guiones de 3 bloques de 8 s (máximo ~20 palabras por bloque): problema → por qué pasa → solución con CTA suave.
- Prompt de la avatar sobre verde croma (#00FF00) para Flow, por secciones (FORMATO / ESCENA / SUJETO / ACCIÓN /
  CÁMARA / EVITAR), voz porteña con "vos", sin música y sin texto en pantalla.
- Prompts de fondos B-roll para cada bloque, muy específicos (con la sección EVITAR).
- Texto en pantalla con la oferta, texto principal y título del anuncio.
- Checklist de edición (CapCut, ElevenLabs Voice Changer para unificar la voz).

REGLAS: solo reseñas, números y antes/después reales; sin promesas de salud ni resultados garantizados; CTA suave
(nada de "comprá ya"); cada entrega dice para qué buyer persona es; respetar el CLAUDE.md de la marca.

CASOS DE PRUEBA: VERDEA (Lucía y Marta), ORDI (Caro y Silvia) y un producto nuevo sin buyer personas.
GUARDARLA en herramientas-skills/creativos-ugc-ar/ + el .skill, y subir a la rama.
```

---

## 3 · auditar-landing-ar (prompt)

```
Creá con skill-creator una skill llamada auditar-landing-ar.

OBJETIVO: revisar una página de producto antes de pautar y decirme qué cambiar para que venda más, en orden de
impacto.

SE ACTIVA cuando paso un link de mi tienda o de la competencia, un archivo HTML de landing, o pregunto "¿por qué
no me compran?", "¿está bien mi página?", "¿qué le cambio?".

PASOS: abrir la página en celular y en PC (con capturas), y puntuar de 0 a 100:
- Primera pantalla: se entiende qué es, para quién, el precio y el botón sin bajar.
- Oferta: packs, precio por unidad que baja, envío, cuotas, regalo.
- Prueba social: reseñas con foto, cantidad y que sean reales.
- Objeciones: preguntas frecuentes, garantía, cambios, tiempos de envío.
- Confianza: medios de pago, contacto, políticas.
- Velocidad y peso de imágenes, y que todo funcione en celular.
- Seguimiento: píxel de Meta y evento de compra.

ENTREGA: puntaje por bloque, los 5 cambios más importantes ordenados por impacto y esfuerzo, el texto o el
código listo para pegar de cada cambio, y lo que hace bien la competencia si paso su link.

REGLAS: no inventar reseñas ni números; español rioplatense; si la página es de mi repo, proponer el cambio
directo en el archivo.

CASOS DE PRUEBA: la landing de VERDEA, la de ORDI en modo prueba y una página con errores a propósito.
GUARDARLA en herramientas-skills/auditar-landing-ar/ + el .skill, y subir a la rama.
```

---

## Plantilla para pedir cualquier otra skill

```
Creá con skill-creator una skill llamada [nombre-en-minúsculas-con-guiones].
OBJETIVO: [qué problema me resuelve y qué decisión me ayuda a tomar]
SE ACTIVA cuando: [frases que yo diría, aunque no nombre la skill]
RECIBE: [links, archivos, números, capturas]
PASOS: [1, 2, 3…]
REGLAS: [cada dato con su fuente, nada inventado, español rioplatense, reglas de la marca]
ENTREGA (formato exacto): [secciones y tablas]
SCRIPT (si hay cuentas): [qué calcula]
CASOS DE PRUEBA: [3-4 situaciones reales]
GUARDARLA en herramientas-skills/[nombre]/ + el .skill, y subir a la rama.
```
