# Arquitectura física y matemática H2B2A7

> - **Estado:** borrador científico v0.6 (documentación de estudiantes A0–A4-1A); incorporada la certificación numérica de origen H2-A4→H2-B0 y la reducción 21→8 por trazas parciales y la descomposición exacta 16→10 sobre la variedad B8, además de ALS R3; descripción de las piezas sustentadas por evidencia integrada, no especificación final certificada de extremo a extremo.
> - **Rama documental:** `feature/h2b2a7-documentacion-cientifica`.
> - **Procedencia:** documento derivado de `00_MAPA_CIENTIFICO.md`, INTEGRACIÓN-00, INTEGRACIÓN-01 y síntesis 3D.
> - **Regla editorial:** separar identidades algebraicas, implementaciones verificadas, resultados retrospectivos y dependencias por verificar.

## 1. Problema y alcance

El problema central es la discriminación entre materiales con etiquetas **ferromagnética (FM)** y **antiferromagnética (AFM)** mediante una representación cuántica de descriptores de materiales y una función de puntuación. La línea H2B2A7 reúne trabajos previos de codificación, observables físicos, compresión de una referencia de discriminación y arquitecturas estudiante.

El objetivo de este documento es explicar **cómo se conectan los objetos matemáticos**, no atribuir a la arquitectura final todos los resultados de sus precursores. En particular, los experimentos H1/H2A, H2B1 y H2B2 deben distinguirse por la fuente de supervisión, los datos empleados y la naturaleza de su evaluación.

## 2. Mapa de objetos y dimensiones

| Objeto | Forma o dimensión respaldada | Papel | Reserva |
|---|---|---|---|
| Estado de referencia de siete qubits | \(\lvert\psi_7(x)\rangle\in(\mathbb C^2)^{\otimes 7}\) | Codificación previa empleada en el desarrollo multicopia | Documentar el circuito exacto, normalizaciones y transformaciones de entrada desde el notebook original |
| Estado multicopia previo | \(\lvert\psi_7(x)\rangle^{\otimes 3}\) (21 qubits) | Construcción de tres copias de la codificación de siete qubits | La traza parcial es exacta para los subsistemas retenidos, sin preservar todos los observables 21q |
| Observable \(O_f^\star\) de H2B1A | Matriz compleja 256 × 256 para cada uno de cinco folds | Referencia de discriminación en un espacio de ocho qubits | Falta certificar qué entradas y etiquetas se usaron para ajustarlo originalmente |
| Diez canales efectivos H2B1E1 | Cuatro términos diagonales y seis pares Pauli simétricos; operadores \(64\times64\) | Reproducir exactamente el *score* de \(O_f^\star\) sobre \(\rho_6\otimes\rho_4\otimes\rho_4\) | Equivalencia de expectativas sobre B8, no igualdad universal de las matrices 256×256 |
| Configuración C5 de H2B1E3 | `II`, `IY`, `IZ`, `XY`, `ZZ` | Cinco canales fijos para la representación reducida | Su elección global pertenece al desarrollo exploratorio de arquitectura |
| Teacher R3 | \(\widehat s_r=f^\top a+f^\top Q_rg\), con \(Q_r\in\mathbb R^{5\times5}\) y \(\operatorname{rank}(Q_r)\le r\) | Destilación bilineal del score C5; R3 utiliza \(r=3\) | MSE sin penalización explícita, pero la elección global del rango no es una validación confirmatoria |
| Operadores Student 1E/1F | `O_j = U_j† D_j U_j`, con `D_j` diagonal de 64 entradas | Observables efectivos implementados en seis qubits | No se ha certificado el costo físico end-to-end ni el QPY original de 1F |

**Nota de alcance:** las secciones 3 y 4 demuestran algebraicamente el mapa de reducción de estados y de scores dentro de la familia B8. Queda por certificar la procedencia original de los arreglos reducidos, la construcción inicial de \(O_f^\star\) y la equivalencia de recursos físicos de una implementación real.

## 3. Antecedente multicopia y reducción física 21→8

### 3.1. Estado de siete qubits y tres copias

Para cada material \(x\), la codificación previa asigna un vector de amplitudes normalizado \(|\psi_7(x)\rangle\in\mathbb C^{128}\) y una matriz densidad pura:

$$
\rho_7(x)=|\psi_7(x)\rangle\langle\psi_7(x)|.
$$

El antecedente multicopia está descrito por

$$
\rho_{21}(x)=\rho_7^A(x)\otimes\rho_7^B(x)\otimes\rho_7^C(x)
\in\mathbb C^{2^{21}\times2^{21}}.
$$

Son **tres copias preparadas de forma independiente** del mismo estado codificado; la independencia entre copias no implica que los siete qubits *dentro* de cada copia estén separables.

### 3.2. Subestados que se conservan

La celda histórica 77, **H2B2A7-19A**, lee el vector original \(\psi_7\) de forma explícita; no acepta reconstruirlo desde expectativas de seis qubits, porque éstas no determinan una purificación única (`L00149–L00270`). Para examinar los subestados, ejecutaría (si se corriera) las operaciones:

```python
rho6 = partial_trace(state, [6])
rho4 = partial_trace(state, [0, 1, 2, 3, 5, 6])
```

**Fuente primaria:** celda 77, `L00414–L00427`. Bajo la convención Qiskit del índice de qubit, las definiciones son

$$
\rho_6(x):=\operatorname{Tr}_{q_6}[\rho_7(x)]\in\mathbb C^{64\times64}
$$

y

$$
\rho_4(x):=\operatorname{Tr}_{q_0,q_1,q_2,q_3,q_5,q_6}[\rho_7(x)]
\in\mathbb C^{2\times2}.
$$

El subíndice **4** de \(\rho_4\) identifica el *qubit original* \(q_4\); **no** denota una matriz densidad de cuatro qubits. La primera reducción conserva \(q_0,\ldots,q_5\). En \(\rho_6\), el registro local se indexa como esos mismos seis qubits.

### 3.3. Identidad exacta de traza parcial y dimensión B8

Conservemos los seis qubits \(q_0,\ldots,q_5\) de la copia \(A\), el qubit original \(q_4\) de \(B\) y el qubit original \(q_4\) de \(C\). Se descartan respectivamente \(1+6+6=13\) qubits. Por la propiedad de factorización de la traza parcial,

$$
\begin{aligned}
\operatorname{Tr}_{\rm desc}\!\left[\rho_7^A\otimes\rho_7^B\otimes\rho_7^C\right]
&=\operatorname{Tr}_{q_6^A}[\rho_7^A]\otimes
\operatorname{Tr}_{\{q_0,q_1,q_2,q_3,q_5,q_6\}^B}[\rho_7^B]
\otimes\operatorname{Tr}_{\{q_0,q_1,q_2,q_3,q_5,q_6\}^C}[\rho_7^C]\\
&=\boxed{\rho_6\otimes\rho_4\otimes\rho_4}\equiv\rho_{\mathrm{B8}}.
\end{aligned}
$$

La dimensión retenida es \(2^6\cdot2\cdot2=256=2^8\). La celda 9 construye de manera explícita esta matriz (`L01362–L01389`) mediante

```python
R = torch.einsum("nij,nab,ncd->niacjbd", r6, r4, r4)
R = R.reshape(n_muestras, 256, 256)
```

