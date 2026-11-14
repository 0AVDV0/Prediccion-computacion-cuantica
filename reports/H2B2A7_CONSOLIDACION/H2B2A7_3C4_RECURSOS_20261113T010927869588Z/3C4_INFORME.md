# H2B2A7 — 3C.4: auditoría de recursos conocidos

## Evidencia
- Se verifican la huella del CSV de costos de INTEGRACIÓN-00 y el SHA del código de INTEGRACIÓN-01.
- Los Student tienen dos decodificadores de 6 qubits, cada uno con 102 RZ, 102 RY y 48 RXX.
- Los 504 operadores de puerta elementales de ambas U no constituyen el circuito integral del modelo.
- QWC24/QWC64: 24/64 bases y 10.000 shots **incrementales/parciales** para rho6.
- QWC365: 365 bases; 100.000 shots rho6 + 10.000 rho4 = 110.000 de presupuesto **lógico de referencia**.

## Interpretación
No existe evidencia suficiente para comparar costo total físico de Student frente a QWC ni para afirmar ventaja cuántica.
Los conteos Student no incluyen preparación de estados, otros cuatro cabezales, asignación global de shots, compilación, conectividad ni mitigación de errores.
La reducción de bases o de puertas no implica automáticamente menor tiempo real ni mayor precisión.

## Limitaciones
- QWC24/QWC64: 10000 shots incrementales sobre rho6, no shots de toda la arquitectura.
- QWC365: 110000 shots es un presupuesto logico de referencia, NO tiempo, fidelidad ni costo QPU.
- Student: 96 RXX en dos U, NO 96 RXX del modelo integral; faltan preparacion, cuatro cabezales, rho4 y ejecucion fisica.
- No hay base suficiente para comparar AUC/costos entre Student INNER y QWC OUTER como un frente de Pareto homogéneo.
- No se convierten puertas abstractas en CNOT, profundidad ISA, errores de hardware ni duraciones.
- No se ha certificado un costo end-to-end comparable para todos los modelos.
