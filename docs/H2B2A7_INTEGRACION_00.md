# H2B2A7 — INTEGRACIÓN-00: procedencia y reproducibilidad Pauli/QWC

**Estado histórico certificado:** `REPLAY_PAULI_QWC_VERIFICADO_STUDENT_PENDIENTE`  
**Fecha del replay:** 10 de noviembre de 2026 (UTC, según `INTEGRACION00_RESUMEN.json`).  
**Rama de trabajo:** `feature/pauli-qwc`.

## 1. Qué es esta certificación

Este registro conserva una **reconstrucción de scores congelados**, no un nuevo entrenamiento, una evaluación independiente adicional ni una prueba en hardware cuántico. La fuente es una celda de 571 líneas extraída, sin modificaciones, del notebook histórico; se mantiene en `experiments/INTEGRACION_00.ipynb`.

SHA-256 del **texto de código de la celda** (no del archivo JSON `.ipynb`):

```text
350bc3d092f1c2098a28fdf7c05f5f92b1e6004f6a9b692afe9a149ecdff7ca9
```

La fuente histórica se conserva fuera de Git, junto con checkpoints binarios y la evaluación H2B2A7-13. Los checkpoints no se incorporan automáticamente al repositorio; sus hashes están consignados en los manifiestos de resultados.

## 2. Resultados archivados

| Arquitectura | Split | N | Error máximo absoluto de score | Estado |
|---|---|---:|---:|---|
| Teacher R3 | Archivo completo | 7483 | 2.7755575615628914e-17 | REPRODUCIDO |
| HEAD4 + SAFE | TRAIN | 4788 | 5.606596437113254e-09 | REPRODUCIDO |
| HEAD4 + SAFE | INNER VAL | 1198 | 3.723073363492979e-09 | REPRODUCIDO |
| SAFE ideal | OUTER HOLD archivado | 1497 | 1.3877787807814457e-17 | REPRODUCIDO |
| QWC24 ideal | OUTER HOLD archivado | 1497 | 5.551115123125783e-17 | REPRODUCIDO |
| QWC64 ideal | OUTER HOLD archivado | 1497 | 8.326672684688674e-17 | REPRODUCIDO |
| Student U,D | INNER VAL / OUTER | — | — | PARÁMETROS ENCONTRADOS; SCORE PENDIENTE |

Datos tomados de `INTEGRACION00_RESUMEN.json` generado por la ejecución congelada. Para SAFE/QWC24/QWC64 se verifica el replay contra scores previamente almacenados; **OUTER HOLD ya estaba abierto** antes de esta comprobación. No se seleccionaron nuevos hiperparámetros ni umbrales.

Los siete checkpoints enumerados en `H2B2A7_13_FINAL_OUTER_HOLD/MANIFEST_PREVIO.json` se verificaron físicamente contra SHA-256 en la auditoría local. El manifiesto de H2B2A7-18 corresponde a otra validación y **no sustituye** al de H2B2A7-13.

**Cobertura de procedencia:** 19 de 20 artefactos localizados. Falta la copia del notebook histórico con sufijo de fecha (`ContinuacionnuevaModelosdataset2(20261105-030316).ipynb`); su celda INTEGRACIÓN-00 sí se conserva en este repositorio, y el notebook histórico disponible se denomina `ContinuacionnuevaModelosdataset2.ipynb`.

## 3. Reproducción en una instalación distinta

Requisitos: Python 3.10+, `numpy`, y acceso autorizado a la carpeta histórica con los checkpoints y el CSV original. Las rutas absolutas del equipo original **no** son necesarias para ejecutar `scripts/replay_integracion00.py`.

Desde la raíz del repositorio, en PowerShell:

```powershell
# Primer paso: valida notebook, siete checkpoints y configuración sin ejecutar.
python .\scripts\replay_integracion00.py --historical-root "C:\ruta\a\Tesis4"

# Solo cuando se desea generar una nueva auditoría, de forma explícita:
python .\scripts\replay_integracion00.py --historical-root "C:\ruta\a\Tesis4" --run
```

El ejecutor verifica el hash del **código de la celda** y el hash de siete checkpoints frente al manifiesto H2B2A7-13. Inserta en memoria el origen y el directorio de salida; **no reescribe el notebook** ni modifica los artefactos históricos. Los informes nuevos se crean, con marca UTC, debajo de `reports/H2B2A7_INTEGRACION_00/`. No contiene llamadas a IBM Quantum ni instrucciones de entrenamiento.

Para comprobar la integridad de una ejecución ya almacenada, sin repetir los cálculos:

```powershell
$run = Get-ChildItem ".\reports\H2B2A7_INTEGRACION_00" -Directory | Sort-Object Name -Descending | Select-Object -First 1
python .\scripts\replay_integracion00.py --verify-report $run.FullName
```

La verificación de informes lee los hashes de `INTEGRACION00_HUELLAS_SHA256.json`. Las huellas de un reporte no prueban por sí solas su validez científica: deben interpretarse junto a `INTEGRACION00_INFORME_CIENTIFICO.md` y `INTEGRACION00_RESUMEN.json`.

## 4. Alcance y limitaciones

- **Teacher/SAFE/QWC:** reconstrucción de puntuaciones idealizadas o archivadas; no certificación end-to-end de preparación, medición y lectura en QPU.
- **Student 1E/1F:** los parámetros `U,D` y QPY encontrados son evidencia de decodificadores, pero **no** reconstruyen automáticamente el score completo. Esta parte debe certificarse por separado en `feature/student-certification` sobre una partición identificada.
- **Costo:** los 10 000 shots de QWC24/64 en H2B2A7-13 son un presupuesto incremental parcial de medición. No es un costo físico total por material. La referencia H2B2A7-16 contiene un presupuesto lógico de medición diferente; no confundir shots con duración real de QPU.
- **Evaluación:** no ajustar modelos ni comparar resultados de INNER VAL y OUTER HOLD como si fueran un mismo split pareado.
- **Portabilidad de datos:** el script es portable en cuanto a rutas, **pero requiere acceso a los checkpoints y datos congelados**, que no están incluidos en Git. Por tanto, el repositorio por sí solo todavía no permite reconstrucción completa desde cero.

## 5. Evidencia y política de publicación

La ejecución archivada incluye ocho artefactos: resumen JSON, informe científico MD, tabla de reproducibilidad, checkpoints, costos, manifiesto de hashes, referencias de cobertura y CSV con scores OUTER HOLD. Conservar sus versiones originales permite auditar los resultados.

**Aviso de privacidad y publicación:** los reportes íntegros incluyen rutas locales del equipo y potencialmente información de los datos experimentales. Aunque este repositorio es privado, cualquier versión pública futura debe revisar y, de ser necesario, **publicar una historia de Git depurada o una exportación limpia**. Borrar rutas en un commit posterior no las elimina de commits anteriores. No registrar credenciales, tokens ni datos sin autorización.

## 6. Próximos pasos documentados

1. Integrar este ejecutor en la rama Pauli/QWC y validar su modo de comprobación y de verificación de resultados existentes.
2. Mantener intactos el notebook y sus ocho artefactos certificados; no volver a calcular scores innecesariamente.
3. Auditar la arquitectura Student por separado, incluyendo preparación de estados, decodificación, cabezales previos y coherencia de particiones.
4. Añadir pruebas automáticas de funciones matemáticas extraídas, dependencias y portabilidad antes de afirmar reproducibilidad completa desde una instalación nueva.
