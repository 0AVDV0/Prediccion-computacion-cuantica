# H2B2A7 — Procedencia de los DataFrames composicionales y estructurales

> **Estado:** revisión forense documental, 18 de noviembre de 2026. **No es una reproducción ejecutada de los DataFrames** ni una certificación de correspondencia registro por registro con la codificación cuántica. Las fuentes archivadas se inspeccionaron sin ejecutar sus celdas.

## 1. Propósito y objetos distintos

Se estudian tres versiones históricas que no deben intercambiarse por coincidencia parcial de nombres ni de número de filas:

| Objeto | Conteo citado históricamente | Fuente creadora / evidencia presente | Estado de procedencia |
|---|---:|---|---|
| Universo composicional inicial | 24.174 | `Pipelineobtenciondescriptores.ipynb` y bloques históricos `bloque_1.csv`–`bloque_final.csv` | Código creador localizado; **conteo y filas no reproducidos con datos** |
| DataFrame usado en la línea de modelos | 10.691 | `ModelosDataset2.ipynb` (celda 1, procesamiento independiente) y celdas posteriores 170/218/231 | Código de preparación localizado y expectativas de 10.691; **no probado que la celda 1 por sí misma produzca ese tamaño** |
| Exportación con estructura cristalográfica | 10.678 | `VisualizaciondeDatos.ipynb`, celda 281, `dataset_listo_opcion_A.csv` | Código de exportación localizado; **no demostrado que genere el DataFrame de 10.691** |

La pregunta siguiente es **qué datos, índices y columnas** alimentaron la construcción de `PSI7_ALL_3S.npy` (7.483 estados de 7 qubits de la rama de experimentos H2B2). No inferir la identidad de esas filas solo a partir del valor 7.483 de TRAIN.

## 2. Fuentes e integridad de las extracciones

Paquete fuente examinado: `FUENTES_PREPROCESAMIENTO_DF_24174_10691.zip`. Contiene 108 celdas y tres ficheros de metadatos. Las 108 fuentes textuales coincidieron con su huella SHA256 registrada en `MANIFIESTO_SHA256_FUENTES.json`; el ZIP pasó su verificación de integridad. Esto **no equivale a una segunda verificación byte por byte de los notebooks en el equipo histórico**.

| Notebook histórico | SHA256 de notebook consignado por extractor | Celdas extraídas |
|---|---|---:|
| `Pipelineobtenciondescriptores.ipynb` | `7ef097025cf5d7bf8b884b9d61edf8deed6d26316f64712b1da91ad9a284e5f3` | 85 |
| `ModelosDataset2.ipynb` | `da4c720fa3af1ce13d88184a703aa214cc7d243961e56e12617af9631532a9fd` | 4 |
| `notebooks/VisualizaciondeDatos.ipynb` | `fb52c36537c09fc0f54e8185d6fc45de1eabbc3ba77e8410f84d2704410fcc6c` | 19 |

La numeración de celdas empleada a continuación es **base cero**; no es el orden de ejecución.

## 3. Ruta del universo composicional: `Pipelineobtenciondescriptores`

**Celdas creadoras fundamentales:** 0 (lectura de `magnetic_materials.csv`), 5 (descarta algunas columnas), 9–14 (descarta registros sin fórmula representativa y separa `df1/df2`), 16–32 (intentos de conversión de fórmulas), **36** (define `df_total = pd.concat([df1], ...)`, dejando comentada la recuperación de otras filas), 37, 46–58 (promedios y otras propiedades composicionales), **67** (filtro de campos Curie/Néel), **69** (etiquetas FM/AFM), **71** (fracciones atómicas), 72 y 80 (diagnósticos/columnas eliminadas). Celdas posteriores 87/116/168 reutilizan los resultados.

### 3.1. Etiquetado histórico

El algoritmo retiene solamente patrones de presencia exclusivos de Curie/Curie(Tc) o exclusivos de Néel/Neel(Tn): 6 combinaciones de las 16 posibles. Descarta las 9 combinaciones con ambas familias, además de la combinación sin ninguna. En consecuencia, para el código inspeccionado, la asignación secuencial FM seguida por AFM no cambia ninguna etiqueta FM retenida por ese filtro. Hay que medir el **número de filas descartadas** y la representatividad química de estas exclusiones.

