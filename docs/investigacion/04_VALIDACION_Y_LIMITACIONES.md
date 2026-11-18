# H2B2A7 — Validación científica, amenazas a la validez y criterios de confirmación

> **Estado:** borrador metodológico v0.3, actualizado el 18 de noviembre de 2026. **No describe una nueva evaluación ejecutada ni certifica generalización o ventaja cuántica.**
>
> **Rama de destino:** `feature/h2b2a7-documentacion-cientifica`.
>
> **Propósito:** distinguir la validez algebraica y la reproducibilidad de resultados archivados de la independencia estadística de las evaluaciones; fijar el significado admisible de cada resultado y especificar las condiciones de una futura prueba prospectiva.

## 1. Alcance y relación con la documentación existente

Este documento complementa, sin sustituir, la [arquitectura](01_ARQUITECTURA_H2B2A7.md), el [linaje experimental](02_LINEAJE_EXPERIMENTAL.md) y la [matriz de evidencia](03_MATRIZ_DE_EVIDENCIA.md). Los identificadores `E01`–`E27` corresponden a la matriz; conservan sus reservas y no se elevan de categoría por estar mencionados aquí.

Los procedimientos estudiados emplearon varias representaciones, particiones y estrategias de medición. **No existe una única AUC «de H2B2A7» que pueda agruparlas sin identificar el modelo, la fuente de supervisión, las muestras y el protocolo.**

### 1.1. Cinco preguntas distintas

| Pregunta | Ejemplo de evidencia adecuada | Qué no demuestra |
|---|---|---|
| ¿El archivo es el mismo? | Hash de artefacto y manifiesto preexistente | Que el método sea estadísticamente válido |
| ¿La transformación es correcta? | Reconstrucción del score, equivalencia de matrices o tests numéricos | Independencia del conjunto evaluado |
| ¿El predictor funciona en las muestras retenidas? | Predicciones y etiquetas alineadas en un protocolo sin selección sobre el hold | Generalización a composiciones nunca vistas, si los grupos se solapan |
| ¿La arquitectura generaliza a grupos químicos nuevos? | Evaluación agrupada, anidada y con pipeline completo entrenado dentro de los folds | Ventaja sobre un baseline no comparado |
| ¿Hay ventaja física cuántica? | Protocolo y costo end-to-end homogéneos, más evidencia física pertinente | La ventaja a partir de AUC idealizadas o shots parciales |

## 2. Jerarquía de particiones y alcance de las métricas

### 2.1. Distinciones del archivo histórico

El historial describe un CORE de `7.483` materiales utilizado en las etapas de entrenamiento y análisis, además de particiones históricas de validación (`1.069`) y prueba (`2.139`) de una versión de `10.691` registros. Estas cantidades **no autorizan** a afirmar que las particiones adicionales permanezcan vírgenes ni que todas las versiones del dataset tengan filas idénticas (E01).

En el piloto H2B2A0, dentro de los `7.483` registros se identificaron:

| Partición del piloto | Cantidad | Relación |
|---|---:|---|
| `outer_train` | 5.986 | Incluye `inner_train` e `inner_val` |
| `outer_hold` | 1.497 | Disjunto del `outer_train` por índice; históricamente ya consultado |
| `inner_train` | 4.788 | Subconjunto del `outer_train` |
| `inner_val` | 1.198 | Subconjunto del `outer_train` |

El teacher R3 había sido ajustado utilizando `outer_train` **antes** de crear `inner_val`. Por tanto, su AUC sobre `inner_val` —`0,978803438` en el registro histórico— no mide independencia estadística de ese teacher. La separación de índices entre `inner_train` e `inner_val` **no deshace** el ajuste previo (E11).

### 2.2. AUC conservadas y uso permitido

| Resultado archivado | Evaluación histórica | AUC | Interpretación admisible |
|---|---|---:|---|
| H1 Helstrom | Predicciones OOF históricas, con reservas de procedencia upstream | ≈0,907406 | Soporte de ajuste por fold y coherencia de cachés, no certificación completa de la cadena |
| Observable O★ H2B1E1 | Media de cinco AUC sobre holds | 0,923686699 | Diagnóstico retrospectivo de representación |
| C5 H2B1E3 | Media de cinco AUC sobre holds | 0,921981265 | Exploración retrospectiva de compresión |
| Student 1E | `inner_val`, n=1.198, ya examinado | 0,913537480155041 | Replay de la AUC agregada histórica |
| Student 1F | `inner_val`, n=1.198, ya examinado | 0,9159889583363131 | Replay de la AUC agregada histórica |
| `TEACHER_S3_REFERENCIA_OUTER` | `outer_hold`, n=1.497, ya examinado | 0,92899819 | Resultado descriptivo del objeto archivado con ese nombre |
| SAFE ideal | `outer_hold`, n=1.497, ya examinado | 0,92508499 | Resultado descriptivo retrospectivo |
| QWC24 ideal | `outer_hold`, n=1.497, ya examinado | 0,91248910 | Resultado descriptivo retrospectivo |
| QWC64 ideal | `outer_hold`, n=1.497, ya examinado | 0,91779707 | Resultado descriptivo retrospectivo |