La celda 10 repite la misma contracción en NumPy (`L00587–L00641`), fija **\(q_0\) como bit menos significativo** y declara que \(q_0,q_1\) de B8 son los dos factores finales, mientras \(q_2,\ldots,q_7\) representan el bloque \(\rho_6\) (`L00242–L00251`). Así, el orden de matriz de izquierda a derecha es \(\rho_6\otimes\rho_4\otimes\rho_4\), sin confundir los nombres locales de los qubits B8 con los índices originales de \(\psi_7\).

Esta reducción es una **identidad exacta de estados reducidos** y no requiere aproximación de rango ni aprendizaje. La traza parcial, sin embargo, puede convertir el estado puro original en un estado mixto: no afirmamos que conserve su pureza ni su espectro. No hay una identidad que transforme cualquier observable de 21 qubits en uno de ocho: para \(O_8\) sobre los subsistemas conservados,

$$
\operatorname{Tr}[O_8\rho_{\mathrm{B8}}]
=\operatorname{Tr}[(O_8\otimes I_{\mathrm{desc}})\rho_{21}],
$$

a condición de respetar la permutación de factores que lleva los subsistemas retenidos al orden B8.

**Límite físico:** ocho qubits describen el soporte efectivo del *score* examinado; no prueban que la preparación de tres copias, estados mixtos reducidos, descargas/ancillas o lectura sean realizables con solo ocho qubits físicos y menor costo integral.

### 3.4. Tipo de evidencia y pendiente de procedencia

La identidad de traza parcial es un resultado matemático, y las convenciones de implementación están explícitas en las celdas 9, 10 y 77. **Estas fuentes son código inspeccionado, no una nueva ejecución histórica.** En particular, la celda 77 es una auditoría posterior de preparación de \(\psi_7\), no por sí sola la celda que creó originalmente `RHO6_H2B1A` y `RHO4_H2B1A`. Sus índices, hashes de arrays y proceso generador inicial deben reconstruirse antes de proclamar la trazabilidad completa de esos objetos.

## 4. Procedencia y descomposición exacta del observable B8

### 4.1. Cadena documental y convención de producto tensorial

La secuencia observada de objetos inmediatos es:

```text
H2B1A  O_FOLDS_H2B1A                  (5 × 256 × 256)
   ↓  recuperado por H2B1E0 (celda 10; alternativa: artefacto/objeto previo)
H2B1E0 OSTAR_FOLDS_H2B1E0
   ↓  recuperado por H2B1E1 (celda 11; alternativas de RAM y disco)
H2B1E1 OSTAR_FOLDS_H2B1E1
   ↓  descomposición de matriz en 16 bloques Pauli 6|1|1
H2B1E1 diez canales simétricos EXACTOS para scores sobre B8
   ↓  selección exploratoria; ya no es identidad general
H2B1E3 C5 = (II, IY, IZ, XY, ZZ)
   ↓  destilación bilineal ALS, aproximación de rango r=3
H2B1E3 Teacher R3 → H2B2A0 y etapas posteriores
```

**Fuente inmediata:** celda 10, `L00368–L00472`; celda 11, `L00297–L00490`. Existen rutas alternativas de recuperación desde RAM o un archivo NPZ; el recorrido concreto de la ejecución histórica está documentado en las auditorías de linaje previas. **El origen H2-A4→H2-B0 está ahora certificado numéricamente sin HOLD (§4.2); estas celdas posteriores por sí solas no certifican la identidad de cada objeto en RAM durante todas las transferencias.**

La celda 11 trabaja con el operador hermítico \(O_f^\star\in\mathbb C^{256\times256}\) de cada fold y con los tres bloques físicos \(6|1|1\). La celda 10, por su parte, investiga geometría y entrelazamiento de operadores (Schmidt/MPO/Pauli), pero **no es la fuente primaria de la reducción 16→10**: esa reducción está implementada en la celda 11.

### 4.2. Certificación numérica de origen H2-A4 → H2-B0 (17-11-2026)

**Resultado verificado:** la reconstrucción independiente de los cinco observables de ocho qubits desde los coeficientes originales `B_LABEL_KRR` reproduce las matrices archivadas `O_folds` de H2-B0 con diferencias compatibles con precisión simple, **sin consultar etiquetas, predicciones ni AUC de `OUTER HOLD`, y sin corrección de signo**. Este cierre es de **proveniencia matricial**, no de independencia confirmatoria de la selección global de arquitectura.

**Fuente creadora:** `ModelosDataset2.ipynb`, SHA-256 del notebook `da4c720fa3af1ce13d88184a703aa214cc7d243961e56e12617af9631532a9fd`; celda 312 `4F-H2A4` (SHA-256 de código `fa20d0b6d33d3696210abe1a7c485bef8698ada9ddea24d3ffab2185df596ca8`) y celda 313 `4F-H2B0` (SHA-256 de código `4e2a7acbe0114e728624cdfcae04d1351cc035adeb0b871c84c74738c4f9da26`). La celda 314 identifica la transferencia por RAM/NPZ hacia `O_FOLDS_H2B1A`; la ruta concretamente ejecutada para todas las etapas posteriores y sus hashes de RAM no se autentican por esta prueba.

**Archivos históricos identificados por SHA-256:**

| Archivo | SHA-256 |
|---|---|
| `ARCH4FH2A4_LINEAR_OBSERVABLE_MODELS.npz` | `3eee4d0712b22b688635667eeeb9a8bfb1bdff1a29a929c0924850953254edf2` |
| `ARCH4FH2B0_FOLD_OBSERVABLES.npz` | `2de96b09df0d8150b26801f116dd86ed4a1cdd8e2af1ff28a6a9719cb09d4d5c` |
| `PSI7_ALL_3S.npy` | `85761c0a7df704e46d5e75ff6ac858b7c8c8335dc84506bde5cc9d33d8ebe362` |
| `ARCH4FH2A4_LINEAR_OBSERVABLE_REPORT.json` | `e50a0136df55eb2216aa3826fd2e1757ba62604f70b6f2f2e7e34ceda2552a96` |

**Ajuste original de los coeficientes:** H2-A4 implementa por fold una partición `OUTER TRAIN`/`OUTER HOLD`. `B_LABEL_KRR` escoge el parámetro $\lambda$ mediante un `StratifiedShuffleSplit` interno con 22 % de validación *dentro* de `OUTER TRAIN`, luego reajusta el modelo sobre todo `OUTER TRAIN`. Resuelve

$$
\bigl(K_{T_f,T_f}+|T_f|\lambda_f I\bigr)\alpha_f=2y_{T_f}-1,
$$

con núcleo de Hilbert–Schmidt $K_{ij}=\operatorname{Tr}(\rho_{6,i}\rho_{6,j})[\operatorname{Tr}(\rho_{4,i}\rho_{4,j})]^2$. Los arrays archivados contienen `train_idx_f0...f4` y `alpha_B_LABEL_KRR_f0...f4`: 5.986 entradas en folds 0–2, 5.987 en folds 3–4. Los 7.483 índices forman cinco conjuntos HOLD complementarios **disjuntos y exhaustivos** (cada muestra aparece en HOLD exactamente una vez). No se detectó un vector de coeficientes con soporte explícito en HOLD.

**Reconstrucción sin etiquetas de HOLD:** dados $T_f$ y $\alpha_f$ recuperados directamente del NPZ, se calculó

