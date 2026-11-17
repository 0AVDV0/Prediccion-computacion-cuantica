# Arquitectura física y matemática H2B2A7

> - **Estado:** borrador científico v0.3, ampliado con derivación de ALS R3 cotejada con código histórico; descripción de las piezas sustentadas por evidencia integrada, no especificación final certificada de extremo a extremo.
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
| Estado multicopia previo | \(\lvert\psi_7(x)\rangle^{\otimes 3}\) (21 qubits) | Punto de partida conceptual de la reducción del sistema | La derivación exacta que conduce al espacio efectivo debe cotejarse con las fuentes históricas |
| Observable \(O_f^\star\) de H2B1A | Matriz compleja 256 × 256 para cada uno de cinco folds | Referencia de discriminación en un espacio de ocho qubits | Falta certificar qué entradas y etiquetas se usaron para ajustarlo originalmente |
| Diez canales efectivos H2B1E1 | 10 términos de una descomposición física de `O*_f` | Descomponer el score preservando la reconstrucción numérica histórica | Reconstrucción algebraica no implica selección confirmatoria |
| Configuración C5 de H2B1E3 | `II`, `IY`, `IZ`, `XY`, `ZZ` | Cinco canales fijos para la representación reducida | Su elección global pertenece al desarrollo exploratorio de arquitectura |
| Teacher R3 | \(\widehat s_r=f^\top a+f^\top Q_rg\), con \(Q_r\in\mathbb R^{5\times5}\) y \(\operatorname{rank}(Q_r)\le r\) | Destilación bilineal del score C5; R3 utiliza \(r=3\) | MSE sin penalización explícita, pero la elección global del rango no es una validación confirmatoria |
| Operadores Student 1E/1F | `O_j = U_j† D_j U_j`, con `D_j` diagonal de 64 entradas | Observables efectivos implementados en seis qubits | No se ha certificado el costo físico end-to-end ni el QPY original de 1F |

**Nota de alcance:** las dimensiones anteriores describen piezas documentadas; la identidad completa entre el modelo matemático de veintiún qubits, la representación reducida y las implementaciones posteriores debe desarrollarse en una derivación independiente, con referencias de código.

## 3. Antecedente multicopia y reducción física

Para un material `x`, la construcción multicopia previa puede escribirse como

$$
|\Psi_{21}(x)\rangle = |\psi_7(x)\rangle_A \otimes |\psi_7(x)\rangle_B \otimes |\psi_7(x)\rangle_C.
$$

El espacio de Hilbert completo tiene dimensión `2^21`. La línea H2B1 trabaja posteriormente con un observable **B8** (`256 = 2^8`) y con operadores efectivos de **seis qubits** para ciertos canales. El objetivo documental es demostrar, a partir del código histórico, las hipótesis y transformaciones que hacen legítima esa reducción. **No debe inferirse equivalencia de toda observable de 21 qubits con cualquier observable de 8 qubits**: se trata de la representación efectiva usada en esta investigación bajo restricciones particulares.

**Pendiente de certificación:** ecuación completa de la reducción, convenciones de orden de qubits, trazas parciales y relación exacta entre `ρ₆`, los factores restantes y el observable B8.

## 4. Cadena comprobada de procedencia del observable

Las salidas históricas conservadas permiten establecer la siguiente secuencia concreta:

```text
H2B1A  O_FOLDS_H2B1A
   ↓
H2B1E0 OSTAR_FOLDS_H2B1E0
   ↓
H2B1E1 OSTAR_FOLDS_H2B1E1
   ↓
Descomposición física en diez canales
   ↓
H2B1E3 cinco canales fijos: II, IY, IZ, XY, ZZ
   ↓
Factorización / aproximación R3
   ↓
H2B2A0 y línea posterior H2B2A7
```

La ejecución histórica conservada en el notebook indica que H2B1E0 leyó `O_FOLDS_H2B1A` desde memoria; H2B1E1 leyó `OSTAR_FOLDS_H2B1E0` desde memoria. Esto **resuelve la fuente inmediata**, pero todavía no prueba que el `O*_f` original se haya construido sin etiquetas del hold correspondiente.

### 4.1. Score por canales

De manera esquemática, la descomposición permite representar un score como una suma de contribuciones:

$$
s_f(x) = \sum_{c\in\mathcal C_{10}} s_{f,c}(x),
\qquad s_{f,c}(x)=F_{f,c}(x)G_{f,c}(x),
$$

Aquí \(F_{f,c}\) y \(G_{f,c}\) representan, esquemáticamente, los dos factores de cada contribución; sus normalizaciones y la correspondencia exacta con los arreglos del notebook deben conservarse al ampliar la derivación. La expresión no debe confundirse con la factorización posterior de rango tres mediante ALS. En H2B1E1 se verificó numéricamente la equivalencia entre el score del observable heredado y la reconstrucción con diez canales. La configuración reducida C5 retiene únicamente el subconjunto fijo