**Reglas:** no restar AUC de Student `inner_val` y QWC/SAFE `outer_hold` para alegar una mejora pareada; no equiparar `TEACHER_S3_REFERENCIA_OUTER` con cualquier objeto `R3` sin cotejar checkpoint e índices; no considerar la coincidencia de una AUC agregada como prueba de identidad de todos los scores individuales (E12–E15).

## 3. Amenazas a la validez identificadas

### 3.1. Supervisión antes de la validación (E02–E04)

En la ruta histórica 3K/4F, una base de coordenadas Helstrom de 512 componentes fue ajustada de manera supervisada sobre las `7.483` muestras CORE de entrenamiento. La validación posterior de un predictor **no es OOF del pipeline completo** cuando su representación ya incorporó etiquetas de las muestras retenidas. Los AUC históricos próximos a `0,965419` y `0,971824` pertenecen a ese protocolo y no se deben reetiquetar como independientes.

H1 presenta evidencia más fuerte de ajuste Helstrom específico de cada fold y predicciones OOF coherentes con cachés. La ausencia de identificadores históricos exhaustivos de entrada limita la certificación retrospectiva del pipeline completo; tampoco permite extrapolar automáticamente esta seguridad a rutas distintas.

### 3.2. Selección retrospectiva de complejidad (E05–E10)

La transferencia observada del observable es `O_FOLDS_H2B1A` → `OSTAR_FOLDS_H2B1E0` → `OSTAR_FOLDS_H2B1E1`. **Actualización:** los cinco $O_f^\star$ archivados en H2-B0 se reconstruyeron desde `B_LABEL_KRR` H2-A4, usando exclusivamente vectores de coeficientes TRAIN, con error máximo de elemento $3.506\times10^{-7}$ y sin consulta de etiquetas/AUC HOLD; los cinco conjuntos HOLD complementarios son disjuntos y exhaustivos (E19–E20). Esta evidencia identifica y reproduce el origen H2-A4→H2-B0, pero no verifica directamente la memoria de todas las transferencias ni autentica integralmente la procedencia de la preparación *upstream*.

La descomposición de diez canales presenta verificaciones de reconstrucción de score dentro de la representación implementada (E07). La configuración fija C5 se compone de `II`, `IY`, `IZ`, `XY` y `ZZ` (E08). La exploración de 1.023 subconjuntos incluyó una frontera por `mean_hold_AUC` para estudiar complejidad. Aunque seleccionar un subconjunto dentro de cada fold mediante entrenamiento es diferente de usar su hold para tomar decisiones globales, **la posterior elección de C5 no debe describirse como confirmatoria sin una historia de decisión independiente del hold** (E09).

El fragmento de ALS R3 examinado utiliza factores y objetivos sobre índices del entrenamiento externo. Esto limita el riesgo de uso **directo** del hold en ese ajuste. Sin embargo, H2-A4 eligió el *método ganador* entre A/B/C utilizando la media AUC de OUTER HOLD, y H2-B0 disponía de una ruta de recuperación/orientación de coeficientes guiada por esa AUC (E21). El cotejo independiente E20 muestra que la orientación HOLD **no era necesaria para reproducir las matrices observadas**, pero no hace confirmatorios los resultados del ganador ni el carácter exploratorio de canales, rango y variantes (E10).

### 3.3. Solapamiento químico entre particiones (E01, E18)

Separar filas o índices no garantiza separar materiales por composición química. Composiciones repetidas y registros con etiquetas FM/AFM contradictorias pueden aparecer en el dataset histórico. Por ello, un AUC estimado con división aleatoria por fila no responde automáticamente a «¿generaliza a composiciones químicas inéditas?».

Se necesita definir una **clave de composición canónica antes de los splits** y decidir explícitamente cómo tratar duplicados, fórmulas equivalentes y contradicciones de etiquetas. No debe descartarse ninguna discrepancia silenciosamente ni ajustarse esa regla usando el resultado del conjunto retenido.

