#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""H2B2A7 FASE 3C.3: ranking retrospectivo INNER VAL, sin reentrenamiento ni QPU.

Solo lee el informe 3C.1/3C.2 local y valida sus SHA-256 antes de usarlo.
Sin argumentos valida sin escribir. Con --write produce seis nuevos archivos.
Se ejecuta desde cualquier directorio (raiz del repositorio = padre de scripts/).
"""
from __future__ import annotations
import argparse
import csv
from datetime import datetime, timezone
import hashlib
import json
import math
from pathlib import Path

REQUIRED = ("3C_ERRORES_POR_MATERIAL.csv", "3C_INFORME.md", "3C_NORMAS_OPERADORES.csv", "3C_RESUMEN.json")
MODELS = ("STUDENT_1E", "STUDENT_1F")
N_EXPECTED = 1198
SPLIT = "INNER_VAL_YA_EXAMINADO"
ROOT = Path(__file__).resolve().parents[1]
REPORTS = ROOT / 'reports' / 'H2B2A7_CONSOLIDACION'
COLS = ('modelo', 'split', 'global_index', 'score_objetivo_B', 'score_student_recalculado',
        'delta_score', 'peso_score_B1', 'peso_score_B2', 'delta_expectativa_B1',
        'delta_expectativa_B2', 'error_abs_expectativa_B1', 'error_abs_expectativa_B2')


def sha256(p: Path) -> str:
    h = hashlib.sha256()
    with p.open('rb') as stream:
        for b in iter(lambda: stream.read(1 << 20), b''):
            h.update(b)
    return h.hexdigest()


def fail_if(condition: bool, reason: str):
    if condition:
        raise ValueError(reason)


def resolve_source(requested: str | None) -> Path:
    if requested:
        p = Path(requested).resolve()
    else:
        candidates = sorted(p for p in REPORTS.glob('H2B2A7_3C_OBSERVABLES_*') if p.is_dir())
        fail_if(not candidates, f'No hay carpetas 3C en {REPORTS}.')
        fail_if(len(candidates) != 1, 'Hay multiples ejecuciones 3C: especifica --source-3c con la ruta correcta.')
        p = candidates[0]
    fail_if(not p.is_dir(), f'No existe carpeta 3C: {p}')
    return p


def load_verified(p: Path):
    manifest_path = p / '3C_MANIFIESTO_SHA256.json'
    fail_if(not manifest_path.is_file(), 'No existe manifiesto 3C.')
    manifest = json.loads(manifest_path.read_text(encoding='utf-8-sig'))
    products = manifest.get('productos_sha256', {})
    fail_if(set(products) != set(REQUIRED), 'El manifiesto 3C no enumera exactamente los 4 productos esperados.')
    for filename in REQUIRED:
        q = p / filename
        fail_if(not q.is_file(), f'Falta evidencia 3C: {filename}')
        fail_if(sha256(q) != products[filename], f'Fallo de integridad SHA-256: {filename}')
    summary = json.loads((p/'3C_RESUMEN.json').read_text(encoding='utf-8-sig'))
    fail_if(summary.get('n_materiales') != N_EXPECTED or summary.get('n_filas') != 2*N_EXPECTED,
            'Resumen 3C con conteos inesperados.')
    with (p / '3C_ERRORES_POR_MATERIAL.csv').open(newline='', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        fail_if(not set(COLS).issubset(reader.fieldnames or []), 'Faltan columnas requeridas en CSV 3C.')
        data = {m:{} for m in MODELS}
        count=0
        for row in reader:
            count+=1
            name=row['modelo']
            fail_if(name not in MODELS, f'Modelo inesperado {name}')
            fail_if(row['split'] != SPLIT, f'Split ajeno al INNER VAL esperado: {row["split"]}')
            ind=int(row['global_index'])
            fail_if(ind in data[name], f'Indice repetido en {name}: {ind}')
            values={k:float(row[k]) for k in COLS[3:]}
            fail_if(any(not math.isfinite(v) for v in values.values()), 'Valor no finito en scores 3C')
            a,b,d=values['score_objetivo_B'],values['score_student_recalculado'],values['delta_score']
            fail_if(abs((b-a)-d)>1e-10,f'Score no coincide con delta: {name}, {ind}')
            decomposition=(values['peso_score_B1']*values['delta_expectativa_B1']
                           +values['peso_score_B2']*values['delta_expectativa_B2'])
            fail_if(abs(decomposition-d)>1e-10, f'Descomposicion fisica incompatible en {name}, {ind}')
            data[name][ind]=values
    fail_if(count != 2*N_EXPECTED or any(len(data[m])!=N_EXPECTED for m in MODELS), 'Conteo 3C no esperado.')
    ids=sorted(data[MODELS[0]])
    fail_if(set(ids)!=set(data[MODELS[1]]), 'Los dos Students no tienen los mismos indices.')
    fail_if(any(abs(data['STUDENT_1E'][i]['score_objetivo_B']-data['STUDENT_1F'][i]['score_objetivo_B'])>1e-12 for i in ids),
            'Los scores objetivo no coinciden entre Student 1E/1F.')
    return data, ids, summary


def avg_ranks_high(values):
    n=len(values); order=sorted(range(n),key=lambda i:(-values[i],i))
    ranks=[0.]*n; i=0
    while i<n:
        j=i+1
        while j<n and values[order[j]] == values[order[i]]: j+=1
        r=(i+1+j)/2
        for k in range(i,j): ranks[order[k]]=r
        i=j
    return ranks


def pearson(a,b):
    n=len(a); ma=sum(a)/n; mb=sum(b)/n
    va=sum((x-ma)**2 for x in a); vb=sum((x-mb)**2 for x in b)
    return sum((x-ma)*(y-mb) for x,y in zip(a,b))/math.sqrt(va*vb) if va*vb>0 else float('nan')


def pair_report(a,b,errors=None):
    """Count exact Kendall tau-b and inversions among n(n-1)/2 unordered pairs."""
    n=len(a);con=dis=tie_a=tie_b=tie_both=0
    safe=0;unsafe=0; margin_changes=[]
    for i in range(n-1):
        ai=a[i];bi=b[i]
        for j in range(i+1,n):
            da=ai-a[j];db=bi-b[j]
            if da==0 and db==0:tie_both+=1
            elif da==0:tie_a+=1
            elif db==0:tie_b+=1
            elif da*db>0:con+=1
            else:
                dis+=1; margin_changes.append(abs(da))
            if errors is not None:
                if abs(da)>errors[i]+errors[j]:
                    safe+=1
                    fail_if(da*db<0, 'Error matematico: inversion pese a margen suficiente.')
                else:unsafe+=1
    non_ties=con+dis
    denom=math.sqrt((non_ties+tie_a)*(non_ties+tie_b))
    return {'n_materiales':n,'n_pares':n*(n-1)//2, 'concordantes':con,'discordantes':dis,
            'empates_solo_primero':tie_a, 'empates_solo_segundo':tie_b,'empates_ambos':tie_both,
            'fraccion_inversiones_total':dis/(n*(n-1)/2),
            'kendall_tau_b':(con-dis)/denom if denom else None,
            'pearson':pearson(a,b),
            'spearman':pearson(avg_ranks_high(a),avg_ranks_high(b)),
            'pares_margen_suficiente_a_posteriori':safe if errors is not None else None,
            'fraccion_margen_suficiente_a_posteriori':safe/(n*(n-1)/2) if errors is not None else None,
            'max_margen_objetivo_en_inversiones':max(margin_changes) if margin_changes else None,
            'p95_margen_objetivo_en_inversiones':percentile(margin_changes,.95) if margin_changes else None,
            'nota_margen':'Condicion calculada con diferencias individuales OBSERVADAS; no certifica muestras nuevas.' if errors is not None else ''}


def percentile(v,p):
    s=sorted(v)
    if not s:return None
    pos=(len(s)-1)*p;lo=math.floor(pos);hi=math.ceil(pos)
    return s[lo]+(s[hi]-s[lo])*(pos-lo)


def top_set(vals,k,high=True):
    return set(sorted(range(len(vals)),key=lambda i:(-vals[i] if high else vals[i],i))[:k])


def rows_csv(p,rows,cols):
    with p.open('w',newline='',encoding='utf-8-sig') as f:
        w=csv.DictWriter(f,fieldnames=cols,extrasaction='ignore');w.writeheader();w.writerows(rows)


def write_outputs(data, ids, smry, source):
    target=[data['STUDENT_1E'][i]['score_objetivo_B'] for i in ids]
    vectors={m:[data[m][i]['score_student_recalculado'] for i in ids] for m in MODELS}
    ranks={'OBJETIVO_B':avg_ranks_high(target),**{m:avg_ranks_high(vectors[m]) for m in MODELS}}
    comparisons=[]
    for m in MODELS:
        errors=[abs(vectors[m][j]-target[j]) for j in range(len(ids))]
        comparisons.append({'comparacion':'OBJETIVO_B vs '+m, 'split':SPLIT,
                            **pair_report(target,vectors[m],errors)})
    comparisons.append({'comparacion':'STUDENT_1E vs STUDENT_1F','split':SPLIT,
                        **pair_report(vectors['STUDENT_1E'],vectors['STUDENT_1F'])})
    top=[]
    for pair in [('OBJETIVO_B','STUDENT_1E'),('OBJETIVO_B','STUDENT_1F'),('STUDENT_1E','STUDENT_1F')]:
        va=target if pair[0]=='OBJETIVO_B' else vectors[pair[0]]
        vb=target if pair[1]=='OBJETIVO_B' else vectors[pair[1]]
        for pct in (5,10,20):
            k=math.ceil(len(ids)*pct/100)
            for extreme in ('MAYOR_SCORE','MENOR_SCORE'):
                hi=extreme=='MAYOR_SCORE'
                aa=top_set(va,k,hi); bb=top_set(vb,k,hi)
                top.append({'comparacion':f'{pair[0]} vs {pair[1]}','split':SPLIT,
                            'extremo':extreme,'porcentaje':pct,'k':k,
                            'interseccion':len(aa&bb),'proporcion_interseccion':len(aa&bb)/k})
    per=[]
    for j,i in enumerate(ids):
        e=data['STUDENT_1E'][i];f=data['STUDENT_1F'][i]
        per.append({'global_index':i,'split':SPLIT,'score_objetivo_B':target[j],
                    'score_student_1e':vectors['STUDENT_1E'][j],
                    'score_student_1f':vectors['STUDENT_1F'][j],
                    'delta_1e':e['delta_score'],'delta_1f':f['delta_score'],
                    'abs_delta_1e':abs(e['delta_score']),'abs_delta_1f':abs(f['delta_score']),
                    'rank_objetivo_alto_1':ranks['OBJETIVO_B'][j],
                    'rank_1e_alto_1':ranks['STUDENT_1E'][j],
                    'rank_1f_alto_1':ranks['STUDENT_1F'][j],
                    'desplazamiento_rank_1e':ranks['STUDENT_1E'][j]-ranks['OBJETIVO_B'][j],
                    'desplazamiento_rank_1f':ranks['STUDENT_1F'][j]-ranks['OBJETIVO_B'][j],
                    'abs_error_expectativa_1e_B1':e['error_abs_expectativa_B1'],
                    'abs_error_expectativa_1e_B2':e['error_abs_expectativa_B2'],
                    'abs_error_expectativa_1f_B1':f['error_abs_expectativa_B1'],
                    'abs_error_expectativa_1f_B2':f['error_abs_expectativa_B2']})
    out={'etapa':'H2B2A7-FASE-3C3','estado':'DESCRIPTIVO_INNER_VAL_YA_EXAMINADO',
         'fuente_3c':str(source.relative_to(ROOT)), 'n_materiales':len(ids),
         'n_pares':len(ids)*(len(ids)-1)//2, 'comparaciones':comparisons,
         'topk':top, 'observaciones':['Ranking objetivo es el score B congelado de 3C, NO una etiqueta FM/AFM.',
                                     'No se recalcula AUC; sin etiquetas en CSV.',
                                     'No se compara INNER VAL contra OUTER HOLD.',
                                     'Correlacion Student 1E vs 1F no mide fidelidad al objetivo.',
                                     'Margen suficiente se verifica a posteriori con deltas observados.',
                                     'No es validacion independiente ni prueba de ventaja cuantica.']}
    when=datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
    dest=REPORTS / ('H2B2A7_3C3_RANKING_'+when)
    dest.mkdir(parents=True,exist_ok=False)
    csvs={
      '3C3_COMPARACIONES_RANKING.csv':comparisons,
      '3C3_SOLAPAMIENTOS_TOPK.csv':top,
      '3C3_RANKING_POR_MATERIAL.csv':per,
    }
    for fname,rows in csvs.items():rows_csv(dest/fname,rows,list(rows[0]))
    (dest/'3C3_RESUMEN.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    md=['# H2B2A7 — Fase 3C.3: estabilidad del ranking','',
        '## Alcance','Solo INNER VAL previamente examinado: ranking del score B objetivo frente a Student 1E y 1F.',
        'Sin entrenamiento, QPU, OUTER HOLD, etiquetas ni nueva AUC.','',
        '| Comparación | Spearman | Kendall τ-b | Inversiones (%) | Fracción pares con margen suficiente (%) |',
        '|---|---:|---:|---:|---:|']
    for row in comparisons:
        safe=row['fraccion_margen_suficiente_a_posteriori']
        md.append(f"| {row['comparacion']} | {row['spearman']:.6f} | {row['kendall_tau_b']:.6f} | {100*row['fraccion_inversiones_total']:.3f} | {100*safe:.3f} |" if safe is not None else
                  f"| {row['comparacion']} | {row['spearman']:.6f} | {row['kendall_tau_b']:.6f} | {100*row['fraccion_inversiones_total']:.3f} | — |")
    md+=['','## Lectura correcta','Los pares de materiales con ranking invertido se miden entre todos los pares no ordenados.',
         'La condición |sB(x)-sB(y)| > |Δs(x)|+|Δs(y)| es suficiente para preservar el orden de ese par; aquí se evalúa a posteriori sobre INNER VAL.',
         'Las listas top-k comparan puntuaciones sin utilizar etiquetas; el porcentaje no mide precisión de clasificación.','',
         '## Limitaciones','El OUTER HOLD permanece excluido. Los experimentos y decisiones históricas ya habían usado INNER VAL. No hay estimaciones de generalización nueva.',
         'No se infieren costos de circuitos, shots ni ventajas en hardware cuántico.','']
    (dest/'3C3_INFORME.md').write_text('\n'.join(md),encoding='utf-8')
    products={p.name:sha256(p) for p in dest.iterdir() if p.is_file()}
    (dest/'3C3_MANIFIESTO_SHA256.json').write_text(json.dumps({'etapa':'H2B2A7-3C3','productos_sha256':products,
                                                             'nota':'Este manifiesto no se incluye en su propia lista.'},indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    return dest,comparisons,top


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source-3c',type=str,default=None,help='Carpeta de la ejecucion 3C (si hay mas de una).')
    parser.add_argument('--write',action='store_true',help='Genera una carpeta nueva con 6 productos.')
    args=parser.parse_args()
    p=resolve_source(args.source_3c)
    data,ids,summary=load_verified(p)
    print('H2B2A7 | 3C.3 | PREFLIGHT DE RANKING')
    print('Fuente:',p)
    print('SHA-256: 4/4 productos de 3C coinciden')
    print('Modelos: 1E/1F | INNER VAL:',len(ids),'cada uno | indices iguales, score objetivo identico')
    print('Sin OUTER HOLD, AUC, entrenamiento ni QPU.')
    print('PREFLIGHT OK')
    if args.write:
        dest,comparisons,top=write_outputs(data,ids,summary,p)
        print('RESULTADOS:',dest)
        for x in comparisons:
            print(f"  {x['comparacion']}: rho={x['spearman']:.6f}, tau={x['kendall_tau_b']:.6f}, inversiones={100*x['fraccion_inversiones_total']:.3f}%")
        print('Archivos nuevos: 6. Ninguna evidencia existente modificada.')

if __name__=='__main__':
    main()
