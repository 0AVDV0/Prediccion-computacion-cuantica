#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""H2B2A7 FASE 3A: inventario verificable, solo usa evidencia incluida en Git.

Por defecto no escribe nada. --write crea un NUEVO informe en reports/H2B2A7_CONSOLIDACION.
No utiliza Tesis4, NumPy, Qiskit, redes, IBM Quantum ni reentrena modelos.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
from collections import Counter
from datetime import datetime, timezone
from itertools import combinations
from pathlib import Path

ROOT0 = Path('reports/H2B2A7_INTEGRACION_00/H2B2A7_INTEGRACION_00_AUDITORIA_DOS_RUTAS_20261110T232931050887Z')
ROOT1 = Path('reports/H2B2A7_INTEGRACION_01/H2B2A7_INTEGRACION_01_CERT_20261111T221029053812Z')
OUT_BASE = Path('reports/H2B2A7_CONSOLIDACION')
SCORES0 = 'INTEGRACION00_SCORES_OUTER_REPLAY_ARCHIVADO.csv'
SCORES1 = 'INTEGRACION01_SCORES_INNER_VAL_RECONSTRUIDOS.csv'
CODE0 = ('experiments/INTEGRACION_00.ipynb', '350bc3d092f1c2098a28fdf7c05f5f92b1e6004f6a9b692afe9a149ecdff7ca9')
CODE1 = ('experiments/INTEGRACION_01_CERT.ipynb', '089415d27e535700d5de2d56e78d4f255edc2c718d57141be125bd30ef9556d8')


def sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    with p.open('rb') as f:
        for data in iter(lambda: f.read(1024 * 1024), b''):
            h.update(data)
    return h.hexdigest()


def read_json(p: Path):
    return json.loads(p.read_text(encoding='utf-8-sig'))


def read_csv(p: Path):
    with p.open('r', encoding='utf-8-sig', newline='') as f:
        reader = csv.DictReader(f)
        if reader.fieldnames is None:
            raise ValueError(f'CSV vacío: {p}')
        return reader.fieldnames, list(reader)


def verify_manifest(folder: Path, filename: str, field: str) -> int:
    manifest = read_json(folder / filename)
    expected = manifest[field]
    if not isinstance(expected, dict) or not expected:
        raise ValueError(f'Manifiesto sin hashes: {filename}')
    for name, expected_hash in expected.items():
        if not name or Path(name).name != name:
            raise ValueError(f'Nombre inseguro en manifiesto: {name!r}')
        p = folder / name
        if not p.is_file() or sha256_file(p).lower() != str(expected_hash).lower():
            raise ValueError(f'Archivo ausente o hash diferente: {p}')
    return len(expected)


def verify_code(repo: Path, relative: str, expected_hash: str) -> None:
    notebook = read_json(repo / relative)
    cells = notebook.get('cells', [])
    if len(cells) != 1 or cells[0].get('cell_type') != 'code':
        raise ValueError(f'Notebook inesperado: {relative}')
    digest = hashlib.sha256(''.join(cells[0]['source']).encode('utf-8')).hexdigest()
    if digest != expected_hash:
        raise ValueError(f'Código de celda modificado: {relative}')


