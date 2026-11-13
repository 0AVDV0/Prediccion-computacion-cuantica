#!/usr/bin/env python3
# coding: utf-8
"""H2B2A7 3C.4 — auditoría local de recursos conocidos, sin entrenamiento ni QPU.

Ejecutar sin argumentos: preflight sin escritura.
Ejecutar con --write: crea una carpeta NUEVA bajo reports/H2B2A7_CONSOLIDACION.
No necesita NumPy, Qiskit ni los archivos externos de Tesis4.
"""
from __future__ import annotations

import argparse
import ast
import csv
import hashlib
import io
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
R0 = ROOT / 'reports/H2B2A7_INTEGRACION_00/H2B2A7_INTEGRACION_00_AUDITORIA_DOS_RUTAS_20261110T232931050887Z'
R1 = ROOT / 'reports/H2B2A7_INTEGRACION_01/H2B2A7_INTEGRACION_01_CERT_20261111T221029053812Z'
COST_FILE = R0 / 'INTEGRACION00_COSTOS_POR_MATERIAL.csv'
MAN0 = R0 / 'INTEGRACION00_HUELLAS_SHA256.json'
MAN1 = R1 / 'INTEGRACION01_HUELLAS_SHA256.json'
NB = ROOT / 'experiments/INTEGRACION_01_CERT.ipynb'


def sha(path: Path):
    h = hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda: f.read(1 << 20), b''):
            h.update(chunk)
    return h.hexdigest()


def load_json(path: Path):
    return json.loads(path.read_text(encoding='utf-8-sig'))


def read_csv(path: Path):
    with path.open('r', encoding='utf-8-sig', newline='') as f:
        return list(csv.DictReader(f))


def csv_bytes(rows, headers):
    buf = io.StringIO(newline='')
    writer = csv.DictWriter(buf, fieldnames=headers, extrasaction='raise', lineterminator='\n')
    writer.writeheader()
    for row in rows:
        writer.writerow(row)
    return buf.getvalue().encode('utf-8-sig')


