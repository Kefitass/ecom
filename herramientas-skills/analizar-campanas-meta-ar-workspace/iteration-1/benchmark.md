# Skill Benchmark: analizar-campanas-meta-ar

**Model**: subagente de Claude Code
**Date**: 2026-10-17T04:38:35Z
**Evals**: 1, 2, 3, 4 (1 run each per configuration)

## Summary

| Metric | With Skill | Without Skill | Delta |
|--------|------------|---------------|-------|
| Pass Rate | 100% ± 0% | 68% ± 16% | +0.32 |
| Time | 722.8s ± 105.7s | 592.6s ± 168.1s | +130.2s |
| Tokens | 203720 ± 23101 | 144992 ± 32808 | +58728 |
## Notas del análisis

- Las aserciones que separan a las dos configuraciones son casi todas de formato (semáforo, secciones, tabla, etiquetas de origen) más la de '3 ideas'. En las de decisión (cortar, escalar, no tocar, píxel, página) el baseline acertó en los 4 casos: el repo ya tiene mucho contexto (validación y plan de testeo de ORDI, análisis de VERDEA). Sin esa carpeta de marca la diferencia de criterio probablemente sería mayor (no medido).
- Costo de la skill: +22% de tiempo (+130 s) y +41% de tokens por corrida. Las respuestas con skill son más largas (11-13 mil caracteres contra 4,5-11 mil): se agregó un objetivo de 900-1.300 palabras.
- En VERDEA, las dos configuraciones encontraron prueba social inventada en la landing (estrellas, '+1.083 clientes', cartel de 'compró hace X min'). La skill no lo pedía explícitamente: se agregó revisar la landing de la marca cuando la venta se cae en la página.
- En ORDI, la corrida con skill recalculó el CPA de equilibrio con la mezcla real de packs ($17.800) en vez del valor interpolado por el script ($19.324): el script ahora deduce la mezcla de packs desde el valor de las compras.
- Una sola corrida por configuración: no se puede medir la variación entre corridas.