def build_inventory(repo: Path):
    folder0, folder1 = repo / ROOT0, repo / ROOT1
    if not folder0.is_dir() or not folder1.is_dir():
        raise FileNotFoundError('Faltan los informes certificados de INTEGRACIÓN-00 o INTEGRACIÓN-01.')
    hashes0 = verify_manifest(folder0, 'INTEGRACION00_HUELLAS_SHA256.json', 'productos_sha256')
    hashes1 = verify_manifest(folder1, 'INTEGRACION01_HUELLAS_SHA256.json', 'archivos_resultado_sha256')
    verify_code(repo, *CODE0)
    verify_code(repo, *CODE1)

    summary0 = read_json(folder0 / 'INTEGRACION00_RESUMEN.json')
    summary1 = read_json(folder1 / 'INTEGRACION01_RESUMEN_DECISION.json')
    detail1 = read_json(folder1 / 'INTEGRACION01_DETALLES_MATRICIALES.json')
    assert summary0['out_hold_previamente_abierto'] is True
    assert summary1['outer_hold_NO_evaluado'] is True

    cols0, raw0 = read_csv(folder0 / SCORES0)
    expected_cols0 = {'global_index','y_FM_ARCHIVADA','teacher_s3_archivado_checkpoint',
                      'score_SAFE_ideal_replay','score_QWC24_ideal_replay','score_QWC64_ideal_replay',
                      'score_SAFE_ideal_archivado','score_QWC24_ideal_archivado','score_QWC64_ideal_archivado'}
    if not expected_cols0.issubset(cols0) or len(raw0) != 1497:
        raise ValueError('Formato o cantidad inesperada del CSV OUTER archivado.')
    outer = {}
    for row in raw0:
        idx = int(row['global_index'])
        if idx in outer:
            raise ValueError(f'Índice OUTER duplicado: {idx}')
        label = int(row['y_FM_ARCHIVADA'])
        if label not in (0, 1):
            raise ValueError(f'Etiqueta OUTER no binaria: {idx}')
        for name in expected_cols0 - {'global_index','y_FM_ARCHIVADA'}:
            if not math.isfinite(float(row[name])):
                raise ValueError(f'Score no finito en OUTER: {name}:{idx}')
        outer[idx] = row

    cols1, raw1 = read_csv(folder1 / SCORES1)
    if not {'modelo','global_index','score','split'}.issubset(cols1):
        raise ValueError('Columnas faltantes en scores de Student.')
    students = {'STUDENT_1E': {}, 'STUDENT_1F': {}}
    for row in raw1:
        model = row['modelo']
        if model not in students or row['split'] != 'INNER_VAL_YA_EXAMINADO':
            raise ValueError(f'Modelo/split inesperado en Student: {model}')
        idx = int(row['global_index'])
        if idx in students[model] or not math.isfinite(float(row['score'])):
            raise ValueError(f'Score Student duplicado/no finito: {model}:{idx}')
        students[model][idx] = float(row['score'])
    if len(raw1) != 2396 or any(len(v) != 1198 for v in students.values()):
        raise ValueError('Cantidad de filas Student inesperada.')
    if set(students['STUDENT_1E']) != set(students['STUDENT_1F']):
        raise ValueError('1E y 1F no tienen los mismos índices de INNER VAL.')
    if summary1.get('fallos') or summary1.get('reservas') or summary1.get('IBM_jobs') != 0:
        raise ValueError('INTEGRACIÓN-01 declara fallos/reservas/jobs inesperados.')

    # Cada registro representa una cobertura documentada, NO un score universal entre splits.
    coverage = []
    for item in summary0['replay']:
        if item['arquitectura'] == 'STUDENT_U_DEC_D':
            continue  # INTEGRACIÓN-00 todavía lo declaraba pendiente; INTEGRACIÓN-01 es la fuente posterior.
        model = item['arquitectura']
        split = item['split']
        rowlevel = split == 'OUTER_HOLD_ARCHIVADO' and model in ('SAFE_ideal','QWC24_ideal','QWC64_ideal')
        coverage.append({
            'modelo': model, 'split': split, 'n_materiales': item['n_materiales'],
            'tipo_evidencia': 'SCORES_INDIVIDUALES' if rowlevel else 'SOLO_RESUMEN',
            'archivo_evidencia': str(ROOT0 / (SCORES0 if rowlevel else 'INTEGRACION00_RESUMEN.json')),
            'auc_archivada': '', 'estado': item['estado'],
            'notas': 'OUTER HOLD YA ABIERTO' if rowlevel else 'No hay vector individual en el paquete consolidado'
        })

    coverage.append({
        'modelo': 'TEACHER_S3_REFERENCIA_OUTER', 'split': 'OUTER_HOLD_ARCHIVADO', 'n_materiales': len(outer),
        'tipo_evidencia': 'SCORES_INDIVIDUALES', 'archivo_evidencia': str(ROOT0 / SCORES0),
        'auc_archivada': '', 'estado': 'COLUMNA_ARCHIVADA',
        'notas': 'Columna teacher_s3_archivado_checkpoint; no asumir identidad con TEACHER_R3 sin trazar checkpoint'
    })
    for model in ('STUDENT_1E', 'STUDENT_1F'):
        obj = detail1[model + '_INNER_VAL']
        if int(obj['n']) != 1198 or abs(float(obj['auc_recalculada'])-float(obj['auc_archivada'])) > 1e-12:
            raise ValueError(f'AUC de {model} no coincide con el informe histórico.')
        coverage.append({
            'modelo': model, 'split': 'INNER_VAL_YA_EXAMINADO', 'n_materiales': len(students[model]),
            'tipo_evidencia': 'SCORES_INDIVIDUALES_SIN_ETIQUETAS', 'archivo_evidencia': str(ROOT1 / SCORES1),
            'auc_archivada': obj['auc_archivada'], 'estado': 'PRUEBAS_NUMERICAS_SUPERADAS',
            'notas': 'AUC archivada; sin vector histórico pareado de referencia; QPY 1F no cotejado' if model.endswith('1F') else 'AUC archivada; no hay scores históricos pareados'
        })

    outer_models = ['TEACHER_S3_REFERENCIA_OUTER','SAFE_ideal','QWC24_ideal','QWC64_ideal']
    pairs = []
    for a,b in combinations(outer_models,2):
        pairs.append({
            'modelo_a': a,'modelo_b': b, 'split': 'OUTER_HOLD_ARCHIVADO', 'n_indices_comunes': len(outer),
            'etiquetas_presentes': 'SI', 'comparacion_permitida': 'SOLO_DESCRIPTIVA_POST_APERTURA',
            'aviso': 'No usar este OUTER HOLD ya abierto para ajustar o seleccionar arquitecturas'
        })
    pairs.append({
        'modelo_a': 'STUDENT_1E', 'modelo_b': 'STUDENT_1F', 'split': 'INNER_VAL_YA_EXAMINADO',
        'n_indices_comunes': len(students['STUDENT_1E']), 'etiquetas_presentes': 'NO_EN_ESTE_CSV',
        'comparacion_permitida': 'SCORES_PAREADOS_SIN_AUC_RECALCULADA',
        'aviso': 'Las AUC archivadas proceden de INTEGRACIÓN-01; este CSV no trae etiquetas'
    })

    overlap = len(set(outer) & set(students['STUDENT_1E']))
    diagnostics = {
        'metodologia': 'FASE 3A: inventario de evidencia, no una evaluación adicional',
        'archivos_con_SHA_verificado': {'integracion00': hashes0, 'integracion01': hashes1},
        'codigo_notebooks_sha_verificado': 2,
        'filas_scores_outer': len(raw0), 'filas_scores_student': len(raw1),
        'inner_por_modelo': {m: len(v) for m,v in students.items()},
        'pares_comparables_descriptivamente': len(pairs),
        'interseccion_indices_inner_y_outer': overlap,
        'aviso_cruce': 'Un índice global coincidente no permite mezclar splits; revisar procedencia' if overlap else 'No se encontraron índices comunes en los CSV',
        'etiquetas_en_csv_outer': True, 'etiquetas_en_csv_student': False,
        'limites': [
            'INNER VAL y OUTER HOLD NO son el mismo split, aunque sus métricas puedan tener el mismo nombre',
            'OUTER HOLD ya estaba abierto: cualquier comparación es retrospectiva/descriptiva',
            'HEAD4_SAFE tiene solo resumen en la evidencia disponible, no score individual para comparación pareada',
            'Las AUC Student son históricas, no fueron recalculadas por esta fase de inventario',
            'No se mide costo QPU ni se entrena un modelo',
            'No hay etiquetas de INNER VAL en el CSV Student consolidado',
            'La identidad de Student 1F sigue sin hash histórico anterior ni QPY original cotejado'
        ]
    }
    return coverage, pairs, diagnostics


