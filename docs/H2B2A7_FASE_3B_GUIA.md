# H2B2A7 — Fase 3B: análisis descriptivo pareado

## Objetivo

Calcular correlaciones de scores, estabilidad del ranking y diferencias descriptivas entre modelos **sobre índices idénticos**, sin mezclar los splits ni seleccionar arquitecturas a partir del OUTER HOLD ya examinado.

- **OUTER**: 1.497 materiales con etiquetas para Teacher S3 de referencia, SAFE ideal, QWC24 ideal y QWC64 ideal. Seis pares con Pearson, Spearman, Kendall tau-b, diferencias de scores y AUC descriptivas.
- **INNER**: 1.198 materiales pareados Student 1E/1F. Un par con Pearson, Spearman, Kendall tau-b y diferencias de scores; **sin AUC recalculada** por falta de etiquetas en los CSV disponibles.
- **Bootstrap**: 1.000 repeticiones estratificadas por clase en OUTER, usando los mismos índices para ambos modelos de cada par. Intervalos percentiles condicionales a los datos observados: **no representan un nuevo test independiente**.

## Requisitos

Python con `numpy` y `scipy` instalados; ejecutar en la raíz de `Tesis5_CONSOLIDACION`. Los archivos de integración 00 y 01 deben seguir intactos y estar presentes en el Worktree. El inventario 3A debe conservar sus cinco archivos.

## Comandos PowerShell

```powershell
cd "C:\Users\javie\Tesis5_CONSOLIDACION"
python .\scripts\analizar_consolidacion_3b.py
python .\scripts\analizar_consolidacion_3b.py --write
```

El primer comando hace **solo preflight de integridad**; el segundo calcula y guarda cinco nuevos artefactos en `reports/H2B2A7_CONSOLIDACION/H2B2A7_3B_ANALISIS_<UTC>/`.

**No ejecutar** antes de revisar la salida del preflight. No hacer commit ni push de los informes hasta comprobar su consistencia y procedencia.

## Precauciones científicas

1. OUTER HOLD ya había sido examinado: prohibido utilizar diferencias de AUC o intervalos para elegir modelos y luego presentarlo como evaluación independiente.
2. Student 1E y 1F no cuentan con etiquetas en el CSV de esta fase: sus AUC históricas pueden citarse separadamente, pero no recalcularse aquí.
3. `TEACHER_S3_REFERENCIA_OUTER` y `TEACHER_R3` no son equivalentes demostrados sin trazabilidad adicional del checkpoint.
4. Las diferencias de scores dependen de la escala y no deben confundirse con fidelidad cuántica ni con errores de los observables.
5. Sin ejecución de circuitos, reentrenamiento, cambios de datos históricos o escrituras fuera del Worktree.
