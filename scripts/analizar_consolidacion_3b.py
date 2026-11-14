#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Fase 3B: análisis retrospectivo pareado de H2B2A7.

Sin reentrenamiento, sin QPU y sin alterar evidencias de 3A/INTEGRACIONES.
Los 6 pares OUTER son descriptivos POST APERTURA; Student INNER sin etiquetas.
Ejecutar desde la raíz del worktree Tesis5_CONSOLIDACION.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
from pathlib import Path
from datetime import datetime, timezone
from itertools import combinations

EXPECTED_OUTER = {
    'TEACHER_S3_REFERENCIA_OUTER': 'teacher_s3_archivado_checkpoint',
    'SAFE_ideal': 'score_SAFE_ideal_replay',
    'QWC24_ideal': 'score_QWC24_ideal_replay',
    'QWC64_ideal': 'score_QWC64_ideal_replay',
}
STUDENT_MODELS = ('STUDENT_1E', 'STUDENT_1F')
EXPECTED_N_OUTER = 1497
EXPECTED_N_INNER = 1198


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open('rb') as f:
        for part in iter(lambda: f.read(1024 * 1024), b''):
            h.update(part)
    return h.hexdigest()


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open('r', encoding='utf-8-sig', newline='') as f:
        rows = list(csv.DictReader(f))
    if not rows:
        raise ValueError(f'CSV vacío: {path}')
    return rows


def check_sha_folder(folder: Path, manifest_name: str, field: str, count: int) -> None:
    manifest = json.loads((folder / manifest_name).read_text(encoding='utf-8'))
    items = manifest[field]
    if len(items) != count:
        raise ValueError(f'{manifest_name}: {len(items)} archivos (esperado {count})')
    for name, expect in items.items():
        if not name or Path(name).name != name:
            raise ValueError(f'Nombre de archivo inseguro: {name}')
        file = folder / name
        if not file.is_file() or digest(file).lower() != expect.lower():
            raise ValueError(f'Integridad fallida en {file}')


def file_from_coverage(worktree: Path, coverage: list[dict], model: str, split: str) -> Path:
    selected = [r for r in coverage if r['modelo'] == model and r['split'] == split]
    if len(selected) != 1:
        raise ValueError(f'Cobertura ausente/duplicada: {model} / {split}')
    rel = Path(selected[0]['archivo_evidencia'].replace('\\', '/'))
    dest = (worktree / rel).resolve(strict=True)
    if not dest.is_relative_to(worktree):
        raise ValueError('Ruta de evidencia fuera del worktree')
    return dest


