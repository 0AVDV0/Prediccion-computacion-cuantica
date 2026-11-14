# H2B2A7 Fase 3B — comparación descriptiva pareada

Analiza 7 pares identificados en 3A: 6 sobre OUTER HOLD archivado y 1 sobre INNER VAL.
Verifica SHA-256 de 3A, INTEGRACIÓN-00 e INTEGRACIÓN-01 antes de calcular.

## Regla de interpretación
- OUTER HOLD estaba **abierto**: estadísticas y bootstrap son **retrospectivos**. No son validación independiente nueva.
- Bootstrap pareado y estratificado por etiqueta en OUTER: percentiles 2.5/97.5 de la diferencia AUC condicionados a las muestras observadas.
- INNER VAL Student no contiene etiquetas en los archivos fuente: NO se recalcula AUC.
- TEACHER_S3_REFERENCIA_OUTER no equivale automáticamente al Teacher R3 completo.
- Correlaciones de ranking pueden ser altas aunque cambie la escala/calibración de los scores.
- Sin cambios en checkpoints, notebooks o informes previos; sin QPU ni entrenamiento.

## Valores retrospectivos OUTER

| Modelo | AUC recalculada (descriptiva) |
|---|---:|
| TEACHER_S3_REFERENCIA_OUTER | 0.92899819 |
| SAFE_ideal | 0.92508499 |
| QWC24_ideal | 0.91248910 |
| QWC64_ideal | 0.91779707 |

## Archivos
- 3B_COMPARACION_PAREADA.csv: correlaciones, diferencias, y cambios AUC solo donde hay etiquetas.
- 3B_AUC_OUTER_RETROSPECTIVAS.csv: AUC descriptivas de cuatro vectores OUTER.
- 3B_DIAGNOSTICO.json: procedencia y reservas.
- 3B_MANIFIESTO_SHA256.json: hash de los tres productos y de este informe.
