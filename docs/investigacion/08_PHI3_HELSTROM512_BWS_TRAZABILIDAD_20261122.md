# H2B2A7 — Corte documental pos-`13d3eaf`: Phi3, cobertura, Helstrom512 y operador BWS

> **Corte documental:** 22 de noviembre de 2026.  
> **Repositorio:** `0AVDV0/Prediccion-computacion-cuantica`.  
> **Rama de investigación:** `feature/h2b2a7-documentacion-cientifica`.  
> **Base remota consultada:** [`13d3eaf`](https://github.com/0AVDV0/Prediccion-computacion-cuantica/commit/13d3eafab43f9c3ebfc3de4f4e4bd4f512b368fb) — `docs(h2b2a7): verificar codificacion 3S, cache y particiones`.  
> **Tipo de evidencia:** auditorías retrospectivas, independientes y de solo lectura sobre artefactos históricos; no son nuevos entrenamientos ni evaluación prospectiva.  
> **Estado:** `PHI3_Y_HELSTROM512_EXHAUSTIVOS_VERIFICADOS__BWS_6_MODOS_VERIFICADOS__BWS_512_Y_PESOS_PENDIENTES`.

## 1. Propósito, límite y relación con `07`

El commit `13d3eaf` ya documenta la reconstrucción `PSI7_ALL_3S.npy` desde `df_final.pkl` y la coherencia del caché 3S (7.483 estados `complex64` idénticos), así como la partición por posiciones. **El presente informe registra las auditorías posteriores**, sin sustituir `07_CODIFICACION_3S_VERIFICACION_NUMERICA_PSI7.md`, sin modificar checkpoints y sin afirmar cronologías de ejecución.

Se distinguen **dos objetos matemáticos relacionados, pero auditados por separado**: la codificación 3S en siete qubits, y las amplitudes simétricas `Phi3` de tres copias sobre un soporte de 8.399 triples. Ambos emplean fracciones atómicas y fase composicional, pero la reconstrucción exhaustiva aquí documentada parte directamente de `df_final.pkl` y los splits; no presupone una dependencia histórica probada entre archivos `PSI7_ALL_3S.npy` y `Phi3_*`.

**Regla de interpretación:** exactitud entre archivos o residuos pequeños no prueban origen temporal, ausencia de fuga composicional, calidad predictiva, optimalidad global del subespacio ni ejecución QPU.

### Registro lógico de auditorías posteriores a `13d3eaf`

| Paso lógico | Evidencia analizada | Alcance y resultado |
|---|---|---|
| Inspección de fuente | `EXTRACCION_BWS_PHI3_CORREGIDA.txt`; `EXTRACCION_ORDEN_COMPOSICIONAL_PHI3.txt` | Inspección estática de celdas y funciones, sin ejecución del notebook. |
| Base y coordenadas: prueba inicial | `AUDITORIA_PHI3_BWS_COORDENADAS_RESULTADO.json` | 16 TRAIN y 16 VAL; errores máximos de reconstrucción `6,0643e-8` y `6,1439e-8`; 181 VAL subnormalizadas identificadas. |
| Origen composicional: prueba inicial | `AUDITORIA_ORIGEN_COMPOSICIONAL_PHI3_RESULTADO.json` | 16 TRAIN y 16 VAL; orden atómico compatible y orden original del DataFrame incompatible. |
| Origen composicional exhaustivo | `AUDITORIA_PHI3_EXHAUSTIVA_RESULTADO.json` | 8.552 de 8.552 filas verificadas. |
| Cobertura y novedad | `AUDITORIA_PHI3_COBERTURA_181_RESULTADO.json` | Masa proyectada y cruce 292/777 con 181 incompletas explicadas. |
| Coordenadas Helstrom512 exhaustivas | `AUDITORIA_HELSTROM512_EXHAUSTIVA_RESULTADO.json` | 8.552 de 8.552 filas verificadas y masa adicional fuera de 512 cuantificada. |
| Acción del operador BWS | `AUDITORIA_OPERADOR_BWS_RESIDUOS_RESULTADO.json` | Seis pares propios seleccionados; residuos muy pequeños. |

Los informes muestrales y las extracciones anteriores se conservaron como antecedentes locales; **las cuatro salidas exhaustiva/cobertura/espectral agregadas constituyen el paquete publicable actual**. No atribuir fechas individuales de ejecución que no estén respaldadas por los artefactos.

**Incidencia de reproducibilidad:** el primer script de cobertura interrumpió su ejecución por una referencia a la variable `decimals` en lugar de `decimales`. Se corrigió sin modificar fuentes históricas; el JSON de cobertura incorporado corresponde a una ejecución posterior completa. La falla inicial no se interpreta como discrepancia científica y no se omite de la trazabilidad.

## 2. Archivos de entrada y autenticación

| Archivo histórico (permanece fuera del repositorio) | SHA-256 | Rol |
|---|---|---|
| `df_final.pkl` | `42c0a2afc92c65b29a9f081bdff813362a8246f020e928bd634ed4a6599008f2` | 10.691 muestras; 84 columnas `p_X` |
| `transfer_splits_A4_AQ4.npz` | `1f9eb162adaf0d10301f5b6deb761a15ba5ef9fbb231080e38f0902c826812ed` | 7.483 TRAIN; 1.069 VAL; TEST no utilizado en estas verificaciones |
| `Phi3_train_exact.npy` | `6c2f514200cb806705663bfee928c438fa21ce83c57aadc949e17fcf0bde7af3` | Phi3 TRAIN, (7483, 8399) |
| `Phi3_val_exact.npy` | `010d7089bad3b8e204f7a0909985b0f402aec38a7d7079d2d06a40afb31f4051` | Phi3 VAL, (1069, 8399) |
| `Phi3_support_triples.npy` | `f3b232dde3865498a0a17a6d3ab9a6d23399e5e60c7b3ad4082cdb6aad73c2c5` | Soporte de 8.399 triples ordenados |
| `HELSTROM512_EXT_BASIS_REBUILT.npz` | `1831b92ff336bb9aa86bc5850d48cab3f40bcabc42658ed58f9969a4a1e9c9b4` | `Vplus` (8399, 320); `Vminus` (8399, 192) y autovalores |
| `HELSTROM512_COORDINATES_CACHE.npz` | `4a2ebcd6f1fc19663c68ae202eb9caca4a3d607a17dc410e2efaf5f7898f27d3` | Coordenadas `C_train` y `C_val` (512 dimensiones) |
| `EXT_WEIGHT_train_weights.npy` | `d4b79177d23db03270dd480a5d94bd41a52c2fcf2d24c1a87a16388f7179b4c6` | Pesos utilizados en el operador BWS; **SHA calculado en auditoría reciente, sin cotejo con hash histórico independiente** |

Los SHA referidos son de los **archivos de entrada históricos**; no de las versiones publicables de los informes JSON. No se incluyen datos brutos, composiciones por fila, vectores complejos individuales, contraseñas ni tokens.

## 3. Auditoría A: origen composicional y reconstrucción exhaustiva de Phi3

En el orden del DataFrame, el soporte no coincidía (6.155 triples faltantes y 6.155 adicionales en la comparación muestral). Ordenando las 84 fracciones `p_X` por **número atómico ascendente**, la reconstrucción produjo exactamente el soporte archivado de **8.399 triples**, sin faltantes ni extras.

Se define `p_i>=0` normalizado por fila y la amplitud de una copia:

$$\alpha_i(x)=\sqrt{p_i(x)}\exp(i\pi p_i(x)).$$

La coordenada para `i <= j <= k`, cuando el triple está en el soporte TRAIN, es

$$[\Phi_3(x)]_{ijk}=\sqrt{m_{ijk}}\,\alpha_i(x)\alpha_j(x)\alpha_k(x),\qquad m_{ijk}\in\{1,3,6\}.$$

La auditoría exhaustiva comparó todas las amplitudes archivadas de las **8.552** filas, con tolerancia por amplitud `1e-6`.

| Verificación | TRAIN | VAL |
|---|---:|---:|
| Filas verificadas y coincidentes | 7.483 / 7.483 | 1.069 / 1.069 |
| Amplitudes por fila | 8.399 | 8.399 |
| Error máximo por amplitud | 1,0745380e-7 | 8,6001670e-8 |
| Error RMS | 4,782180e-10 | 4,787246e-10 |
| Filas con norma² < 0,999999 | 0 | 181 |

**Conclusión certificada:** consistencia numérica exhaustiva del origen composicional de `Phi3_train_exact.npy` y `Phi3_val_exact.npy` desde el DataFrame y la partición identificados. **No certifica** la cronología del notebook.

**Evidencia:** [`AUDITORIA_PHI3_EXHAUSTIVA_RESULTADO.json`](../../reports/H2B2A7_PHI3_HELSTROM512_BWS/AUDITORIA_PHI3_EXHAUSTIVA_RESULTADO.json).

## 4. Auditoría B: cobertura del soporte y composiciones nuevas

El soporte simétrico fue reconstruido exclusivamente de TRAIN. Su masa teórica retenida en validación es:

$$C(x)=\sum_{(i,j,k)\in S_{\rm TRAIN}}m_{ijk}p_i(x)p_j(x)=\|\Phi_{3,S}(x)\|^2.$$

La masa excluida es `L(x)=1-C(x)`, equivalente a sumar los triples fuera del soporte. El error máximo entre norma² archivada y retención analítica fue **6,2229225e-8**; el error máximo de la identidad `C(x)+L(x)=1` fue **1,1102230e-15**.

| Composiciones de VAL (comparación por fracciones redondeadas) | Cobertura completa | Cobertura incompleta | Total |
|---|---:|---:|---:|
| Ya vistas en TRAIN | 292 | 0 | 292 |
| Nuevas frente a TRAIN | 596 | 181 | 777 |
| **Total** | **888** | **181** | **1.069** |

La tabla es **idéntica** con redondeos de 6, 9, 10 y 12 decimales y reproduce el resultado de la auditoría composicional XV (292 coincidencias a 10 decimales). «Nueva» se refiere a **fracción composicional**, no a estructura cristalográfica.

En las 181 incompletas: norma² media `0,86744517`, norma² mínima cercana a `0,25`, masa omitida media `0,13255484`, mediana `0,09876543`, máximo `0,75`; media de triples faltantes `2,265` y máximo `16`. **Cero** muestras contienen elementos individuales ausentes de TRAIN. Las **181/181** pierden masa por triples nuevos formados por elementos ya vistos; masa omitida total por ese mecanismo `23,99242657` (suma sobre muestras, **no** porcentaje global).

**Conclusión certificada:** la subnormalización de validación se explica cuantitativamente por una proyección al soporte TRAIN; no equivale por sí misma a error predictivo ni a fuga de etiquetas.

**Evidencia:** [`AUDITORIA_PHI3_COBERTURA_181_RESULTADO.json`](../../reports/H2B2A7_PHI3_HELSTROM512_BWS/AUDITORIA_PHI3_COBERTURA_181_RESULTADO.json).

## 5. Auditoría C: reconstrucción exhaustiva de las coordenadas Helstrom512

La base archivada define `Vret = [Vplus | Vminus]`, de dimensión `(8399,512)`, con 320 modos de autovalor positivo y 192 negativo. Con estados en convención de filas, las coordenadas se reproducen mediante

$$C_{512}(x)=\Phi_3(x)\,\overline{V_{\rm ret}}.$$

| Comprobación | TRAIN | VAL |
|---|---:|---:|
| Filas coincidentes (tol. `1e-5`) | 7.483 / 7.483 | 1.069 / 1.069 |
| Error máximo de coordenada | 4,7880349e-8 | 4,6020381e-8 |
| Error RMS | 1,3125310e-9 | 1,2798691e-9 |
| Norma² media Phi3 | 1,0000000073 | 0,9775562034 |
| Norma² media Helstrom512 | 0,8154279392 | 0,7788475334 |
| Masa media fuera del subespacio 512 **dentro de Phi3** | 0,1845720681 | 0,1987086701 |

`max_exceso_norma2_512_sobre_phi3 = 0` en ambos grupos. La ortogonalidad sólo se verificó en una **muestra de 48 modos** (error máximo `3,2705432e-8`): no declarar aquí ortogonalidad completa de los 512.

En las **181** muestras con soporte incompleto, norma² media `C512=0,55075699`; la pérdida media **adicional dentro del espacio Phi3** es `0,31668818`. Al sumarla a la pérdida media del soporte `0,13255484`, se obtiene una norma cuadrática residual aproximada `0,55075699`. Las 181 reconstrucciones no presentan anomalía de precisión: error máximo `4,0705995e-8`.

**Conclusión certificada:** la coordenada archivada es una proyección de los `Phi3` archivados sobre los modos de la base congelada, coincidente en 8.552 filas. **No demuestra** la procedencia del propio operador espectral, su rango óptimo, ni la calidad de clasificación de los estados proyectados.

**Evidencia:** [`AUDITORIA_HELSTROM512_EXHAUSTIVA_RESULTADO.json`](../../reports/H2B2A7_PHI3_HELSTROM512_BWS/AUDITORIA_HELSTROM512_EXHAUSTIVA_RESULTADO.json).

## 6. Auditoría D: ecuación propia del operador BWS ponderado — seis modos

Del código histórico se extrajo la definición del operador, con `eta=0,5`, TRAIN y pesos de muestra:

$$\Delta_{\rm BWS}=\eta\rho_{\rm FM}-(1-\eta)\rho_{\rm AFM},\qquad \rho_c=\frac{\sum_{n:y_n=c}w_n|\Phi_3(x_n)\rangle\langle\Phi_3(x_n)|}{\sum_{n:y_n=c} w_n}.$$

La auditoría **no ejecuta `eigsh` ni reajusta una base**. Comprueba la ecuación `Delta v_k ≈ lambda_k v_k` contra seis pares propios archivados (tres positivos: posiciones `0,159,319`; tres negativos: `0,95,191`).

| Modo | Autovalor archivado | Residuo relativo L2 |
|---|---:|---:|
| `+` índice 0 | +0,0364354370 | 2,1629e-8 |
| `+` índice 159 | +0,0003383527 | 4,4659e-8 |
| `+` índice 319 | +0,0001439036 | 1,0534e-7 |
| `−` índice 0 | −0,0106926361 | 5,0424e-8 |
| `−` índice 95 | −0,0006151504 | 3,9824e-8 |
| `−` índice 191 | −0,0003211893 | 7,8101e-8 |

Máximo residuo absoluto `7,8806438e-10`; relativo `1,0533646e-7`; ortogonalidad de los seis modos `3,0354519e-8`. El cociente de Rayleigh reproduce los seis autovalores con errores entre ~`1e-20` y ~`1e-16`.

Se utilizaron etiquetas `y_train` archivadas (`AFM=3144`, `FM=4339`) previamente comparadas con el DataFrame y pesos `EXT_WEIGHT_train_weights.npy` (mínimo `1,01499914`, media `1,49942255`, máximo `2,98281343`). **La huella de los pesos fue calculada ahora, pero no está autenticada contra una fuente anterior independiente.**

**Conclusión certificada:** compatibilidad numérica muy alta entre los seis pares propios seleccionados y la acción del operador BWS definido por los artefactos disponibles. No se extiende el resultado a los 512 modos ni se declara optimalidad espectral global.

**Evidencia:** [`AUDITORIA_OPERADOR_BWS_RESIDUOS_RESULTADO.json`](../../reports/H2B2A7_PHI3_HELSTROM512_BWS/AUDITORIA_OPERADOR_BWS_RESIDUOS_RESULTADO.json).

## 7. Hipótesis y dependencias todavía abiertas

**Prioridad inmediata, NO ejecutada en este corte:** `AUDITAR_BWS_512_MODOS_Y_ORIGEN_PESOS_SOLO_LECTURA.py`. Debe comprobar residuos de **320+192** modos, la ortogonalidad global y, si existe un archivo OOF de dificultad autorizado, comparar los pesos por fila con la regla histórica `Smooth-L2-K10`:

$$w_n=1+2\sigma\left[-10(2y_n-1)(d_n-0,5)\right].$$

La coincidencia de pesos, aun si fuera exacta, no establecería el linaje temporal de su dificultad OOF. Tampoco certifica la selección óptima de los 512 autovalores extremos de todo el espectro ni la preparación de estados en QPU.

Además, siguen **abiertas y separadas** las amenazas metodológicas de validación ya documentadas en `04_VALIDACION_Y_LIMITACIONES.md`, especialmente el solapamiento de composiciones entre las particiones originales. Son pruebas de integridad matemática retrospectiva, **no** evaluación confirmatoria en composiciones nunca vistas.

| Afirmación | Estado al corte |
|---|---|
| Origen desde composiciones y soporte de Phi3 (TRAIN+VAL) | **Verificación exhaustiva** |
| Explicación de las 181 normas² incompletas | **Verificación analítica y numérica** |
| Reconstrucción de coordenadas Helstrom512 (TRAIN+VAL) | **Verificación exhaustiva** |
| Ecuación propia del operador BWS | **Muestreo de 6/512 modos** |
| Origen algebraico fila a fila de los pesos | **Pendiente** |
| Residuos de los 512 modos y ortogonalidad total | **Pendiente** |
| Extremos globales del espectro / optimalidad | **No certificado** |
| Teacher, cronología, generalización estricta, QPU | **No certificados por estas pruebas** |

## 8. Protocolo de preservación y publicación

1. Publicar este documento nuevo como `docs/investigacion/08_PHI3_HELSTROM512_BWS_TRAZABILIDAD_20261122.md`, sin reescribir `07` ni los checkpoints.
2. Conservar los JSON agregados en `reports/H2B2A7_PHI3_HELSTROM512_BWS/` y el manifiesto de hashes de fuentes. Se ha **redactado una ruta absoluta local** en la copia publicable del informe BWS; el original permanece local e inalterado.
3. No agregar a GitHub los archivos binarios `.npy`, `.npz`, `.pkl`, datasets, índices por fila ni el notebook completo por defecto. Antes de añadir scripts de auditoría, comprobar su versión exacta y sus autopruebas.
4. Verificar `git status`, rama y `origin` localmente; hacer `git fetch origin`; sólo usar `git pull --ff-only` si corresponde y el árbol local está limpio. No utilizar `git push --force`.
5. Incorporar los archivos documentales nuevos mediante **commit independiente** del protocolo BWS-512 pendiente; usar una nueva entrada documental posterior cuando exista su informe real.

## 9. Fuentes internas y ruta de navegación

- [`07_CODIFICACION_3S_VERIFICACION_NUMERICA_PSI7.md`](07_CODIFICACION_3S_VERIFICACION_NUMERICA_PSI7.md): corte anterior ya publicado.
- [`03_MATRIZ_DE_EVIDENCIA.md`](03_MATRIZ_DE_EVIDENCIA.md): reglas de alcance científico.
- [`04_VALIDACION_Y_LIMITACIONES.md`](04_VALIDACION_Y_LIMITACIONES.md): validez y solapamiento composicional.
- [`reports/H2B2A7_PHI3_HELSTROM512_BWS/README.md`](../../reports/H2B2A7_PHI3_HELSTROM512_BWS/README.md): inventario de JSON y convención de publicación.
- [`reports/H2B2A7_PHI3_HELSTROM512_BWS/MANIFIESTO_FUENTES_SHA256.csv`](../../reports/H2B2A7_PHI3_HELSTROM512_BWS/MANIFIESTO_FUENTES_SHA256.csv): huellas de los archivos originales.

**Veredicto documental al 22/11/2026:** cadena composicional y proyección `Phi3→Helstrom512` numéricamente verificadas exhaustivamente para TRAIN y VAL. Soporte BWS respaldado muestralmente por seis pares propios. La prueba de los 512 modos, el origen OOF de pesos y la validez predictiva fuera de composición continúan pendientes.