$$
O_f^{\mathrm{raw}}=\sum_{i\in T_f}\alpha_{f,i}
\bigl(\rho_{6,i}\otimes\rho_{4,i}\otimes\rho_{4,i}\bigr),\quad
c_f=\frac{\operatorname{Tr} O_f^{\mathrm{raw}}}{256},\quad
O_f^{\mathrm{recon}}=\frac{O_f^{\mathrm{raw}}-c_f I}{\lVert O_f^{\mathrm{raw}}-c_fI\rVert_\infty}.
$$

La fuente `PSI7_ALL_3S.npy` contiene `(7483,128)` amplitudes `complex64`. La comparación del kernel inducido desde los estados de siete qubits con el kernel guardado `ARCH4FH2A4_B8_HS_KERNEL_FLOAT32.npy` produjo **diferencia máxima $1.115\times10^{-7}$ en 40 pares muestreados**; no equivale a verificar las $7483^2$ entradas. La desviación máxima de la norma cuadrada de los estados respecto de la unidad fue $2.086\times10^{-7}$.

| Fold | $|T_f|$ | $\|O_f^{\mathrm{recon}}-O_f^{\mathrm{guardado}}\|_{\max}$ | Error Frobenius relativo | Signo necesario |
|---:|---:|---:|---:|---|
| 0 | 5.986 | $3.505765\times10^{-7}$ | $2.407770\times10^{-7}$ | Original |
| 1 | 5.986 | $1.619781\times10^{-7}$ | $1.650668\times10^{-7}$ | Original |
| 2 | 5.986 | $1.697563\times10^{-7}$ | $1.641059\times10^{-7}$ | Original |
| 3 | 5.987 | $2.948927\times10^{-7}$ | $1.771284\times10^{-7}$ | Original |
| 4 | 5.987 | $2.514801\times10^{-7}$ | $2.191255\times10^{-7}$ | Original |

Las comparaciones con **signo invertido** dieron errores máximos de orden $0.54$–$0.67$ y error Frobenius relativo $2.0$, descartando una coincidencia obtenida por inversión de signo. Los cinco `O_folds` también verifican hermiticidad al nivel almacenado, traza normalizada cercana a cero y norma espectral cercana a uno; el orden físico es `[5,4,3,2,1,0,11,18]`.

**Límite metodológico crucial:** el H2-A4 original elige **entre** objetivos `A_TEACHER_KRR`, `B_LABEL_KRR` y `C_PAIRWISE_RANKRLS` ordenando sus AUC promedio sobre los cinco `OUTER HOLD`. H2-B0 permite escoger y orientar vectores candidatos para reconstrucción usando AUC HOLD y norma $\ell_1$; **la reconstrucción directa aquí auditada demuestra que ese paso no era necesario para obtener ninguna de las cinco matrices archivadas**. Ello no convierte en confirmatoria la selección histórica del método, ni las decisiones posteriores de canales C5, rango R3 o estudiantes basadas en evaluaciones ya consultadas. La AUC original `B_LABEL_KRR` media por fold `0.9236863323397297` y OOF combinada `0.9234362199284905` son métricas históricas retrospectivas, **no** nuevas AUC calculadas en esta auditoría.

**Evidencia local primaria:** `FUENTE_ENTRENAMIENTO_H2A4_ORIGEN_OSTAR_H2B2A7.txt`, `FUENTE_CREADORA_OSTAR_C313_C314_H2B2A7.txt`, `AUDITORIA_ESTRUCTURAL_OSTAR_H2B2A7.txt` y `AUDITORIA_NUMERICA_H2A4_A_H2B0_SIN_HOLD.txt`. Fueron examinados el código y los informes de ejecución externa del auditor; no se reprodujo ni volvió a entrenar H2-A4 ni se ejecutaron las celdas del notebook histórico.

### 4.3. Descomposición completa del operador: 16 bloques

Definimos \(\sigma_0=I\), \(\sigma_1=X\), \(\sigma_2=Y\) y \(\sigma_3=Z\). Por completitud y ortogonalidad Hilbert–Schmidt de la base Pauli de dos qubits, todo operador \(O_f^\star\) sobre \(\mathbb C^{64}\otimes\mathbb C^2\otimes\mathbb C^2\) se escribe exactamente como

$$
\boxed{O_f^\star=\sum_{\mu,\nu=0}^{3}B_{f,\mu\nu}\otimes\sigma_\mu\otimes\sigma_\nu},
\qquad B_{f,\mu\nu}\in\mathbb C^{64\times64},
$$

con la proyección de coeficientes

$$
\boxed{B_{f,\mu\nu}=\frac14\,\operatorname{Tr}_{\mathrm{últimos}\;2}
\left[O_f^\star(I_{64}\otimes\sigma_\mu\otimes\sigma_\nu)\right].}
$$

El factor \(1/4\) procede de \(\operatorname{Tr}(\sigma_\mu\sigma_\alpha)=2\delta_{\mu\alpha}\) para cada uno de los dos qubits. El código construye esos bloques por contracción de índices (`decompose_611_h2b1e1`, celda 11, `L00744–L00848`) y reconstruye el operador 256×256 sumando sus 16 términos (`reconstruct_16_h2b1e1`, `L00849–L00897`).

Ésta sí es una **identidad de operadores** en el espacio B8 completo; no depende todavía de que las dos copias \(\rho_4\) sean iguales.

### 4.4. Simetría de las copias idénticas y 10 canales visibles

Para \(\rho_{\mathrm{B8}}(x)=\rho_6(x)\otimes\rho_4(x)\otimes\rho_4(x)\), definamos los momentos Pauli reales de un qubit

$$
m_\mu(x):=\operatorname{Tr}[\sigma_\mu\rho_4(x)],\quad
m_0=1,\quad \mu=0,1,2,3.
$$

La linealidad y la factorización de la traza dan

$$
\begin{aligned}
s_f^\star(x)&:=\operatorname{Tr}[O_f^\star\rho_{\mathrm{B8}}(x)]\\
&=\sum_{\mu,\nu=0}^3
m_\mu(x)m_\nu(x)\operatorname{Tr}[B_{f,\mu\nu}\rho_6(x)].
\end{aligned}
$$

Dado que ambos factores \(\rho_4\) son idénticos, \(m_\mu m_\nu=m_\nu m_\mu\). Definimos entonces **diez** operadores efectivos hermíticos sobre seis qubits:

$$
\boxed{A_{f,\mu\nu}=\begin{cases}
B_{f,\mu\mu},&\mu=\nu,\\
B_{f,\mu\nu}+B_{f,\nu\mu},&\mu<\nu,
\end{cases}}
\qquad 0\le\mu\le\nu\le3.
$$

Así, sin descartar ninguna contribución al score dentro de B8,

$$
\boxed{s_f^\star(x)=\sum_{0\le\mu\le\nu\le3}
\underbrace{m_\mu(x)m_\nu(x)}_{f_{\mu\nu}(x)}
\underbrace{\operatorname{Tr}[A_{f,\mu\nu}\rho_6(x)]}_{g_{f,\mu\nu}(x)}.}
$$

Son \(4+\binom42=10\) pares no ordenados. La lista literal del código (`CHANNEL_PAIRS_H2B1E1`, celda 11, `L00680–L00743`) es

$$
\mathcal C_{10}=(II,IX,IY,IZ,XX,XY,XZ,YY,YZ,ZZ).
$$

