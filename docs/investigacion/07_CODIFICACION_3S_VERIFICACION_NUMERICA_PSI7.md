# H2B2A7 — Auditoría independiente de la codificación 3S y trazabilidad de PSI7

> **Estado:** verificación numérica local de artefactos históricos; **no** certificación de procedencia temporal ni de todos los estados derivados. Fecha del corte documental: 18 de noviembre de 2026.  
> **Ámbito:** conjunto de entrenamiento, sin ejecución de experimentos y sin consulta a resultados de validación/test.

## 1. Objetivo y fuentes

Comprobar que los estados complejos de siete qubits archivados para el entrenamiento 3S pueden reconstruirse desde `df_final.pkl` y la partición `idx_train`, y que la copia `CACHE_PSI7_ALL_3S.npz` almacena los mismos valores. Las pruebas se ejecutaron en el equipo de investigación y se conservaron sus resultados agregados, sin exportar registros individuales.

Artefactos de entrada, identificados mediante SHA-256:

| Artefacto | SHA-256 | Papel |
|---|---|---|
| `df_final.pkl` | `42c0a2afc92c65b29a9f081bdff813362a8246f020e928bd634ed4a6599008f2` | DataFrame histórico de 10.691 filas |
| `transfer_splits_A4_AQ4.npz` | `1f9eb162adaf0d10301f5b6deb761a15ba5ef9fbb231080e38f0902c826812ed` | Índices de train/val/test |
| `PSI7_ALL_3S.npy` | `85761c0a7df704e46d5e75ff6ac858b7c8c8335dc84506bde5cc9d33d8ebe362` | Estados archivados de train |
| `CACHE_PSI7_ALL_3S.npz` | `d0ecf20f798512b70ce5c89a60b19ec1e5042bf8261bb000db26bd969b5b7797` | Copia de estados del checkpoint |

**Trazabilidad del algoritmo:** `ModelosDataset2.ipynb`, celda 231 (numeración desde cero), función `encode_sparse_composition_3s`, según el código fuente identificado. La reproducción se hizo con `AUDITAR_ORIGEN_PSI7_3S_SOLO_LECTURA.py`; no fue una reejecución íntegra del notebook.

## 2. Mapa de la codificación

Se extraen las 84 columnas composicionales `p_X` en el orden de elementos que implementa el experimento 3S, a partir de las posiciones `idx_train` del DataFrame histórico. El auditor sustituye valores no finitos por cero, limita a valores no negativos, normaliza la fila y forma un vector complejo:

$$
|\psi_7(x)\rangle = \sum_{j=0}^{83} \sqrt{p_j(x)} \exp(i\pi p_j(x)) |j\rangle,
\qquad \sum_j p_j(x)=1.
$$

Las componentes 84–127 se fijan a cero. Se almacena en precisión `complex64`, con `2^7=128` componentes. Esta especificación corresponde a la reconstrucción numérica validada, no a una síntesis de circuito físico para preparar el estado.

**Propiedad matemática:** las fracciones idealmente pueden recuperarse como `p_j=|<j|psi_7>|^2`, por lo que esta transformación completa no elimina información de las 84 fracciones suministradas. Esto **no implica** que las fracciones codifiquen toda la información cristalográfica, ni que las matrices reducidas u observables preserven la misma información. La precisión de coma flotante introduce pequeñas desviaciones de norma.

## 3. Auditoría A — reconstrucción independiente

| Magnitud | Resultado |
|---|---:|
| Filas del DataFrame histórico | 10,691 |
| Índices de entrenamiento utilizados | 7,483 |
| Columnas composicionales utilizadas | 84 |
| Matriz archivada | `(7483, 128)` |
| Tipo del estado | `complex64` |
| Estados con coincidencia exacta valor a valor | **7,483 / 7,483** |
| Estados con error máximo ≤ `1e-6` | 7,483 |
| Diferencia máxima de amplitud | **0.0** |
| Error RMS de amplitud | **0.0** |
| Amplitud máxima en posiciones 84–127 | 0.0 |
| Desviación máxima de la norma al cuadrado | 2.38418579102e-07 |

