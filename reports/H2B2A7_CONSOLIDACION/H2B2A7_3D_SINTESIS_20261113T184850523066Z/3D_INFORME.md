# H2B2A7 — Síntesis científica 3D (retrospectiva)

## Alcance y trazabilidad

- Etapas auditadas: 5 (3A, 3B, 3C, 3C.3, 3C.4).
- Productos verificados: 22/22 SHA-256.
- Coincidencia exacta local: 22; coincidencia con blob Git por diferencia de checkout: 0.
- No se consultaron checkpoints locales de Tesis4 ni se ejecutaron circuitos.

## Predicción descriptiva: OUTER HOLD archivado

| Modelo | AUC retrospectiva |
|---|---:|
| TEACHER_S3_REFERENCIA_OUTER | 0.92899819 |
| SAFE_ideal | 0.92508499 |
| QWC24_ideal | 0.91248910 |
| QWC64_ideal | 0.91779707 |

Estas AUC pertenecen al OUTER HOLD ya examinado: no son validación independiente nueva.
No comparar estas AUC con las AUC Student de INNER VAL como prueba pareada.

## Ranking y observables: INNER VAL previamente examinado

| Comparación | Spearman | Kendall τ-b | Pares invertidos |
|---|---:|---:|---:|
| OBJETIVO_B vs STUDENT_1E | 0.913585 | 0.743855 | 12.806% |
| OBJETIVO_B vs STUDENT_1F | 0.911397 | 0.739330 | 13.032% |
| STUDENT_1E vs STUDENT_1F | 0.995589 | 0.943085 | 2.845% |

| Student | Error absoluto medio de score |
|---|---:|
| STUDENT_1E | 0.01490987 |
| STUDENT_1F | 0.01559087 |

En 3C se reconstruyó O=U†DU; la discrepancia matricial no equivale a discrepancia de expectativa.
La condición de margen de 3C.3 es suficiente para preservar el orden de un par, pero se aplicó a posteriori.

## Recursos conocidos, sin costos físicos completos

- Student: 504 puertas en dos decodificadores U, de las cuales 96 son RXX.
- QWC24/QWC64: 24/64 bases; 10000 shots incrementales rho6.
- QWC de referencia: 110000 shots lógicos planificados, no shots físicos ejecutados.
- No está certificado costo end-to-end comparable entre Student y QWC.

## Reservas metodológicas

- Los resultados OUTER son retrospectivos y el conjunto ya habia sido abierto.
- Las AUC OUTER no se comparan directamente con AUC INNER VAL de Student.
- Las 22 huellas verifican productos archivados, no una reevaluacion independiente.
- El ranking del score objetivo B no es una etiqueta FM/AFM.
- Los shots parciales de QWC y las puertas de dos U Student no son costos end-to-end equivalentes.
- No hubo ejecucion QPU ni entrenamiento nuevo.

## Próximas validaciones (no realizadas aquí)

Documentar procedencia histórica pendiente de 1F/OPS; diseñar costo end-to-end bajo mismo hardware; preparar protocolo de evaluación externa nueva sin reutilizar OUTER.