def csv_bytes(rows):
    import io
    f=io.StringIO(newline='')
    writer=csv.DictWriter(f,fieldnames=list(rows[0].keys()))
    writer.writeheader(); writer.writerows(rows)
    return f.getvalue().encode('utf-8-sig')


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--repo',type=Path,default=Path.cwd(),help='Worktree de consolidación (predeterminado: directorio actual)')
    p.add_argument('--write',action='store_true',help='Escribir un informe nuevo; sin esto solo hace verificaciones')
    a=p.parse_args()
    root=a.repo.resolve(strict=True)
    if not (root/'.git').exists():
        raise RuntimeError(f'No parece un worktree Git: {root}')
    coverage, pairs, diag=build_inventory(root)
    print('H2B2A7 | FASE 3A | INVENTARIO VERIFICADO')
    print(f"Hashes de reportes: {diag['archivos_con_SHA_verificado']['integracion00']}/7 INTEGRACION-00 y {diag['archivos_con_SHA_verificado']['integracion01']}/6 INTEGRACION-01")
    print('Códigos originales: 2/2 SHA256 OK')
    print(f"Coberturas: {len(coverage)} | Pares con scores: {len(pairs)}")
    print(f"OUTER: {diag['filas_scores_outer']} materiales | INNER: {diag['inner_por_modelo']['STUDENT_1E']} por Student")
    print(f"Intersección de índices INNER/OUTER: {diag['interseccion_indices_inner_y_outer']} (NO combinar splits)")
    print('No se han recalculado AUC, entrenado modelos ni ejecutado QPU.')
    if not a.write:
        print('PREFLIGHT OK. No se escribió ningún archivo. Para crear el informe: agrega --write')
        return
    output_root=(root/OUT_BASE).resolve()
    if not output_root.is_relative_to(root):
        raise RuntimeError('Salida fuera del worktree')
    stamp=datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
    dest=output_root/('H2B2A7_3A_INVENTARIO_'+stamp)
    dest.mkdir(parents=True,exist_ok=False)
    results={
        '3A_MATRIZ_COBERTURA.csv':csv_bytes(coverage),
        '3A_PARES_COMPARABLES.csv':csv_bytes(pairs),
        '3A_DIAGNOSTICO.json':(json.dumps(diag,ensure_ascii=False,indent=2)+'\n').encode('utf-8'),
    }
    lines=[
        '# H2B2A7 Fase 3A — Inventario científico',
        '',
        'Este informe SOLO organiza evidencia ya certificada en INTEGRACIÓN-00 e INTEGRACIÓN-01.',
        'No introduce una evaluación independiente nueva ni recalcula AUC.',
        '',
        f"- Integridad: **{diag['archivos_con_SHA_verificado']['integracion00']}/7** y **{diag['archivos_con_SHA_verificado']['integracion01']}/6** hashes de informes correctos.",
        f'- Coberturas: **{len(coverage)}**. Pares con scores bajo un mismo split: **{len(pairs)}**.',
        f"- OUTER HOLD ya examinado: **{diag['filas_scores_outer']}** registros con etiquetas y scores.",
        f"- INNER VAL ya examinado: **{diag['inner_por_modelo']['STUDENT_1E']}** registros por Student, sin etiquetas en este CSV.",
        f"- Coincidencia de índices entre ambos CSV: **{diag['interseccion_indices_inner_y_outer']}**, sin autorización para mezclar splits.",
        '', '## Limitaciones',
        *[f'- {v}' for v in diag['limites']],
        '', '## Archivos',
        '- `3A_MATRIZ_COBERTURA.csv`: disponibilidad de evidencia individual o resumida por modelo/split.',
        '- `3A_PARES_COMPARABLES.csv`: únicamente pares con muestras de la misma partición.',
        '- `3A_DIAGNOSTICO.json`: integridad y conteos.',
        '- `3A_MANIFIESTO_SHA256.json`: huellas de los tres productos anteriores y este informe.',
        '', 'Para futuras etapas: no comparar AUC de INNER VAL frente a AUC de OUTER HOLD como prueba pareada.',
        ''
    ]
    results['3A_INFORME.md']='\n'.join(lines).encode('utf-8')
    for name,blob in results.items():
        (dest/name).write_bytes(blob)
    manifest={'etapa':'H2B2A7-FASE-3A', 'fuentes':['INTEGRACION-00','INTEGRACION-01'],
              'productos_sha256':{name:hashlib.sha256(blob).hexdigest() for name,blob in results.items()},
              'nota':'Manifiesto no se certifica a sí mismo'}
    (dest/'3A_MANIFIESTO_SHA256.json').write_text(json.dumps(manifest,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    print('INFORME GENERADO EN:',dest)
    print('Nuevos archivos: 5. Ninguna evidencia anterior modificada.')

if __name__=='__main__':
    try:
        main()
    except Exception as exc:
        import sys
        print(f'ERROR 3A: {type(exc).__name__}: {exc}',file=sys.stderr)
        raise SystemExit(1)
