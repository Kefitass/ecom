# Generador de CV + landing nueva: cómo subir todo

Son 4 pasos. Hacelos en este orden.

## 1. Subir el generador a una página oculta

1. Shopify → **Tienda online → Páginas → Agregar página**.
   - Título: **Generador de CV**. Contenido: vacío.
   - Abajo, en **Vista previa del motor de búsqueda → Editar**, poné como dirección `herramienta-cv-m30`.
   - Visibilidad: **Visible**. Guardá.
2. **Tienda online → Personalizar**. Arriba, en el selector de páginas: **Páginas → Crear plantilla**.
   - Nombre: **generador**. Basada en: **Página predeterminada**.
3. En esa plantilla, borrá las secciones que traiga (título y contenido de la página).
   Tocá **Agregar sección → Liquid personalizado**, pegá **todo** el contenido de `para-shopify.liquid.txt` y guardá.
4. Volvé a **Páginas → Generador de CV**. A la derecha, en **Plantilla de tema**, elegí **generador**. Guardá.
5. Probalo: `https://somosmetodo30.myshopify.com/pages/herramienta-cv-m30`

No la agregues a ningún menú: solo llega quien tiene el link.

## 2. Que el link le llegue a cada comprador

**Mail de entrega del ebook** (app de productos digitales → Configuración → plantilla del correo). Debajo del link de descarga:

```
🎁 BONUS: tu Generador de CV
Armá tu CV listo para pasar los filtros en 10 minutos:
https://somosmetodo30.myshopify.com/pages/herramienta-cv-m30
```

**Confirmación de pedido** (Configuración → Notificaciones → Confirmación de pedido → Editar código). Debajo del texto de agradecimiento:

```
<p>🎁 <b>BONUS:</b> armá tu CV listo para pasar los filtros con nuestro <a href="https://somosmetodo30.myshopify.com/pages/herramienta-cv-m30">Generador de CV</a>.</p>
```

## 3. Subir el video demo (opcional, recomendado)

1. **Contenido → Archivos → Subir archivos** → `demo-generador.mp4`.
2. Copiá el link del archivo (empieza con `https://cdn.shopify.com/…`).
3. En `ebooks-landing-snippet.txt`, buscá `video: ""` (en la parte «GENERADOR DE CV») y pegá el link entre las comillas.
   Si lo dejás vacío, la landing muestra una maqueta del generador.

## 4. Reemplazar el código de la landing

1. Donde tenés pegada la landing ahora (el bloque Liquid personalizado de la página del producto), borrá el código viejo.
2. Pegá todo `ebooks-landing-snippet.txt` y guardá.
3. Cambiá el **nombre del producto** a: **Conseguí trabajo en 30 días + Generador de CV**
   (Productos → el ebook → Título). El título de arriba de la página sale de ahí.

## Checklist final

- [ ] El link del generador abre y deja descargar el PDF.
- [ ] El mail de entrega tiene el link del generador.
- [ ] La landing muestra la sección «Tu CV listo para pasar los filtros en 10 minutos» arriba de todo.
- [ ] El producto se llama «… + Generador de CV».
