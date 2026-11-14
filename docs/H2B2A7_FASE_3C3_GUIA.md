# H2B2A7 — Fase 3C.3: inversión de ranking y márgenes

## Justificación

La fase 3C.1/3C.2 comprobó que los observables `Student 1E` y `Student 1F` no reconstruyen globalmente las matrices objetivo, aunque los errores de expectativa sobre INNER VAL son inferiores a sus cotas globales. El siguiente paso mide **qué pares de materiales cambian de orden**.

## Ejecución

Desde cualquier ubicación en PowerShell, una vez extraído el paquete en `C:\Users\javie\Tesis5_CONSOLIDACION`:

```powershell
python "C:\Users\javie\Tesis5_CONSOLIDACION\scripts\analizar_consolidacion_3c3.py"
python "C:\Users\javie\Tesis5_CONSOLIDACION\scripts\analizar_consolidacion_3c3.py" --write
```

El script localiza automáticamente el único directorio `H2B2A7_3C_OBSERVABLES_*`. Si hay más de uno, exige `--source-3c "RUTA_EXACTA"`, para evitar seleccionar una ejecución accidental. No necesita `Tesis4`, NumPy ni Qiskit.

## Comparaciones

1. Score objetivo B frente a Student 1E (mismos 1198 índices INNER VAL).
2. Score objetivo B frente a Student 1F (mismos 1198 índices INNER VAL).
3. Student 1E frente a Student 1F (misma muestra).

Métricas: Pearson, Spearman con rangos promedio en empates, Kendall τ-b exacto, pares invertidos, top/bottom 5/10/20 %, ranking por material. La condición suficiente

\[
|s_B(x)-s_B(y)|>|\Delta s(x)|+|\Delta s(y)|
\]

se verifica con los *errores observados a posteriori*; no se presenta como garantía en datos nuevos.

## Seguridad y limitaciones

Solo se leen los 4 archivos de la evidencia 3C y se comprueban sus SHA-256. El script no accede a OUTER HOLD ni a los checkpoints originales, no reconstruye etiquetas ni estima AUC, no optimiza, no reentrena y no llama a IBM/QPU. Todos los resultados se crean en una carpeta nueva bajo `reports/H2B2A7_CONSOLIDACION` y los informes previos no se tocan. No hacer commit antes de revisión.