**Normalización importante:** para \(\mu<\nu\) el operador de canal que multiplica al único producto de momentos es la **suma**, no el promedio, \(A_{\mu\nu}=B_{\mu\nu}+B_{\nu\mu}\). El promedio aparece en cambio al reconstruir el observable *simetrizado* \(O_{\mathrm{visible}}\): cada uno de los dos Pauli strings recibe \((B_{\mu\nu}+B_{\nu\mu})/2\). Estas dos convenciones son compatibles pero no intercambiables (`build_visible_operator_h2b1e1`, `L00897–L01025`; `effective_channels_h2b1e1`, `L01200–L01343`).

### 4.5. Qué se conserva: score sobre la variedad física, no el operador global

Sea \(S\) el operador SWAP sobre los dos últimos qubits (y la identidad sobre los primeros seis). El componente visible de cualquier observable es

$$
O_{f,\mathrm{visible}}=\tfrac12(O_f^\star+S O_f^\star S),
\qquad O_{f,\mathrm{invisible}}=\tfrac12(O_f^\star-S O_f^\star S).
$$

Como \(S\rho_{\mathrm{B8}}S=\rho_{\mathrm{B8}}\) para todo estado de la forma \(\rho_6\otimes\rho_4\otimes\rho_4\), se deduce

$$
\operatorname{Tr}[O_{f,\mathrm{invisible}}\rho_{\mathrm{B8}}]
=0,
\quad\text{y}\quad
\boxed{\operatorname{Tr}[O_f^\star\rho_{\mathrm{B8}}]
=\operatorname{Tr}[O_{f,\mathrm{visible}}\rho_{\mathrm{B8}}].}
$$

Por lo tanto, la reducción 16→10 es una **equivalencia exacta de funcionales de score sobre la familia de estados B8**; en general, \(O_f^\star\ne O_{f,\mathrm{visible}}\) como matrices de 256×256. La celda 11 mide explícitamente la fracción de energía de Frobenius del operador invisible (`L01500–L01730`), sin afirmar que tal energía sea cero.

El código contiene controles con los siguientes criterios (`L01700–L01900`): error máximo de reconstrucción de los 16 bloques no mayor que \(10^{-8}\); error de score a diez canales y de score del operador visible no mayor que \(2\times10^{-7}\); y diferencia AUC en *hold* no mayor que \(10^{-10}\). Son **umbrales programados**, no nuevas mediciones efectuadas durante esta revisión documental. La prueba de 16 bloques corresponde a identidad global; las dos pruebas con diez canales corresponden a igualdad de scores evaluados en estados B8. No se infiere nueva validez predictiva independiente.

### 4.6. Del conjunto exacto C10 al subconjunto exploratorio C5

La etapa H2B1E1 enumera los \(2^{10}-1=1023\) subconjuntos no vacíos. Para cada tamaño, los subconjuntos y el signo del score se eligen por AUC de **TRAIN dentro de cada fold**, se informa la AUC en *hold* y los coeficientes heredados de \(O_f^\star\) no se reoptimizan (`L01344–L01483`, `L02000–L02375`, `L02593–L02710`). Sin embargo, la función `first_k_reaching_h2b1e1` utiliza explícitamente `mean_hold_AUC` para analizar las fronteras globales de complejidad (`L02843–L02965`). La elección posterior de un tamaño fijo y de C5 debe tratarse como **desarrollo exploratorio condicionado por las evaluaciones históricas**.

El subconjunto C5 utilizado por R3 es

$$
\mathcal C_5=(II,IY,IZ,XY,ZZ).
$$

En particular, la correspondencia de factores locales es

| Canal | \(f_c(x)\) | Operador 6q efectivo \(A_{f,c}\) |
|---|---|---|
| `II` | \(1\) | \(B_{f,II}\) |
| `IY` | \(\langle Y\rangle\) | \(B_{f,IY}+B_{f,YI}\) |
| `IZ` | \(\langle Z\rangle\) | \(B_{f,IZ}+B_{f,ZI}\) |
| `XY` | \(\langle X\rangle\langle Y\rangle\) | \(B_{f,XY}+B_{f,YX}\) |
| `ZZ` | \(\langle Z\rangle^2\) | \(B_{f,ZZ}\) |

Esto enlaza **exactamente la convención de los diez canales** con el vector de características \(\mathbf f=(1,\langle Y\rangle,\langle Z\rangle,\langle X\rangle\langle Y\rangle,\langle Z\rangle^2)^\top\) utilizado en §5 para R3. No convierte el *score* C5 en una reconstrucción universalmente exacta de \(O_f^\star\): eliminar los otros cinco canales es una **ablación aproximada**, y ALS R3 introduce una **segunda aproximación distinta** sobre el score C5.

### 4.7. Alcance físico, estadístico y de ejecución

- **Matemática:** 21→8 es exacto por traza parcial para los subsistemas indicados; 16 bloques es una expansión exacta del operador 8q; 16→10 es exacto para scores sobre B8; 10→5 y C5→R3 no son identidades globales.
- **Trazabilidad:** las celdas heredaron estados reducidos y observables que existían previamente; resta localizar/cotejar la generación inicial y los datos usados para ajustar \(O_f^\star\).
- **Validación histórica:** el código define comparaciones y pruebas, pero esta extracción no incluye sus *outputs*. Mantener separadas las identidades matemáticas demostrables y las tolerancias que el experimento habría verificado al ejecutarse.
- **Recursos físicos:** canales de operadores hermíticos 6q no equivalen automáticamente a seis qubits físicos suficientes para toda la preparación multicopia, a diez circuitos, ni a diez bases Pauli. El costo real exige un plan de preparación, bases, shots y transpilación común a las alternativas.

## 5. Teacher R3: formulación y ajuste ALS cotejados con código histórico

### 5.1. Alcance y fuente primaria

Esta sección se reconstruye directamente a partir de la celda histórica **4F-H2B1E3 — TASK-ALIGNED LOW-RANK BILINEAR SCORE COMPRESSION**, no de una pérdida supuesta. La extracción documental conservó las siguientes referencias:

| Identificador | Valor documentado |
|---|---|
| Notebook original | `ContinuacionnuevaModelosdataset2.ipynb` |
| Celda | Índice **13**, base cero; 4.389 líneas de código |
| SHA-256 del notebook completo, consignado por el extractor | `706319a4375e37098bcd35ec08428fa30e551679f370015f53a5f6977f99c20c` |
| SHA-256 del texto de código de la celda, consignado por el extractor | `79dc041745f32efc063d3d527603934d991570c712ad5c6768afb0a0b269fad1` |
| Evidencia primaria | `FUENTE_PRIMARIA_H2B1E3_R3_H2B2A7.txt`, conservada localmente y **todavía no integrada** en el repositorio |
| Naturaleza de la comprobación | Lectura de fuente; **no** se ejecutó ALS, se comprobaron *outputs* ni se reentrenó el modelo |

Los números `Lxxxxx` que se citan abajo corresponden a las líneas **del código de la celda**, no a líneas físicas del informe de extracción. El hash consignado identifica la fuente declarada por el extractor; la identidad del notebook y los artefactos de ejecución debe corroborarse aparte si se requiere certificación independiente.

### 5.2. Factores físicos y score de referencia C5

La celda fija el orden de canales

$$
\mathcal C_5=(II,IY,IZ,XY,ZZ).
$$

Para cada muestra \(x\) y fold \(k\), define el vector de factores locales

$$
\mathbf f(x)=
\begin{bmatrix}
1 & \langle Y\rangle & \langle Z\rangle &
\langle X\rangle\langle Y\rangle & \langle Z\rangle^2
\end{bmatrix}^{\!\top}
\in\mathbb R^5,
$$

