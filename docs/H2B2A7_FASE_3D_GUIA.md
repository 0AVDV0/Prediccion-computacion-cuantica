# H2B2A7 — Fase 3D: síntesis y auditoría automatizada

## Alcance

Esta fase **no** reentrena, recalcula AUC, ejecuta QPU, modifica `Tesis4` ni compara estadísticas de INNER VAL con OUTER HOLD como si fueran el mismo experimento. Consolida evidencias ya existentes mediante una auditoría offline de cinco manifiestos independientes: 3A, 3B, 3C, 3C3 y 3C4.

Los informes originales son **inmutables**. Se verifica el hash SHA-256 de sus 22 productos y la coherencia de los principales metadatos (1497 OUTER, 1198 INNER por Student, 717003 pares, recursos parciales, no QPU). El script distingue entre la coincidencia de bytes del archivo local y la del blob comprometido en Git, que puede ser relevante ante la conversión de finales de línea en Windows.

## Ejecución

Desde cualquier consola:

```powershell
python "C:\Users\javie\Tesis5_CONSOLIDACION\scripts\auditar_sintesis_3d.py"
```

Esperar `PREFLIGHT OK`. Después:

```powershell
python "C:\Users\javie\Tesis5_CONSOLIDACION\scripts\auditar_sintesis_3d.py" --write
```

Esto crea una sola carpeta nueva `reports/H2B2A7_CONSOLIDACION/H2B2A7_3D_SINTESIS_<UTC>/` con cuatro archivos: `3D_RESUMEN.json`, `3D_INFORME.md`, `3D_INTEGRIDAD_PRODUCTOS.csv`, `3D_MANIFIESTO_SHA256.json`. No usar `git add .` ni `git clean`, no borrar repeticiones históricas.

## GitHub Actions

`h2b2a7-consolidacion-integridad.yml` prueba la consistencia de los informes **sin** descargar datasets privados, ejecutar notebooks o requerir paquetes externos. Activar mediante commit independiente **después de validar localmente**. Si las verificaciones fallan por normalización de archivos, se deben inspeccionar los hashes y las versiones comprometidas; no modificar manifiestos para ocultar discrepancias.

## Interpretación científica

- Los resultados de 3B sobre OUTER HOLD son *retrospectivos* porque el conjunto ya estaba examinado.
- Los Student se contrastan en INNER VAL previamente examinado.
- Los errores de operadores, expectativas, puntuaciones y ranking no son intercambiables.
- Las cantidades de shots y puertas son *parciales* y no comparan el costo físico integral de los modelos.
- Una verificación SHA-256 exitosa prueba consistencia de artefactos archivados, no generalización ni ventaja cuántica.
