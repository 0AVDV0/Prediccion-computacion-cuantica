# H2B2A7 — Fase 3C.3: estabilidad del ranking

## Alcance
Solo INNER VAL previamente examinado: ranking del score B objetivo frente a Student 1E y 1F.
Sin entrenamiento, QPU, OUTER HOLD, etiquetas ni nueva AUC.

| Comparación | Spearman | Kendall τ-b | Inversiones (%) | Fracción pares con margen suficiente (%) |
|---|---:|---:|---:|---:|
| OBJETIVO_B vs STUDENT_1E | 0.913585 | 0.743855 | 12.806 | 67.202 |
| OBJETIVO_B vs STUDENT_1F | 0.911397 | 0.739330 | 13.032 | 65.688 |
| STUDENT_1E vs STUDENT_1F | 0.995589 | 0.943085 | 2.845 | — |

## Lectura correcta
Los pares de materiales con ranking invertido se miden entre todos los pares no ordenados.
La condición |sB(x)-sB(y)| > |Δs(x)|+|Δs(y)| es suficiente para preservar el orden de ese par; aquí se evalúa a posteriori sobre INNER VAL.
Las listas top-k comparan puntuaciones sin utilizar etiquetas; el porcentaje no mide precisión de clasificación.

## Limitaciones
El OUTER HOLD permanece excluido. Los experimentos y decisiones históricas ya habían usado INNER VAL. No hay estimaciones de generalización nueva.
No se infieren costos de circuitos, shots ni ventajas en hardware cuántico.
