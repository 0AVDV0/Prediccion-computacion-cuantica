#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""H2B2A7: verifica PSI7_ALL_3S.npy vs CACHE_PSI7_ALL_3S.npz y splits.

Solo lectura de NPY/NPZ no pickle; NO ejecuta notebooks, NO usa etiquetas,
NO modifica estados, NO entrena y NO exporta muestras individuales.
Se ejecuta como: python AUDITAR_CACHE_Y_SPLITS_PSI7_3S_SOLO_LECTURA.py --help
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import sys
from tempfile import TemporaryDirectory

import numpy as np

EXPECTED_DF_ROWS = 10691
EXPECTED_TRAIN_ROWS = 7483
EXPECTED_DIM = 128


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open('rb') as f:
        for b in iter(lambda: f.read(1024 * 1024), b''):
            h.update(b)
    return h.hexdigest()


def validate_indices(x, key: str, n_total: int):
    arr = np.asarray(x)
    if arr.ndim != 1 or not np.issubdtype(arr.dtype, np.integer):
        raise ValueError(f'{key}: se esperaba vector 1D de enteros')
    if len(np.unique(arr)) != len(arr):
        raise ValueError(f'{key}: hay indices repetidos')
    if len(arr) and (arr.min() < 0 or arr.max() >= n_total):
        raise ValueError(f'{key}: indices fuera de [0,{n_total})')
    return arr


def load_cache(path: Path, target_shape):
    preferred = ('PSI7_ALL_3S', 'PSI7_ALL', 'psi7_all_3s', 'psi7')
    with np.load(path, allow_pickle=False) as z:
        keys = list(z.files)
        candidates = [k for k in preferred if k in keys]
        if len(candidates) > 1:
            raise ValueError(f'Cache ambiguo: varias claves esperadas {candidates}')
        if candidates:
            key = candidates[0]
            data = np.asarray(z[key])
        else:
            compatible = []
            for k in keys:
                data_k = np.asarray(z[k])
                if data_k.shape == target_shape and np.issubdtype(data_k.dtype, np.complexfloating):
                    compatible.append(k)
            if len(compatible) != 1:
                raise ValueError(f'No existe clave unica de estados complejos {target_shape}. Claves: {keys}, candidatos: {compatible}')
            key = compatible[0]
            data = np.asarray(z[key])
    return key, data, keys


def audit(psi_path: Path, cache_path: Path, splits_path: Path,
          n_train: int = EXPECTED_TRAIN_ROWS, n_total: int = EXPECTED_DF_ROWS):
    for p in (psi_path, cache_path, splits_path):
        if not p.is_file():
            raise FileNotFoundError(p)
    psi = np.load(psi_path, allow_pickle=False)
    if psi.shape != (n_train, EXPECTED_DIM) or not np.issubdtype(psi.dtype, np.complexfloating):
        raise ValueError(f'PSI7 .npy inesperado: forma={psi.shape}, dtype={psi.dtype}')
    cache_key, cache, cache_keys = load_cache(cache_path, psi.shape)
    if cache.shape != psi.shape or not np.issubdtype(cache.dtype, np.complexfloating):
        raise ValueError(f'Cache PSI7 inesperado: forma={cache.shape}, dtype={cache.dtype}')
    dif = np.abs(psi.astype(np.complex128) - cache.astype(np.complex128))
    err_row = np.max(dif, axis=1)
    exact = int(np.count_nonzero(err_row == 0))
    within_tol = int(np.count_nonzero(err_row <= 1e-6))
    if not (np.isfinite(psi).all() and np.isfinite(cache).all()):
        raise ValueError('Existen estados no finitos')
    with np.load(splits_path, allow_pickle=False) as z:
        keys = list(z.files)
        splits = {}
        for name in ('idx_train', 'idx_val', 'idx_test'):
            if name in keys:
                splits[name] = validate_indices(z[name], name, n_total)
    if 'idx_train' not in splits:
        raise ValueError('Falta idx_train en archivo de splits')
    if len(splits['idx_train']) != n_train:
        raise ValueError(f'idx_train: se esperaban {n_train} muestras, hay {len(splits["idx_train"])}')
    split_sizes = {k: int(len(v)) for k,v in splits.items()}
    intersections = {}
    names = list(splits)
    for i, left in enumerate(names):
        for right in names[i+1:]:
            intersections[f'{left}_x_{right}'] = int(np.intersect1d(splits[left],splits[right]).size)
    all_inds = np.concatenate(list(splits.values()))
    total_unique = int(len(np.unique(all_inds)))
    complete = bool(len(splits) == 3 and total_unique == n_total and
                    all(x == 0 for x in intersections.values()))
    return {
        'tipo': 'auditoria_cache_psi7_y_particiones_solo_lectura',
        'archivos': {p.name:sha256(p) for p in (psi_path,cache_path,splits_path)},
        'psi7_archivado': {'forma': list(map(int,psi.shape)), 'dtype': str(psi.dtype)},
        'cache': {'clave_usada':cache_key,'claves_en_npz':cache_keys,'forma':list(map(int,cache.shape)),'dtype':str(cache.dtype)},
        'comparacion_cache': {
            'n_filas_iguales_exactamente':exact,
            'n_filas_error_max_le_1e-6':within_tol,
            'error_max_amplitud':float(np.max(dif)),
            'error_rms_amplitud':float(np.sqrt(np.mean(dif**2))),
            'igualdad_exacta_de_valores':bool(np.array_equal(psi, cache)),
            'norma2_desviacion_max_psi7':float(np.max(np.abs(np.sum(np.abs(psi)**2,axis=1)-1))),
            'norma2_desviacion_max_cache':float(np.max(np.abs(np.sum(np.abs(cache)**2,axis=1)-1))),
        },
        'splits': {
            'claves_en_npz': keys,
            'tamanos':split_sizes,
            'intersecciones':intersections,
            'indices_unicos_total':total_unique,
            'n_filas_df_esperadas':n_total,
            'particion_total_disjunta_y_completa':complete,
        },
        'conclusion': 'cache_exacto' if exact == n_train else (
            'cache_coincide_a_1e-6' if within_tol == n_train else 'cache_discrepante'),
        'limitaciones': [
            'No se valida fecha de generacion ni origen historico de cada artefacto.',
            'La coincidencia entre cache y PSI7 no prueba etiquetas ni alineacion con C_ALL_3P/Y_ALL_3P.',
            'No se comprueba construccion de matrices reducidas rho6/rho4.',
            'No se exportan indices, composiciones, etiquetas, nombres ni estados individuales.',
            'Se cargan solo NPZ/NPY con allow_pickle=False.'
        ]
    }


