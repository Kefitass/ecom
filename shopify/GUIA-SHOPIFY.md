# Guía para cargar los ebooks en Shopify

Todo lo necesario para vender los dos ebooks y darle a cada comprador acceso a su versión interactiva. Seguilo en orden: son unos 60 a 90 minutos la primera vez.

**Qué vas a tener al final:**
- La página del producto con la landing (ebook solo o combo).
- Pago, mail de compra y PDF automáticos.
- Una biblioteca "Mis ebooks" donde cada comprador lee la versión interactiva de lo que compró, con checklists para tildar. Quien no compró no puede verla.

---

## 0. La marca: Método 30

- *Configuración → Detalles de la tienda*: nombre de la tienda **Método 30**.
- *Tienda online → Temas → Personalizar → Encabezado*: logo `marca/logo-metodo30.png` (o `logo-metodo30-blanco.png` si tu encabezado es oscuro).
- *Configuración del tema → Logo → Favicon*: `marca/icono-metodo30.png`. El mismo ícono sirve como foto de perfil de Instagram.

## 0B. Las páginas de la tienda (inicio, catálogo, contacto y pie)

Son secciones nativas, igual que las de Verdea, para el tema **ecom-x** (o Dawn). Para cada una: *Editar código → Sections → Agregar una nueva sección*, poné el nombre, borrá lo que trae, pegá el archivo y guardá.

| Nombre de la sección | Archivo | Dónde se agrega en *Personalizar* |
| --- | --- | --- |
| `metodo30-inicio` | `tienda/metodo30-inicio.liquid` | Página de inicio → ocultá las secciones del tema → Agregar sección → "MÉTODO 30 · Inicio" |
| `metodo30-catalogo` | `tienda/metodo30-catalogo.liquid` | Arriba al medio elegí "Colecciones" → ocultá las del tema → "MÉTODO 30 · Catálogo" |
| `metodo30-contacto` | `tienda/metodo30-contacto.liquid` | "Páginas" → "contact" → ocultá las del tema → "MÉTODO 30 · Contacto" |
| `metodo30-footer` | `tienda/metodo30-footer.liquid` | Pie de página → ocultá el del tema → "MÉTODO 30 · Pie de página" |

En cada sección elegí el producto, las tapas y la foto de portada desde el editor. Completá el WhatsApp, el mail, las redes y el link del botón de arrepentimiento. Los precios del inicio y del catálogo salen solos del producto.

**Reseñas en el inicio:** agregá bloques "Testimonio (real)" solo con reseñas reales. Sin bloques, la sección no aparece.

**Menú:** en *Tienda online → Menús → Menú principal*, dejá Inicio, Catálogo y Contacto. "Mis ebooks" conviene agregarlo también, para que el comprador lo encuentre fácil.

## 1. Subí los archivos

*Contenido → Archivos → Subir archivos*

| Archivo (en el repo) | Para qué |
| --- | --- |
| `ebook/tapas/tapa-consegui-trabajo.png` | Tapa en la biblioteca y en la landing. **No le cambies el nombre** |
| `ebook/tapas/tapa-secretos-de-reclutador.png` | Ídem. **No le cambies el nombre** |
| `landing/fotos/problema.jpg`, `resultado.jpg`, `combo-fondo.jpg` | Secciones de la landing |
| `landing/fotos/hero.jpg` | Foto para la galería del producto |

Después de subir cada uno, copiá su URL (botón de copiar link): la vas a pegar en la landing (paso 7).

## 2. Creá el producto

*Productos → Agregar producto*

- **Título:** Conseguí trabajo en 30 días
- **Fotos:** tapa del ebook 1, foto del hero, tapa del ebook 2 (en ese orden)
- **Variantes:** agregá la opción **"Formato"** con dos valores:

| Variante | Precio | Precio de comparación |
| --- | --- | --- |
| Ebook | $18.000 | (vacío) |
| Combo 2 ebooks | $27.000 | $33.000 |

- En cada variante: **destildá "Es un producto físico"** (no requiere envío) y **destildá "Seguir cantidad"**, así nunca se agota.
- Guardá. Revisá que el handle de la URL sea `consegui-trabajo-en-30-dias`. Si es otro, avisame o cambiá `PRODUCT_URL` en `shopify/build_shopify.py`.
- **Anotá el ID de cada variante:** entrá a cada variante y copiá el número del final de la URL del navegador (`…/variants/123456789`). Lo necesitás en el paso 7.

## 3. Entrega automática del PDF

1. Instalá la app gratuita **Digital Downloads** (de Shopify) desde la tienda de apps.
2. En la app, buscá el producto y adjuntá:
   - Variante **Ebook** → `Consegui-trabajo-en-30-dias.pdf`
   - Variante **Combo 2 ebooks** → los dos PDF
3. Shopify manda el link de descarga en el mail de confirmación y en la página de "gracias".

## 4. Activá las cuentas de cliente

*Configuración → Cuentas de cliente* → activá las cuentas de cliente y mostrá los links de inicio de sesión en la tienda.

Es lo que permite que el comprador entre a "Mis ebooks" con su mail.

## 5. Etiquetá a cada comprador con Shopify Flow

La biblioteca da acceso según la **etiqueta** del cliente: `ebook1` abre el ebook 1 y `ebook2` abre el ebook 2.

