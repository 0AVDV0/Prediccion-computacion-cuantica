# H2B2A7 — Revisión independiente de resultados INTEGRACIÓN-01

**Estado:** REPLAY NUMÉRICO FAVORABLE; CERTIFICACIÓN CIENTÍFICA Y FÍSICA AÚN PARCIAL.
**Alcance:** revisión de los cuatro productos de una ejecución local de certificación; no se ejecutaron checkpoints ni circuitos originales en este entorno.
**Objetivo:** registrar lo comprobado sin inventar evaluaciones nuevas o adjudicar superioridad física.

## 1. Integridad y cobertura de la auditoría

- 94 filas de pruebas, 94 `PASS`, cero `FAIL` y cero reservas registradas.
- SHA previo cotejado: `TEACHER`, `SAFE`, `X6`, `STUDENT_1E`, `QPY_1E`.
- Existencia con SHA nuevo, **sin cotejo histórico**: operadores `B1B2`, `STUDENT_1F`, `A6_2B1`, `A6_2B2`.
- Splits disjuntos: TRAIN=4788, INNER_VAL=1198, OUTER_HOLD=1497; total 7483.
- Dimensiones de datos Pauli: `(7483, 4096)`; 6 qubits, 4^6=4096 cadenas de Pauli.
- Contrastes de convenciones y coeficientes Pauli aprobados para 4 cadenas elegidas; chequeos de `rho6` sobre 10 índices, no exhaustivos de todo el conjunto.
- Para 1E y 1F la reconstrucción matricial frente a Qiskit muestra errores <1e-15; la unitariedad, <3.4e-15.
- Solamente **1E** posee cotejo explícito con QPY archivado: dos circuitos, discrepancia <1e-14; 1F no recibe equivalencia QPY con esa evidencia.

## 2. Métricas reproducidas (INNER_VAL, 1198 materiales)

| Modelo | AUC reconstruida | AUC histórica | Diferencia |
|---|---:|---:|---:|
| Student 1E | 0.913537480155041 | 0.913537480155041 | 0 |
| Student 1F | 0.915988958336313 | 0.915988958336313 | 1.1e-16 |

Incremento 1F − 1E = **0.002451478**. Esta coincidencia de AUC es evidencia de reproducción agregada, **no** de coincidencia de cada score con un archivo original, ya que ambos registros `score_por_material_archivado=false`.

## 3. Resultado físico-matemático relevante: ranking vs. fidelidad de operador

Se examina el observable de cada corrección en la forma:

`O_j = U_j^† D_j U_j`, con `U_j` unitario y `D_j` diagonal de 64 entradas.

La distancia de Frobenius reportada frente a `B*_j` es:

| Modelo | `||O_1-B*_1||_F` | `||O_2-B*_2||_F` |
|---|---:|---:|
| 1E | 1.472895531 | 1.489082115 |
| 1F | 1.492418806 | 1.510448254 |

1F tiene mayor distancia matricial, pero mejora algo el ranking AUC. **No es un error de implementación por sí mismo**: ajustar el ranking sobre la distribución de materiales no es equivalente a optimizar una norma global de operadores. Hace falta analizar los errores de score por material, no solo la norma de Frobenius. Sin `||B*_j||_F` ni escala de scores, estas distancias absolutas no bastan para juzgar si la aproximación es grande o pequeña.

## 4. Recursos: únicamente lo realmente comprobado

Para cada circuito QPY de 1E se informa: `rz=348`, `sx=204`, `cx=96`. Dos circuitos suman `rz=696`, `sx=408`, `cx=192` **solo para los dos decodificadores archivados**. No se dispone de costo global certificado por material ni layout ISA de backend, ni de medición física de la diagonal general `D_j`, otros cuatro cabezales, mezclas para preparar `rho6`, réplicas de `rho[4]`, shot budget y costos de lectura; por ello **no existe demostración de ventaja de recursos QPU**.

## 5. Límites y decisión

1. 1F y candidatos A6 tienen hash calculado, pero ningún hash histórico anterior contrastado aquí; no afirmar autenticación histórica plena.
2. 1F tiene unitariedad y equivalencia con Qiskit, pero no comparación con QPY propio.
3. Diez chequeos de estado/expectativas no son una prueba exhaustiva de todos los estados.
4. No existe vector pareado original de scores por material para certificación completa del replay.
5. INNER_VAL ya fue empleado históricamente; los resultados son **diagnósticos**, no un nuevo holdout independiente. El OUTER_HOLD no se evaluó en esta certificación.
6. El hallazgo 1F > 1E en AUC es descriptivo. La significancia estadística y el costo físico no fueron certificados.
7. El estado del informe fuente es `PRUEBAS_NUMERICAS_SUPERADAS_VALIDACION_HISTORICA_PENDIENTE`. Mantener esta etiqueta.

**Decisión:** autorizar versionado de código, informe y tests de equivalencia numérica en Git; **no** autorizar nuevo entrenamiento, selección de arquitectura por OUTER_HOLD, ni afirmar que el student es ejecutable económicamente en QPU.

## 6. Próxima tarea reproducible (sin entrenar)

A. Inventariar, autenticar y localizar los checkpoints y circuitos propios de 1F y A6.
B. Recuperar los vectores de score originales por material, si existen; comparar bajo el mismo orden de índices. Si no existen, documentar el bloqueo.
C. Evaluar sobre los mismos materiales la distribución de `delta_j(x)=Tr[(B*_j-O_j) rho6(x)]`, error global de score y cambios de orden de pares FM/AFM.
D. Construir presupuesto **completo** de recursos incluyendo preparación y medición de diagonal; solo entonces valorar una futura ejecución física.

## 7. Procedencia

El manifiesto `INTEGRACION01_MANIFIESTO_FUENTES_SHA256.csv` registra el SHA-256 de los cuatro archivos aportados. Estas huellas identifican el **resultado de auditoría**, no sustituyen el SHA-256 de todos los binarios ni de datos de entrenamiento.

No registrar secretos, tokens, datos privados ni rutas absolutas de usuario en reportes públicos.
