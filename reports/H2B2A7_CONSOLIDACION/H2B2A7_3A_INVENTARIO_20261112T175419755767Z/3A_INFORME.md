# H2B2A7 Fase 3A — Inventario científico

Este informe SOLO organiza evidencia ya certificada en INTEGRACIÓN-00 e INTEGRACIÓN-01.
No introduce una evaluación independiente nueva ni recalcula AUC.

- Integridad: **7/7** y **6/6** hashes de informes correctos.
- Coberturas: **9**. Pares con scores bajo un mismo split: **7**.
- OUTER HOLD ya examinado: **1497** registros con etiquetas y scores.
- INNER VAL ya examinado: **1198** registros por Student, sin etiquetas en este CSV.
- Coincidencia de índices entre ambos CSV: **0**, sin autorización para mezclar splits.

## Limitaciones
- INNER VAL y OUTER HOLD NO son el mismo split, aunque sus métricas puedan tener el mismo nombre
- OUTER HOLD ya estaba abierto: cualquier comparación es retrospectiva/descriptiva
- HEAD4_SAFE tiene solo resumen en la evidencia disponible, no score individual para comparación pareada
- Las AUC Student son históricas, no fueron recalculadas por esta fase de inventario
- No se mide costo QPU ni se entrena un modelo
- No hay etiquetas de INNER VAL en el CSV Student consolidado
- La identidad de Student 1F sigue sin hash histórico anterior ni QPY original cotejado

## Archivos
- `3A_MATRIZ_COBERTURA.csv`: disponibilidad de evidencia individual o resumida por modelo/split.
- `3A_PARES_COMPARABLES.csv`: únicamente pares con muestras de la misma partición.
- `3A_DIAGNOSTICO.json`: integridad y conteos.
- `3A_MANIFIESTO_SHA256.json`: huellas de los tres productos anteriores y este informe.

Para futuras etapas: no comparar AUC de INNER VAL frente a AUC de OUTER HOLD como prueba pareada.