def load_evidence(worktree: Path, folder3a: Path):
    # Certificación hash 3A, además de ambas integraciones (fuentes del inventario).
    check_sha_folder(folder3a, '3A_MANIFIESTO_SHA256.json', 'productos_sha256', 4)
    coverage = read_csv(folder3a / '3A_MATRIZ_COBERTURA.csv')
    pairs = read_csv(folder3a / '3A_PARES_COMPARABLES.csv')
    if len(coverage) != 9 or len(pairs) != 7:
        raise ValueError('Matriz 3A alterada: se esperan 9 coberturas y 7 pares')
    exp_pairs = {frozenset(p) for p in combinations(EXPECTED_OUTER, 2)} | {frozenset(STUDENT_MODELS)}
    actual_pairs = {frozenset((p['modelo_a'], p['modelo_b'])) for p in pairs}
    if exp_pairs != actual_pairs or len(actual_pairs) != 7:
        raise ValueError('Pares 3A distintos a los siete esperados')
    for p in pairs:
        is_outer = p['modelo_a'] in EXPECTED_OUTER and p['modelo_b'] in EXPECTED_OUTER
        expected_split = 'OUTER_HOLD_ARCHIVADO' if is_outer else 'INNER_VAL_YA_EXAMINADO'
        if p['split'] != expected_split or int(p['n_indices_comunes']) != (1497 if is_outer else 1198):
            raise ValueError('Partición/cobertura inconsistente en pares 3A')

    f0 = file_from_coverage(worktree, coverage, 'SAFE_ideal', 'OUTER_HOLD_ARCHIVADO')
    f1 = file_from_coverage(worktree, coverage, 'STUDENT_1E', 'INNER_VAL_YA_EXAMINADO')
    check_sha_folder(f0.parent, 'INTEGRACION00_HUELLAS_SHA256.json', 'productos_sha256', 7)
    check_sha_folder(f1.parent, 'INTEGRACION01_HUELLAS_SHA256.json', 'archivos_resultado_sha256', 6)
    outer = read_csv(f0)
    students = read_csv(f1)
    if len(outer) != EXPECTED_N_OUTER or len(students) != 2 * EXPECTED_N_INNER:
        raise ValueError('Número inesperado de filas originales')
    outer_by_id = {}
    for r in outer:
        k = int(r['global_index'])
        if k in outer_by_id:
            raise ValueError(f'Índice OUTER repetido: {k}')
        y = int(r['y_FM_ARCHIVADA'])
        if y not in (0, 1):
            raise ValueError('Etiqueta OUTER no binaria')
        scores = {m: float(r[col]) for m, col in EXPECTED_OUTER.items()}
        if not all(math.isfinite(x) for x in scores.values()):
            raise ValueError(f'Score OUTER no finito: {k}')
        outer_by_id[k] = (y, scores)
    students_by_model = {m: {} for m in STUDENT_MODELS}
    for r in students:
        m = r['modelo']
        if m not in students_by_model or r['split'] != 'INNER_VAL_YA_EXAMINADO':
            raise ValueError('Modelo o partición inesperada en Student')
        k = int(r['global_index'])
        if k in students_by_model[m]:
            raise ValueError(f'Índice Student duplicado: {k}')
        score = float(r['score'])
        if not math.isfinite(score):
            raise ValueError('Score Student no finito')
        students_by_model[m][k] = score
    if (any(len(d) != EXPECTED_N_INNER for d in students_by_model.values()) or
        set(students_by_model['STUDENT_1E']) != set(students_by_model['STUDENT_1F'])):
        raise ValueError('Student 1E/1F no usan los mismos 1198 índices')
    if set(outer_by_id) & set(students_by_model['STUDENT_1E']):
        raise ValueError('Intersección inesperada INNER/OUTER')
    if len(set(y for y, _ in outer_by_id.values())) != 2:
        raise ValueError('OUTER debe contener ambas clases')
    return outer_by_id, students_by_model, f0, f1


def auc(y, scores):
    # ROC AUC empírica mediante ranking, válida con empates (rankdata).
    import numpy as np
    from scipy.stats import rankdata
    y = np.asarray(y, dtype=int)
    s = np.asarray(scores, dtype=float)
    npos = int((y == 1).sum()); nneg = len(y) - npos
    if npos == 0 or nneg == 0:
        raise ValueError('AUC requiere ambas clases')
    ranks = rankdata(s, method='average')
    return float((ranks[y == 1].sum() - npos * (npos + 1) / 2) / (npos * nneg))


