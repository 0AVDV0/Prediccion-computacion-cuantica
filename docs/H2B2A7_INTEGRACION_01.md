# H2B2A7 — INTEGRACIÓN-01: certificación numérica Teacher–Student 1E/1F

**Estado:** `PRUEBAS_NUMERICAS_SUPERADAS_VALIDACION_HISTORICA_PENDIENTE`  
**Fecha del reporte:** 11 de noviembre de 2026 (UTC según el identificador de ejecución)  
**Rama de trabajo:** `feature/student-certification`  
**Directorio de la evidencia:** `reports/H2B2A7_INTEGRACION_01/H2B2A7_INTEGRACION_01_CERT_20261111T221029053812Z`

## 1. Alcance y procedencia

Esta integración **no entrena modelos**, **no ejecuta circuitos en IBM Quantum** y **no utiliza OUTER HOLD en esta ejecución**. Conserva una celda original extraída (356 líneas) en `experiments/INTEGRACION_01_CERT.ipynb`; su SHA-256 sobre el **texto de código** es:

`089415d27e535700d5de2d56e78d4f255edc2c718d57141be125bd30ef9556d8`

El ejecutor `scripts/replay_integracion01_controlado.py` coteja esa huella, hace preflight de nueve fuentes del archivo histórico Tesis4 y, si se pasa `--run`, reconstruye resultados colocando los productos en una subcarpeta nueva bajo el worktree Student. **No se incluyen checkpoints históricos en Git**.

## 2. Resultado numérico observado

- **94/94 pruebas PASS**, cero fallos, cero reservas. Fuente: `INTEGRACION01_PRUEBAS_DE_CERTIFICACION.csv` y `INTEGRACION01_RESUMEN_DECISION.json`.
- **Student 1E**: AUC recalculada de INNER VAL = **0.913537480155041**, AUC archivada = **0.913537480155041** (n=1198; diferencia 0).
- **Student 1F**: AUC recalculada de INNER VAL = **0.9159889583363131**, AUC archivada ≈ **0.915988958336313** (n=1198; diferencia ≈ 1.11×10⁻¹⁶).
- `INTEGRACION01_SCORES_INNER_VAL_RECONSTRUIDOS.csv` contiene 2396 filas: 1198 por modelo, con idénticos índices `global_index` y el indicador `INNER_VAL_YA_EXAMINADO`.
- Se verificaron propiedades matriciales de U, diagonal D, hermiticidad de O, endianess, consistencia con Qiskit y referencias X6. El QPY **histórico de Student 1E** fue cotejado; **1F no dispone de un QPY histórico cotejado** en esta auditoría.
- Las desviaciones de Frobenius frente a los operadores objetivo B★ son aproximadamente 1.47–1.51. Esos valores **no** son errores de unitariedad ni un certificado de aproximación exacta.

## 3. Fuentes y huellas

El inventario `INTEGRACION01_INVENTARIO_Y_HUELLAS.csv` confirma nueve fuentes localizadas. **Cinco** tienen SHA-256 anteriores cotejados: TEACHER, SAFE, X6, STUDENT_1E y QPY_1E. **Cuatro** se hallaron con SHA calculado en esta auditoría, pero sin referencia previa: OPS_B1B2, STUDENT_1F, A6_2B1 y A6_2B2. Sus hashes observados se guardan como trazabilidad, **no** como certificación histórica retrospectiva.

`INTEGRACION01_HUELLAS_SHA256.json` contiene SHA-256 de los seis productos originales byte por byte y un inventario de huellas de fuentes. No incorpora un hash de sí mismo, para evitar autorreferencia.

## 4. Reproducibilidad y verificación

Desde PowerShell ubicado en `Tesis5_STUDENT`:

```powershell
python .\scripts\verificar_integracion01_evidencia.py
```

El verificador **solo lee** el notebook, manifiesto y reportes. Comprueba los 6/6 hashes de resultados, 94/94 pruebas PASS, estructura de los 2396 scores, igualdad de los índices entre modelos, AUC archivadas y alcance sin OUTER HOLD ni QPU.

Preflight de fuentes históricas (requiere disponer de Tesis4 en esa ubicación):

```powershell
python .\scripts\replay_integracion01_controlado.py --historical-root "C:\Users\javie\OneDrive\Escritorio\Tesis4"
```

Para repetir una auditoría **únicamente** si es necesario, agregar `--run`. Genera otro directorio con timestamp sin sustituir los informes certificados. Antes de ejecutar se debe revisar la ruta de origen y la salida prevista. No ejecutar `Run All` sobre el notebook original ni modificar datos históricos.

## 5. Límites explícitos de interpretación

1. INNER VAL **ya había sido explorado**. La auditoría no constituye una evaluación externa independiente ni demuestra generalización adicional.
2. La coincidencia de **AUC agregada** no certifica igualdad de cada score frente al vector histórico, que no fue cotejado pareadamente.
3. El valor 1F observado no certifica identidad histórica previa de su archivo ni de QPY (no cotejado).
4. Ni los costos físicos end-to-end, ni el layout ISA, ni una ventaja cuántica están certificados aquí.
5. El informe y el CSV de inventario contienen rutas absolutas de Windows; mantener el repositorio **privado**, o limpiar esta información **antes de una futura publicación** y tener presente que una eliminación posterior no borra el historial Git.

**Conclusión:** la reconstrucción matemática de Student 1E y 1F y sus AUC de INNER VAL está respaldada por las pruebas de la auditoría; la certificación de procedencia histórica completa sigue pendiente.
