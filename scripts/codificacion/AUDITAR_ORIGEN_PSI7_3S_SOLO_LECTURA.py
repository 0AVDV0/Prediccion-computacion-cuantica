#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""H2B2A7: comprobacion independiente de la codificacion 3S, SOLO LECTURA.

Fuente historica: ModelosDataset2.ipynb, celda 231 (base cero),
funcion encode_sparse_composition_3s; 84 p_X por orden atomico,
psi_i=sqrt(p_i)*exp(1j*pi*p_i), padding a 128, complex64.

NO ejecuta notebooks, NO recalcula matrices densidad, NO entrena modelos,
NO usa etiquetas de validacion/test, NO identifica muestras en el JSON.
Un .pkl no es seguro si proviene de una fuente desconocida.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import sys

import numpy as np

ELEMENTS_Z_3S = '''H He Li Be B C N O F Ne Na Mg Al Si P S Cl Ar K Ca Sc Ti V Cr Mn Fe Co Ni Cu Zn Ga Ge As Se Br Kr Rb Sr Y Zr Nb Mo Tc Ru Rh Pd Ag Cd In Sn Sb Te I Xe Cs Ba La Ce Pr Nd Pm Sm Eu Gd Tb Dy Ho Er Tm Yb Lu Hf Ta W Re Os Ir Pt Au Hg Tl Pb Bi Po At Rn Fr Ra Ac Th Pa U Np Pu Am Cm Bk Cf Es Fm Md No Lr Rf Db Sg Bh Hs Mt Ds Rg Cn Nh Fl Mc Lv Ts Og'''.split()
EXPECTED_P = 84
EXPECTED_N = 10691
EXPECTED_TRAIN = 7483
EXPECTED_DIM = 128


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open('rb') as f:
        for block in iter(lambda: f.read(1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()


def encode_3s(x):
    x = np.asarray(x, dtype=np.float64)
    rs = np.sum(x, axis=1, keepdims=True)
    if not np.all(np.isfinite(x)) or np.any(rs <= 0):
        raise ValueError('Composicion no finita o suma no positiva')
    xn = x / rs
    amplitude = np.sqrt(xn) * np.exp(1j * np.pi * xn)
    psi = np.zeros((len(xn), EXPECTED_DIM), dtype=np.complex64)
    psi[:, :EXPECTED_P] = amplitude.astype(np.complex64)
    return psi


def test():
    assert len(ELEMENTS_Z_3S) == 118
    x = np.zeros((3, 84), np.float64)
    x[0, :2] = [1, 0]
    x[1, :2] = [1, 1]
    x[2, 5] = 0.25
    x[2, 12] = 0.75
    y = encode_3s(x)
    assert y.shape == (3, 128) and y.dtype == np.complex64
    assert np.max(np.abs(np.sum(np.abs(y) ** 2, axis=1) - 1)) < 3e-7
    assert not np.any(y[:, 84:])
    assert np.allclose(np.abs(y[:, :84])**2, x/x.sum(axis=1,keepdims=True), atol=1e-7)
    assert np.array_equal(y, encode_3s(x.copy()))
    alterado=y.copy();alterado[1,0]+=0.001
    assert np.max(np.abs(y-alterado)) > 1e-5
    print('SELF-TEST PASS | 84 -> 128; fases; normalizacion; padding; corrupcion detectable')


def discover(root: Path):
    wanted = {'df_final.pkl','transfer_splits_A4_AQ4.npz',
              'PSI7_ALL_3S.npy','CACHE_PSI7_ALL_3S.npz'}
    print('Buscar artefactos por nombre, sin abrir datos:')
    found = 0
    for p in sorted(root.rglob('*')):
        if p.is_file() and p.name.lower() in {x.lower() for x in wanted}:
            print(str(p))
            found += 1
    print('Candidatos encontrados:',found)
    if found==0:
        print('No se hallaron rutas. Especifica --df-pkl, --splits y --psi7 manualmente.')


def read_psi(path: Path):
    if path.suffix.lower() == '.npy':
        return np.load(path, allow_pickle=False)
    if path.suffix.lower() == '.npz':
        with np.load(path, allow_pickle=False) as z:
            keys=['PSI7_ALL_3S','PSI7_ALL','psi7_all_3s','psi7']
            found = [k for k in keys if k in z.files]
            if len(found)!=1:
                raise ValueError('NPZ: no se pudo determinar una clave unica de PSI7. Claves: '+repr(z.files))
            return np.asarray(z[found[0]])
    raise ValueError('PSI7 debe ser .npy o .npz')


def run(args):
    if not args.confio_en_este_pickle_local:
        raise ValueError('Para leer el .pkl local se requiere --confio-en-este-pickle-local; no uses pickles desconocidos')
    import pandas as pd
    paths = [Path(args.df_pkl), Path(args.splits), Path(args.psi7)]
    for p in paths:
        if not p.is_file():
            raise FileNotFoundError(str(p))
    df = pd.read_pickle(paths[0])
    if not isinstance(df, pd.DataFrame):
        raise TypeError('El .pkl no contiene un DataFrame de pandas')
    if len(df) != EXPECTED_N:
        raise ValueError(f'Se esperaban {EXPECTED_N} filas, hay {len(df)}')
    pcols=[f'p_{el}' for el in ELEMENTS_Z_3S if f'p_{el}' in df.columns]
    pcols += [c for c in df.columns if str(c).startswith('p_') and c not in pcols]
    if len(pcols)!=EXPECTED_P:
        raise ValueError(f'Se esperaban 84 columnas p_X, hay {len(pcols)}')
    with np.load(paths[1], allow_pickle=False) as split:
        if 'idx_train' not in split.files:
            raise ValueError('El archivo de splits no incluye idx_train')
        inds=np.asarray(split['idx_train'])
    if inds.ndim != 1 or len(inds)!=EXPECTED_TRAIN:
        raise ValueError('idx_train tiene forma incorrecta')
    if not np.issubdtype(inds.dtype,np.integer):
        raise TypeError('idx_train no contiene indices enteros')
    if len(np.unique(inds))!=len(inds) or np.min(inds)<0 or np.max(inds)>=len(df):
        raise ValueError('idx_train duplicados o fuera de rango')
    arr=df.iloc[inds][pcols].replace([np.inf,-np.inf],np.nan).fillna(0.0).to_numpy(dtype=np.float64)
    arr=np.clip(arr,0.0,None)
    row_sum=np.sum(arr,axis=1)
    if np.any(row_sum<=0):
        raise ValueError('Filas con composicion de suma cero')
    x=arr/row_sum[:,None]
    reconstruidos=encode_3s(x)
    archivados=np.asarray(read_psi(paths[2]))
    if archivados.shape != (EXPECTED_TRAIN,EXPECTED_DIM):
        raise ValueError(f'Forma archivada inesperada: {archivados.shape}')
    if not np.issubdtype(archivados.dtype,np.complexfloating):
        raise TypeError('Los estados archivados no son complejos')
    diff=np.abs(reconstruidos.astype(np.complex128)-archivados.astype(np.complex128))
    row_error=diff.max(axis=1)
    ref_rho=np.sum(np.abs(archivados)**2,axis=1)
    calc_rho=np.sum(np.abs(reconstruidos)**2,axis=1)
    exactas=int(np.count_nonzero(row_error==0))
    tol_1e6=int(np.count_nonzero(row_error<=1e-6))
    salida={
        'tipo':'auditoria_independiente_estado_3S_solo_lectura',
        'codificacion':'sqrt(p_i)*exp(i*pi*p_i); posiciones 0..83; 84..127=0',
        'origen_codigo':'ModelosDataset2.ipynb celda 231 (base cero), funcion encode_sparse_composition_3s',
        'n_filas_df':int(len(df)),
        'n_train':int(len(inds)),
        'n_fracciones':int(len(pcols)),
        'forma_estados_archivados':list(map(int,archivados.shape)),
        'dtype_estados_archivados':str(archivados.dtype),
        'n_filas_iguales_exactamente_en_valor':exactas,
        'n_filas_con_error_maximo_le_1e-6':tol_1e6,
        'diferencia_maxima_amplitud':float(np.max(diff)),
        'diferencia_rms_amplitud':float(np.sqrt(np.mean(diff**2))),
        'norma2_max_desviacion_archivados':float(np.max(np.abs(ref_rho-1))),
        'norma2_max_desviacion_reconstruidos':float(np.max(np.abs(calc_rho-1))),
        'max_amplitud_fuera_84_archivados':float(np.max(np.abs(archivados[:,84:]))),
        'hashes_sha256':{p.name:sha256(p) for p in paths},
        'conclusion_numerica': 'coincidencia_a_1e-6' if tol_1e6==len(inds) else 'discrepancia_numerica',
        'limites':[
            'Coincidencia numerica no prueba por si sola procedencia historica o fecha de creacion',
            'No se verifican las etiquetas ni la correspondencia con C_ALL_3P/Y_ALL_3P',
            'No se comprueba la construccion de matrices rho6/rho4 ni su alineacion',
            'No se ejecutan experimentos ni se consulta validacion/test',
            'No se exportan filas, nombres quimicos ni estados individuales'
        ]
    }
    out=Path(args.out)
    out.parent.mkdir(parents=True,exist_ok=True)
    if out.exists():
        raise FileExistsError('No se sobrescribe un informe existente: '+str(out))
    out.write_text(json.dumps(salida,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    print('AUDITORIA COMPLETADA | '+salida['conclusion_numerica'])
    print('Reconstruidos:',len(reconstruidos),'| err max:',salida['diferencia_maxima_amplitud'])
    print('Reporte:',out)


def main():
    ap=argparse.ArgumentParser(description=__doc__,formatter_class=argparse.RawTextHelpFormatter)
    ap.add_argument('--self-test',action='store_true')
    ap.add_argument('--buscar-en',help='Ruta raiz para localizar posibles artefactos, sin abrir archivos')
    ap.add_argument('--df-pkl')
    ap.add_argument('--splits')
    ap.add_argument('--psi7')
    ap.add_argument('--confio-en-este-pickle-local',action='store_true')
    ap.add_argument('--out')
    args=ap.parse_args()
    if args.self_test:
        test();return
    if args.buscar_en:
        discover(Path(args.buscar_en));return
    if not all((args.df_pkl,args.splits,args.psi7,args.out)):
        ap.error('Para auditar proporciona --df-pkl --splits --psi7 --out')
    run(args)

if __name__=='__main__':
    try: main()
    except Exception as e:
        print(type(e).__name__+': '+str(e),file=sys.stderr)
        sys.exit(1)