### 3.2. Fracciones `p_X`

La celda 71 utiliza `pymatgen.core.Composition`: para la fórmula con conteos atómicos $n_X$, calcula $p_X=n_X/\sum_Y n_Y$. Los símbolos se reúnen del dataset procesado y se ordenan alfabéticamente; **el número de componentes y su orden deben registrarse**, y no debe suponerse que un orden reconstruido en otra versión coincide con el empleado en `PSI7`.

**Riesgo identificado:** ante errores del parser, la función `elemental_proportions` conserva su diccionario inicial lleno de ceros (`except: pass`). Las filas mal parseadas deben registrarse; no son composiciones químicas válidamente codificadas.

El procedimiento histórico también calcula propiedades como número atómico medio, masa atómica media, electronegatividad media, entropía composicional y fracciones de elementos magnéticos/tierras raras. Documentar qué columnas realmente entraron en cada modelo, en lugar de confundir columnas disponibles con features usadas.

## 4. Ruta de modelado: `ModelosDataset2`

**Celda 1:** vuelve a leer directamente `magnetic_materials.csv` y realiza numerosas operaciones parecidas a la ruta inicial, como conversión de fórmulas, características y fracciones `p_X`, con un filtro Curie/Néel del mismo tipo. En las líneas 339–340 del texto extraído, la opción que concatena `df1, df_convertidos1, df_convertibles2` aparece comentada, y la asignación activa es `df_total = pd.concat([df1], ignore_index=True)`. La celda termina con `df_nuevo = df_total.drop(...)`; **no hay aquí una escritura comprobada de un CSV con 10.691 filas**.

**Celdas 170/218/231:** esperan o localizan posteriormente el DataFrame de 10.691 materiales con `magnetic_label` y columnas composicionales `p_X`, y trabajan con splits/estados. Su dependencia de un objeto en memoria o un checkpoint exige rastrear el último productor exacto y registrar hashes de los datos originales.

**Limitación:** no declarar `24.174 → 10.691` como un simple filtro ni atribuir el `df_final.pkl` histórico a la celda 1 sin cotejo del contenido y del orden de filas.

## 5. Ruta estructural: `VisualizaciondeDatos`

- **Celda 0:** concatena trece bloques composicionales (`bloque_1` a `bloque_12`, más `bloque_final`).
- **Celdas 263–279:** procesamiento de fórmulas, descriptores y etiquetas, análogo en partes a la ruta inicial, seguido de reducción de columnas hacia `df_nuevo`.
- **Celda 281:** selecciona filas con `Space_Group` **y** `Crystal_Structure` no nulos, requiere una composición interpretable desde `Material_Name`, recalcula propiedades utilizando `ElementProperty.from_preset("magpie")` y guarda `dataset_listo_opcion_A.csv`.

Este filtro restringe el universo a casos con datos cristalográficos disponibles. **No se ha probado que esta exportación sea el origen de los 10.691 registros de modelado**; la diferencia histórica de 13 filas entre ambas referencias NO demuestra que difieran en solo 13 compuestos.

## 6. Riesgos abiertos antes de la reproducción

1. Confirmar versiones/licencias de `magnetic_materials.csv`, `pandas`, `pymatgen`, `matminer` y criterio de parsing; no ejecutar masivamente los notebooks originales.
2. Distinguir registros (filas) de materiales químicamente únicos y fórmulas equivalentes/duplicadas; cotejar proporciones por la misma convención de símbolos y precisión.
3. Documentar qué filas descartó cada criterio, cuántas fallaron al interpretar fórmulas, qué valores nulos se imputaron o conservaron y si hay contradicciones FM/AFM entre fórmulas idénticas.
4. Identificar el DataFrame de 10.691 por su **contenido, huella, columnas, etiquetas e índices**, no solamente por su nombre o tamaño; distinguir de la rama estructural de 10.678.
5. Rastrear el orden exacto de las 84 columnas `p_X` usadas para amplitudes de 7 qubits y la relación `dataset → split → PSI7_ALL_3S.npy`. Confirmar si el estado final tiene fases y cómo se construyen `rho6/rho4`.
6. Para inferencia estadística posterior, prevenir fuga por materiales de igual composición que aparezcan en distintos conjuntos; las auditorías actuales son retrospectivas.