def main():
    ap = argparse.ArgumentParser(description='Auditoría H2B2A7 3C.4, sin QPU ni entrenamiento.')
    ap.add_argument('--write', action='store_true', help='Crear un directorio nuevo de informes.')
    args = ap.parse_args()
    for path in [COST_FILE, MAN0, MAN1, NB]:
        if not path.is_file():
            raise SystemExit(f'PREFLIGHT BLOQUEADO: no existe {path}')
    m0, m1 = load_json(MAN0), load_json(MAN1)
    expected_cost = m0['productos_sha256']['INTEGRACION00_COSTOS_POR_MATERIAL.csv']
    cost_sha = sha(COST_FILE)
    if cost_sha != expected_cost:
        raise SystemExit('PREFLIGHT BLOQUEADO: hash de costos INTEGRACION-00 no coincide.')

    nb = load_json(NB)
    codes = [c for c in nb['cells'] if c.get('cell_type') == 'code']
    if len(codes) != 1:
        raise SystemExit(f'PREFLIGHT BLOQUEADO: se esperaban una celda de código y hay {len(codes)}.')
    source = codes[0]['source']
    source = ''.join(source) if isinstance(source, list) else source
    code_sha = hashlib.sha256(source.encode('utf-8')).hexdigest()
    expected_code = m1['codigo_fuente']['sha256_texto_celda']
    if code_sha != expected_code:
        raise SystemExit('PREFLIGHT BLOQUEADO: hash de código Student de INTEGRACION-01 no coincide.')
    tree = ast.parse(source)
    fn = next((node for node in tree.body if isinstance(node, ast.FunctionDef) and node.name == 'qiskit_builder'), None)
    if fn is None:
        raise SystemExit('PREFLIGHT BLOQUEADO: no existe qiskit_builder en la fuente congelada.')
    gate_types = {node.func.attr for node in ast.walk(fn)
                  if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute)
                  and node.func.attr in {'rz', 'ry', 'rxx'}}
    if gate_types != {'rz', 'ry', 'rxx'}:
        raise SystemExit(f'PREFLIGHT BLOQUEADO: puertas inesperadas {gate_types}.')
    if 'MATCHINGS' not in {node.targets[0].id for node in tree.body
                           if isinstance(node, ast.Assign) and len(node.targets) == 1
                           and isinstance(node.targets[0], ast.Name)}:
        raise SystemExit('PREFLIGHT BLOQUEADO: falta MATCHINGS.')
    matches = next(ast.literal_eval(node.value) for node in tree.body if isinstance(node, ast.Assign)
                   and len(node.targets) == 1 and isinstance(node.targets[0], ast.Name)
                   and node.targets[0].id == 'MATCHINGS')
    if len(matches) != 5 or not all(len(pairs) == 3 for pairs in matches):
        raise SystemExit('PREFLIGHT BLOQUEADO: topología MATCHINGS inesperada.')
    if 'a.shape==(2,17,6,2)' not in source or 't.shape==(2,48)' not in source or 'd0.shape==(2,64)' not in source:
        raise SystemExit('PREFLIGHT BLOQUEADO: formas esperadas no halladas en auditoría original.')
    # Los conteos provienen de la construcción congelada de qiskit_builder, NO de transpilation.
    n_heads, n_qubits, n_local_layers, n_ent_layers, ent_pairs_per_layer = 2, 6, 17, 16, 3
    per_head = {'RZ': n_qubits * n_local_layers, 'RY': n_qubits * n_local_layers,
                'RXX': n_ent_layers * ent_pairs_per_layer}
    if per_head['RXX'] != 48:
        raise SystemExit('PREFLIGHT BLOQUEADO: el conteo RXX no coincide con el checkpoint.')

    raw = read_csv(COST_FILE)
    required_routes = {'QWC24_ARCHIVADA', 'QWC64_ARCHIVADA',
                       'PAULI_QWC_COMPLETO_16_REFERENCIA', 'STUDENT_DOS_DECODIFICADORES'}
    if {r['ruta'] for r in raw} != required_routes:
        raise SystemExit('PREFLIGHT BLOQUEADO: rutas inesperadas en INTEGRACION-00.')
    by_name = {r['ruta']: r for r in raw}
    expected = {'QWC24_ARCHIVADA': (24, 10000), 'QWC64_ARCHIVADA': (64, 10000)}
    for route, (bases, shots) in expected.items():
        row = by_name[route]
        if int(row['lecturas_bases']) != bases or int(row['shots_rho6_incrementales']) != shots or row['tipo'] != 'INCREMENTAL_PARCIAL':
            raise SystemExit(f'PREFLIGHT BLOQUEADO: presupuesto {route} no coincide.')
    row_ref = by_name['PAULI_QWC_COMPLETO_16_REFERENCIA']
    if tuple(map(int, [row_ref['lecturas_bases'], row_ref['shots_rho6_incrementales'],
                       row_ref['shots_rho4'], row_ref['shots_totales_plan_logico']])) != (365, 100000, 10000, 110000):
        raise SystemExit('PREFLIGHT BLOQUEADO: presupuesto lógico de referencia cambió.')

    cost_keys = ['ruta', 'tipo', 'lecturas_bases', 'shots_rho6_incrementales', 'shots_rho4',
                 'shots_totales_plan_logico', 'certificacion_alcance', 'advertencia']
    costs = [{k: r.get(k, '') for k in cost_keys} for r in raw]
    for r in costs:
        r['certificacion_alcance'] = ('INCREMENTAL_PARCIAL' if r['ruta'].startswith('QWC24_') or r['ruta'].startswith('QWC64_')
                                     else 'PLAN_LOGICO_REFERENCIA_SIN_QPU' if r['ruta'] == 'PAULI_QWC_COMPLETO_16_REFERENCIA'
                                     else 'DOS_CABEZALES_SIN_COSTO_TOTAL')
    gates = []
    for name, factor in [('DECODIFICADOR_B1', 1), ('DECODIFICADOR_B2', 1), ('SUMA_DOS_DECODIFICADORES', 2)]:
        rz, ry, rxx = (per_head[k] * factor for k in ['RZ', 'RY', 'RXX'])
        gates.append({'componente': name, 'qubits_por_circuito': n_qubits, 'capas_locales_por_circuito': n_local_layers,
                      'rondas_rxx_por_circuito': n_ent_layers, 'puertas_RZ': rz, 'puertas_RY': ry,
                      'puertas_RXX': rxx, 'puertas_logicas_totales': rz + ry + rxx,
                      'valores_diagonal_D': 64 * factor, 'tipo_conteo': 'CIRCUITO_U_SIN_TRANSPILAR',
                      'costo_end_to_end': 'NO_CUANTIFICADO'})
    limitations = [
        'QWC24/QWC64: 10000 shots incrementales sobre rho6, no shots de toda la arquitectura.',
        'QWC365: 110000 shots es un presupuesto logico de referencia, NO tiempo, fidelidad ni costo QPU.',
        'Student: 96 RXX en dos U, NO 96 RXX del modelo integral; faltan preparacion, cuatro cabezales, rho4 y ejecucion fisica.',
        'No hay base suficiente para comparar AUC/costos entre Student INNER y QWC OUTER como un frente de Pareto homogéneo.',
        'No se convierten puertas abstractas en CNOT, profundidad ISA, errores de hardware ni duraciones.',
        'No se ha certificado un costo end-to-end comparable para todos los modelos.'
    ]
    compares = [
        {'comparacion': 'QWC24 vs QWC64', 'permitida': 'SI_PARCIAL', 'metrica': 'bases rho6 y shots incrementales',
         'justificacion': 'Dos presupuestos parciales con 10000 shots incrementales rho6; no equivalen al costo completo.'},
        {'comparacion': 'QWC24 o QWC64 vs QWC365', 'permitida': 'NO_HOMOGENEA', 'metrica': 'ningun costo total directamente comparable',
         'justificacion': 'Los primeros son parciales; QWC365 es presupuesto lógico más completo, sin QPU.'},
        {'comparacion': 'Student 1E vs Student 1F', 'permitida': 'SI_TOPOLOGIA_CONGELADA', 'metrica': 'puertas U y parámetros D',
         'justificacion': 'Misma topología de 2 decodificadores; diferentes valores de ángulos y diagonal.'},
        {'comparacion': 'Student vs QWC', 'permitida': 'NO_END_TO_END', 'metrica': 'ninguna métrica total homogénea certificada',
         'justificacion': 'Student carece de shots y total de cabezales; QWC24/64 son parciales.'}
    ]
    summary = {
        'etapa': 'H2B2A7-3C4', 'estado': 'INVENTARIO_RECURSOS_LOGICOS_SIN_QPU',
        'fuente_costos': str(COST_FILE.relative_to(ROOT)).replace('\\', '/'), 'sha_costos': cost_sha,
        'fuente_circuitos': str(NB.relative_to(ROOT)).replace('\\', '/'), 'sha_codigo_certificado': code_sha,
        'n_heads_student': n_heads, 'qubits_por_decoder': n_qubits,
        'rotaciones_RZ_por_decoder': per_head['RZ'], 'rotaciones_RY_por_decoder': per_head['RY'],
        'entrelazantes_RXX_por_decoder': per_head['RXX'], 'puertas_logicas_U_por_decoder': sum(per_head.values()),
        'RXX_en_dos_decoders': 2 * per_head['RXX'], 'puertas_U_en_dos_decoders': 2 * sum(per_head.values()),
        'shot_incremental_qwc24_qwc64': 10000,
        'bases_qwc24': 24, 'bases_qwc64': 64, 'bases_plan_qwc_ref': 365,
        'shots_logicos_plan_referencia_rho6': 100000,
        'shots_logicos_plan_referencia_rho4': 10000,
        'shots_logicos_plan_referencia_total': 110000,
        'costos_end_to_end_equivalentes': False, 'IBM_jobs': 0, 'QPU_shots_ejecutados': 0,
        'sin_entrenamiento': True, 'limites': limitations
    }
    print('H2B2A7 3C.4 | AUDITORIA DE RECURSOS LOGICOS')
    print('Hashes: informe COSTOS 00 OK; notebook INTEGRACION-01 OK.')
    print('Student: 2 U; cada U 102 RZ + 102 RY + 48 RXX = 252 puertas sin transpilar.')
    print('QWC24/QWC64: 24/64 bases, 10000 shots incrementales rho6 en ambos.')
    print('QWC referencia: 365 bases, 110000 shots logicos de plan (100000 rho6 + 10000 rho4).')
    print('AVISO: ningun costo end-to-end homogenizado; cero QPU y cero entrenamiento.')
    if not args.write:
        print('PREFLIGHT OK. Sin archivos escritos. Para generar inventario: --write')
        return
    payload = {
        '3C4_COSTOS_ARCHIVADOS.csv': csv_bytes(costs, cost_keys),
        '3C4_CIRCUITOS_STUDENT.csv': csv_bytes(gates, list(gates[0])),
        '3C4_COMPARABILIDAD.csv': csv_bytes(compares, list(compares[0])),
        '3C4_RESUMEN.json': (json.dumps(summary, ensure_ascii=False, indent=2) + '\n').encode('utf-8'),
    }
    lines = [
        '# H2B2A7 — 3C.4: auditoría de recursos conocidos', '',
        '## Evidencia',
        '- Se verifican la huella del CSV de costos de INTEGRACIÓN-00 y el SHA del código de INTEGRACIÓN-01.',
        '- Los Student tienen dos decodificadores de 6 qubits, cada uno con 102 RZ, 102 RY y 48 RXX.',
        '- Los 504 operadores de puerta elementales de ambas U no constituyen el circuito integral del modelo.',
        '- QWC24/QWC64: 24/64 bases y 10.000 shots **incrementales/parciales** para rho6.',
        '- QWC365: 365 bases; 100.000 shots rho6 + 10.000 rho4 = 110.000 de presupuesto **lógico de referencia**.',
        '', '## Interpretación',
        'No existe evidencia suficiente para comparar costo total físico de Student frente a QWC ni para afirmar ventaja cuántica.',
        'Los conteos Student no incluyen preparación de estados, otros cuatro cabezales, asignación global de shots, compilación, conectividad ni mitigación de errores.',
        'La reducción de bases o de puertas no implica automáticamente menor tiempo real ni mayor precisión.',
        '', '## Limitaciones',
    ] + ['- ' + x for x in limitations]
    payload['3C4_INFORME.md'] = ('\n'.join(lines) + '\n').encode('utf-8')
    manifest = {'etapa': 'H2B2A7-3C4', 'productos_sha256':
                {name: hashlib.sha256(content).hexdigest() for name, content in payload.items()},
                'nota': 'El manifiesto no incluye su propia huella.'}
    payload['3C4_MANIFIESTO_SHA256.json'] = (json.dumps(manifest, ensure_ascii=False, indent=2) + '\n').encode('utf-8')
    dest = ROOT/'reports'/'H2B2A7_CONSOLIDACION'/('H2B2A7_3C4_RECURSOS_'+datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ'))
    dest.mkdir(parents=True, exist_ok=False)
    for name, content in payload.items():
        (dest/name).write_bytes(content)
    print(f'INFORME GENERADO EN: {dest}')
    print(f'Archivos nuevos: {len(payload)}. Ninguna evidencia anterior modificada.')


if __name__ == '__main__':
    main()
