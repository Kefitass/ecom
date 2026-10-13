# Costos, fórmulas y alertas para Argentina

## Valores por defecto (VERIFICAR: cambian seguido)

Son referencias razonables para arrancar cuando el usuario no sabe sus números. Siempre
decí que son supuestos y preferí los porcentajes reales del usuario si los tiene.

| Concepto | Valor por defecto | Notas |
|---|---|---|
| Comisión de la pasarela (Mercado Pago u otra) | 7% del precio | Depende del plazo de acreditación y del plan; incluye IVA aprox. |
| Costo de ofrecer 3 cuotas sin interés | 8% del precio | Lo absorbe el vendedor; varía con las tasas. 6 cuotas: bastante más. |
| Comisión de la plataforma | 2% (Shopify sin pasarela propia) / 0–2% (Tiendanube) | Mercado Libre: 13–17% + costo fijo en precios bajos. |
| Impuestos sobre ventas (Ingresos Brutos, etc.) | 4% | Depende de la provincia y la condición fiscal. |
| Envío al cliente (si se ofrece gratis) | $6.000–$9.000 por paquete chico | Correo Argentino / Andreani / OCA; varía por zona y peso. |
| Empaque | $500–$1.500 | Caja, relleno, etiqueta. |
| Reserva por devoluciones/roturas | 3% del precio | Más alto en frágiles, talles o electrónica. |

## Fórmulas

Para un pedido con precio P (lo que paga el cliente):

```
costos_variables = costo_producto
                 + envío_absorbido
                 + empaque
                 + P × (pasarela + cuotas + plataforma + impuestos + devoluciones)

margen_contribución = P − costos_variables        (antes de publicidad)
margen_% = margen_contribución / P

CPA_equilibrio  = margen_contribución             (lo máximo que podés pagar en anuncios por venta sin perder)
ROAS_equilibrio = P / margen_contribución         (cuánto tiene que facturar cada $1 de anuncios para no perder)
```

**Precio para un margen objetivo** (por ejemplo 35% antes de anuncios):
```
P = (costo_producto + envío_absorbido + empaque) / (1 − suma_de_porcentajes − margen_objetivo)
```

**Packs**: recalculá con N unidades, el precio del pack y un solo envío/empaque. Los packs suelen
mejorar mucho el margen porque el envío y parte de la comisión se reparten entre más unidades.

## Cómo leer los resultados

- **ROAS de equilibrio ≤ 2** → hay mucho aire para pautar. Muy bueno.
- **ROAS de equilibrio entre 2 y 3** → viable con buenos creativos.
- **ROAS de equilibrio > 3** → difícil de escalar con Meta Ads; subí el precio, armá packs o buscá otro proveedor.
- **CPA de equilibrio < $8.000** en Argentina → muy ajustado: pocas ventas cubren el aprendizaje del algoritmo.

## Alertas regulatorias y de riesgo (Argentina)

No es asesoramiento legal: es una alerta para que el usuario verifique antes de vender.

- **ANMAT**: cosméticos, productos de higiene personal, suplementos dietarios, productos médicos
  y alimentos suelen requerir registro/habilitación.
- **SENASA**: fertilizantes, enmiendas, agroquímicos, fitosanitarios y productos para animales pueden
  requerir inscripción según su formulación.
- **ENACOM**: productos con radiofrecuencia (Bluetooth, WiFi, transmisores) requieren homologación.
- **Seguridad eléctrica**: artefactos eléctricos pueden requerir certificación.
- **Marcas de terceros**: réplicas o productos con logos/nombres registrados ajenos → no vender.
- **Promesas**: "cura", "elimina", "garantizado en X días" sin respaldo → riesgo legal (Defensa del
  Consumidor) y rechazo de anuncios en Meta.
- **Logística**: líquidos (derrames), vidrio (roturas), productos pesados o voluminosos (envío caro),
  talles (cambios y devoluciones).