y los cinco valores de expectativa de operadores efectivos de seis qubits:

$$
g_{k,c}(x)=\operatorname{Tr}\!\left[A_{k,c}\rho_6(x)\right],
\qquad
\mathbf g_k(x)\in\mathbb R^5.
$$

El score C5 **a reproducir** es

$$
s_{C5,k}(x)=\mathbf f(x)^\top\mathbf g_k(x)
=\sum_{c\in\mathcal C_5} f_c(x)g_{k,c}(x).
$$

**Fuentes:** comentario inicial de la celda, `L00007–L00031`; canales `L00203–L00218`; recuperación de operadores `L00470–L00575`; matrices `F` y `G` `L00584–L00659`; cómputo del teacher `L01815–L01833`.

La convención de las matrices reducidas, el orden de qubits y la deducción exacta de los cinco factores del score C5 quedan ahora desarrollados en §§3–4. Aún debe certificarse la procedencia histórica de los arreglos originales, no confundida con estas identidades algebraicas.

### 5.3. Modelo de compresión bilineal de rango restringido

La función aproximante es

$$
\boxed{\widehat s_{r,k}(x)=\mathbf f(x)^\top\mathbf a_k+
\mathbf f(x)^\top Q_{r,k}\,\mathbf g_k(x)}
$$

con

$$
\mathbf a_k\in\mathbb R^5,\qquad
Q_{r,k}\in\mathbb R^{5\times5},\qquad
\operatorname{rank}(Q_{r,k})\le r.
$$

Para satisfacer la restricción de rango, el código parametriza

$$
Q_{r,k}=U_{r,k}V_{r,k}^{\top},\qquad
U_{r,k},V_{r,k}\in\mathbb R^{5\times r},
$$

de donde

$$
\widehat s_{r,k}(x)=\mathbf f(x)^\top\mathbf a_k+
\sum_{j=1}^{r}
\big[\mathbf f(x)^\top\mathbf u_{k,j}\big]
\big[\mathbf v_{k,j}^{\top}\mathbf g_k(x)\big].
$$

Esta es una **restricción de rango en la matriz bilineal de coeficientes \(Q\)**, no una compresión de rango de la matriz densidad \(\rho_6\), ni una reducción de seis a tres qubits, ni por sí misma una reducción de número de bases Pauli. **Fuentes:** `L00044–L00101`, `L00950–L00971` y `L00975–L00991`.

### 5.4. Función objetivo exacta y naturaleza de la regularización

Para el conjunto de entrenamiento externo \(T_k\) de cada fold, el optimizador ajusta los parámetros al score C5 previamente calculado:

$$
\boxed{\min_{\mathbf a,U,V}\;\mathcal L_k(\mathbf a,U,V)
=\frac{1}{|T_k|}\sum_{i\in T_k}
\left[
s_{C5,k}(x_i)-\mathbf f_i^\top\mathbf a
-\mathbf f_i^\top U V^\top\mathbf g_{k,i}
\right]^2.}
$$

Aquí \(U,V\in\mathbb R^{5\times r}\); el límite de rango se cumple mediante la factorización. **No se encontró un término de regularización explícita** como \(\lambda\|U\|_F^2\), \(\lambda\|Q\|_F^2\) o una penalización L1. La implementación utiliza *mínimos cuadrados no regularizados* con un procedimiento de estabilización numérica:

- Escalado de cada columna del diseño por su raíz del promedio cuadrático, seguido de desescalado de los coeficientes (`L00882–L00947`). El propio comentario declara que no cambia el problema de mínimos cuadrados no regularizados.
- Solución con `np.linalg.lstsq(..., rcond=1e-12)` (`L00927–L00944`). El parámetro `rcond` fija un umbral de rango numérico de la pseudoinversa; **no es un hiperparámetro Ridge**.
- Reparametrizaciones QR de los factores para estabilizar la libertad de representación \(UV^\top\), preservando \(Q\) salvo redondeo (`L01202–L01221`, `L01280–L01301`).

No se debe describir esta implementación como *ALS con regularización Ridge* ni atribuirle un \(\lambda\) que no existe en el código examinado. **Fuentes:** objetivo declarado `L00104–L00130`; `fit_rank_als_h2b1e3`, `L00991–L01406`.

### 5.5. Dos subproblemas lineales alternados

A cada iteración, el código alterna dos problemas de mínimos cuadrados:

**Bloque A — con \(V\) fijo:** sea \(\mathbf z_i=V^\top\mathbf g_{k,i}\in\mathbb R^r\). La predicción es lineal en \(\mathbf a\) y en los \(5r\) elementos de \(U\):

$$
\widehat s_i=\mathbf f_i^\top\mathbf a
+\sum_{p=1}^{5}\sum_{q=1}^{r}f_{i,p}\,z_{i,q}\,U_{p,q}.
$$

Por ello, el diseño por fila concatena \(\mathbf f_i^\top\) y los productos \(f_{i,p}z_{i,q}\). Se resuelven conjuntamente \(5+5r\) coeficientes mediante `stable_lstsq_h2b1e3`. El código forma `Z=G@V`, `X_U=einsum(F,Z).reshape(n,5*r)` y `X1=[F, X_U]` (`L01140–L01199`).

**Bloque B — con \(U\) fijo:** sea \(\mathbf w_i=U^\top\mathbf f_i\in\mathbb R^r\). Ahora el diseño concatena \(\mathbf f_i^\top\) y \(g_{k,i,p}w_{i,q}\), y se vuelven a ajustar \(\mathbf a\) y los \(5r\) componentes de \(V\). El código forma `W=F@U`, `X_V=einsum(G,W).reshape(n,5*r)` y `X2=[F,X_V]` (`L01224–L01277`).

En ambos bloques, la vectorización usada por `.reshape` es el orden de almacenamiento de NumPy (fila mayor por defecto). No son dos redes neuronales ni dos circuitos cuánticos; son dos soluciones lineales alternadas de una función objetivo **no convexa conjuntamente** en \(U,V\).

El valor de pérdida se recalcula como MSE del score del teacher después de cada par de actualizaciones (`L01304–L01337`).

### 5.6. Convergencia, inicialización y casos de control

Los parámetros de ejecución son:

| Parámetro | Valor en la celda | Línea de código |
|---|---:|---|
| Grados de rango examinados | \(r=0,1,2,3,4,5\) | `L00221–L00229` |
| Iteraciones máximas ALS | 80 | `L00241` |
| Tolerancia de cambio relativo de pérdida | \(10^{-11}\) | `L00243`, `L01350–L01375` |
| `lstsq` `rcond` | \(10^{-12}\) | `L00247`, `L00927–L00944` |
| Reinicios aleatorios deterministas por configuración | 8 | `L00245`, `L01584–L01633` |
| Semilla base | 20261006 | `L00249` |
| Umbral relativo de rango efectivo por SVD | \(10^{-10}\) | `L00254`, `L01691–L01710` |

Para \(r\in\{1,2,3,4\}\) se prueban inicializaciones PCA de \(G_{\mathrm{train}}\), un subconjunto coordenado si está disponible y ocho inicios aleatorios ortogonales. El mejor reinicio se selecciona **únicamente por MSE de score del teacher en TRAIN**, no por AUC del hold (`L01413–L01633`, `L01982–L02098`).

Los dos extremos son controles estructurales:

