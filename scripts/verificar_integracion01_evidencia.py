#!/usr/bin/env python3
"""Valida sin escrituras los seis informes, su SHA-256 y consistencia estructural."""
from __future__ import annotations
import argparse, csv, hashlib, json, math, sys
from collections import Counter
from pathlib import Path

DEFAULT_REPORT = Path('reports/H2B2A7_INTEGRACION_01/H2B2A7_INTEGRACION_01_CERT_20261111T221029053812Z')
SOURCE_HASH = '089415d27e535700d5de2d56e78d4f255edc2c718d57141be125bd30ef9556d8'

def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open('rb') as f:
        for block in iter(lambda: f.read(1024*1024), b''):
            h.update(block)
    return h.hexdigest()

def main() -> int:
    pa = argparse.ArgumentParser(description=__doc__)
    pa.add_argument('--worktree', type=Path, default=Path.cwd())
    pa.add_argument('--report', type=Path, default=DEFAULT_REPORT, help='Directorio de evidencias relativo al worktree o absoluto')
    a = pa.parse_args()
    root=a.worktree.resolve(strict=True)
    report=(root/a.report).resolve(strict=True)
    if report != root and not report.is_relative_to(root):
        raise ValueError('Solo se admiten informes dentro del worktree.')
    manifest=json.loads((report/'INTEGRACION01_HUELLAS_SHA256.json').read_text(encoding='utf-8'))
    declared=manifest['archivos_resultado_sha256']
    if len(declared)!=6:
        raise ValueError(f'Se esperaban seis archivos, se declararon {len(declared)}.')
    for name,expected in declared.items():
        if Path(name).name != name:
            raise ValueError('Ruta no permitida en manifest: '+name)
        p=report/name
        if not p.is_file():
            raise FileNotFoundError(p)
        actual=sha256(p)
        if actual.lower()!=expected.lower():
            raise ValueError(f'SHA256 distinto en {name}: {actual}')
    code= json.loads((root/'experiments/INTEGRACION_01_CERT.ipynb').read_text(encoding='utf-8'))
    cells=code['cells']
    if len(cells)!=1 or cells[0]['cell_type']!='code':
        raise ValueError('Notebook de origen inesperado.')
    h=hashlib.sha256(''.join(cells[0]['source']).encode('utf-8')).hexdigest()
    if h!=SOURCE_HASH:
        raise ValueError('El SHA del código de INTEGRACIÓN-01 ya no coincide.')
    with (report/'INTEGRACION01_PRUEBAS_DE_CERTIFICACION.csv').open('r',encoding='utf-8-sig',newline='') as f:
        pruebas=list(csv.DictReader(f))
    if len(pruebas)!=94 or any(p['estado']!='PASS' for p in pruebas):
        raise ValueError('El CSV no contiene 94/94 PASS.')
    with (report/'INTEGRACION01_SCORES_INNER_VAL_RECONSTRUIDOS.csv').open('r',encoding='utf-8-sig',newline='') as f:
        scores=list(csv.DictReader(f))
    bymodel={m:set() for m in ('STUDENT_1E','STUDENT_1F')}
    counts=Counter()
    for r in scores:
        m=r['modelo']
        if m not in bymodel:
            raise ValueError('Modelo inesperado: '+m)
        if r['split']!='INNER_VAL_YA_EXAMINADO':
            raise ValueError('Split inesperado: '+r['split'])
        index=int(r['global_index'])
        if index in bymodel[m] or not math.isfinite(float(r['score'])):
            raise ValueError('Duplicado o score no finito: '+m)
        bymodel[m].add(index)
        counts[m]+=1
    if counts!={'STUDENT_1E':1198,'STUDENT_1F':1198} or bymodel['STUDENT_1E']!=bymodel['STUDENT_1F']:
        raise ValueError('Los dos modelos no cubren exactamente las mismas 1198 muestras.')
    summary=json.loads((report/'INTEGRACION01_RESUMEN_DECISION.json').read_text(encoding='utf-8'))
    if summary['fallos'] or summary['reservas'] or not summary['outer_hold_NO_evaluado'] or summary['IBM_jobs']!=0 or summary['QPU_shots']!=0:
        raise ValueError('La decisión no confirma la auditoría local sin fallos/OUTER/QPU.')
    details=json.loads((report/'INTEGRACION01_DETALLES_MATRICIALES.json').read_text(encoding='utf-8'))
    for key in ('STUDENT_1E_INNER_VAL','STUDENT_1F_INNER_VAL'):
        obj=details[key]
        if obj['n']!=1198 or abs(obj['auc_recalculada']-obj['auc_archivada'])>1e-12:
            raise ValueError('Error en la comparación AUC: '+key)
    print('VERIFICACION OK | 6/6 SHA256 | 94/94 PASS | 2396 scores de INNER VAL')
    print('Notebook: SHA-256 del texto de la celda coincidente.')
    print('1E AUC:',details['STUDENT_1E_INNER_VAL']['auc_recalculada'])
    print('1F AUC:',details['STUDENT_1F_INNER_VAL']['auc_recalculada'])
    print('Sin escrituras, sin entrenamiento, sin QPU, sin OUTER HOLD nuevo.')
    return 0

if __name__=='__main__':
    try:
        raise SystemExit(main())
    except Exception as ex:
        print('ERROR DE VERIFICACION:',ex,file=sys.stderr)
        raise SystemExit(1)