**Conclusión A:** los 7.483 vectores reconstruidos con este algoritmo y estos archivos son idénticos en los valores numéricos comparados a `PSI7_ALL_3S.npy`. La coincidencia exacta va más allá de una tolerancia de `1e-6`, pero no autentica la fecha de generación del archivo.

## 4. Auditoría B — caché y particiones

| Magnitud | Resultado |
|---|---:|
| Clave usada en el caché | `PSI7_ALL_3S` |
| Forma y tipo del caché | `(7483, 128)`, `complex64` |
| Estados idénticos entre `.npy` y caché | **7,483 / 7,483** |
| Error máximo / RMS | 0.0 / 0.0 |
| `idx_train` / `idx_val` / `idx_test` | 7,483 / 1,069 / 2,139 |
| Intersecciones entre particiones | **0 en los tres pares** |
| Índices únicos en total | **10,691 de 10,691** |
| Partición completa, sin solapamientos | **Sí** |

**Conclusión B:** el caché almacena los mismos valores `complex64` y mantiene el mismo orden interno que el archivo archivado; los índices de `train`, `val` y `test` son disjuntos y cubren las 10.691 posiciones del DataFrame. El informe no evalúa si el procedimiento estadístico de partición fue estratificado, agrupado por composición o seguro frente a fuga composicional.

## 5. Consistencia entre auditorías

El SHA-256 de `PSI7_ALL_3S.npy` es idéntico en los informes A y B, al igual que el de `transfer_splits_A4_AQ4.npz`. Se construye así una cadena de consistencia **numérica y posicional para train**:

`df_final.pkl` + `idx_train` + codificación 3S → `PSI7_ALL_3S.npy` = contenido de `CACHE_PSI7_ALL_3S.npz`.

La relación entre `df_final.pkl` y sus archivos de preprocesamiento previos se documenta con reservas por separado en `06_ORIGEN_Y_PREPROCESAMIENTO_DATOS.md` y `06A_AUDITORIA_COMPARATIVA_DF_20261118.md`.

## 6. Limitaciones y auditorías pendientes

1. **Etiquetas y versiones:** no se verificó `Y_ALL_3P`, `C_ALL_3P`, las etiquetas `magnetic_label` de `df_final.pkl` ni sus órdenes de correspondencia. La reconstrucción no valida los objetivos supervisados utilizados por entrenamientos posteriores.
2. **Estados reducidos:** no se comprobó la generación de `rho6`, `rho4` ni los índices de qubits trazados; la reducción puede perder información aunque el estado completo codifique todas las fracciones.
3. **Caché vs procedencia:** SHA y igualdad numérica no acreditan cuándo, en qué ejecución, ni bajo qué entorno se produjeron originalmente los archivos.
4. **Validación científica:** no hay AUC, generalización, pruebas en QPU ni certificación de ausencia de fugas entre composiciones repetidas de distintas particiones.
5. **Privacidad y seguridad:** las auditorías no exportan filas, identificadores, estados ni fórmulas químicas; el script de reconstrucción requiere cargar un pickle histórico de origen confiable. Nunca debe cargarse un `.pkl` desconocido.

## 7. Próxima prueba prioritaria

Determinar cómo se construyeron `Y_ALL_3P`, `C_ALL_3P` y sus relaciones de índice con `idx_train` y el DataFrame de 10.691 filas, contrastando etiquetas **sin consultar la partición de test para ajustar el modelo**. En una segunda etapa, verificar algebraicamente las trazas parciales y el convenio de orden de qubits de `rho6` y `rho4`.

## 8. Informes reproducibles del paquete

- `reports/H2B2A7_CODIFICACION_3S/AUDITORIA_ORIGEN_PSI7_3S_RESULTADO.json`
- `reports/H2B2A7_CODIFICACION_3S/AUDITORIA_CACHE_Y_SPLITS_PSI7_3S_RESULTADO.json`
- `scripts/codificacion/AUDITAR_ORIGEN_PSI7_3S_SOLO_LECTURA.py`
- `scripts/codificacion/AUDITAR_CACHE_Y_SPLITS_PSI7_3S_SOLO_LECTURA.py`

**Alcance del cierre:** codificación 3S y redundancia exacta del caché, **sí**; linaje histórico completo, correspondencia supervisada y matrices reducidas, **todavía no**.