- \(r=0\): \(Q=0\), se ajusta solamente \(\mathbf f^\top\mathbf a\) mediante mínimos cuadrados; no hay observable variable de \(\rho_6\) (`L01022–L01093`, `L01900–L01931`).
- \(r=5\): se fija \(\mathbf a=0\) y \(Q=I_5\), por lo que \(\widehat s_{5}=s_{C5}\) **algebraicamente por construcción**; no se ejecuta ALS para ese caso (`L01933–L01979`). El código impone un control numérico de error máximo y AUC con tolerancia \(10^{-12}\) (`L02937–L02964`); esta inspección textual no constituye una nueva ejecución de ese control.

La parada temprana se produce cuando la variación relativa absoluta entre dos pérdidas consecutivas cae por debajo de \(10^{-11}\), o se agotan 80 iteraciones. Esa regla **no equivale a una garantía de óptimo global**.

### 5.7. Interpretación física mediante SVD del operador comprimido

Tras ajustar \(Q\), el código calcula la SVD canónica

$$
Q_{r,k}=L_k\,\Sigma_k\,R_k^\top,
\qquad \Sigma_k=\operatorname{diag}(\sigma_{k,1},\ldots).
$$

Con los vectores derechos \(R_{k,cj}\), define los observables efectivos sobre seis qubits

$$
B_{k,j}=\sum_{c\in\mathcal C_5}R_{k,cj}\,A_{k,c},
\qquad B_{k,j}\in\mathbb C^{64\times64}.
$$

La identidad de expectativas sigue de la linealidad de la traza:

$$
\mathbf r_{k,j}^\top\mathbf g_k(x)
=\sum_cR_{k,cj}\operatorname{Tr}[A_{k,c}\rho_6(x)]
=\operatorname{Tr}[B_{k,j}\rho_6(x)].
$$

Por tanto, la misma función aproximante admite la expresión física

$$
\boxed{\widehat s_{r,k}(x)=\mathbf f(x)^\top\mathbf a_k
+\sum_{j=1}^{r_{\mathrm{ef}}}\sigma_{k,j}
\big[\mathbf f(x)^\top\boldsymbol\ell_{k,j}\big]
\operatorname{Tr}[B_{k,j}\rho_6(x)],}
$$

con \(r_{\mathrm{ef}}\le r\) según el umbral numérico de la SVD. El código forma \(B_j\) y simetriza numéricamente \((B_j+B_j^\dagger)/2\) (`L02366–L02507`). **En R3, esto implica hasta tres combinaciones lineales de observables de seis qubits**, no necesariamente tres bases de medida, tres circuitos o un costo de medición integral de tres unidades.

**Fuentes:** canonicalización `L01636–L01729`, carga de operadores `L02366–L02508` y proyector de subespacio `L02510–L02538`.

### 5.8. Particiones, uso de etiquetas y límites de la selección de rango

El bucle recorre cinco particiones declaradas en `SPLITS_H2B1A`. Los arreglos `F_train`, `G_train` y `teacher_train` se obtienen mediante `train_idx`; la función ALS se invoca solamente con esos arreglos (`L01755–L01833`, `L02010–L02021`). Para el ajuste de \(a,Q\), el `target` es el **score exacto C5**, no las etiquetas FM/AFM de forma directa.

Sin embargo, hay **tres niveles diferentes de uso de supervisión**:

1. El teacher C5 depende de operadores y decisiones previas potencialmente supervisadas, cuya procedencia completa todavía no está certificada.
2. Tras ajustar cada candidato, el código utiliza `y_train` para elegir la orientación del score por AUC de TRAIN (`L02139–L02149`). Por ello, **la orientación sí es una decisión supervisada**, aunque el MSE de ALS no incluya directamente etiquetas.
3. Los valores `y_hold` se emplean para calcular AUC descriptivas. Más adelante, el código utiliza `mean_hold_AUC` para identificar los rangos mínimos que superan umbrales y producir la decisión de compresión (`L02980–L03049`, `L03501–L03545`). Por tanto, **la elección global del rango a partir de esas fronteras es exploratoria y condicionada por el hold**.

Estos tres hechos son compatibles: *el ajuste local de los factores ALS se realiza sobre TRAIN*, pero ello **no convierte una selección posterior de rango basada en HOLD en confirmatoria**. El reporte generado por la celda dice `hold_usage: evaluation only` y `labels_used_for_fit: False` (`L04225–L04241`), afirmaciones acotadas al ajuste de parámetros; no deben ampliarse a una afirmación de independencia integral del *pipeline*.

### 5.9. Teacher R3 histórico frente a las particiones posteriores H2B2A0

R3 denomina aquí a la **variante de rango solicitado \(r=3\)** de la familia H2B1E3. Cada fold conserva sus coeficientes, espectro y observables; la celda serializa esas configuraciones en un NPZ con claves por fold y por rango (`L03938–L04034`). No debe confundirse este archivo multiparámetro con un único modelo universal reentrenado en todos los datos.

La etapa piloto H2B2A0 reutilizó un teacher R3 previamente ajustado y definió estas particiones para los 7.483 registros históricos de desarrollo:

| Partición | Materiales | Interpretación |
|---|---:|---|
| Outer train | 5.986 | Conjunto sobre el cual se ajustó el teacher precursor del piloto |
| Outer hold | 1.497 | Evaluación externa histórica ya examinada |
| Inner train | 4.788 | Desarrollo/ajuste de componentes posteriores |
| Inner val | 1.198 | Evaluación interna de estudiantes; **no** validación independiente del teacher ya ajustado con outer train |

La AUC de ese teacher R3 en inner val pertenece a una partición cuyos ejemplos ya contribuyeron a su ajuste; no puede presentarse como evaluación OOF del propio teacher. Además, la identificación del checkpoint exacto del piloto con el objeto correspondiente de H2B1E3 se debe vincular con hashes e índices antes de afirmar equivalencia completa.

### 5.10. Alcance del avance y reservas que permanecen

**Resuelto por inspección de fuente:** modelo matemático \(\widehat s=f^\top a+f^\top Qg\), objetivo MSE de destilación C5, restricción de rango, dos subproblemas ALS, ausencia de regularizador penalizado explícito, control numérico, inicializaciones, límite de tres combinaciones 6q para R3 y usos locales de TRAIN/HOLD.

**Resuelto en §§3–4 mediante lectura de celdas 9, 10, 11 y 77:** identidades y convenciones del mapa \(21\to 8\), expansión 16 bloques, simetrización 16→10 sobre B8 y factores locales C5. **Ahora resuelto:** procedencia H2-A4→H2-B0 por reconstrucción numérica sin HOLD de los cinco observables guardados (§4.2). **Sigue pendiente:** cotejar byte a byte o con tolerancia justificada el objeto efectivamente transferido en RAM a `O_FOLDS_H2B1A` y estados específicos posteriores; identidad integral de checkpoints; independencia confirmatoria de la selección de objetivos/C5/R3; ventaja de recursos físicos end-to-end.

## 6. Observables estudiante y rutas de medición

Para los modelos Student 1E/1F, la integración archivada reconstruyó observables de seis qubits mediante

$$
O_j = U_j^{\dagger}D_j U_j,
$$

con `U_j` unitario y `D_j` diagonal de `2^6 = 64` entradas. La certificación numérica verificó propiedades matriciales, convenciones relevantes, consistencia con Qiskit y reprodujo las AUC agregadas históricas en **inner val (n = 1198)**.