### 3.4. Reutilización de particiones en el desarrollo (E11–E15)

El mismo `outer_hold` se utilizó históricamente para diagnósticos de distintos candidatos, ablations y complejidades. Por tanto, una evaluación posterior sin reentrenamiento puede reproducir correctamente valores anteriores, pero **no se transforma en una prueba prospectiva nueva**.

Del mismo modo, `inner_val` fue usado durante el desarrollo de estudiantes. La reconstrucción numérica de INTEGRACIÓN-01 es valiosa para comprobar implementación y reproducibilidad, pero su resultado no se convierte retrospectivamente en test final.

## 4. Qué quedó respaldado por las integraciones de Git

### 4.1. Reproducibilidad de INTEGRACIÓN-00 (E12)

El [informe INTEGRACIÓN-00](../H2B2A7_INTEGRACION_00.md) describe un replay de scores congelados del Teacher, HEAD4+SAFE, SAFE y rutas QWC. La verificación de integridad y la concordancia de valores respaldan **fidelidad de reconstrucción respecto de los artefactos comparados**. No se ejecutó IBM Quantum, no se reentrenó y no se confirmó costo end-to-end.

### 4.2. Reproducción de Student 1E/1F (E13)

La [INTEGRACIÓN-01](../H2B2A7_INTEGRACION_01.md) reporta `94/94` pruebas numéricas satisfactorias, igualdad de AUC agregadas en `inner_val` y reconstrucción de observables `O_j = U_j^† D_j U_j`. Se verificó un QPY original de Student 1E; **no** se cotejó un QPY histórico propio de 1F ni un vector de scores históricos individualmente pareado para ambos.

Una distancia matricial `||O_j - B_j★||` y un error de expectativa `Tr[ρ(O_j-B_j★)]` son magnitudes distintas. Las verificaciones de puntuación y ranking deben conservar su conjunto, norma, escala y criterio de comparación.

### 4.3. Consolidación retrospectiva 3A–3D (E14–E16)

La [síntesis 3D](../../reports/H2B2A7_CONSOLIDACION/H2B2A7_3D_SINTESIS_20261113T184850523066Z/3D_INFORME.md) documenta `22/22` productos con SHA-256 verificado. Su alcance comprende comparaciones, errores de expectativas, inversión de ranking y recursos parciales. **Hash válido no es validez estadística.**

La [fase 3C.4](../H2B2A7_FASE_3C4_GUIA.md) registra 504 puertas lógicas en dos decodificadores U Student, de ellas 96 RXX, además de 24/64 bases QWC y presupuestos lógicos de shots. Estos conteos **no** incluyen un presupuesto físico homogéneo de preparación, transpilation/ISA, ejecución, medición y lectura por material.

### 4.4. Evidencia QPU (E17)

La matriz de evidencia menciona resultados del programa histórico 19X, cuyos artefactos completos aún **no están integrados a esta rama documental**. En consecuencia, aquí solo se conserva el dictamen de alcance: **no hay base documental integrada para afirmar una ventaja cuántica confirmada**. Cualquier valor de significación o resultado QPU específico deberá citar su protocolo, artefacto y versión antes de incorporarse como conclusión.

### 4.5. Certificaciones no invasivas A0–A4-1A (E22–E27)

La nueva consolidación [05_RESULTADOS_Y_AUDITORIAS_H2B2.md](05_RESULTADOS_Y_AUDITORIAS_H2B2.md) distingue explícitamente cuatro tipos de constatación:

1. **Identidad de artefacto y checkpoint:** cotejo SHA256, parámetros congelados y arrays correspondientes a cada barrido seleccionado.
2. **Reconstrucción matemática y física:** recomputación de objetivos en `INNER TRAIN/VAL`, expectativas desde `PSI7` sobre submuestras y controles Fourier locales con coeficientes fijos.
3. **AUC histórica:** lectura de resultados guardados de `INNER VAL`, que se había empleado para seleccionar variantes y no constituye prueba nueva.
4. **Hipótesis de expresividad:** el contraste entre cabezales restringidos y el observable Pauli general *sugiere* información adicional accesible, pero no aísla causalmente capacidad, regularización, selección y coste físico.

La auditoría A1 mostró una mejoría retrospectiva al añadir no linealidad en el decodificador **sin cambiar circuitos**. A2 aportó un cuarto cabezal, A3 añadió puertas RZ/Cartan, y A4-0 ensayó H5; sus ganancias AUC frente a A2 fueron modestas. A4-1A alcanzó históricamente AUC `0.939362387` frente a `0.846775462` de A2; ambas métricas corresponden a `INNER VAL`, no a OUTER HOLD ni a un test prospectivo. Es inválido presentar esta diferencia como ventaja cuántica implementada.

