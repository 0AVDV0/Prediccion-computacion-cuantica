# H2B2A7 — Fase 3C.1 y 3C.2: observables y errores de expectativas

## Finalidad

Evaluar los dos observables Student de 1E y 1F, sin entrenamiento, selección ni uso de OUTER HOLD. Se reconstruyen las matrices `U` con la topología original congelada, se forma `O_j=U_j†D_jU_j` y se comparan con `B*_j` en la base de seis qubits. Se recuperan las expectativas a partir de las 4096 expectativas Pauli cacheadas en X6, sobre **INNER VAL ya examinado**.

Se reportan: `||O_j-B*_j||_F`, su valor relativo, `||O_j-B*_j||_op`, errores absolutos de expectativas por material y desviación en el score completo. El cambio de score se factoriza como

`Δs(x) = Σ_j [λ(x) Cᵀ]_j Tr(ρ(x)[O_j - B*_j])`.

Se comprueba la desigualdad `|Δs(x)| ≤ Σ_j |[λ(x)Cᵀ]_j| ||O_j-B*_j||_op`, bajo la validez de la representación cuántica usada. Se cotejan **todos los scores reconstruidos** con el CSV certificado de INTEGRACIÓN-01, sin recalcular AUC ni ajustar parámetros.

## Ejecución (PowerShell)

Desde cualquier terminal, sin importar la carpeta actual:

```powershell
python "C:\Users\javie\Tesis5_CONSOLIDACION\scripts\analizar_consolidacion_3c.py" --historical-root "C:\Users\javie\OneDrive\Escritorio\Tesis4"
```

El comando anterior es preflight **sin escrituras**. Si devuelve `PREFLIGHT OK`, ejecutar:

```powershell
python "C:\Users\javie\Tesis5_CONSOLIDACION\scripts\analizar_consolidacion_3c.py" --historical-root "C:\Users\javie\OneDrive\Escritorio\Tesis4" --write
```

Los resultados se crean exclusivamente en una carpeta nueva con UTC bajo `Tesis5_CONSOLIDACION/reports/H2B2A7_CONSOLIDACION/H2B2A7_3C_OBSERVABLES_*`.

## Integridad y límites

Antes de cualquier cálculo se comprueban 13 hashes de informes 00/01, dos hashes del código original, seis hashes de fuentes históricas (cuatro con huellas preexistentes, y dos con huellas observadas en la auditoría 01). **El hecho de cotejar ahora la huella de Student 1F y OPS no establece que su identidad histórica estuviera certificada antes**.

`numpy` es la única dependencia adicional. `X6` se abre como memoria mapeada, sin copiar los 122 MB completos ni modificarlo. El script **no ejecuta el notebook histórico**, no accede a IBM Quantum y no modifica los archivos `.npz`, `.npy` o resultados originales. No debe convertirse una correlación descriptiva en una afirmación causal de ventaja cuántica o de generalización independiente.

**No hacer commit ni push hasta revisar los resultados y el manifiesto.**