- Student 1E: AUC histórica reconstruida `0.913537480155041`.
- Student 1F: AUC histórica reconstruida `0.9159889583363131`.

Son resultados sobre **inner val previamente examinado** y no certifican por sí mismos generalización independiente. Se cotejó un QPY original del Student 1E, pero no un QPY histórico propio de 1F en esa auditoría. La igualdad de AUC agregadas no prueba por sí sola igualdad fila a fila de los scores frente a un archivo histórico no cotejado.

Por otra parte, INTEGRACIÓN-00 reproduce scores congelados de referencias Teacher y rutas de medición SAFE/Pauli-QWC, incluyendo evaluaciones archivadas sobre **outer hold (n = 1497)**. Esas AUC no son directamente comparables con las de Student inner val como si pertenecieran a un mismo test pareado.

### 6.1. Línea piloto A0: circuitos de seis qubits y lectura latente

La ruta experimental A0–A4 analizada retrospectivamente **no debe identificarse automáticamente** con las variantes Student 1E/1F documentadas arriba. Se basa en el teacher R3 congelado y emplea expectativas de observables unitariamente conjugados:

$$
z_h(x;\theta_h)=\operatorname{Tr}\!\left[\rho_6(x)U_h(\theta_h)^\dagger Z_{r_h}U_h(\theta_h)\right].
$$

A0 utiliza tres cabezales con raíces $r_h\in\{q_0,q_2,q_4\}$. Cada circuito contiene seis RY y cinco bloques de tres rotaciones de Pauli (RXX, RYY, RZZ), para **21 parámetros nominales por cabezal**. Las expectativas se transforman mediante un decodificador afín hacia las tres respuestas latentes del teacher. La pérdida archivada suma una MSE de score normalizada, una MSE latente ponderada normalizada y una penalización $10^{-6}\Vert A\Vert_F^2$ sobre la lectura, con peso latente $\alpha=0.25$ en el checkpoint final de A0:

$$
\mathcal L=\mathcal L_{\mathrm{score}}+\alpha\mathcal L_{\mathrm{latent}}+10^{-6}\Vert A\Vert_F^2,
\quad D_{\mathrm{score}}=0.002296306926438,\quad D_{\mathrm{latent}}=0.002672843134841.
$$

Los denominadores proceden de `INNER TRAIN` y se mantienen constantes en VAL. El informe [05, §4](05_RESULTADOS_Y_AUDITORIAS_H2B2.md) detalla la pérdida y sus comprobaciones; la MSE latente conserva los pesos históricos, que no se deben reemplazar por una MSE genérica sin cotejar la fuente.

### 6.2. Ampliaciones de lectura y de cabezales: A1, A2 y A3

En **A1**, los parámetros cuánticos y sus características $Z$ permanecieron congelados. Se comparó la lectura lineal con un mapa cuadrático de nueve características:

$$
\phi(z_1,z_2,z_3)=(z_1,z_2,z_3,z_1^2,z_2^2,z_3^2,z_1z_2,z_1z_3,z_2z_3).
$$

El mejor ajuste cuadrático archivado obtuvo AUC `INNER VAL` **0.842985254**, frente a **0.838085158** de A0. Esa ganancia mide capacidad de lectura clásica sobre características congeladas, no mejora del circuito.

**A2-0** incorporó un cuarto cabezal con raíz $q_1$, inicialmente manteniendo congelados los tres anteriores. El cuarto circuito tiene 21 parámetros nominales y 20 coordenadas observables efectivas, porque la RZZ terminal conmuta con la lectura $Z_{q_1}$ y no altera su expectativa. **A2-1** refinó conjuntamente los cuatro cabezales: 84 parámetros nominales y 80 efectivos bajo la misma convención. La mejor AUC histórica `INNER VAL` fue **0.846775462**. Los informes verificaron la continuidad de checkpoints, los objetivos y expectativas sobre muestras independientes de simulación; no reprodujeron todos los barridos históricos.

**A3-0** intercaló tres RZ nuevos en cada cabezal de A2-1 (12 ángulos en total); el checkpoint seleccionado conservó los ángulos en cero y el modelo A2-1. **A3-1** añadió tres bloques Cartan entre ramas por cabezal (RXX/RYY/RZZ por bloque; 36 nuevos ángulos). Su mejor AUC `INNER VAL` fue **0.847376175**, una diferencia de `+0.000600712` frente a A2-1. Las dos ramas parten de la misma referencia A2 y no son etapas obligatorias de una única arquitectura final.

### 6.3. Dos alternativas de quinta característica en A4

**A4-0** ensayó un quinto cabezal jerárquico de seis qubits con 24 parámetros nominales y 23 observables efectivos; conservó congelados los cuatro cabezales de A2-1. El checkpoint elegido por AUC histórica fue **el barrido 0**, con las puertas inicializadas y **solo un reajuste del decodificador**. Su AUC fue **0.847482014**. No debe atribuirse esa pequeña ganancia al entrenamiento de las nuevas puertas.

**A4-1A** es una alternativa distinta: conserva cuatro expectativas de A2-1 y añade un observable hermítico y sin traza general de seis qubits, expresado en la base de Pauli:

$$
B_5=\sum_{P\in\mathcal P_6\setminus\{I\}}\beta_P P,\qquad z_5(x)=\operatorname{Tr}[\rho_6(x)B_5],\qquad 4^6-1=4095.
$$

Su «rango uno» es el rango de la **nueva contribución al espacio de lectura de características**, no el rango matricial de $B_5$. La auditoría reprodujo $z_5$ mediante la caché Pauli para todos los **4.788 TRAIN y 1.198 VAL**, y directamente desde `PSI7` en submuestras. La AUC `INNER VAL` **0.939362387** es **histórica y exploratoria**; los índices FIT/TUNE no quedaron disponibles para una certificación independiente de esa selección.

### 6.4. Distinción entre observable hermítico general y medición dicotómica

Un circuito de la forma $U^\dagger Z_rU$ tiene espectro $\{-1,+1\}$. Por el contrario, $B_5$ es un hermítico general de $64\times64$ con espectro no dicotómico: bajo la normalización archivada $\|\beta\|_2=1$, sus extremos calculados fueron **−2.31722036** y **+2.16332237**. Por ello, **no representa directamente** una lectura binaria $U^\dagger ZU$ ejecutable con un único circuito. Para implementarlo se tendría que especificar y presupuestar una estrategia física de medición y estimación del observable.

La renormalización de $\beta$ junto con la compensación inversa en el decodificador deja invariantes las puntuaciones, **pero no necesariamente el término de regularización ridge**. La evidencia de capacidad expresiva no equivale a una demostración de menor coste de circuitos, shots o ejecución QPU.

### 6.5. Alcance de la nueva verificación de A0–A4-1A

Los auditores contrastaron archivos con huellas SHA256, checkpoints, objetivos y ciertas expectativas reconstruidas desde `PSI7`. La certificación Fourier fue local sobre coordenadas y submuestras, no una repetición completa del proceso de optimización. Las **AUC solo se leyeron de los registros históricos de `INNER VAL`**, sin volver a utilizar etiquetas ni `OUTER HOLD`; no son un test confirmatorio. Véase [05: resultados y auditorías](05_RESULTADOS_Y_AUDITORIAS_H2B2.md), [03: evidencia](03_MATRIZ_DE_EVIDENCIA.md) (E22–E27) y [04: limitaciones](04_VALIDACION_Y_LIMITACIONES.md).