1. Instalá **Shopify Flow** (gratis) y creá un flujo nuevo.
2. **Disparador:** "Pedido pagado" (Order paid).
3. **Condición:** algún artículo del pedido tiene el título de variante igual a `Combo 2 ebooks`.
   - **Si se cumple →** acción "Agregar etiquetas de cliente": `ebook1, ebook2`
   - **Si no →** segunda condición: algún artículo tiene el título de producto `Conseguí trabajo en 30 días` → acción "Agregar etiquetas de cliente": `ebook1`
4. Activá el flujo.

**Plan B manual:** en *Clientes*, abrí al cliente y agregale las etiquetas a mano. Sirve si alguien escribe que no puede entrar.

## 6. Subí las páginas de la biblioteca al tema

*Tienda online → Temas → (⋯) → Editar código → carpeta Templates → Agregar una nueva plantilla*

Creá estas tres. En cada una elegí **page** y el tipo **liquid** (no JSON), escribí el nombre, pegá TODO el contenido del archivo y guardá.

| Nombre | Archivo para pegar |
| --- | --- |
| `ebook-1` | `shopify/templates/page.ebook-1.liquid` |
| `ebook-2` | `shopify/templates/page.ebook-2.liquid` |
| `mis-ebooks` | `shopify/templates/page.mis-ebooks.liquid` |

Después, en *Tienda online → Páginas*, creá tres páginas (el contenido puede quedar vacío):

| Título | Plantilla | La URL tiene que terminar en |
| --- | --- | --- |
| Conseguí trabajo en 30 días | `page.ebook-1` | `/pages/consegui-trabajo-en-30-dias` |
| Secretos de reclutador | `page.ebook-2` | `/pages/secretos-de-reclutador` |
| Mis ebooks | `page.mis-ebooks` | `/pages/mis-ebooks` |

La URL (handle) se edita abajo de todo, en "Vista previa del motor de búsqueda". **Tiene que ser exacta.**

No agregues estas páginas al menú: el acceso es solo desde el mail y la biblioteca.

## 7. Instalá la landing en la página del producto

1. En *Editar código → Snippets → Agregar un nuevo snippet*, creá `ebooks-landing` y pegá todo `landing/ebooks-landing-snippet.txt`.
2. En el **panel de configuración** del principio del snippet, completá cada dato marcado con ⚠️:
   - `slugURL`: la URL completa del producto.
   - `varianteId` del Ebook y del Combo (los IDs del paso 2).
   - Las URLs de las imágenes (paso 1). Las tapas también van ahí.
   - La respuesta de medios de pago.
3. En *Tienda online → Temas → Personalizar*, abrí la plantilla del producto. Dentro de "Información del producto", agregá un bloque **Liquid personalizado** con esta única línea:

```liquid
{% render 'ebooks-landing' %}
```

4. Guardá y abrí el producto en la tienda para revisarlo en el celular y en la compu.

## 8. Sumá el link de la biblioteca al mail de compra

*Configuración → Notificaciones → Confirmación del pedido → Editar código.* Pegá esto donde quieras que aparezca, por ejemplo después del saludo:

```liquid
<p style="font-size:16px;line-height:1.5">
  <strong>Tu versión interactiva ya está lista.</strong><br>
  Entrá con este mismo mail a
  <a href="{{ shop.url }}/pages/mis-ebooks">{{ shop.url }}/pages/mis-ebooks</a>
  para tildar las tareas del plan y copiar las plantillas.
</p>
```

## 9. Pagos y aspectos legales

- **Pagos:** en *Configuración → Pagos*, activá **Mercado Pago** como proveedor para cobrar en pesos y en cuotas.
- **Políticas:** en *Configuración → Políticas*, cargá términos y política de reembolso. Aclará que es un producto digital de entrega inmediata.
- **Botón de arrepentimiento:** en Argentina, las tiendas online tienen que mostrar un "Botón de arrepentimiento" en la home (Resolución 424/2020). Si todavía no lo tenés, revisalo con tu contador o abogado.

## 10. Probá todo antes de publicar anuncios

1. Creá un código de descuento del 100%, de un solo uso.
2. Comprá el **Ebook** con un mail tuyo y revisá:
   - que llegue el mail con el PDF y el link a la biblioteca;
   - que el cliente tenga la etiqueta `ebook1` (*Clientes*);
   - que `/pages/mis-ebooks` muestre el ebook 1 para leer y el ebook 2 bloqueado;
   - que `/pages/secretos-de-reclutador` pida comprarlo.
3. Repetí con el **Combo** y otro mail: tienen que abrirse los dos.
4. Abrí `/pages/consegui-trabajo-en-30-dias` en una ventana de incógnito: tiene que pedir iniciar sesión.

## 11. Cuando tengas reseñas reales

En el panel de la landing (`testimonios`), reemplazá los ejemplos por reseñas reales, con permiso de cada persona, y borrá `ejemplo: true`. Los ejemplos se ven solo en la vista previa: en la tienda, la sección aparece recién cuando hay reseñas reales. Hasta tres reseñas alcanzan.

---

### Cómo regenerar los archivos si cambia el contenido

```bash
cd ebook
python3 split.py ebook.md
python3 build_web.py ebook1.md web.html main
python3 build_web.py ebook2.md web2.html pro
cd ../shopify && python3 build_shopify.py
cd ../landing && python3 build_preview.py
```

Después volvé a pegar las plantillas que cambiaron (paso 6).
