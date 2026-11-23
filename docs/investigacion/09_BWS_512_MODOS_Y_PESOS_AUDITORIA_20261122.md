# H2B2A7 — Auditoría exhaustiva del operador BWS, 512 pares propios y origen algebraico de los pesos

> **Corte documental:** 22 de noviembre de 2026.
> **Punto de partida Git:** `2069d79` en `feature/h2b2a7-documentacion-cientifica`.
> **Naturaleza:** auditoría retrospectiva, sin reentrenamiento, solo TRAIN; no se accedió a VAL, TEST, predicciones ni QPU.
> **Evidencia original:** `AUDITORIA_BWS_512_MODOS_Y_PESOS_RESULTADO.json`, SHA-256 `ab693ac8e2b84d74497e34a13fd9ba429cb3a1585a281341bdbc85341ce06532` (copia original conservada por separado).
> **Evidencia publicable:** `reports/H2B2A7_PHI3_HELSTROM512_BWS/AUDITORIA_BWS_512_MODOS_Y_PESOS_RESULTADO_PUBLICO.json` (las únicas sustituciones son los campos de rutas absolutas; se agregó una nota de publicación).

## 1. Pregunta científica y relación con el corte 08

La [documentación de Phi3 y Helstrom512](08_PHI3_HELSTROM512_BWS_TRAZABILIDAD_20261122.md) verificó la reconstrucción numérica de 8.552 filas y la compatibilidad espectral **muestral** de seis modos. La presente auditoría evalúa, para los **512 autovectores y autovalores archivados**, si se cumple la ecuación propia del operador BWS reconstruido desde 7.483 estados y pesos TRAIN, y si los pesos se deducen exactamente de las dificultades guardadas.

## 2. Fuentes históricas identificadas

| Artefacto | SHA-256 | Observación |
|---|---|---|
| `Phi3_train_exact.npy` | `6c2f514200cb806705663bfee928c438fa21ce83c57aadc949e17fcf0bde7af3` | TRAIN, 7.483 × 8.399 |
| `HELSTROM512_EXT_BASIS_REBUILT.npz` | `1831b92ff336bb9aa86bc5850d48cab3f40bcabc42658ed58f9969a4a1e9c9b4` | 320 modos positivos, 192 negativos |
| `HELSTROM512_COORDINATES_CACHE.npz` | `4a2ebcd6f1fc19663c68ae202eb9caca4a3d607a17dc410e2efaf5f7898f27d3` | Caché con etiquetas TRAIN usadas en auditoría anterior |
| `EXT_WEIGHT_train_weights.npy` | `d4b79177d23db03270dd480a5d94bd41a52c2fcf2d24c1a87a16388f7179b4c6` | Huella previamente registrada; **sin sello histórico independiente de creación** |
| `EXT_WEIGHT_train_difficulty.npy` | `44eb2a22e83d0d42ca64978ee9d9ec601973dca499f98b824fbf0590db157564` | Dificultad usada para reconstrucción |
| `FINE_ERROR_train_difficulty.npy` | `44eb2a22e83d0d42ca64978ee9d9ec601973dca499f98b824fbf0590db157564` | Archivo byte a byte idéntico al anterior |

La comprobación de etiquetas TRAIN frente a `df_final.pkl` se documentó previamente, por separado; esta prueba no abre `df_final.pkl` ni VAL/TEST. No se validó cronología de archivos.

## 3. Ecuación del operador ponderado

Con `eta = 0,5`, para etiquetas 0=AFM y 1=FM, se auditó:

$$
\Delta_\mathrm{BWS}=\frac12\rho_\mathrm{FM}-\frac12\rho_\mathrm{AFM},\qquad
\rho_c=\frac{\sum_{n:y_n=c}w_n\,|\Phi_3(x_n)\rangle\langle\Phi_3(x_n)|}{\sum_{n:y_n=c}w_n}.
$$

Para cada modo archivado, se calculó la diferencia `r_k = Delta @ v_k - lambda_k * v_k`, su norma L2, su versión relativa y la diferencia entre el autovalor archivado y el cociente de Rayleigh. La aplicación usó productos matrices-vector por bloques, sin formar una matriz densa de 8.399 × 8.399, y sin resolver de nuevo el problema propio con `eigsh`.

## 4. Resultados de ortogonalidad y residuos espectrales

| Métrica | Resultado |
|---|---:|
| Modos evaluados | **512 / 512** |
| Modos positivos | 320 |
| Modos negativos | 192 |
| Error máximo de Gram (`Vᴴ V − I`) | `3.96573809347e-08` |
| Máximo solapamiento fuera de diagonal | `1.50047226533e-08` |
| Máximo residuo propio absoluto | `7.88064368297e-10` |
| Máximo residuo propio relativo | `1.60889790506e-07` |
| Máximo error de Rayleigh | `3.53883589099e-16` |
| Máximo de parte imaginaria del cociente de Rayleigh | `1.83665357103e-17` |
| Modos que satisfacen residuo absoluto `≤ 1e−6` | `512` |
| Modos que satisfacen residuo relativo `≤ 1e−4` | `512` |
| Resultado numérico del operador (`veredicto_numerico`) | **True** |