## 7. Recursos y límites físicos

La síntesis 3D documenta presupuestos de recursos **parciales**: 504 puertas lógicas en dos decodificadores `U` Student, 96 de ellas RXX; 24/64 bases QWC con 10 000 shots incrementales de `ρ₆`; y una referencia lógica de 110 000 shots planificados. Estos números no incluyen necesariamente preparación completa de estados, medición integral, transpilación ISA, ejecución física ni lectura, por lo que **no permiten concluir una ventaja de recursos end-to-end o una ventaja cuántica**.

## 8. Registro de afirmaciones y estado

| Afirmación | Estado documental | Acción antes de tesis final |
|---|---|---|
| Origen H2-A4 → H2-B0: cinco observables B8 reconstruidos sin etiquetas HOLD | **CERTIFICADO NUMÉRICAMENTE: máximo error elemento $3.506\times10^{-7}$; signo original en 5/5 folds** | Conservar hashes, reporte y distinción respecto de independencia estadística |
| Cadena inmediata H2B1A → H2B1E0 → H2B1E1 | Respaldada por salidas históricas | Falta cotejo matricial directo de las transferencias en RAM |
| Reducción 21→8 por trazas parciales | **Identidad algebraica y convenciones cotejadas con código** | Certificar el origen histórico de `RHO6/RHO4_H2B1A` y su alineación fila a fila |
| Descomposición 16→10 en la variedad B8 | **Identidad matemática exacta de scores; controles numéricos identificados en código** | Conservar distinción respecto de identidad global del operador y cotejar *outputs* históricos |
| Relación C10→C5→R3 | **Factores y normalización cotejados en celdas 11 y 13** | C5 es subconjunto exploratorio y R3 es aproximación bilineal; no presentar ninguna como identidad de O* |
| Función objetivo y pasos ALS R3 | **Derivación reconstruida del código de la celda 13** | Mantener hashes y líneas fuente; verificar artefactos congelados sin alterar las ejecuciones |
| ALS R3: fit con TRAIN, orientación con etiquetas TRAIN y frontera de rango con HOLD | **Respaldado localmente por el código; decisión de rango exploratoria** | No atribuir independencia confirmatoria a C5 o al rango elegido |
| Independencia del teacher R3 sobre inner val | **No establecida** | No citar la AUC inner val como prueba independiente del teacher |
| Reproducción de Student 1E/1F en inner val | 94/94 pruebas de la integración aprobadas | Mantener reserva sobre procedencia histórica y evaluación nueva |
| Costo QPU físico total o ventaja cuántica | **No certificado** | Exigir presupuesto homologado y/o ejecución confirmatoria |
| Generalización a composiciones nunca vistas | **No certificada** | Nuevo protocolo agrupado predefinido, con ajuste completo por fold |

## 9. Pendientes para la versión matemática definitiva

1. **Resuelto parcialmente con certificación fuerte:** construcción H2-A4→H2-B0, índices TRAIN de cinco folds, coeficientes `B_LABEL_KRR`, reconstrucción numérica de los cinco $O_f^\star$ sin HOLD. Resta autenticación directa del objeto en memoria de H2B1A y del resto del pipeline; la selección histórica del método ganador sobre outer HOLD sigue siendo exploratoria.
2. **Resuelto algebraicamente en §§3–4:** trazas parciales desde tres copias 7q, tensor B8, 16 bloques Pauli y 10 canales 6q exactos sobre la variedad B8. Falta auditar la **creación original** de los arreglos reducidos y contrastar las salidas numéricas históricas.
3. **Resuelto por lectura de código de la celda 13:** ecuaciones de ALS R3, ausencia de regularización penalizada explícita y parámetros numéricos documentados en §5. Resta cotejar productos de ejecución y checkpoints históricos si se requiere certificación adicional.
4. Separar arquitectónicamente las versiones Student 1E, 1F, SAFE y QWC, y documentar qué componentes son comunes y cuáles son alternativas.
5. Establecer cuál es la arquitectura congelada final de H2B2A7, sin equipararla automáticamente a todos los candidatos explorados.

## 10. Fuentes y procedencia

- [Mapa científico](00_MAPA_CIENTIFICO.md)
- [INTEGRACIÓN-00: Pauli/QWC](../H2B2A7_INTEGRACION_00.md)
- [INTEGRACIÓN-01: Student 1E/1F](../H2B2A7_INTEGRACION_01.md)
- [Fase 3B: comparación descriptiva](../H2B2A7_FASE_3B_GUIA.md)
- [Fase 3C: observables y expectativas](../H2B2A7_FASE_3C_GUIA.md)
- [Fase 3C.3: ranking](../H2B2A7_FASE_3C3_GUIA.md)
- [Fase 3C.4: recursos](../H2B2A7_FASE_3C4_GUIA.md)
- [Síntesis científica 3D](../../reports/H2B2A7_CONSOLIDACION/H2B2A7_3D_SINTESIS_20261113T184850523066Z/3D_INFORME.md)

**Fuentes primarias de la reducción física y la descomposición (aún fuera de Git):**

- `FUENTE_REDUCCION_21A8_ETAPA1.txt`, celdas 9 (**SHA-256 código `8ff545f9dbf5db55b66679935fd2eddc8cb468ecc8529e363793b03053a19a3b`**) y 77 (**`b2bf31aa8051d45304d9ec06f2deee67feff57200562afdbd1d3f1ebc53fce4e`**).
- `FUENTE_REDUCCION_8A6_CANALES_ETAPA2.txt`, celdas 10 (**`688efbd8570d64b93a05510c37e47e65e30e8cf2a3d3754f86ca905b43c2c8ff`**) y 11 (**`bdedd84be142d6c4cbe1aacce898187630763af6c84fda5360974eebe67397fc`**).
- Todas esas extracciones identifican el notebook `ContinuacionnuevaModelosdataset2.ipynb` con SHA-256 consignado `706319a4375e37098bcd35ec08428fa30e551679f370015f53a5f6977f99c20c`. Los hashes proceden de los encabezados del extractor y no constituyen por sí mismos una segunda verificación independiente del notebook original.

**Fuente primaria de ALS R3 (también fuera de Git):** `FUENTE_PRIMARIA_H2B1E3_R3_H2B2A7.txt`, celda histórica 13, SHA-256 de código `79dc041745f32efc063d3d527603934d991570c712ad5c6768afb0a0b269fad1`.

Los extractos completos no deben copiarse al repositorio sin revisar privacidad, rutas locales, tamaño y pertinencia. No se ejecutaron las celdas históricas durante esta revisión.

**Otras fuentes históricas fuera de Git:** informes de cierre `CIERRE_ORIGEN_OSTAR_Y_SELECCION_CANALES_H2B2A7.txt` y `CIERRE_FINAL_FUENTE_OSTAR_Y_DECISION_C5_H2B2A7.txt`, junto con auditorías XIV–XXIV, conservados en el worktree de consolidación como archivos sin seguimiento. Versionar solo después de seleccionar y revisar la evidencia necesaria.

**Nuevas evidencias locales, v0.5:** `AUDITORIA_ESTRUCTURAL_OSTAR_H2B2A7.txt` y `AUDITORIA_NUMERICA_H2A4_A_H2B0_SIN_HOLD.txt`; referencias de integridad en §4.2. No requieren copiar matrices grandes ni datos sensibles al Git.