def self_test():
    with TemporaryDirectory() as dirname:
        root=Path(dirname)
        vals=np.zeros((4,128),dtype=np.complex64)
        vals[:,0]=1+0j
        ref=root/'PSI7_ALL_3S.npy'
        cac=root/'CACHE_PSI7_ALL_3S.npz'
        spl=root/'transfer_splits_A4_AQ4.npz'
        np.save(ref,vals)
        np.savez_compressed(cac,PSI7_ALL_3S=vals, metadata=np.array([1]))
        np.savez_compressed(spl,idx_train=np.array([3,0,4,2]),idx_val=np.array([1]),idx_test=np.array([5]))
        result=audit(ref,cac,spl,n_train=4,n_total=6)
        assert result['comparacion_cache']['n_filas_iguales_exactamente']==4
        assert result['splits']['particion_total_disjunta_y_completa']
        np.savez_compressed(cac,PSI7_ALL_3S=(vals+np.complex64(.001)))
        result_bad=audit(ref,cac,spl,n_train=4,n_total=6)
        assert result_bad['conclusion']=='cache_discrepante'
        np.savez_compressed(spl,idx_train=np.array([3,0,4,2]),idx_val=np.array([3]),idx_test=np.array([5]))
        result_overlap=audit(ref,cac,spl,n_train=4,n_total=6)
        assert not result_overlap['splits']['particion_total_disjunta_y_completa']
        assert result_overlap['splits']['intersecciones']['idx_train_x_idx_val']==1
    print('SELF-TEST PASS | cache exacto, discrepancia detectable, splits y solapamientos')


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--self-test',action='store_true')
    ap.add_argument('--psi7',help='Ruta a PSI7_ALL_3S.npy')
    ap.add_argument('--cache',help='Ruta a CACHE_PSI7_ALL_3S.npz')
    ap.add_argument('--splits',help='Ruta a transfer_splits_A4_AQ4.npz')
    ap.add_argument('--out',help='JSON de salida nueva (no sobrescribe)')
    args=ap.parse_args()
    if args.self_test:
        self_test();return
    if not all((args.psi7,args.cache,args.splits,args.out)):
        ap.error('Se requieren --psi7 --cache --splits --out')
    out=Path(args.out)
    if out.exists():
        raise FileExistsError(f'No se sobrescribe {out}')
    data=audit(Path(args.psi7),Path(args.cache),Path(args.splits))
    out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    print('AUDITORIA COMPLETADA |',data['conclusion'])
    print('Cache exacto:',data['comparacion_cache']['n_filas_iguales_exactamente'],'/',EXPECTED_TRAIN_ROWS)
    print('Split disjunto y completo:',data['splits']['particion_total_disjunta_y_completa'])
    print('Reporte:',out)

if __name__=='__main__':
    try:main()
    except Exception as e:
        print(f'{type(e).__name__}: {e}',file=sys.stderr)
        sys.exit(1)
