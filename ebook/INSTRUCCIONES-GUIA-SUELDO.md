# Guía «Cuánto pedir de sueldo»: cómo subirla a Shopify

Archivos: `Cuanto-pedir-de-sueldo.pdf` (29 páginas) y `tapas/tapa-cuanto-pedir-de-sueldo.png`.

Precio suelto **$6.900**. Agregado en el carrito con el ebook: **$4.199** (lo aplica un descuento automático).

## 1. Crear el producto

**Productos → Agregar producto**

- **Título:** `Cuánto pedir de sueldo · Guía 2026`
- **Descripción:**

  > La guía para saber cuánto pedir y cómo negociarlo, sin quedarte corto ni quedar afuera.
  >
  > - Bruto, neto y cuánto cobrás en mano (aportes, aguinaldo y vacaciones).
  > - Cómo armar tu número: piso, objetivo y techo.
  > - Qué responder a «¿cuánto pretendés?» en cada etapa, con frases listas.
  > - Cómo negociar una oferta sin perderla.
  > - Inflación, ajustes y ofertas en dólares.
  > - Cómo pedir un aumento y qué hacer si te dicen que no.
  > - Caja de herramientas: calculadora, 10 frases y checklists.
  >
  > PDF de 29 páginas. Te llega por mail apenas se acredita el pago.

- **Multimedia:** subí `tapa-cuanto-pedir-de-sueldo.png`.
- **Precio:** `6900`. Sin precio de comparación.
- **Inventario:** destildá el seguimiento de inventario.
- **Envío:** desactivá «Es un producto físico».
- **Estado:** Activo, en el canal Tienda online.
- **Identificador de URL** (abajo, en «Publicación en motores de búsqueda»): `cuanto-pedir-de-sueldo`.
- **Guardar.**

## 2. Adjuntar el PDF

En el mismo producto, en el recuadro **Digital Products** (abajo), tocá **Agregar recurso** y subí `Cuanto-pedir-de-sueldo.pdf`. Así le llega por mail a quien lo compra, solo o como agregado.

## 3. El descuento automático que lo deja en $4.199

**Descuentos → Crear descuento → «Comprá X y llevate Y»**

- **Método:** Descuento automático.
- **Título:** `Guía de sueldo con tu ebook` (lo ve el cliente en el checkout).
- **Los clientes compran:** cantidad mínima de artículos `1`, de **productos específicos** → `Conseguí trabajo en 30 días + Generador de CV`.
- **Los clientes reciben:** cantidad `1`, de **productos específicos** → `Cuánto pedir de sueldo · Guía 2026`.
- **Valor del descuento:** **Monto de descuento por artículo** → `2701` (6.900 − 2.701 = 4.199).
- **Usos máximos por pedido:** `1`.
- **Combinaciones:** tildá **Descuentos de productos** y **Descuentos en pedidos**, así el código METODO30 de los lunes sigue funcionando.
- **Fecha de inicio:** hoy. Sin fecha de finalización.
- **Guardar.**

Revisá también el código **METODO30**: si hoy aplica a todos los productos, limitalo al ebook (Descuentos → METODO30 → Se aplica a → Productos específicos), así no se suma encima del precio de $4.199.

## 4. Activar la casilla en la landing

Avisame cuando el producto esté creado: yo saco el ID de la variante desde la tienda y te paso la landing con la casilla activada y la tapa puesta.

Si querés hacerlo vos: abrí `https://somosmetodo30.myshopify.com/products/cuanto-pedir-de-sueldo.js`, copiá el número que aparece en `"variants":[{"id":` y pegalo en `varianteId: ""`, dentro de `agregado`, en `ebooks-landing-snippet.txt`. Para la imagen, subí la tapa a **Contenido → Archivos**, copiá el link y pegalo en `imagen: ""`.

## 5. Probarlo

1. Abrí la landing, tildá la casilla y tocá **Quiero empezar hoy**.
2. Tiene que llevarte directo al checkout con el ebook elegido y la guía, y la guía tiene que figurar a **$4.199** con el descuento «Guía de sueldo con tu ebook».
3. Hacé una compra de prueba con un código del 100 % y fijate que te lleguen los dos PDF.
