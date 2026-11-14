# H2B2A7 — 3C.1/3C.2: operadores y errores de expectativa

## Alcance
Solo INNER VAL previamente examinado. Sin entrenamiento, OUTER, QPU, AUC nueva ni seleccion de modelos.

Se reconstruye U con la topologia congelada de Student 1E/1F, O=U† D U y se cotejan los scores con INTEGRACION-01.
Las expectativas se calculan mediante X6 y los coeficientes Pauli; no se necesitan estados rho6 densos para los 1198 materiales.

## Normas matriciales
- STUDENT_1E B1: ||O-B*||_F / ||B*||_F = 1.472895531; ||O-B*||_op = 3.242914635
- STUDENT_1E B2: ||O-B*||_F / ||B*||_F = 1.489082115; ||O-B*||_op = 3.184529636
- STUDENT_1F B1: ||O-B*||_F / ||B*||_F = 1.492418806; ||O-B*||_op = 3.325935343
- STUDENT_1F B2: ||O-B*||_F / ||B*||_F = 1.510448254; ||O-B*||_op = 3.215261515

## Errores en estados efectivamente codificados
- STUDENT_1E: media |Δexp B1|=0.0791705485; media |Δexp B2|=0.0735944699; media |Δscore|=0.0149098683; max diferencia score vs 01=8.33e-17
- STUDENT_1F: media |Δexp B1|=0.0820303755; media |Δexp B2|=0.07580187; media |Δscore|=0.0155908733; max diferencia score vs 01=6.25e-17

## Identidad de score y cota
Δs(x)=Σ_j [lambda(x) C^T]_j × Tr[rho(x)(O_j-B*_j)].
|Δs(x)| ≤ Σ_j |[lambda(x) C^T]_j| × ||O_j-B*_j||_op.
La cota es una garantia general; los errores reales pueden ser menores para los estados materiales.

## Limitaciones
Esta fase cuantifica error de expectativas y scores; NO demuestra causalidad en rankings ni ventaja de recursos.
INNER VAL ya habia sido examinado. 1F/OPS carecen de hashes historicos originales previos.
