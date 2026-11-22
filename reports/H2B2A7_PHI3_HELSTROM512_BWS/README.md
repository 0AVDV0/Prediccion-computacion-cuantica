# H2B2A7 — Evidencia publicable del corte posterior a `13d3eaf`

Este directorio contiene **resultados agregados** de auditorías retrospectivas y de solo lectura, no datasets, pesos entrenables nuevos, estados complejos por muestra ni artefactos de QPU.

## Contenido

- `AUDITORIA_PHI3_EXHAUSTIVA_RESULTADO.json`: coincidencia composicional de Phi3 en 7.483 TRAIN + 1.069 VAL.
- `AUDITORIA_PHI3_COBERTURA_181_RESULTADO.json`: cobertura de los 8.399 triples, 181 normas incompletas, 292/777 composiciones vistas/nuevas.
- `AUDITORIA_HELSTROM512_EXHAUSTIVA_RESULTADO.json`: reconstrucción de 512 coordenadas para 8.552 filas, retención de norma y grupos.
- `AUDITORIA_OPERADOR_BWS_RESIDUOS_RESULTADO.json`: residuos en seis pares propios BWS y hash reciente del archivo de pesos.
- `MANIFIESTO_FUENTES_SHA256.csv`: identidades SHA-256 de fuentes históricas, **no** de estos JSON de publicación.

**Procedencia editorial.** Estas cuatro copias proceden de los informes históricos proporcionados para el corte del 22 de noviembre de 2026. En el JSON de BWS se sustituyó únicamente la ruta absoluta de usuario por un marcador y se añadió una nota de publicación; no es idéntico byte a byte al JSON local original. En la primera auditoría se normalizó el nombre de la copia que había sido subida como `(1)`; el contenido se preservó como JSON legible. Los archivos históricos siguen fuera de Git.

**No publicar como hecho:** 512 modos BWS verificados, reconstrucción OOF de pesos, optimalidad global, fecha exacta de generación, no contaminación composicional, capacidad predictiva validada o QPU. Ver documento [`08_PHI3_HELSTROM512_BWS_TRAZABILIDAD_20261122.md`](../../docs/investigacion/08_PHI3_HELSTROM512_BWS_TRAZABILIDAD_20261122.md).
