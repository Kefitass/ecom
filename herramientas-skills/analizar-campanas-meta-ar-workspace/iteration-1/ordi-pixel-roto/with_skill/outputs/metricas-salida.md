## Datos leídos [Meta]
- Período: 2026-10-07 a 2026-10-09 (3 días) · nivel: anuncio · números en formato 1.234,56 · moneda ARS
- Columnas encontradas: alcance, anuncio, campana, carritos, clics, compras, conjunto, cpc_meta, cpm_meta, ctr_meta, fecha_fin, fecha_inicio, frecuencia, gasto, impresiones, pagos, rep3s, thruplays, valor, visitas

## Resumen [Calculado]
| | |
|---|---|
| Gasto | $63.000 |
| Compras (Meta) | 0 |
| Ventas en Shopify [Usuario] | 7 |
| CPA con ventas de Shopify | $9.000 |
| CPA (costo por venta) | — |
| ROAS (facturación / gasto) | 0,00 |
| Ticket promedio | — |
| CPA de equilibrio [Calculado] con el pack de menor margen (todavía no hay ventas con valor) | $13.524 |
| ROAS de equilibrio | 2,58 |
| CTR del enlace · CPC · CPM | 1,58% · $256 · $4.054 |
| Frecuencia | 1,2 |

Margen por pack (= CPA de equilibrio de cada uno): x1 $34.900 → $13.524 · x2 $59.900 → $20.524 · x3 $79.900 → $15.724

**Semáforo sugerido: AMARILLO** · Meta no mide las compras: primero arreglar el píxel (con las ventas de Shopify el CPA real es $9.000)

## Resultados por anuncio
| Anuncio | Gasto | CTR | Gancho | CPC | Carritos | Compras | CPA | ROAS | Decisión |
|---|---|---|---|---|---|---|---|---|---|
| Caro 1 · Placard caos (dolor) (Caro · mujeres 25-40) | $21.350 | 1,88% | 36,9% | $222 | 13 | 0 | — | 0,00 | **NO DECIDIR** |
| Caro 3 · Se arman en 10 s (demo) (Caro · mujeres 25-40) | $20.980 | 1,43% | 31,1% | $266 | 10 | 0 | — | 0,00 | **NO DECIDIR** |
| Silvia 2 · Una caja para cada rincón (Silvia · mujeres 32-50) | $20.670 | 1,45% | 31,3% | $291 | 9 | 0 | — | 0,00 | **NO DECIDIR** |
| **Total cuenta** | $63.000 | 1,58% | 33,1% | $256 | 32 | 0 | — | 0,00 | AMARILLO |

### Por qué
- **Caro 1 · Placard caos (dolor) → NO DECIDIR**: Meta no está midiendo las compras: no se puede juzgar por ventas
- **Caro 3 · Se arman en 10 s (demo) → NO DECIDIR**: Meta no está midiendo las compras: no se puede juzgar por ventas
- **Silvia 2 · Una caja para cada rincón → NO DECIDIR**: Meta no está midiendo las compras: no se puede juzgar por ventas

## Embudo total
| Etapa | Cantidad | Tasa | Referencia (orientativa) |
|---|---|---|---|
| Impresiones | 15.540 | — |  |
| Clics en el enlace | 246 | 1,6% | flojo si < 0,8% |
| Visitas a la página | 215 | 87,4% | flojo si < 70,0% |
| Agregados al carrito | 32 | 14,9% | flojo si < 4,0% |
| Pagos iniciados | 19 | 59,4% | flojo si < 40,0% |
| Compras ⚠️ | 0 | 0,0% | flojo si < 40,0% |

Donde más se cae: **Compras** (0% de la referencia) → checkout, medios de pago o medición del evento de compra

Lectura: la gente compra (lo dice Shopify) pero Meta no lo ve: es un problema de medición, no de los anuncios ni de la página.

## Alertas
- MEDICIÓN: Shopify registró 7 ventas y Meta 0 compras. El píxel o la API de conversiones no está mandando el evento de compra. Arreglarlo antes de juzgar anuncios por ventas.

## Presupuesto sugerido (próximos 4 días)
| Conjunto | Quedan | Hoy por día | Día 1 | Día 2 | Día 3 | Día 4 |
|---|---|---|---|---|---|---|
| Caro · mujeres 25-40 | Caro 1 · Placard caos (dolor) (no decidir), Caro 3 · Se arman en 10 s (demo) (no decidir) | $14.110 | $14.110 | $14.110 | $14.110 | $14.110 |
| Silvia · mujeres 32-50 | Silvia 2 · Una caja para cada rincón (no decidir) | $6.890 | $6.890 | $6.890 | $6.890 | $6.890 |
| **Total** | | $21.000 | $21.000 | $21.000 | $21.000 | $21.000 |
- Con presupuesto por conjunto (ABO), cargá esa cifra en cada conjunto: es la suma de los anuncios que quedan, así que baja cuando apagás un perdedor aunque el ganador suba 20%. Con presupuesto de campaña (Advantage+), usá el total.
- No cambies presupuestos ni sumes anuncios hasta que Meta vuelva a ver las compras: sin eso no hay con qué decidir y el algoritmo optimiza a ciegas.
- Subir como máximo 20% por día; cambiar una cosa por vez para no reiniciar el aprendizaje de Meta.