El observable $B_5$ de A4-1A tiene **4095 coeficientes Pauli** y espectro diferente de ±1, de modo que **no** puede identificarse con una sola lectura dicotómica $U^\dagger ZU$. Un presupuesto de recursos deberá especificar descomposición, mediciones compatibles, precisión estadística y shots. La invariancia de la puntuación ante reescalado del operador no implica invariancia de la regularización ridge. Los índices FIT/TUNE completos no se archivaron en la evidencia examinada: la corrección del aislamiento interno procede del código fuente, no de una reconstrucción independiente de sus índices.

### 4.6. Reconciliación de avances matemáticos y reservas abiertas

La derivación condicionada **21→8 mediante trazas parciales** y la descomposición exacta **16→10 en la familia B8** ya están incorporadas en [arquitectura §§3–4](01_ARQUITECTURA_H2B2A7.md). Esto **no** resuelve la procedencia fila a fila de todos los estados reducidos originales ni demuestra equivalencia universal de recursos físicos. La formulación y los subproblemas ALS de R3 también se transcribieron desde la celda histórica 13 en [arquitectura §5](01_ARQUITECTURA_H2B2A7.md); ello no acredita independencia global de su selección ni todos sus checkpoints.

Estas actualizaciones corrigen el estado **documental** de L02 y L03 sin declarar resueltas las amenazas a la validez estadística. La identificación exacta de las variantes Student 1E/1F y de una eventual configuración final H2B2A7 continúa pendiente.

## 5. Protocolo propuesto para comprobar composiciones inéditas (no ejecutado)

### 5.1. Congelamiento previo a cualquier evaluación

Antes de abrir un nuevo conjunto retenido se debe producir y fechar un protocolo con:

- Versión y SHA-256 del dataset; definición de etiqueta FM/AFM y reglas para contradicciones.
- Clave canónica de composición y agrupaciones; reporte de grupos disjuntos entre entrenamiento, validación y test.
- Arquitectura exacta seleccionada (incluidos `O★`, C5 o variante justificada, rango, heads, calibración y procedimiento de medición), con checkpoint y criterio de selección.
- Baselines clásicos y sus descriptores, ajustes e hiperparámetros; comparación sobre los **mismos grupos químicos**.
- Métrica principal, incertidumbre, presupuesto experimental, semillas, criterio de decisión y tratamiento de datos faltantes definidos *antes* de inspeccionar resultados retenidos.

### 5.2. Flujo de entrenamiento y evaluación

1. **Reservar grupos externos** mediante una separación por composición. Guardar los identificadores de grupos y comprobar intersección vacía entre subconjuntos.
2. **Dentro de cada entrenamiento externo**, realizar toda selección y ajuste: escaladores, ingeniería de descriptores aprendida, bases Helstrom, aprendizaje de observables, selección de canales, rango ALS, estudiantes y calibración. No reutilizar componentes supervisados ajustados con datos del grupo externo.
3. **Seleccionar arquitectura con validación interna también agrupada**, sin optimizar según AUC del test externo.
4. **Congelar la regla de decisión** y producir predicciones del conjunto externo solamente una vez bajo el protocolo predefinido.
5. **Reportar** AUC y medidas pertinentes con incertidumbre adecuada a la unidad de independencia (grupo), tamaños de clase/grupo, fallos de ejecución y baseline clásico pareado.

Si el resultado requiere rediseñar la arquitectura, el conjunto usado para ese rediseño pasa a ser desarrollo; cualquier nueva afirmación confirmatoria necesita un conjunto independiente distinto.

### 5.3. Restricciones de interpretación

Una validación agrupada puede medir transferencia entre grupos de composición según su definición; no prueba sin más extrapolación a otras familias químicas, otras fuentes de datos, estructura cristalina no representada ni condiciones termodinámicas distintas. El nivel de generalización depende de qué similitudes permanezcan entre grupos y de cómo se obtengan las etiquetas.

## 6. Evidencia mínima para evaluar recursos de hardware

Para comparar métodos físicos sobre una misma tarea se requeriría, como mínimo, registrar por material:

- Preparación del estado y número de circuitos ejecutados, incluidas réplicas y mezclas necesarias.
- Compilación específica de backend, layout ISA, puertas nativas de uno y dos qubits, profundidad y necesidad de routing.
- Bases de medición y shots realmente ejecutados; lectura, errores, mitigación y política de descarte.
- Tiempo de ejecución, uso de QPU y criterio de parada, cuando se disponga de mediciones reales.
- Alineación del mismo conjunto de materiales y la misma calidad predictiva objetivo para comparar recursos.