Por sector:

| Sector | Modos | Residuo relativo medio | Residuo relativo máximo |
|---|---:|---:|---:|
| Positivo | 320 | `5.70888257692e-08` | `1.60889790506e-07` |
| Negativo | 192 | `4.41174456971e-08` | `1.36071616913e-07` |

El peor residuo relativo procede del modo positivo de índice 311 (índice base cero), con valor `1.60889790506e-07`. Todos los 512 modos satisfacen las tolerancias de esta auditoría.

**Conclusión respaldada:** los 512 pares propios almacenados son numéricamente compatibles con la acción del operador BWS definida por las entradas archivadas. **No se certifica** por este método que sean exactamente los 320 mayores autovalores positivos y los 192 más negativos del espectro *global* de 8.399 dimensiones; la prueba tampoco autentica el entrenamiento original.

## 5. Pesos históricos Smooth-L2-K10

La regla identificada en la fuente experimental histórica y evaluada sobre las 7.483 filas es:

$$
w_n = 1+2\operatorname{sigmoid}\big[-10(2y_n-1)(d_n-0.5)\big].
$$

| Métrica | Resultado |
|---|---:|
| Pesos TRAIN | 7.483 |
| Peso mínimo | `1.01499914447` |
| Peso medio | `1.49942255128` |
| Peso máximo | `2.98281342624` |
| Coincidencias usando `EXT_WEIGHT_train_difficulty.npy` | 7.483/7.483 |
| Coincidencias usando `FINE_ERROR_train_difficulty.npy` | 7.483/7.483 |
| Error máximo de reconstrucción | `4.4408920985e-16` |
| Error RMS | `6.09595713982e-17` |

Los dos archivos de dificultad tienen **la misma huella SHA-256**. Ello respalda identidad de contenido, no independencia de origen. La reconstrucción del vector de pesos valida su regla algebraica y el orden compatible con las etiquetas TRAIN almacenadas, **pero no demuestra que los valores de dificultad fueran calculados mediante folds OOF válidos** ni que no hubiesen sido derivados de resultados usados más tarde en validación.

## 6. Incidencia de ejecución: FileExistsError

El registro de PowerShell contiene una ejecución terminada con `veredicto_numerico=True` y salida a `Downloads`. Posteriormente, una ejecución de la misma auditoría dirigida a `Tesis5_CONSOLIDACION` completó los cálculos pero falló al guardar porque **ya existía** `AUDITORIA_BWS_512_MODOS_Y_PESOS_RESULTADO.json` en la ruta de salida. El programa abre el archivo en modo `x` para impedir sobrescritura. Es una colisión de salida, **no un error del operador**. No eliminar ni sobrescribir evidencias anteriores para resolverlo: si se necesita otro informe, usar nombre distinto y comparar SHA-256.

## 7. Dictamen y pendientes

**Certificado numéricamente dentro de las tolerancias:** (1) todos los 512 pares propios cumplen los residuos; (2) la base es casi ortonormal; (3) las dificultades archivadas reconstruyen exactamente el vector de pesos TRAIN mediante Smooth-L2-K10; (4) el informe muestra los hashes de entradas utilizadas.

**No certificado todavía:** (a) procedencia OOF y separación de folds en `difficulty`; (b) extremalidad del conjunto espectral frente a autovalores excluidos; (c) cronología original de artefactos; (d) validez estadística prospectiva, fuga composicional, evaluaciones VAL/TEST o QPU. El `veredicto_numerico=True` del script depende de Gram y residuos; la reconstrucción algebraica de pesos queda reportada como comprobación adicional y es positiva para ambas fuentes.

**Siguiente auditoría prioritaria recomendada:** trazabilidad forense del procedimiento OOF que produjo `FINE_ERROR_train_difficulty.npy` (definición de folds, aislamiento de etiquetas de validación, `seed`, datos de entrada y fechas/versiones de checkpoint); en paralelo, diseñar una prueba de extremalidad fuera del subespacio retenido con un operador matricial de TRAIN, para evitar asumir optimalidad global sin medirla.

## 8. Reproducibilidad y publicación

- Informe agregado: [`AUDITORIA_BWS_512_MODOS_Y_PESOS_RESULTADO_PUBLICO.json`](../../reports/H2B2A7_PHI3_HELSTROM512_BWS/AUDITORIA_BWS_512_MODOS_Y_PESOS_RESULTADO_PUBLICO.json), conserva los 512 resultados por modo sin divulgar rutas locales absolutas.
- Script reproducible adaptado para rutas portables: [`AUDITAR_BWS_512_MODOS_Y_ORIGEN_PESOS_SOLO_LECTURA.py`](../../scripts/auditoria/AUDITAR_BWS_512_MODOS_Y_ORIGEN_PESOS_SOLO_LECTURA.py); la adaptación pública modifica **únicamente rutas por defecto**, y su `--self-test` pasa localmente.
- No se adjuntan vectores de estado, etiquetas individuales, datos composicionales por muestra ni `.npy` históricos.
- Los valores incluidos no justifican afirmar un entrenamiento nuevo, un experimento QPU, la ausencia de fugas o un AUC prospectivo.
