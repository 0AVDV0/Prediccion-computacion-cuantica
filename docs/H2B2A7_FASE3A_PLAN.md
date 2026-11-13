# H2B2A7 — Fase 3A: matriz de cobertura y trazabilidad

El objetivo es establecer qué comparaciones científicas son posibles con la evidencia ya incorporada a `develop`.

1. Ejecutar `python .\scripts\auditar_consolidacion_3a.py` sin argumentos para verificar exclusivamente los informes y las fuentes; no escribe datos.
2. Si indica `PREFLIGHT OK`, ejecutar `python .\scripts\auditar_consolidacion_3a.py --write` para generar cinco productos en un subdirectorio nuevo bajo `reports/H2B2A7_CONSOLIDACION/`.
3. Revisar el CSV de coberturas y el de pares antes de realizar inferencias estadísticas.
4. No incluir resultados de INNER VAL en análisis pareados con OUTER HOLD.
5. Mantener `main` y el Worktree `creacion-de-modelo` intactos. La revisión y el PR serán pasos posteriores.

El inventario lee únicamente los reportes de INTEGRACIÓN-00 e INTEGRACIÓN-01 que están bajo control de Git. No depende de `Tesis4`, Qiskit ni NumPy. El código original y ambos manifiestos son verificados antes de generar el reporte.

**Limitación:** los CSV de Student contienen scores e índices, pero no las etiquetas de INNER VAL, de modo que esta fase no recalcula AUC. Las AUC archivadas se indican como tales. Los índices globales no sustituyen la verificación de procedencia de datos.
