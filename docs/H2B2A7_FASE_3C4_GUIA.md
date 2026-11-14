# H2B2A7 — fase 3C.4: auditoría de recursos cuánticos

**Propósito.** Inventariar costos lógicos respaldados por las evidencias congeladas, separando presupuestos parciales, un plan de medición de referencia y las puertas de los dos decodificadores Student. **No** inferir costo total, tiempo QPU ni ventaja cuántica.

## Ejecución en PowerShell

Desde cualquier directorio:

```powershell
python "C:\Users\javie\Tesis5_CONSOLIDACION\scripts\auditar_recursos_3c4.py"
```

El script no escribe datos sin `--write`. Debe indicar `PREFLIGHT OK` tras verificar los SHA-256 del CSV de costos INTEGRACIÓN-00 y del código Student INTEGRACIÓN-01.

```powershell
python "C:\Users\javie\Tesis5_CONSOLIDACION\scripts\auditar_recursos_3c4.py" --write
```

Se crearán **seis archivos nuevos** en una carpeta `H2B2A7_3C4_RECURSOS_...` bajo `reports/H2B2A7_CONSOLIDACION/`. No se modifican reportes ni checkpoints anteriores.

## Alcance científico

- **QWC24 / QWC64:** 24/64 bases, **10.000 shots incrementales/parciales** por material, exclusivos del componente rho6 examinado. No se representan como presupuesto end-to-end.
- **QWC de referencia (fase 16):** 365 bases, 100.000 shots de rho6 y 10.000 de rho4; total **110.000 shots lógicos planificados**, sin tiempo de QPU ni compilación hardware.
- **Student 1E / 1F:** dos operadores de corrección implementados con `U† D U`. Para aplicar U en la base de medición, cada circuito congelado usa 102 RZ, 102 RY y 48 RXX; **252 puertas lógicas por U** o 504 para ambas U. El conteo está antes de transpilar y no incluye otros cuatro cabezales, la preparación de rho, overhead ni shots.
- La matriz diagonal `D` tiene 64 valores por cabezal, **no** 64 puertas.

**No mezclar:** Student INNER VAL y QWC OUTER no son evaluaciones homólogas para inferir una curva costo–AUC; la ausencia de un presupuesto end-to-end impide establecer una ventaja de recursos del modelo completo.

No hacer commit ni push de esta fase sin revisar primero su salida.