def summarize_pairs(outer: dict, students: dict, n_boot: int, seed: int):
    import numpy as np
    from scipy.stats import spearmanr, kendalltau, pearsonr
    rows = []
    auc_rows = []
    indexes = sorted(outer)
    y = np.asarray([outer[k][0] for k in indexes], dtype=int)
    outer_scores = {m: np.asarray([outer[k][1][m] for k in indexes], dtype=float) for m in EXPECTED_OUTER}
    auc_per_model = {m: auc(y, v) for m, v in outer_scores.items()}
    for m, a in auc_per_model.items():
        auc_rows.append({'modelo': m, 'split': 'OUTER_HOLD_ARCHIVADO', 'n': len(y),
                         'auc_recalculada_retro': a, 'interpretacion': 'DESCRIPTIVA_POST_APERTURA'})
    rng = np.random.default_rng(seed)
    pos = np.where(y == 1)[0]; neg = np.where(y == 0)[0]
    for a, b in combinations(EXPECTED_OUTER, 2):
        va = outer_scores[a]; vb = outer_scores[b]
        delta = va - vb
        auc_delta = auc_per_model[a] - auc_per_model[b]
        boot = []
        for _ in range(n_boot):
            ix = np.concatenate((rng.choice(pos, len(pos), replace=True),
                                 rng.choice(neg, len(neg), replace=True)))
            yy = y[ix]
            boot.append(auc(yy, va[ix]) - auc(yy, vb[ix]))
        low, high = np.quantile(boot, [0.025, 0.975])
        rows.append({'modelo_a': a, 'modelo_b': b, 'split': 'OUTER_HOLD_ARCHIVADO',
                     'n': len(y), 'etiquetas_disponibles': True,
                     'pearson': float(pearsonr(va, vb).statistic),
                     'spearman': float(spearmanr(va, vb).statistic),
                     'kendall_tau_b': float(kendalltau(va, vb).statistic),
                     'mae_scores': float(np.abs(delta).mean()),
                     'rmse_scores': float(np.sqrt((delta ** 2).mean())),
                     'max_abs_delta_score': float(np.abs(delta).max()),
                     'auc_a_retro': auc_per_model[a], 'auc_b_retro': auc_per_model[b],
                     'delta_auc_a_menos_b': auc_delta,
                     'bootstrap_95_inf_condicional': float(low),
                     'bootstrap_95_sup_condicional': float(high),
                     'bootstrap_repeticiones': n_boot,
                     'alcance': 'RETROSPECTIVO_OUTER_YA_ABIERTO_NO_GENERALIZACION_NUEVA'})
    ids = sorted(students['STUDENT_1E'])
    v1 = np.asarray([students['STUDENT_1E'][k] for k in ids])
    v2 = np.asarray([students['STUDENT_1F'][k] for k in ids])
    delta = v1 - v2
    rows.append({'modelo_a': 'STUDENT_1E', 'modelo_b': 'STUDENT_1F',
                 'split': 'INNER_VAL_YA_EXAMINADO', 'n': len(ids),
                 'etiquetas_disponibles': False,
                 'pearson': float(pearsonr(v1, v2).statistic),
                 'spearman': float(spearmanr(v1, v2).statistic),
                 'kendall_tau_b': float(kendalltau(v1, v2).statistic),
                 'mae_scores': float(np.abs(delta).mean()),
                 'rmse_scores': float(np.sqrt((delta ** 2).mean())),
                 'max_abs_delta_score': float(np.abs(delta).max()),
                 'auc_a_retro': None, 'auc_b_retro': None,
                 'delta_auc_a_menos_b': None,
                 'bootstrap_95_inf_condicional': None,
                 'bootstrap_95_sup_condicional': None,
                 'bootstrap_repeticiones': 0,
                 'alcance': 'INNER_SCORES_SIN_ETIQUETAS_NO_RECALCULAR_AUC'})
    return rows, auc_rows


