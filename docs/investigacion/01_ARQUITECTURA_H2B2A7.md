# Arquitectura física y matemática H2B2A7

> - **Estado:** borrador científico v0.2, revisado editorialmente; descripción de las piezas sustentadas por evidencia integrada, no especificación final certificada de extremo a extremo.
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
| Teacher R3 | Modelo de aproximación de rango 3 sobre factores `F`, `G` | Referencia congelada usada en la etapa posterior H2B2 | Su ajuste no debe confundirse con una validación interna independiente |
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

## 5. Teacher R3 y particiones de H2B2A0

La implementación histórica de H2B1E3 consume factores `F` y respuestas `G` derivados de los cinco canales, y ajusta una aproximación de rango reducido mediante **ALS**. La inspección del código indica uso de ejemplos del entrenamiento externo para ese ajuste; no hay evidencia de suministro directo de etiquetas del outer hold al optimizador ALS examinado. Esta conclusión es local al código inspeccionado y **no certifica las dependencias upstream** de `O*` y C5.

La etapa piloto H2B2A0 reutilizó un teacher R3 previamente ajustado y definió las siguientes particiones para los 7 483 registros de desarrollo:

| Partición | Materiales | Interpretación |
|---|---:|---|
| Outer train | 5 986 | Base de la que deriva el entrenamiento del teacher previo |
| Outer hold | 1 497 | Evaluación externa histórica ya examinada |
| Inner train | 4 788 | Entrenamiento interno de desarrollos posteriores |
| Inner val | 1 198 | Validación de estudiantes y decisiones posteriores; **no** nueva validación independiente del teacher ya entrenado con outer train |

La separación de índices entre inner train, inner val y outer hold es necesaria, pero no suficiente para afirmar independencia de todos los **ajustes upstream**. En particular, la AUC del teacher R3 sobre inner val corresponde a observaciones que ya habían contribuido a entrenarlo antes de formar ese split.

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
| ALS R3 sin etiquetas directas de outer hold en el ajuste inspeccionado | Evidencia parcial local | Verificar construcción upstream de `O*_f` |
| Independencia del teacher R3 sobre inner val | **No establecida** | No citar la AUC inner val como prueba independiente del teacher |
| Reproducción de Student 1E/1F en inner val | 94/94 pruebas de la integración aprobadas | Mantener reserva sobre procedencia histórica y evaluación nueva |
| Costo QPU físico total o ventaja cuántica | **No certificado** | Exigir presupuesto homologado y/o ejecución confirmatoria |
| Generalización a composiciones nunca vistas | **No certificada** | Nuevo protocolo agrupado predefinido, con ajuste completo por fold |

## 9. Pendientes para la versión matemática definitiva

1. Localizar la construcción de `O_FOLDS_H2B1A` y establecer qué etiquetas e índices fueron utilizados para ajustar cada observable.
2. Precisar la fórmula completa del mapa de estados de siete qubits al espacio efectivo B8 y los operadores de seis qubits, con convenciones de indexación.
3. Identificar las ecuaciones del ajuste ALS R3 y su regularización exacta a partir del notebook histórico.
4. Separar arquitectónicamente las versiones Student 1E, 1F, SAFE y QWC, y documentar qué componentes son comunes y cuáles son alternativas.
5. Establecer cuál es la arquitectura congelada final de H2B2A7, sin equipararla automáticamente a todos los candidatos explorados.

## 10. Fuentes versionadas

- [Mapa científico](00_MAPA_CIENTIFICO.md)
- [INTEGRACIÓN-00: Pauli/QWC](../H2B2A7_INTEGRACION_00.md)
- [INTEGRACIÓN-01: Student 1E/1F](../H2B2A7_INTEGRACION_01.md)
- [Fase 3B: comparación descriptiva](../H2B2A7_FASE_3B_GUIA.md)
- [Fase 3C: observables y expectativas](../H2B2A7_FASE_3C_GUIA.md)
- [Fase 3C.3: ranking](../H2B2A7_FASE_3C3_GUIA.md)
- [Fase 3C.4: recursos](../H2B2A7_FASE_3C4_GUIA.md)
- [Síntesis científica 3D](../../reports/H2B2A7_CONSOLIDACION/H2B2A7_3D_SINTESIS_20261113T184850523066Z/3D_INFORME.md)

**Fuentes históricas fuera de Git:** informes de cierre `CIERRE_ORIGEN_OSTAR_Y_SELECCION_CANALES_H2B2A7.txt` y `CIERRE_FINAL_FUENTE_OSTAR_Y_DECISION_C5_H2B2A7.txt`, junto con auditorías XIV–XXIV, conservados en el worktree de consolidación como archivos sin seguimiento. Versionar solo después de seleccionar y revisar la evidencia necesaria.