$$
\mathcal C_5=\{II,IY,IZ,XY,ZZ\}.
$$

**Advertencia:** conservar un subconjunto de canales no es una identidad universal de reconstrucción exacta del operador original; su suficiencia discriminativa se investigó empíricamente.

### 4.2. Selección exploratoria de C5

H2B1E1 examinó los `2^10−1=1023` subconjuntos no vacíos y produjo comparaciones por tamaño. Si bien la orientación y la selección de subconjuntos dentro del fold se describen mediante cantidades de entrenamiento, en el desarrollo posterior se consultaron fronteras de AUC sobre *hold* para estudiar tamaños y rangos. Así, la elección global de C5 **no debe calificarse retrospectivamente como independiente del hold** sin evidencia documental adicional.

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

La notación de valores esperados es la declarada por el código; la construcción detallada de \(\rho_4\), \(\rho_6\), el orden de qubits y la correspondencia integral con el espacio B8 **siguen pendientes** de una derivación independiente.

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

**No resuelto por esta extracción:** origen y ajuste creador de `O_FOLDS_H2B1A`; derivación completa de \(\rho_4,\rho_6\) desde las tres copias de siete qubits; reproducibilidad de los valores finales sin ejecutar ni cotejar *outputs*; identificación integral de checkpoints; independencia confirmatoria de la elección C5/R3; ventaja de recursos físicos end-to-end.

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

## 7. Recursos y límites físicos

La síntesis 3D documenta presupuestos de recursos **parciales**: 504 puertas lógicas en dos decodificadores `U` Student, 96 de ellas RXX; 24/64 bases QWC con 10 000 shots incrementales de `ρ₆`; y una referencia lógica de 110 000 shots planificados. Estos números no incluyen necesariamente preparación completa de estados, medición integral, transpilación ISA, ejecución física ni lectura, por lo que **no permiten concluir una ventaja de recursos end-to-end o una ventaja cuántica**.

## 8. Registro de afirmaciones y estado

| Afirmación | Estado documental | Acción antes de tesis final |
|---|---|---|
| Cadena inmediata H2B1A → H2B1E0 → H2B1E1 | Respaldada por salidas históricas | Incorporar referencia o anexo selectivo sin datos sensibles |
| Reconstrucción del score B8 por diez canales | Verificación numérica histórica identificada | Citar fórmula y tolerancia exactas desde la fuente |
| Identidad y uso de los cinco canales C5 | Respaldado por el código histórico | Explicar que su selección global fue exploratoria |
| Función objetivo y pasos ALS R3 | **Derivación reconstruida del código de la celda 13** | Mantener hashes y líneas fuente; verificar artefactos congelados sin alterar las ejecuciones |
| ALS R3: fit con TRAIN, orientación con etiquetas TRAIN y frontera de rango con HOLD | **Respaldado localmente por el código; decisión de rango exploratoria** | No atribuir independencia confirmatoria a C5 o al rango elegido |
| Independencia del teacher R3 sobre inner val | **No establecida** | No citar la AUC inner val como prueba independiente del teacher |
| Reproducción de Student 1E/1F en inner val | 94/94 pruebas de la integración aprobadas | Mantener reserva sobre procedencia histórica y evaluación nueva |
| Costo QPU físico total o ventaja cuántica | **No certificado** | Exigir presupuesto homologado y/o ejecución confirmatoria |
| Generalización a composiciones nunca vistas | **No certificada** | Nuevo protocolo agrupado predefinido, con ajuste completo por fold |

## 9. Pendientes para la versión matemática definitiva

1. Localizar la construcción de `O_FOLDS_H2B1A` y establecer qué etiquetas e índices fueron utilizados para ajustar cada observable.
2. Precisar la fórmula completa del mapa de estados de siete qubits al espacio efectivo B8 y los operadores de seis qubits, con convenciones de indexación.
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

**Fuente primaria de esta actualización (aún fuera de Git):** `FUENTE_PRIMARIA_H2B1E3_R3_H2B2A7.txt`, extracción de solo lectura del código de la celda histórica 13, con SHA-256 del texto `79dc041745f32efc063d3d527603934d991570c712ad5c6768afb0a0b269fad1`. El extracto no debe copiarse íntegro al repositorio sin revisar privacidad y pertinencia.

**Otras fuentes históricas fuera de Git:** informes de cierre `CIERRE_ORIGEN_OSTAR_Y_SELECCION_CANALES_H2B2A7.txt` y `CIERRE_FINAL_FUENTE_OSTAR_Y_DECISION_C5_H2B2A7.txt`, junto con auditorías XIV–XXIV, conservados en el worktree de consolidación como archivos sin seguimiento. Versionar solo después de seleccionar y revisar la evidencia necesaria.