def dump_csv(file: Path, rows: list[dict]):
    with file.open('w', encoding='utf-8-sig', newline='') as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader(); w.writerows(rows)


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--worktree', type=Path, default=Path.cwd(), help='Worktree de consolidación; defecto: cwd')
    p.add_argument('--inventario-3a', type=Path, help='Carpeta exacta con los cinco resultados de fase 3A')
    p.add_argument('--bootstrap', type=int, default=1000, help='Repeticiones estratificadas descriptivas OUTER (por defecto 1000)')
    p.add_argument('--seed', type=int, default=20261112)
    p.add_argument('--write', action='store_true', help='Calcula y escribe resultados nuevos; sin flag: solo preflight')
    a = p.parse_args()
    root = a.worktree.resolve(strict=True)
    folderbase = (root / 'reports' / 'H2B2A7_CONSOLIDACION').resolve(strict=True)
    if a.inventario_3a:
        folder3a = a.inventario_3a.resolve(strict=True)
    else:
        candidates = sorted(x for x in folderbase.glob('H2B2A7_3A_INVENTARIO_*') if x.is_dir())
        if not candidates:
            raise FileNotFoundError('No se encontró carpeta de inventario 3A')
        folder3a = candidates[-1]
    if not folder3a.is_relative_to(root):
        raise ValueError('3A debe encontrarse dentro del worktree')
    if not 100 <= a.bootstrap <= 10000:
        raise ValueError('--bootstrap debe estar entre 100 y 10000')
    outer, students, f0, f1 = load_evidence(root, folder3a)
    print('H2B2A7 | FASE 3B | PREFLIGHT OK')
    print('3A, INTEGRACION-00 e INTEGRACION-01: huellas verificadas')
    print('OUTER:', len(outer), 'registros con etiquetas; 6 pares retrospectivos')
    print('INNER:', len(students['STUDENT_1E']), 'registros por Student; 1 par sin etiquetas')
    print('Índices INNER/OUTER comunes: 0')
    if not a.write:
        print('Sin escrituras ni cálculos estadísticos. Usa --write para generar resultados 3B.')
        return
    rows, auc_rows = summarize_pairs(outer, students, a.bootstrap, a.seed)
    tag = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
    output = folderbase / ('H2B2A7_3B_ANALISIS_' + tag)
    if not output.is_relative_to(root) or output.exists():
        raise RuntimeError('Salida fuera del worktree o existente')
    output.mkdir(parents=True, exist_ok=False)
    files = {
        '3B_COMPARACION_PAREADA.csv': rows,
        '3B_AUC_OUTER_RETROSPECTIVAS.csv': auc_rows,
    }
    for name, content in files.items():
        dump_csv(output / name, content)
    summary = {'etapa': 'H2B2A7-FASE-3B', 'estado': 'DESCRIPTIVO_POST_APERTURA',
               'fuente_3a': str(folder3a.relative_to(root)).replace('\\', '/'),
               'fuente_scores_outer': str(f0.relative_to(root)).replace('\\', '/'),
               'fuente_scores_student': str(f1.relative_to(root)).replace('\\', '/'),
               'n_pares': 7, 'n_outer': len(outer),
               'n_inner_por_student': len(students['STUDENT_1E']),
               'n_bootstrap': a.bootstrap, 'seed': a.seed,
               'auc_out': {r['modelo']: r['auc_recalculada_retro'] for r in auc_rows},
               'limitaciones': [
                   'OUTER HOLD previamente abierto: análisis retrospectivo, NO evidencia de generalización nueva',
                   'Intervalos bootstrap condicionales a la muestra, sin corrección por selección/modelado previos',
                   'INNER VAL sin etiquetas en CSV Student: NO se recalculó AUC ni su incertidumbre',
                   'No se infirió identidad entre TEACHER_S3_REFERENCIA_OUTER y TEACHER_R3',
                   'Errores absolutos entre scores requieren cautela por sus escalas',
                   'NO se entrenaron modelos, usaron OUTER para selección, ni ejecutaron QPU'
               ]}
    (output / '3B_DIAGNOSTICO.json').write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding='utf-8')
    md = ['# H2B2A7 Fase 3B — comparación descriptiva pareada', '',
          'Analiza 7 pares identificados en 3A: 6 sobre OUTER HOLD archivado y 1 sobre INNER VAL.',
          'Verifica SHA-256 de 3A, INTEGRACIÓN-00 e INTEGRACIÓN-01 antes de calcular.', '',
          '## Regla de interpretación',
          '- OUTER HOLD estaba **abierto**: estadísticas y bootstrap son **retrospectivos**. No son validación independiente nueva.',
          '- Bootstrap pareado y estratificado por etiqueta en OUTER: percentiles 2.5/97.5 de la diferencia AUC condicionados a las muestras observadas.',
          '- INNER VAL Student no contiene etiquetas en los archivos fuente: NO se recalcula AUC.',
          '- TEACHER_S3_REFERENCIA_OUTER no equivale automáticamente al Teacher R3 completo.',
          '- Correlaciones de ranking pueden ser altas aunque cambie la escala/calibración de los scores.',
          '- Sin cambios en checkpoints, notebooks o informes previos; sin QPU ni entrenamiento.', '',
          '## Valores retrospectivos OUTER', '',
          '| Modelo | AUC recalculada (descriptiva) |', '|---|---:|']
    for r in auc_rows:
        md.append(f"| {r['modelo']} | {r['auc_recalculada_retro']:.8f} |")
    md += ['', '## Archivos', '- 3B_COMPARACION_PAREADA.csv: correlaciones, diferencias, y cambios AUC solo donde hay etiquetas.',
           '- 3B_AUC_OUTER_RETROSPECTIVAS.csv: AUC descriptivas de cuatro vectores OUTER.',
           '- 3B_DIAGNOSTICO.json: procedencia y reservas.',
           '- 3B_MANIFIESTO_SHA256.json: hash de los tres productos y de este informe.', '']
    (output / '3B_INFORME.md').write_text('\n'.join(md), encoding='utf-8')
    products = {x.name: digest(x) for x in sorted(output.iterdir()) if x.is_file()}
    (output / '3B_MANIFIESTO_SHA256.json').write_text(json.dumps({'etapa': 'H2B2A7-FASE-3B', 'productos_sha256': products, 'nota': 'El manifiesto no se autocertifica'}, ensure_ascii=False, indent=2), encoding='utf-8')
    print('ANÁLISIS 3B GENERADO:', output)
    print('Archivos: 5 | Pares: 7 | AUC Student: NO recalculadas')
    print('NO seleccionar/refinar modelos con resultados del OUTER ya abierto.')

if __name__ == '__main__':
    try:
        main()
    except Exception as exc:
        import sys
        print(f'ERROR: {type(exc).__name__}: {exc}', file=sys.stderr)
        raise SystemExit(1)
