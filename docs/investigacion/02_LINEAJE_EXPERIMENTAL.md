# Linaje experimental del proyecto H2B2A7

> **Estado:** borrador documental v0.2 (revisado tras certificación numérica de O★) para revisión; no constituye una certificación experimental nueva.
> **Rama:** `feature/h2b2a7-documentacion-cientifica`.
> **Base de integración:** `develop` en `ed94433` (PR #4, 14-11-2026).
> **Regla:** distinguir antecedentes, dependencias computacionales, variantes exploratorias, reproducciones numéricas y evaluaciones independientes. El orden de presentación no prueba una dependencia causal ni equivale al orden temporal completo de cada experimento.

## 1. Pregunta que responde este documento

¿Cómo se pasó de las primeras representaciones cuánticas y operadores de discriminación FM/AFM a la línea H2B2A7, y qué evidencia justifica —o limita— las decisiones tomadas en ese recorrido?

Este documento **no** atribuye automáticamente a H2B2A7 las métricas de otros experimentos. Tampoco reemplaza el documento [01_ARQUITECTURA_H2B2A7.md](01_ARQUITECTURA_H2B2A7.md), que describe los objetos matemáticos, ni el [mapa científico](00_MAPA_CIENTIFICO.md), que ordena el conjunto de líneas.

## 2. Convenciones para clasificar la evidencia

| Categoría | Significado en este documento |
|---|---|
| **Dependencia comprobada** | Se identifica una lectura, una asignación, un archivo o una reproducción numérica concreta. |
| **Antecedente** | Resultado que motiva una hipótesis posterior, sin probar que sus parámetros fueran reutilizados. |
| **Resultado exploratorio** | Métrica obtenida durante la búsqueda o revisión de arquitecturas, con posibles decisiones posteriores a su observación. |
| **Verificación numérica** | Igualdad de scores, matrices, hashes o propiedades específicas; no es por sí misma un nuevo test independiente. |
| **Pendiente** | La evidencia disponible no permite afirmar el origen, la equivalencia o la validez estadística completa. |

## 3. Representaciones y primeros operadores: antecedentes de H1/H2A

### 3.1. Datos, descriptores y representaciones supervisadas

El historial distingue un conjunto de referencia de **10.691 registros** con particiones CORE históricas de **7.483 entrenamiento, 1.069 validación y 2.139 prueba**. Se utilizan descriptores composicionales —incluidas 84 fracciones `p_X`— en una parte del desarrollo. El dataset y sus particiones pertenecen a un contexto histórico concreto; no debe asumirse que todas las variantes de datos posteriores tienen exactamente esas mismas filas.

La fase histórica 3K construyó una base de coordenadas Helstrom de 512 componentes mediante un ajuste supervisado sobre el conjunto CORE de entrenamiento completo. En consecuencia, los resultados obtenidos sobre esos mismos 7.483 materiales **no son out-of-fold (OOF) del pipeline completo**, aunque etapas posteriores ajusten partes del predictor dentro de folds.

Se registraron, entre otros, los AUC históricos `teacher_D` **0,965419** y `diag513_calibrated` **0,971824**. Son métricas de ese protocolo y no pruebas OOF independientes de toda la representación.

### 3.2. H1: referencia Helstrom ajustada por fold

La implementación H1 contiene ajuste por fold de un operador Helstrom empleando explícitamente los datos y etiquetas del subconjunto de entrenamiento del fold, seguido de predicciones sobre su subconjunto retenido. La auditoría retrospectiva encontró concordancia exacta entre cinco cachés de predicciones y el vector OOF archivado, con AUC combinado **0,907405656**.

**Alcance:** evidencia fuerte de la ejecución y el resultado OOF de H1. **Reserva:** los índices históricos y la procedencia completa de la preparación de entrada no quedaron autenticados exhaustivamente por los cachés. No extender automáticamente esta conclusión a la base 3K.

### 3.3. H2A3/H2A4: transferencia y reducción física

H2A3/H2A4 reutilizaron el vector teacher de H1. En H2A4, el kernel B8 de Hilbert–Schmidt se contrastó con su evaluación directa con una diferencia histórica de aproximadamente `8,5 × 10⁻⁸`. La ruta `B_LABEL_KRR` presenta AUC OOF histórica **0,9234362199284905** y AUC media por fold **0,9236863323397297**, sujetas a las reglas históricas de selección del método sobre los cinco holds. Los cinco observables conservados H2-B0 ya se reconstruyeron directamente desde sus coeficientes originales sin consultar HOLD, con errores máximos de matriz entre $1.620\times10^{-7}$ y $3.506\times10^{-7}$.

**Interpretación:** la equivalencia numérica del kernel es una propiedad de implementación; el AUC no prueba que todas las decisiones de investigación anteriores fueran independientes de las evaluaciones observadas ni que se generalice a composiciones no vistas.

## 4. H2B1: estructura física del observable y compresión

### 4.1. Fuente del observable de ocho qubits

La ejecución histórica conservada permite reconstruir la transferencia inmediata:

```text
O_FOLDS_H2B1A
       |
       v
OSTAR_FOLDS_H2B1E0
       |
       v
OSTAR_FOLDS_H2B1E1
       |
       v
Descomposición en diez canales efectivos
```

En H2B1E0, la salida histórica indica `O* source = O_FOLDS_H2B1A in RAM`. H2B1E1 informa `O* source = OSTAR_FOLDS_H2B1E0 in RAM`. La forma es `(5, 256, 256)`, correspondiente a cinco observables sobre el espacio B8.

**Actualización documental (17-11-2026):** la fuente original está localizada en las celdas 312–314 de `ModelosDataset2.ipynb`. H2-A4 ajusta `B_LABEL_KRR` dentro del outer TRAIN, eligiendo $\lambda$ en validación interna; los cinco vectores de coeficientes guardados y sus índices TRAIN cubren los 7.483 ejemplos con HOLD complementarios disjuntos. La reconstrucción H2-A4→H2-B0 reproduce los cinco observables `O_folds` con error máximo de elemento $3.506\times10^{-7}$ y orientación original sin usar etiquetas ni AUC HOLD. **Pendiente específico:** autenticación directa de la transferencia H2-B0→H2B1A en RAM/checkpoint, así como independencia estadística de la selección de la familia de objetivos, C5/R3 y del pipeline anterior a los estados codificados.

### 4.2. Diez canales efectivos: identidad de reconstrucción

H2B1E1 descompone el score del operador heredado en diez contribuciones efectivas, con una estructura esquemática

$$
s_f(x)=\sum_{c\in\mathcal C_{10}}s_{f,c}(x),
\qquad s_{f,c}(x)=F_{f,c}(x)\,G_{f,c}(x).
$$

Las comprobaciones numéricas históricas reproducen el score del observable completo mediante esos diez canales. **Esto acredita una identidad/reconstrucción dentro de la representación y las convenciones implementadas, no una mejora predictiva confirmatoria.**

### 4.3. Del conjunto completo a C5

H2B1E1 exploró los **1.023 subconjuntos no vacíos** de los diez canales, con selección/orientación local de subconjuntos referida al entrenamiento. También construyó fronteras de complejidad que consultan explícitamente `mean_hold_AUC`. El notebook reconoce que usar esas fronteras para decidir el número de canales que estudiar después es desarrollo/selección de modelo.

H2B1E3 fijó globalmente la configuración

$$
\mathcal C_5=\{\mathrm{II},\mathrm{IY},\mathrm{IZ},\mathrm{XY},\mathrm{ZZ}\}.
$$

Las AUC medias históricas sobre cinco holds para el observable completo y C5 fueron **0,923686699** y **0,921981265**, respectivamente. La diferencia descriptiva es pequeña; **no** es una prueba de que C5 fuera seleccionado antes de observar los holds ni de que sea óptimo en datos nuevos.

### 4.4. Teacher de rango tres (R3)

La etapa H2B1E3 toma las respuestas y factores de los cinco canales y construye una aproximación *task-aligned* de rango reducido mediante ALS. El código inspeccionado utiliza `F_train`, `G_train` y `teacher_train` sobre los índices del entrenamiento externo. No se identificó el suministro directo de etiquetas del `outer_hold` al ajuste ALS analizado.

**Importante:** que ALS se ajuste con datos externos de entrenamiento no resuelve la dependencia *upstream* del observable `O*` ni convierte automáticamente la selección de canales/rango en confirmatoria. Tampoco hay que identificar la factorización por canales con el rango matricial de ALS: son dos operaciones conceptualmente diferentes.

## 5. H2B2: congelamiento del teacher y variantes estudiante

### 5.1. Piloto H2B2A0

La etapa piloto recuperó un teacher R3 previamente construido y definió las siguientes particiones:

| Partición | N | Uso histórico |
|---|---:|---|
| `outer_train` | 5.986 | Entrenamiento externo del R3 precursor |
| `outer_hold` | 1.497 | Hold externo histórico |
| `inner_train` | 4.788 | Desarrollo/ajuste de componentes posteriores |
| `inner_val` | 1.198 | Evaluación y desarrollo interno de estudiantes |

El teacher R3 **ya había sido ajustado usando `outer_train` antes de separar `inner_train` e `inner_val`**. Por ello, su AUC en `inner_val` —históricamente **0,978803438**— **no equivale a una evaluación OOF/independiente del propio teacher**. Esto no implica automáticamente la misma dependencia para cada estudiante: las comprobaciones se interpretan según qué piezas se ajustaron y cuándo.

### 5.2. Ruta Pauli/QWC — INTEGRACIÓN-00

La integración Pauli/QWC reconstruye puntuaciones congeladas de Teacher R3, HEAD4+SAFE, SAFE ideal y rutas QWC24/QWC64 según las particiones archivadas. Los valores de OUTER HOLD tienen carácter **retrospectivo**; no se reentrenó ni se ejecutó una QPU en esa certificación.

Archivos de referencia: [documentación INTEGRACIÓN-00](../H2B2A7_INTEGRACION_00.md), [notebook certificado](../../experiments/INTEGRACION_00.ipynb) y los productos bajo `reports/H2B2A7_INTEGRACION_00/`.

### 5.3. Ruta Student 1E/1F — INTEGRACIÓN-01

La integración Student reconstruyó observables de seis qubits

$$
O_j=U_j^\dagger D_jU_j,
$$

con `D_j` diagonal de 64 entradas, y reprodujo las AUC agregadas archivadas de `inner_val` (1.198 materiales): **Student 1E = 0,913537480155041**; **Student 1F = 0,9159889583363131**. Superó 94/94 pruebas numéricas. El QPY histórico de 1E fue cotejado; no se certificó un QPY original equivalente para 1F.

**Alcance:** reproducibilidad matemática y de métricas agregadas en una partición ya examinada, no evidencia de generalización confirmatoria ni de costo físico completo.

Archivos de referencia: [documentación INTEGRACIÓN-01](../H2B2A7_INTEGRACION_01.md) y [notebook certificado](../../experiments/INTEGRACION_01_CERT.ipynb).

### 5.4. No confundir variantes con una arquitectura final certificada

`Student 1E`, `Student 1F`, `SAFE` y `QWC` representan componentes o estrategias evaluadas bajo **protocolos diferentes**. Las rutas de medición no son necesariamente cuatro modelos entrenados de idéntica forma. Hasta reconciliar checkpoints, código de preparación, cabezales, composición del score y protocolo elegido, evitar afirmar que *todos* constituyen la arquitectura congelada final H2B2A7.

## 6. Integración científica 3A–3D ya realizada

Las fases 3A–3D no crearon un nuevo modelo supervisado. Organizaron y comprobaron evidencias históricas de las dos integraciones anteriores.

| Fase | Contribución |
|---|---|
| **3A** | Cobertura de archivos, splits y pares comparables. |
| **3B** | Comparaciones descriptivas pareadas dentro de cada split; OUTER HOLD ya examinado. |
| **3C** | Errores de matrices, expectativas y scores de observables Student. |
| **3C.3** | Correlaciones, márgenes y cambios de orden de pares de materiales. |
| **3C.4** | Inventario parcial de recursos lógicos y medición. |
| **3D** | Síntesis e integridad de 22 productos archivados. |

La [síntesis 3D](../../reports/H2B2A7_CONSOLIDACION/H2B2A7_3D_SINTESIS_20261113T184850523066Z/3D_INFORME.md) presenta en OUTER HOLD (1.497 materiales) las AUC descriptivas `TEACHER_S3_REFERENCIA_OUTER = 0,92899819`, `SAFE_ideal = 0,92508499`, `QWC24_ideal = 0,91248910` y `QWC64_ideal = 0,91779707`. **No** deben compararse directamente con las AUC Student de `inner_val` como si compartieran un mismo conjunto de evaluación.

El conteo parcial de puertas y shots tampoco es una certificación de costo físico extremo a extremo ni evidencia de ventaja cuántica.

## 7. Auditorías posteriores: qué cambió en la interpretación

Las auditorías de trazabilidad históricas —realizadas localmente y todavía no integradas todas en Git— precisaron aspectos que una comprobación de hashes o replay numérico no podía resolver:

- **3K/4F:** dependencia de supervisión global previa; una puntuación sobre datos utilizados para construir la base no es OOF del pipeline completo.
- **H1:** ajuste por fold y coincidencia exacta de cachés OOF, con reserva sobre autenticación integral de los índices y preparación upstream.
- **H2B1E0/E1:** fuente inmediata de `O*` identificada a partir de las salidas de ejecución históricas.
- **C5:** diez canales y conjunto fijo de cinco identificados; frontera de complejidad consultó el hold durante el desarrollo.
- **R3:** ajuste ALS local sobre entrenamiento externo identificado; quedan dependencias previas de la representación y de decisiones de arquitectura.
- **H2B2A0:** `inner_val` contiene ejemplos usados antes para entrenar el teacher R3; no puede declararse validación independiente de dicho teacher.
- **Generalización química:** los diagnósticos retrospectivos de grupos no sustituyen entrenamiento y validación agrupados por composición desde el inicio.

La matriz local `MATRIZ_EVIDENCIA_H2B2A7_CIERRE_OSTAR_C5_20261116.md` aún **no está versionada** en este repositorio; deberá incorporarse o resumirse con referencias y huellas estables después de revisar su contenido. No publicar masivamente auditorías ni modificar checkpoints históricos.

## 8. Tabla de decisiones científicas y su grado de respaldo

| Decisión / resultado | Evidencia concreta | Interpretación admisible |
|---|---|---|
| Crear referencias de discriminación Helstrom | Celdas históricas de 3K y H1; auditorías XXII/XXIV | Dos protocolos de supervisión distintos; métricas no intercambiables. |
| Estudiar reducción del sistema y kernels B8 | H2A3/H2A4; cotejo del kernel | Antecedente con verificación numérica; separar de desempeño nuevo. |
| Descomponer `O*` en diez canales | H2B1E1; cierre de fuente O* | Reconstrucción física del score respaldada; origen H2-A4→H2-B0 reproducido sin HOLD; selección global del método exploratoria y transferencias en RAM aún no cotejadas. |
| Utilizar C5 `II/IY/IZ/XY/ZZ` | Celda H2B1E3 y análisis de 1.023 subconjuntos | Configuración fija identificada; selección global exploratoria. |
| Ajustar R3 con ALS | H2B1E3; entrenamiento externo identificado | Ajuste localizado, no independencia completa de todas sus fuentes. |
| Reutilizar R3 en piloto H2B2A0 | Celda piloto y particiones archivadas | Teacher congelado antes del split interno; AUC `inner_val` del teacher no independiente. |
| Certificar las rutas Pauli/QWC y Student | Integraciones 00/01; PR #2 y PR #3 | Reproducibilidad numérica de evidencia archivada, no validación nueva. |
| Consolidar experimentos y recursos | Fases 3A–3D; PR #4 | Trazabilidad y análisis retrospectivo, no entrenamiento adicional. |

## 9. Dependencias abiertas y criterio de cierre

1. **Origen original de `O_FOLDS_H2B1A`:** localizar el ajuste y sus índices/etiquetas; si no existe prueba conservada, marcar *no certificable retrospectivamente*.
2. **Mapa físico 21 → 8 qubits:** formalizar bajo las restricciones de los observables/estados usados, sin afirmar equivalencia universal de espacios de Hilbert.
3. **Objetivo exacto de ALS R3:** cotejar la función de pérdida, las regularizaciones y las restricciones con la celda fuente.
4. **Modelo final elegido:** precisar qué checkpoints, cabezales y ruta de medición se congelaron como arquitectura a documentar; no inferirlo de la mejor AUC entre variantes.
5. **Generalización a nuevas composiciones:** especificar una evaluación prospectiva agrupada y aplicar todo ajuste supervisado dentro de los folds definidos.
6. **Resultados de QPU:** separar pilotos exploratorios, protocolos predefinidos y costes físicos realmente medidos; no atribuir superioridad confirmatoria sin evidencia.

**Criterio editorial:** un pendiente irresoluble no exige reabrir toda la historia experimental. Se registra como limitación, con su fuente y el efecto concreto que tiene sobre las afirmaciones de la tesis.

## 10. Fuentes y navegación

### Documentos versionados

- [Mapa científico](00_MAPA_CIENTIFICO.md)
- [Arquitectura H2B2A7](01_ARQUITECTURA_H2B2A7.md)
- [INTEGRACIÓN-00](../H2B2A7_INTEGRACION_00.md)
- [INTEGRACIÓN-01](../H2B2A7_INTEGRACION_01.md)
- [Fase 3A](../H2B2A7_FASE3A_PLAN.md)
- [Fase 3B](../H2B2A7_FASE_3B_GUIA.md)
- [Fase 3C](../H2B2A7_FASE_3C_GUIA.md)
- [Fase 3C.3](../H2B2A7_FASE_3C3_GUIA.md)
- [Fase 3C.4](../H2B2A7_FASE_3C4_GUIA.md)
- [Síntesis 3D](../../reports/H2B2A7_CONSOLIDACION/H2B2A7_3D_SINTESIS_20261113T184850523066Z/3D_INFORME.md)

### Evidencias históricas aún fuera de Git

- `AUDITORIA_XXII_LINEAJE_CV_TEACHER_H2B2A7.txt`
- `AUDITORIA_XXIV_CIERRE_H1_R3_Y_REUSO_HOLD_H2B2A7.txt`
- `CIERRE_TRAZABILIDAD_H2B1E1_H2B2A7.txt`
- `CIERRE_FINAL_FUENTE_OSTAR_Y_DECISION_C5_H2B2A7.txt`

Estas fuentes se conservan en `Tesis5_CONSOLIDACION`; **no** se han movido ni incorporado automáticamente. Se prevé que una futura matriz de evidencia incluya referencias y huellas estables, no una copia indiscriminada de todo el material local.

## 8. Anexo de proveniencia numérica H2-A4 → H2-B0 (incorporación v0.2)

La prueba primaria de esta actualización está en `AUDITORIA_NUMERICA_H2A4_A_H2B0_SIN_HOLD.txt`, complementada por `AUDITORIA_ESTRUCTURAL_OSTAR_H2B2A7.txt`. `PSI7_ALL_3S.npy` y el kernel H2-A4 fueron contrastados en 40 parejas con error máximo $1.115\times10^{-7}$; la prueba de matriz completa fue realizada para los **cinco** observables de 256×256. Los hashes SHA-256 de los artefactos, la fórmula de reconstrucción y el cuadro por fold están recogidos en [arquitectura §4.2](01_ARQUITECTURA_H2B2A7.md). Esta validación no reemplaza un test prospectivo por composición nueva.
