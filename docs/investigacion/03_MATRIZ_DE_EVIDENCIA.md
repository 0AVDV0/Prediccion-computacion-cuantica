# H2B2A7 — Matriz de evidencia y alcance de las afirmaciones

> **Estado:** borrador documental v0.3, ampliado con E22–E31 para revisión científica. **No constituye una nueva evaluación, auditoría ejecutada ni certificación experimental.**
>
> **Base:** integraciones INTEGRACIÓN-00/01, síntesis 3D en `develop` y cierres de procedencia posteriores conservados fuera de Git.
>
> **Propósito:** vincular una afirmación concreta con su fuente, el tipo de prueba realmente disponible y lo que no se puede inferir.

## 1. Reglas de lectura

Esta matriz separa cuatro cuestiones que a menudo se confunden:

1. **Integridad documental:** el archivo o resultado archivado coincide con una huella o un registro anterior.
2. **Corrección físico-matemática:** una ecuación, transformación, matriz, expectativa o score coincide dentro de una tolerancia determinada.
3. **Validez estadística:** el pipeline, incluida toda supervisión y selección de arquitectura, no recibe información de la evaluación durante el ajuste.
4. **Generalización y confirmación:** el modelo congelado es probado sobre datos realmente nuevos, bajo un protocolo fijado antes de inspeccionar sus resultados.

Una evidencia del primer o segundo tipo **no implica** automáticamente las del tercero o cuarto.

**Estados de esta matriz:** `RESPALDADO` = la afirmación especificada tiene evidencia concreta dentro del alcance indicado; `PARCIAL` = existe evidencia, pero hay dependencias o identificadores sin cerrar; `EXPLORATORIO` = el resultado se produjo en el desarrollo, con reutilización o decisiones posteriores al examen de las métricas; `NO CERTIFICADO` = falta la prueba exigida. Ninguna etiqueta significa validación universal.

## 2. Matriz principal

