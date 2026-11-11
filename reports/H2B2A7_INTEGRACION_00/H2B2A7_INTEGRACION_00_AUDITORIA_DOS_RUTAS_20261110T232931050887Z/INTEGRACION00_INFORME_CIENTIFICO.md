# H2B2A7-INTEGRACION-00-v1.2 — Auditoría unificada de las arquitecturas

**Estado:** `REPLAY_PAULI_QWC_VERIFICADO_STUDENT_PENDIENTE`. Fecha UTC: 2026-11-10T23:29:33.076673+00:00.

## 1. Propósito y protección de la evaluación

- **No** se entrena, reoptimiza, transpila, consulta IBM o envía trabajo.
- Los scores OUTER HOLD en H2B2A7-13 **ya fueron evaluados**; aquí solamente se compara
  una reconstrucción independiente del score con la predicción previamente archivada.
- **No** seleccionar un nuevo modelo utilizando OUTER HOLD para volver a llamarlo validación independiente.
- Las métricas INNER VAL de teacher/student y las métricas OUTER HOLD de SAFE/QWC no
  son comparables como diferencias pareadas sin un split idéntico.

## 2. Procedencia y checkpoints

- Encontrados: **19/20**.
- Manifiesto H2B2A7-13 previo a OUTER: **COINCIDE**.
- Checkpoints mínimos faltantes: `[]`.
- Los archivos se identifican por nombre, ruta y SHA-256; una mera coincidencia de nombre
  no autentica por sí misma un checkpoint si falta su manifiesto original.

## 3. Auditoría de score

- Reconstrucción teacher: `baseline + suma(lambdas * t_target)`.
- Reconstrucción SAFE/QWC24/QWC64: fórmulas exactas del código H2B2A7-13,
  si existen los siete checkpoints originales, X6 y `predicciones_OUTER_HOLD.csv`.
- El replay verifica los índices y las etiquetas **sin reajustar pesos ni umbrales**.
- Student: **PARAMETROS_ENCONTRADOS_SCORE_NO_REPRODUCIDO**. Un QPY y sus parámetros no equivalen a scores
  reconstruidos para materiales sin preparación real de estados y decodificación de bits.

## 4. Costo completo vs incremental

La evaluación QWC24/QWC64 del H2B2A7-13 asignó 10 000 shots a la
parte incremental QWC. Las cuatro cabezas originales, el residual SAFE y las
características multicopia se trataron idealmente, por tanto no equivale al
costo completo por material.

La referencia H2B2A7-16, si existe su checkpoint, contiene una asignación
física-lógica de shots a las bases rho6 y copias rho4; se reporta por separado.
**No** convertir shots de subrutinas a segundos reales QPU sin circuitos ISA,
mezclas y tiempos de backend. No contar dos veces canales compartidos.

La corrección student rank-2 requiere considerar los dos decodificadores U,D,
los cuatro cabezales previos, los estados de entrada y las características rho4.
Dos decodificadores **no** equivalen a dos shots ni necesariamente a dos circuitos
por material si la preparación involucra mezcla de componentes.

## 5. Siguiente decisión metodológica

1. Completar archivos faltantes y resolver duplicados de SHA.
2. Certificar replay de scores y alinear particiones por `global_index`.
3. Auditar score de student en INNER VAL, sin usar OUTER para entrenamiento.
4. Obtener costo total por material, no solo número de bases o RXX.
5. Producir una comparación A/B de dos implementaciones congeladas en un split común.
6. Solo después preparar un piloto end-to-end y su autorización independiente.

## 6. Errores o reservas

- No hay fallos detectados en las comprobaciones ejecutadas.