## 7. Acción de archivo y publicación

- **Se puede versionar:** este documento, hashes y las utilidades de verificación **sin datos ni rutas de usuario**.
- **No publicar todavía:** el ZIP forense completo, notebooks históricos íntegros, datos originales, checkpoints, PKL ni scripts históricos con rutas absolutas. Primero comprobar licencias y limpiar trazas privadas.
- **Reproducción pendiente:** preparar una implementación autónoma con pruebas sobre `magnetic_materials.csv` y comparar hash/filas/columnas/etiquetas con los artefactos históricos; separar una reproducción fiel de posibles correcciones propuestas.

La utilidad `scripts/preprocesamiento/diagnosticar_linaje_df.py` hace comparaciones descriptivas agregadas de CSV existentes; no atribuye por sí sola procedencia causal entre tablas.

## 8. Actualización con diagnósticos reales (18-11-2026)

Los informes agregados ejecutados sobre los ficheros locales permiten pasar de la hipótesis de solapamiento a las siguientes observaciones condicionadas: **24.174** filas composicionales; **10.678** filas en CSV estructural; **10.691** filas en `df_final.pkl`. En los tres se identifican **84 columnas `p_X` válidas** por suma de fracciones. No se ha vuelto a ejecutar el código creador.

- El conjunto de 10.678 es submulticonjunto de los 24.174 por las claves `(p_X a 9 decimales, etiqueta)` y también del de 10.691 con 13 ocurrencias adicionales (3 FM, 10 AFM) en el segundo. Dos firmas de composición están presentes únicamente en 10.691 respecto de 10.678. Esta inclusión **no** prueba la misma identidad experimental o estructura en grupos duplicados.
- Los conjuntos de 10.678 y 10.691 comparten **226 nombres de columnas en el mismo orden**. La comparación aproximada conjunta de las 226 columnas **no** encontró inclusión: 67 filas del primer conjunto carecen de huella total coincidente en el segundo, con 80 excedentes en sentido contrario. No equivale a afirmar 67 materiales físicamente distintos o modificados.
- Un diagnóstico posterior evaluó diferencias **marginales condicionadas a `(p_X, etiqueta)`**. En **7.284 grupos con una fila en cada fuente** es posible un emparejamiento único por esa clave; no certifica que sea el mismo registro original. Detectó discrepancias estrictas en **16 columnas Magpie** y **2 descriptores adicionales**, ninguna en cinco columnas de identificación/estructura. Los **84 `p_X` forman la propia clave de agrupación**, por lo que su ausencia de discrepancias estrictas es un resultado condicionado y no una auditoría independiente del encoding.
- El llamado modo «tolerante» del verificador histórico **no** ejecuta `isclose` numérico; formatea números a seis decimales. Reporta discrepancias en 33 columnas; ese número **no debe interpretarse como un conjunto monotónicamente más permisivo** que el de nueve decimales. Dos valores pueden coincidir al formatear nueve decimales y diferir al formatear seis si quedan a lados opuestos del umbral de redondeo.
- Las diferencias estrictas más visibles incluyen `MagpieData avg_dev AtomicWeight` (déficit marginal 18) y `avg_atomic_weight` (15). Son déficits marginales en un multiconjunto condicionado, **no** conteos exactos de filas físicas alteradas.
- `df_final.pkl` debe conservarse intacto. Pendiente: demostrar por código y hashes qué DataFrame y qué orden de columnas/índices generaron los 7.483 estados de `PSI7_ALL_3S.npy`; las similitudes entre los DataFrames **no prueban** esa correspondencia.

Ver el anexo [`06A_AUDITORIA_COMPARATIVA_DF_20261118.md`](06A_AUDITORIA_COMPARATIVA_DF_20261118.md) y los JSON agregados en `reports/H2B2A7_PREPROCESAMIENTO`. Este cierre es **documental**, no una reconstrucción end-to-end del pipeline.