| ID | Afirmación delimitada | Evidencia y localización | Dictamen | No permite afirmar / siguiente acción |
|---|---|---|---|---|
| E01 | El dataset CORE histórico contiene 10.691 registros, con particiones 7.483/1.069/2.139. | Auditorías locales de origen y particiones VI–XIV; [linaje](02_LINEAJE_EXPERIMENTAL.md), §3.1. | **PARCIAL** | El número no identifica automáticamente versiones posteriores del dataset; registrar archivo y huella canónicos antes de la tesis. |
| E02 | La base de coordenadas Helstrom 3K se ajustó supervisadamente sobre el CORE train completo. | Auditorías locales XXII–XXIV; código histórico `fit_helstrom_BWS` identificado; [linaje](02_LINEAJE_EXPERIMENTAL.md), §3.1. | **RESPALDADO para el código examinado** | Las AUC de `teacher_D` ≈0,965419 y `diag513_calibrated` ≈0,971824 sobre muestras empleadas en esa representación **no** son OOF del pipeline completo. |
| E03 | H1 ajustó el discriminador por fold y produjo cinco segmentos OOF coherentes con los cachés conservados. | Auditorías locales XVIII, XXII y XXIV; [linaje](02_LINEAJE_EXPERIMENTAL.md), §3.2. | **PARCIAL, evidencia fuerte** | AUC OOF histórico ≈0,907406; faltan huellas completas de índices y certificación exhaustiva de preparación upstream. |
| E04 | H2A3/H2A4 transmitieron los scores teacher H1 y verificaron un kernel B8 Hilbert–Schmidt. | Auditorías locales XXII–XXIV; [linaje](02_LINEAJE_EXPERIMENTAL.md), §3.3. | **RESPALDADO numéricamente** | La discrepancia histórica ≈8,5×10⁻⁸ verifica el cotejo de kernel, no una validación química externa. El AUC ≈0,923436 de `B_LABEL_KRR` conserva reservas de selección retrospectiva. |
| E05 | En la ejecución conservada, H2B1E1 recibió su observable de H2B1E0 y este de `O_FOLDS_H2B1A`. | `CIERRE_FINAL_FUENTE_OSTAR_Y_DECISION_C5_H2B2A7.txt`, salidas de celdas 10–11; [arquitectura](01_ARQUITECTURA_H2B2A7.md), §4. | **RESPALDADO para esa ejecución** | El origen anterior H2-A4→H2-B0 está certificado numéricamente (E19–E20); falta autenticación matricial de objetos intermedios en RAM. |
| E06 | Los cinco observables heredados son matrices de 256×256 asociadas a la representación B8. | Cierre local de O★, salidas históricas y comprobación de forma `(5, 256, 256)`; [linaje](02_LINEAJE_EXPERIMENTAL.md), §4.1. | **RESPALDADO** | La dimensión por sí sola no demuestra equivalencia universal de estados de 21 y 8 qubits ni seguridad estadística. |
| E07 | La representación H2B1E1 reconstruye el score del observable completo con diez canales efectivos. | `CIERRE_TRAZABILIDAD_H2B1E1_H2B2A7.txt` y salidas históricas de la celda 11; [arquitectura](01_ARQUITECTURA_H2B2A7.md), §4.1. | **RESPALDADO numéricamente dentro de la representación implementada** | Reconstrucción algebraica ≠ independencia de la supervisión con la que se aprendió O★. |
| E08 | La configuración C5 de H2B1E3 usa exactamente `II`, `IY`, `IZ`, `XY`, `ZZ`. | Definición `FIXED_CHANNELS_H2B1E3` en celda histórica 13 y reporte de cierre O★–C5. | **RESPALDADO** | No se ha demostrado que los cinco canales se eligieran globalmente antes de consultar métricas externas. |
| E09 | El desarrollo H2B1E1 exploró los 1.023 subconjuntos no vacíos de diez canales y utilizó fronteras basadas en AUC del hold para estudiar complejidad. | `CIERRE_FINAL_FUENTE_OSTAR_Y_DECISION_C5_H2B2A7.txt`, bloque `first_k_reaching_h2b1e1` y comentario del notebook. | **EXPLORATORIO** | La comparación AUC medio O★ completo ≈0,923686699 frente a C5 ≈0,921981265 **no** certifica selección global independiente ni superioridad en materiales nuevos. |
| E10 | En el código examinado, ALS de H2B1E3 usa `F_train`, `G_train` y `teacher_train` sobre índices de entrenamiento externo. | Auditoría local XXIII y cierre XXIV; [linaje](02_LINEAJE_EXPERIMENTAL.md), §4.4. | **RESPALDADO localmente; independencia global PARCIAL** | El ajuste ALS no recibe directamente las etiquetas del hold en el fragmento examinado, pero depende de O★ y C5 previos y de decisiones de rango. |
| E11 | El piloto H2B2A0 recupera R3 previamente ajustado y divide 5.986 outer train, 1.497 outer hold, 4.788 inner train y 1.198 inner val. | Auditoría local XXI/XXIV y salidas históricas de la celda 20; [arquitectura](01_ARQUITECTURA_H2B2A7.md), §5. | **RESPALDADO para el piloto** | El AUC del propio teacher R3 en inner val ≈0,978803438 **no** es una evaluación independiente: esas muestras pertenecían al outer train usado antes para ajustarlo. |
| E12 | INTEGRACIÓN-00 reproduce scores congelados de Teacher R3, HEAD4+SAFE, SAFE y QWC24/QWC64. | [INTEGRACIÓN-00](../H2B2A7_INTEGRACION_00.md), su [notebook archivado](../../experiments/INTEGRACION_00.ipynb) y reportes asociados. | **RESPALDADO como replay numérico** | Los AUC OUTER son retrospectivos; el replay no es reentrenamiento ni prueba de QPU. |
| E13 | INTEGRACIÓN-01 reconstruye la implementación de los observables Student 1E/1F y sus AUC agregadas de inner val. | [INTEGRACIÓN-01](../H2B2A7_INTEGRACION_01.md), [notebook archivado](../../experiments/INTEGRACION_01_CERT.ipynb); 94/94 pruebas PASS. | **RESPALDADO para implementación y métrica agregada** | 1E AUC ≈0,913537480; 1F ≈0,915988958; 1.198 materiales de inner val ya examinado. No se cotejó QPY histórico propio de 1F ni todos los scores individuales contra vectores originales pareados. |
| E14 | Las fases 3A–3D comparan scores, expectativas, rankings y recursos bajo procedimientos retrospectivos con productos verificables. | [3A](../H2B2A7_FASE3A_PLAN.md), [3B](../H2B2A7_FASE_3B_GUIA.md), [3C](../H2B2A7_FASE_3C_GUIA.md), [3C.3](../H2B2A7_FASE_3C3_GUIA.md), [3C.4](../H2B2A7_FASE_3C4_GUIA.md), [síntesis 3D](../../reports/H2B2A7_CONSOLIDACION/H2B2A7_3D_SINTESIS_20261113T184850523066Z/3D_INFORME.md). | **RESPALDADO como consolidación retrospectiva** | Verificación 22/22 huellas archivadas ≠ evidencia nueva de generalización. |
| E15 | La síntesis 3D contiene AUC descriptivas sobre outer hold (n=1.497) para Teacher S3 de referencia, SAFE ideal, QWC24 y QWC64. | [Síntesis 3D](../../reports/H2B2A7_CONSOLIDACION/H2B2A7_3D_SINTESIS_20261113T184850523066Z/3D_INFORME.md), §«Predicción descriptiva». | **EXPLORATORIO / RETROSPECTIVO** | No comparar estos números contra AUC de Student en *inner val* como si fueran observaciones pareadas; `TEACHER_S3_REFERENCIA_OUTER` no está automáticamente identificado con todos los objetos llamados R3. |
| E16 | Se documentan presupuestos lógicos parciales de medición y circuitos. | [3C.4](../H2B2A7_FASE_3C4_GUIA.md) y [síntesis 3D](../../reports/H2B2A7_CONSOLIDACION/H2B2A7_3D_SINTESIS_20261113T184850523066Z/3D_INFORME.md). | **RESPALDADO como inventario parcial** | Ni 504 puertas lógicas de dos decodificadores ni presupuestos QWC representan costo físico total comparable por material. |
| E17 | Las pruebas históricas QPU 19X no acreditan ventaja bajo el contraste confirmatorio descrito. | Auditorías y productos locales 19X, todavía fuera de este repositorio documental. | **PARCIAL hasta integrar evidencia específica** | El p≈0,4838 confirmatorio no puede reemplazarse por el p≈0,0377 exploratorio de otro protocolo. No publicar una reivindicación confirmatoria de ventaja cuántica. |
| E18 | Generalización a composiciones químicas inéditas. | Diagnósticos locales XV/XVI y [protocolo prospectivo](#5-requisitos-para-una-evaluacion-prospectiva); no hay ejecución nueva asociada en esta rama. | **NO CERTIFICADO** | Predefinir grupos por composición antes del split y rehacer *todas* las transformaciones supervisadas y la selección dentro de entrenamiento, con baseline clásico sobre los mismos grupos. |
| E19 | Los cinco vectores originales `alpha_B_LABEL_KRR_f0...f4` se almacenaron con índices `train_idx_f0...f4`; 7.483 ejemplos aparecen exactamente una vez en HOLD complementario. | `ARCH4FH2A4_LINEAR_OBSERVABLE_MODELS.npz`; `AUDITORIA_ESTRUCTURAL_OSTAR_H2B2A7.txt` (17-11-2026). | **RESPALDADO estructuralmente** | Cinco folds disjuntos no implican ausencia de filtración de información *upstream* ni generalización a composiciones inéditas. |
| E20 | La reconstrucción de los cinco $O_f^\star$ desde coeficientes H2-A4 y estados de 7q coincide con `O_folds` H2-B0 sin etiquetas ni AUC HOLD y sin inversión de signo. | `AUDITORIA_NUMERICA_H2A4_A_H2B0_SIN_HOLD.txt`; [arquitectura §4.2](01_ARQUITECTURA_H2B2A7.md). Error máximo de elemento $3.506\times10^{-7}$; comparación de kernel en 40 pares con error $1.115\times10^{-7}$. | **CERTIFICADO NUMÉRICAMENTE para H2-A4→H2-B0** | No autentica RAM H2B1A→H2B1E1 ni prueba independencia confirmatoria de selección de objetivo/C5/R3. |
| E21 | H2-A4 escoge $\lambda$ de `B_LABEL_KRR` dentro de TRAIN, pero el ganador `B_LABEL_KRR` se determinó comparando AUC media de los cinco OUTER HOLD; H2-B0 tenía una recuperación opcional guiada por AUC HOLD. | `FUENTE_ENTRENAMIENTO_H2A4_ORIGEN_OSTAR_H2B2A7.txt`, celda 312; `FUENTE_CREADORA_OSTAR_C313_C314_H2B2A7.txt`, celda 313. | **ENTRENAMIENTO LOCAL RESPALDADO; SELECCIÓN GLOBAL EXPLORATORIA** | El cotejo sin HOLD E20 elimina la necesidad de esa orientación para reproducir matrices, pero no hace independiente la elección histórica de la familia de objetivos. |

| E22 | A0: tres cabezales de 6q, checkpoint y objetivo TRAIN/VAL reproducidos desde fuentes congeladas. | `AUDITORIA_INDEPENDIENTE_CIRCUITOS_A0.txt`; `AUDITORIA_A0_OBJETIVO_COMPLETO_FOURIER.txt`; [resultados §4](05_RESULTADOS_Y_AUDITORIAS_H2B2.md). | **CERTIFICADO NUMÉRICAMENTE en el alcance auditado** | Simulación física sobre submuestras; 15 coordenadas Fourier, no reejecución completa; teacher R3 ya había usado `INNER VAL` en el ajuste previo. |
| E23 | A1 conserva exactamente las expectativas de A0 y reconstruye los decodificadores lineal y cuadrático elegidos. | `AUDITORIA_INDEPENDIENTE_H2B2A1.txt`; [resultados §5](05_RESULTADOS_Y_AUDITORIAS_H2B2.md). | **CERTIFICADO NUMÉRICAMENTE en decodificadores congelados** | AUC `INNER VAL` retrospectiva; estacionariedad del decodificador no prueba optimalidad global de todos los parámetros. |
| E24 | A2 incorpora H4, verifica continuidad A0→A2-0→A2-1, objetivos y expectativas de cuatro circuitos. | `AUDITORIA_H2B2A2_H4_JOINT4_V2.txt`; [resultados §6](05_RESULTADOS_Y_AUDITORIAS_H2B2.md). | **CERTIFICADO NUMÉRICAMENTE en el alcance auditado** | Cuatro heads con RZZ terminal inactiva; 20 controles Fourier muestreados; AUC de desarrollo no confirmatoria. |
| E25 | A3 anida A2 mediante RZ/Cartan, conserva los 84 parámetros antiguos y reconstruye checkpoints y expectativas. | `AUDITORIA_H2B2A3_RZ_CARTAN_V2.txt`; [resultados §7](05_RESULTADOS_Y_AUDITORIAS_H2B2.md). | **CERTIFICADO NUMÉRICAMENTE en el alcance auditado** | El mejor RZ es el baseline; la mejora Cartan es diminuta; ciertas métricas son diagnósticos reconstruidos porque faltan columnas en el CSV. |
| E26 | A4-0: quinto cabezal jerárquico H5 con cuatro cabezales base congelados; gana `DECODER_ONLY` inicial. | `AUDITORIA_INDEPENDIENTE_H2B2A4_H5.txt`; [resultados §8.1](05_RESULTADOS_Y_AUDITORIAS_H2B2.md). | **CERTIFICADO NUMÉRICAMENTE en el alcance auditado** | No se atribuye la AUC al entrenamiento de H5; simulación y Fourier en submuestras; no hay `val_objective` histórico para cotejo. |
| E27 | A4-1A reconstruye el quinto observable Pauli de 6q y su quinta expectativa desde los estados y una matriz hermítica. | `AUDITORIA_A4_1A_RESULTADO.txt`; [resultados §8.2](05_RESULTADOS_Y_AUDITORIAS_H2B2.md). | **CERTIFICADO NUMÉRICAMENTE en Pauli, checkpoint y gauge** | 4095 Pauli; falta coste de medición y comprobación independiente de índices FIT/TUNE; AUC histórica de desarrollo no implica generalización ni ventaja física. |
| E28 | A4-1B reconstruye el oráculo completo $W\in\mathbb R^{4095\times3}$, su SVD y los tres truncamientos sobre INNER. | `AUDITORIA_INDEPENDIENTE_A4_1B_V2.txt`; fuente C035; [resultados §12](05_RESULTADOS_Y_AUDITORIAS_H2B2.md). | **VERIFICADO NUMÉRICAMENTE en SVD/checkpoint/INNER** | Nueve búsquedas CG con `info != 0`; residuo final $4.030598\times10^{-5}$, sin óptimo estricto ni AUC nueva. |
| E29 | A4-1C tiene $W_2=BC$, $B^\top B\approx I$, rango dos, dos expectativas Pauli físicas y salidas INNER reproducidas. | `AUDITORIA_INDEPENDIENTE_A4_1C.txt`; fuente C036; [resultados §12](05_RESULTADOS_Y_AUDITORIAS_H2B2.md). | **VERIFICADO NUMÉRICAMENTE en geometría/checkpoint/INNER** | ALS 3/3 no convergidos; residuo final bloque $B\approx0.0114353$; AUC histórica y costo físico no confirmados. |
| E30 | A4-1D conserva rango dos y reproduce checkpoint/scores del modelo *task-aware*. | `AUDITORIA_INDEPENDIENTE_A4_1D.txt`; fuente C037; [resultados §12](05_RESULTADOS_Y_AUDITORIAS_H2B2.md). | **VERIFICADO NUMÉRICAMENTE en geometría/checkpoint/INNER** | Pérdida supervisada de ranking no reconstruida sin etiquetas/pares; AUC histórica $0.951494$, menor que A4-1C. |
| E31 | A4-1D2 SAFE reproduce el criterio de selección histórico entre INIT_ONLY/REFINED, rango dos, scores y expectativas desde PSI7. | `AUDITORIA_INDEPENDIENTE_A4_1D2.txt`; fuente C038; [resultados §12](05_RESULTADOS_Y_AUDITORIAS_H2B2.md). | **VERIFICADO NUMÉRICAMENTE en selección archivada/checkpoint/INNER** | Regla basada en TUNE histórico; no se auditaron índices FIT/TUNE ni trayectoria final de gradientes; AUC INNER VAL $0.967330$ no confirmatoria. |

## 3. Métricas que no deben mezclarse

| Fuente / método | Conjunto | Cantidad | Valor histórico | Uso permitido |
|---|---|---:|---:|---|
| H1 Helstrom fold-fit | OOF histórico | 7.483 predicciones agregadas | AUC ≈0,907406 | Evidencia OOF con reservas de procedencia de entradas. |
| O★ H2B1E1, 10 canales | Media de 5 holds | 5 folds | AUC media ≈0,923686699 | Comparación retrospectiva en investigación. |
| C5 H2B1E3 | Media de 5 holds | 5 folds | AUC media ≈0,921981265 | Diagnóstico exploratorio de compresión; no confirmación de selección. |
| Teacher R3 sobre inner val (piloto) | Inner val previamente incluido en entrenamiento R3 | 1.198 | AUC ≈0,978803438 | Medida in-sample respecto al teacher; no desempeño independiente. |
| Student 1E | Inner val ya examinado | 1.198 | AUC ≈0,913537480 | Reproducción agregada histórica. |
| Student 1F | Inner val ya examinado | 1.198 | AUC ≈0,915988958 | Reproducción agregada histórica. |
| `TEACHER_S3_REFERENCIA_OUTER` | Outer hold archivado | 1.497 | AUC ≈0,92899819 | Descriptivo; identidad exacta del teacher de referencia requiere cautela. |
| SAFE ideal | Outer hold archivado | 1.497 | AUC ≈0,92508499 | Descriptivo. |
| QWC24 ideal | Outer hold archivado | 1.497 | AUC ≈0,91248910 | Descriptivo. |
| QWC64 ideal | Outer hold archivado | 1.497 | AUC ≈0,91779707 | Descriptivo. |

**Prohibido interpretar:** la distancia entre AUC de métodos evaluados sobre *splits* distintos como una mejora pareada, o una coincidencia de AUC agregada como coincidencia de cada predicción individual.

## 4. Dependencias abiertas y decisión editorial

| Dependencia | Situación actual | Decisión en la tesis |
|---|---|---|
| Construcción `O_FOLDS_H2B1A` | Origen H2-A4→H2-B0 reconstruido numéricamente; transferencias históricas intermedias por RAM y procedencia *upstream* no autentificadas integralmente. | Describir la procedencia demostrada y dejar pendiente la identidad de todos los objetos transferidos; no alegar *fold safety* universal. |
| Reducción multicopia 21 → 8 y observables efectivos 6q | Derivación condicionada de trazas parciales y canales 16→10 ya incorporada en [arquitectura](01_ARQUITECTURA_H2B2A7.md), §§3–4. | Pendiente cotejar creación y alineación de arrays históricos y determinar recursos físicos end-to-end; no extender la identidad a todos los observables 21q. |
| Función objetivo y regularización exactas ALS | Ecuaciones y subproblemas cotejados con celda histórica 13 e incorporados en [arquitectura §5](01_ARQUITECTURA_H2B2A7.md). | Conservar la formulación histórica, sin inferir seguridad de selección del rango ni optimalidad de todos los checkpoints. |
| Identidad de la arquitectura final congelada | Hay variantes Student 1E/1F, SAFE y QWC bajo protocolos distintos. | No declarar que la mejor AUC entre variantes equivale a una arquitectura final preregistrada. |
| Procedencia histórica QPY de 1F | Implementación numérica reconstruida; QPY histórico propio no cotejado. | Citar únicamente el alcance realmente verificado de INTEGRACIÓN-01. |
| Presupuesto físico end-to-end | Faltan preparación, compilación, medición y lectura homogéneas. | No reivindicar ventaja de recursos ni velocidad QPU. |

## 5. Requisitos para una evaluación prospectiva

Para poder hablar de generalización a composiciones químicas nuevas, el siguiente experimento debería especificar **antes de ejecutarse**:

- Una clave de agrupación química definida y estable; tratamiento explícito de composiciones repetidas y etiquetas contradictorias.
- Split externo por grupos químicos sin solapamiento, con conjunto final reservado para una sola evaluación.
- Ajuste dentro de cada entrenamiento de todos los pasos supervisados: transformaciones de entrada, bases Helstrom, observables O★, canales/selección de C5, rango ALS, calibraciones y Student.
- Validación interna también agrupada para seleccionar hiperparámetros, sin consultar el hold externo para rediseñar la arquitectura.
- Un baseline clásico entrenado y evaluado sobre exactamente los mismos grupos, con variables y presupuesto declarados.
- Métricas, incertidumbre, hipótesis y criterio de decisión fijados antes de inspeccionar el resultado final.

Este protocolo es **una propuesta**, no un experimento ejecutado ni una reparación retroactiva de las AUC históricas.

## 6. Registro de fuentes y preservación

### Evidencias ya integradas

- [Mapa científico](00_MAPA_CIENTIFICO.md), [arquitectura](01_ARQUITECTURA_H2B2A7.md) y [linaje](02_LINEAJE_EXPERIMENTAL.md).
- [INTEGRACIÓN-00](../H2B2A7_INTEGRACION_00.md), [INTEGRACIÓN-01](../H2B2A7_INTEGRACION_01.md) y [síntesis 3D](../../reports/H2B2A7_CONSOLIDACION/H2B2A7_3D_SINTESIS_20261113T184850523066Z/3D_INFORME.md).

### Evidencias locales no incorporadas automáticamente al repositorio

`AUDITORIA_XV_CERTIFICACION_COMPOSICIONAL_H2B2A7.txt`, `AUDITORIA_XVIII_TRAZABILIDAD_TEACHERS_FOLD_SAFETY_H2B2A7.txt`, `AUDITORIA_XXII_LINEAJE_CV_TEACHER_H2B2A7.txt`, `AUDITORIA_XXIII_ORIGEN_SUPERVISION_R3_Y_BASES_H2B2A7.txt`, `AUDITORIA_XXIV_CIERRE_H1_R3_Y_REUSO_HOLD_H2B2A7.txt`, `CIERRE_TRAZABILIDAD_H2B1E1_H2B2A7.txt` y `CIERRE_FINAL_FUENTE_OSTAR_Y_DECISION_C5_H2B2A7.txt`.

**Política de conservación:** estos archivos se mantienen en el worktree de consolidación; no subir paquetes masivos, checkpoints binarios, datos privados ni reportes con rutas locales sin revisión de publicación. El mero nombre del archivo no acredita su contenido: para elevar una afirmación a `RESPALDADO`, conservar fragmento fuente, número de celda o línea, huella de versión y una descripción del alcance.

---

**Próxima revisión de este documento:** reconciliar SHA256 verificables de las fuentes locales seleccionadas con un manifiesto publicable; E22–E31 describen el alcance auditado, no evaluaciones confirmatorias.

**Actualización de procedencia v0.2:** hashes de los artefactos históricos y cuadro de errores por fold en la sección §4.2 del documento de arquitectura. La reconstrucción del observable queda certificada; la evaluación final del pipeline continúa siendo retrospectiva.