El simple número de puertas de dos decodificadores, el número de bases QWC o los shots planificados **no cuantifica el costo integral ni acredita una ventaja física**.

## 7. Registro de límites que debe sobrevivir a la redacción final

| ID | Reserva no resuelta | Efecto directo en la tesis | Condición de cierre |
|---|---|---|---|
| L01 | Origen H2-A4→H2-B0 reproducido numéricamente; falta cotejo de las transferencias intermedias en RAM H2B1A/E0/E1 y de la preparación *upstream* | No atribuir seguridad completa a toda la cadena ni independencia de selección | Identidad de transferencias y entradas históricas, o reserva permanente explícita |
| L02 | Reducción 21→8 derivada algebraicamente en `01` para subsistemas conservados; procedencia exacta de arrays y recursos físicos pendiente | No extender la identidad condicionada a todos los observables ni al costo físico | Trazabilidad de reducción en arrays históricos y presupuesto físico, si se reclama ahorro |
| L03 | Ecuaciones ALS R3 cotejadas con fuente histórica en `01`, pero faltan verificaciones integrales de selección y procedencia de algunos checkpoints | Evitar afirmar seguridad global o convergencia/óptimo no comprobados | Mantener referencias a celda 13, hashes y reservas de selección retrospectiva |
| L04 | Variante final exacta y sus componentes congelados no reconciliados | No describir Student 1E, 1F, SAFE y QWC como si fueran idénticos | Lista fechada de componentes y checkpoints, con protocolo |
| L05 | Hold y inner val consultados históricamente | AUC observadas retrospectivas, no confirmatorias nuevas | Prueba predefinida sobre grupos/datos nuevos |
| L06 | Generalización a composiciones inéditas sin entrenamiento agrupado prospectivo | No atribuir extrapolación química | Experimento nuevo completo con grupos disjuntos |
| L07 | Falta de recursos físicos end-to-end homogéneos | No afirmar menor costo QPU o ventaja física | Presupuesto y/o medición homologados |
| L08 | Cotejo histórico QPY de 1F y ciertos artefactos incompleto | Limitar la afirmación de identidad histórica | Fuentes anteriores autenticadas o reserva permanente |
| L09 | A4-1A: índices exactos FIT/TUNE y coste de medición del observable Pauli general no certificados | No declarar independencia FIT/TUNE demostrada por índices ni ventaja de recursos | Índices archivados o reserva explícita; protocolo de medición con shots/precisión |

El objetivo no es abrir nuevas auditorías generales. Una dependencia irrecuperable se registra con una **limitación precisa**, y la documentación avanza.

## 8. Próxima decisión científica

La base algebraica 21→8, los canales visibles y las ecuaciones ALS R3 están redactadas en `01`; las auditorías A0–A4-1A quedan documentadas como evidencia numérica retrospectiva en `05` y clasificadas en `03` como E22–E27. El siguiente avance exige reconciliar las variantes del sistema final y auditar selectivamente A4-1B/1C, sin dar por confirmatorios resultados de `INNER VAL` ni mezclar Student 1E/1F, SAFE y QWC. Antes de evaluar nueva generalización, se necesita un protocolo por composición previamente fijado. Las reservas L01–L09 siguen vigentes según su alcance actualizado.

## 9. Fuentes versionadas

- [Mapa científico](00_MAPA_CIENTIFICO.md)
- [Arquitectura física y matemática](01_ARQUITECTURA_H2B2A7.md)
- [Linaje experimental](02_LINEAJE_EXPERIMENTAL.md)
- [Matriz de evidencia](03_MATRIZ_DE_EVIDENCIA.md)
- [INTEGRACIÓN-00](../H2B2A7_INTEGRACION_00.md)
- [INTEGRACIÓN-01](../H2B2A7_INTEGRACION_01.md)
- [Síntesis 3D](../../reports/H2B2A7_CONSOLIDACION/H2B2A7_3D_SINTESIS_20261113T184850523066Z/3D_INFORME.md)
- [Fase 3C.4: recursos](../H2B2A7_FASE_3C4_GUIA.md)

**Nota de preservación:** los informes de auditorías locales aún no integrados deben permanecer inmutables hasta seleccionar referencias auditables. No copiar en masa `.txt`, `.py`, `.zip`, datasets o checkpoints al worktree de documentación.
