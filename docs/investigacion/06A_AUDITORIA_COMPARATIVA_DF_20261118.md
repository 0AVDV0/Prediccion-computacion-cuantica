# H2B2A7 — Auditoría descriptiva de tres DataFrames (18-11-2026)

> **Estado:** inventario y contraste agregado retrospectivo con ficheros locales. **No acredita** reproducción de los notebooks, identidad fila a fila, alineación con `PSI7_ALL_3S.npy` ni generalización. Las huellas siguientes identifican los **informes** ejecutados, no sustituyen las huellas de los datos originales.

## 1. Inventario de datos

| Universo | Filas | Columnas | `p_X` | Composiciones únicas por firma (9 decimales) | Firmas con ambas etiquetas | FM / AFM |
|---|---:|---:|---:|---:|---:|---|
| 13 bloques composicionales | 24.174 | 95 | 84 | 15.719 | 341 | 16.364 / 7.810 |
| CSV estructural `dataset_listo_opcion_A.csv` | 10.678 | 226 | 84 | 8.379 | 91 | 6.196 / 4.482 |
| Checkpoint `df_final.pkl` | 10.691 | 226 | 84 | 8.381 | 92 | 6.199 / 4.492 |

Cada fila fue reportada con fracciones composicionales numéricas y suma cercana a uno dentro de `1e-5`; el informe por sí solo no certifica la ausencia de valores negativos en las tres tablas ni autentica la fórmula química original.

## 2. Relaciones de inclusión válidas

- Las 10.678 filas estructurales son un **submulticonjunto** por firma de composición y etiqueta de los 24.174 registros.
- Las 10.678 filas también son un submulticonjunto por firma y etiqueta de los 10.691 registros; en el histórico hay **13 ocurrencias adicionales**, descompuestas en **3 FM y 10 AFM**. Contiene **dos composiciones nuevas** respecto del CSV de 10.678.
- En comparación con los bloques originales, los 10.691 tienen **una firma de composición no encontrada**, cuatro ocurrencias que exceden multiplicidad composicional, o seis si se incluye la etiqueta en la clave.
- La inclusión por `(p_X, etiqueta)` **no** prueba misma fila, estructura o procedencia; las duplicaciones impiden emparejamiento físico inequívoco.

## 3. Comparación de 226 columnas

- Los dos conjuntos de 10.678 y 10.691 tienen las **mismas 226 columnas en el mismo orden**, pero el orden de las primeras 10.678 firmas y etiquetas **no coincide**.
- Por huella conjunta de las 226 columnas, con cifras numéricas redondeadas a 9 decimales y textos exactos, **67** filas de la versión de 10.678 no tienen contrapartida exacta en la de 10.691; hay **80** huellas excedentes en esta última. La resta **80−67=13** conserva la diferencia total. **No afirmar** que existen 67 materiales físicos cambiados.
- La auditoría marginal condicionada a composición + etiqueta detecta **18 de 226 columnas** con déficits bajo modo estricto: **16 Magpie y 2 descriptores adicionales**. Se encontraron **7.284 grupos composicional-etiquetados 1:1**, que no garantizan identidad del registro experimental.
- Entre las discrepancias marginales: `MagpieData avg_dev AtomicWeight`: 18; `avg_atomic_weight`: 15; `MagpieData avg_dev GSmagmom`: 7; `MagpieData avg_dev GSvolume_pa`: 6. El déficit por columna no es un conteo exacto de filas alteradas.
- **Cero discrepancias en las 84 columnas `p_X` es parcialmente tautológico**: dichas columnas ya forman la propia clave de agrupación a nueve decimales. En las cinco columnas de identificación/estructura tampoco hay déficits marginales, lo que **no demuestra** identidad de su asociación conjunta dentro de grupos duplicados.
- La variante llamada «tolerante» compara **formato decimal a seis decimales**, no tolerancias numéricas `abs(a−b)≤tol` o `np.isclose`. Las 33 columnas detectadas por ese modo no deben interpretarse como diferencias físicas adicionales ni como resultado de una regla de tolerancia anidada. Debe hacerse un test `isclose` explícito si se necesita cuantificar errores de redondeo.

## 4. Importancia para la codificación cuántica

La familia de modelos H2B2 utiliza estados `PSI7_ALL_3S.npy` de 7 qubits para 7.483 materiales. **Aún no se ha autenticado** desde cuál versión de DF, orden de muestras, reglas de split, orden de las 84 columnas `p_X`, fases y permutación de amplitudes se generó ese archivo. Tampoco se conoce si las diferencias en Magpie afectaron alguna transformación anterior a dicho encoding.

Al construir estados exclusivamente como función determinista de `p_X`, composiciones idénticas producen estados indistinguibles por una medición que solo tiene ese estado disponible. Las 341/91/92 firmas con etiquetas FM y AFM opuestas son una **alerta de representatividad**, no prueba automática de etiquetas erróneas: pueden representar estructuras y condiciones físicas distintas.

## 5. Fuentes auditables y riesgos

| Informe | SHA256 del archivo |
|---|---|
| `DIAGNOSTICO_DF_24174_10678.json` | `2887ccf63e498702f0a78f4a394e86652648618429f0daa7ed2e155f6b7e3059` |
| `DIAGNOSTICO_DF_24174_10678_10691.json` | `b057cc1fa1816fc52acb8f717c18ed3cf02c81174dfdf61bd6dad59caefbf5c4` |
| `AUDITORIA_13_DIFERENCIAS_RESULTADO.json` | `e95627fc97f36361546666a6b841f82d4c33558e63e5d9f1ff1190e341935d7d` |
| `AUDITORIA_226_COLUMNAS_RESULTADO.json` | `51e12380daa50e60d3e2bb3a53a114dfdb1a3e39ed6135b48d7b73d6cbee2ffd` |

Los informes contienen únicamente agregados, nombres de columnas y huellas; no filas individuales de materiales. Los datasets y notebooks históricos no se incluyen en este paquete. Los hashes de datos originales se conservan en los informes.

**Siguiente auditoría:** cotejo ordenado `df_final.pkl` → índices del split histórico → lista de columnas y amplitudes de `PSI7_ALL_3S.npy`, tomando como referencia la implementación original en el notebook, y sin reentrenar, modificar, consultar OUTER HOLD para selección de parámetros ni ejecutar QPU.
