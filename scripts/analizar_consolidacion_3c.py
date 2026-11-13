#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""H2B2A7 fase 3C: errores de observables y expectativas Student vs B*.

Por defecto: preflight sin escribir archivos.
Con --write: calculo congelado sobre INNER_VAL, con salidas confinadas al
worktree de consolidacion. No Qiskit, entrenamiento, OUTER HOLD ni API IBM.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
import sys

import numpy as np

HASH = {
    "TEACHER": "0d851421e8ad0e370c3cc365dc053e9ad53b8a5ac5c0d437c72e61df67aa9b89",
    "SAFE": "e203c6e3d36266b20b859bce8f2f4e157dd95e82dde41a656d580d1cdc39b256",
    "X6": "5c76826e8f2e64b3effb943beacbce8cb12f0e4f883afa14372a8f5fdbefaee4",
    "STUDENT_1E": "aa18a34dca6284dd8ad17b9c2565d1132fa58f612fc59356eb9df4aa34d41bfd",
    "OPS_B1B2": "5384b8c0f75bc844a55c2aa4cafe1a813a68754685dd517414f82a28dac37f2d",
    "STUDENT_1F": "b481799c5985d73d56254612264659dc73a60a0b31fe54be6b8b4d4675310d7b",
}
SOURCE = {
    "TEACHER": "ARCH4FH2B2A0_FREEZE_R3_TEACHER.npz",
    "SAFE": "ARCH4FH2B2A4_1D2_SAFE_LOCAL_MODEL.npz",
    "OPS_B1B2": "ARCH4FH2B2A5_0_OPERATORS_AND_EIGENBASES.npz",
    "X6": "ARCH4FH2B1D2_X6_PAULI_EXPECTATIONS.npy",
    "STUDENT_1E": "ARCH4FH2B2A5_1E_RANKING_SAFE_MODEL.npz",
    "STUDENT_1F": "H2B2A5_1F_LABEL_AWARE/best_model_1f.npz",
}
# OPS_B1B2 y STUDENT_1F solo tenian huellas observadas en INTEGRACION-01;
# su coincidencia NO establece una certificacion historica previa.
PREVIOUSLY_FIXED = {"TEACHER", "SAFE", "X6", "STUDENT_1E"}
RUN_STUDENT = ("STUDENT_1E", "STUDENT_1F")

ROWS = np.arange(64, dtype=np.int64)
BIT = np.array([(ROWS >> q) & 1 for q in range(6)])
FLIPS = np.array([ROWS ^ (1 << q) for q in range(6)])
MATCHINGS = [
    [(0, 5), (1, 4), (2, 3)], [(0, 4), (5, 3), (1, 2)],
    [(0, 3), (4, 2), (5, 1)], [(0, 2), (3, 1), (4, 5)],
    [(0, 1), (2, 5), (3, 4)],
]


def sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def load_npz(path: Path, *keys: str) -> dict:
    with np.load(path, allow_pickle=False) as d:
        missing = set(keys) - set(d.files)
        if missing:
            raise ValueError(f"Faltan claves de {path.name}: {sorted(missing)}")
        return {k: np.asarray(d[k]) for k in keys}


def original_notebook_hash(path: Path, expected: str) -> None:
    nb = json.loads(path.read_text(encoding="utf-8"))
    cells = nb["cells"]
    if len(cells) != 1 or cells[0]["cell_type"] != "code":
        raise ValueError(f"Notebook inesperado: {path.name}")
    s = "".join(cells[0]["source"])
    actual = hashlib.sha256(s.encode("utf-8")).hexdigest()
    if actual != expected:
        raise ValueError(f"Hash del codigo distinto: {path.name}")


def verify_evidence(worktree: Path) -> None:
    directories = [
        ("H2B2A7_INTEGRACION_00", "H2B2A7_INTEGRACION_00_AUDITORIA_DOS_RUTAS_20261110T232931050887Z", "INTEGRACION00_HUELLAS_SHA256.json", "productos_sha256", 7),
        ("H2B2A7_INTEGRACION_01", "H2B2A7_INTEGRACION_01_CERT_20261111T221029053812Z", "INTEGRACION01_HUELLAS_SHA256.json", "archivos_resultado_sha256", 6),
    ]
    for folder, run, manifest, key, required in directories:
        path = worktree / "reports" / folder / run
        m = json.loads((path / manifest).read_text(encoding="utf-8"))
        digests = m[key]
        if len(digests) != required:
            raise ValueError(f"Numero de informes inesperado en {folder}")
        for name, h in digests.items():
            if Path(name).name != name or sha256_file(path / name) != h:
                raise ValueError(f"Informe alterado: {folder}/{name}")
        print(f"Integridad {folder}: {required}/{required} OK")
    original_notebook_hash(worktree / "experiments" / "INTEGRACION_00.ipynb", "350bc3d092f1c2098a28fdf7c05f5f92b1e6004f6a9b692afe9a149ecdff7ca9")
    original_notebook_hash(worktree / "experiments" / "INTEGRACION_01_CERT.ipynb", "089415d27e535700d5de2d56e78d4f255edc2c718d57141be125bd30ef9556d8")
    print("Codigos originales de los notebooks: 2/2 OK")


def independent_unitary(local: np.ndarray, angles: np.ndarray) -> np.ndarray:
    if local.shape != (17, 6, 2) or angles.shape != (48,):
        raise ValueError(f"Shape Student no esperado: {local.shape}, {angles.shape}")
    U = np.eye(64, dtype=complex)
    def layer(v: np.ndarray, A: np.ndarray) -> np.ndarray:
        for q in range(6):
            rz, ry = map(float, A[q])
            phase = np.exp(-0.5j * rz * (1 - 2 * BIT[q]))
            v = phase[:, None] * v
            v = np.cos(ry/2) * v + np.sin(ry/2) * (2 * BIT[q] - 1)[:, None] * v[FLIPS[q], :]
        return v
    U = layer(U, local[0])
    t = 0
    for r in range(16):
        for q, p in MATCHINGS[r % 5]:
            theta = float(angles[t]); t += 1
            U = np.cos(theta/2) * U - 1j * np.sin(theta/2) * U[ROWS ^ (1 << q) ^ (1 << p), :]
        U = layer(U, local[r+1])
    if t != 48 or np.max(np.abs(U.conj().T @ U - np.eye(64))) >= 1e-9:
        raise ValueError("Reconstruccion unitaria no aprobada")
    return U


def pauli_coefficients(O: np.ndarray) -> np.ndarray:
    """Mismo convenio bit/Pauli de INTEGRACION-01: idx=xmask*64+zmask."""
    c = np.arange(64, dtype=np.int64)
    H = np.array([[1-2*((int(col)&z).bit_count() % 2) for col in c] for z in range(64)], float)
    perm = np.arange(64)[:, None] ^ c[None, :]
    phase = np.array([[(-1j)**((x&z).bit_count()) for z in range(64)] for x in range(64)])
    vals = O[perm, c[None, :]]
    cc = phase * (vals @ H.T) / 64
    if np.max(np.abs(cc.imag)) > 2e-8:
        raise ValueError("Coeficientes Pauli complejos inesperados")
    return cc.real.ravel()


def read_student_scores(worktree: Path) -> dict[str, dict[int, float]]:
    path = worktree / "reports/H2B2A7_INTEGRACION_01/H2B2A7_INTEGRACION_01_CERT_20261111T221029053812Z/INTEGRACION01_SCORES_INNER_VAL_RECONSTRUIDOS.csv"
    scores = {k: {} for k in RUN_STUDENT}
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        for row in csv.DictReader(f):
            model, idx = row["modelo"], int(row["global_index"])
            if model not in scores or idx in scores[model]:
                raise ValueError(f"Modelo/indice duplicado o inesperado: {model}/{idx}")
            scores[model][idx] = float(row["score"])
    if any(len(v) != 1198 for v in scores.values()):
        raise ValueError("Se esperaban 1198 scores archivados por Student")
    return scores


def quantiles(a: np.ndarray) -> dict:
    return {
        "media": float(np.mean(a)),
        "mediana": float(np.median(a)),
        "p95": float(np.quantile(a, 0.95)),
        "max": float(np.max(a)),
    }


def save_csv(path: Path, records: list[dict]) -> None:
    with path.open("w", encoding="utf-8-sig", newline="") as f:
        if not records:
            raise ValueError("No hay datos")
        writer = csv.DictWriter(f, fieldnames=list(records[0].keys()))
        writer.writeheader()
        writer.writerows(records)


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--historical-root", type=Path, required=True, help="Ruta de Tesis4 solo para lectura")
    p.add_argument("--worktree", type=Path, default=Path(__file__).resolve().parent.parent, help="Worktree de consolidacion")
    p.add_argument("--write", action="store_true", help="Calcular y guardar resultados 3C en una carpeta nueva")
    args = p.parse_args()
    root = args.historical_root.expanduser().resolve(strict=True)
    worktree = args.worktree.expanduser().resolve(strict=True)
    if not root.is_dir() or not worktree.is_dir() or root == worktree or root in worktree.parents or worktree in root.parents:
        raise ValueError("Rutas historica y worktree deben existir, estar separadas y no anidadas")
    if not (worktree / ".git").exists():
        raise ValueError("La ruta de worktree no tiene marcador .git")
    print("H2B2A7 | FASE 3C | ANALISIS FISICO DE OBSERVABLES")
    print("Worktree:", worktree)
    print("Historico (solo lectura):", root)
    verify_evidence(worktree)
    historical_files = {k: root / rel for k, rel in SOURCE.items()}
    for k, path in historical_files.items():
        if not path.is_file() or sha256_file(path) != HASH[k]:
            raise ValueError(f"Falta fuente o cambio de hash: {k}")
        tag = "SHA_PREEXISTENTE_OK" if k in PREVIOUSLY_FIXED else "SHA_OBSERVADO_EN_INTEGRACION01_OK"
        print(f"{tag}: {k}")
    teach = load_npz(historical_files["TEACHER"], "inner_val_idx", "lambdas", "baseline")
    safe = load_npz(historical_files["SAFE"], "B", "C", "d", "T_val", "znew_val")
    ops = load_npz(historical_files["OPS_B1B2"], "B1_matrix", "B2_matrix")
    va = np.asarray(teach["inner_val_idx"], dtype=int).ravel()
    L = np.asarray(teach["lambdas"], float)
    baseline = np.asarray(teach["baseline"], float).ravel()
    C = np.asarray(safe["C"], float)
    T = np.asarray(safe["T_val"], float)
    z = np.asarray(safe["znew_val"], float)
    d = np.asarray(safe["d"], float).ravel()
    expected_n = 1198
    if len(va) != expected_n or len(set(va.tolist())) != expected_n or np.min(va) < 0 or np.max(va) >= len(baseline):
        raise ValueError("Indices de INNER VAL inesperados")
    if L.ndim != 2 or C.shape != (2, L.shape[1]) or T.shape != (expected_n, L.shape[1]) or z.shape != (expected_n, 2) or d.shape != (L.shape[1],):
        raise ValueError("Las matrices del score completo no tienen dimensiones coherentes")
    B = [np.asarray(ops["B1_matrix"], complex), np.asarray(ops["B2_matrix"], complex)]
    if any(M.shape != (64,64) or np.max(np.abs(M - M.conj().T)) > 1e-9 for M in B):
        raise ValueError("Matrices B* no hermiticas o dimensiones inesperadas")
    X6 = np.load(historical_files["X6"], mmap_mode="r", allow_pickle=False)
    if X6.shape != (len(baseline), 4096):
        raise ValueError(f"Cache X6 inesperada: {X6.shape}")
    if not args.write:
        print("PREFLIGHT OK: 6 fuentes/6 SHA, 13 informes/13 SHA, 2 notebooks/2 SHA.")
        print("INNER VAL:", len(va), "materiales; X6:", X6.shape)
        print("SIN ESCRITURAS. Para analizar y generar 3C: agrega --write")
        return

    saved_scores = read_student_scores(worktree)
    z_target_from_X6 = np.empty((len(va),2),float)
    bcoeff = [pauli_coefficients(M) for M in B]
    from_safe = np.asarray(safe["B"],float)
    if from_safe.shape != (4095,2) or any(np.max(np.abs(bcoeff[j][1:]-from_safe[:,j])) > 2e-6 for j in range(2)):
        raise ValueError("Coeficientes B* difieren de SAFE")
    for start in range(0,len(va),192):
        end = min(len(va),start+192)
        Xblock = np.asarray(X6[va[start:end]],float)
        for j in range(2):
            z_target_from_X6[start:end,j] = Xblock @ bcoeff[j]
    delta_cache = float(np.max(np.abs(z_target_from_X6 - z)))
    if delta_cache > 3e-4:
        raise ValueError(f"X6 vs znew_val no coincide: max={delta_cache}")

    T4 = T - z @ C - d
    target_score = baseline[va] + np.einsum("ij,ij->i",L[va],T4 + z@C+d)
    weights = L[va] @ C.T  # n x 2; delta score = sum_j weights_ij * delta z_ij
    op_rows = []; rows=[]; summary={}
    for model in RUN_STUDENT:
        st = load_npz(historical_files[model],"local_angles","rxx_angles","diagonal")
        local=np.asarray(st["local_angles"],float)
        angles=np.asarray(st["rxx_angles"],float)
        diag=np.asarray(st["diagonal"],float)
        if local.shape != (2,17,6,2) or angles.shape != (2,48) or diag.shape != (2,64):
            raise ValueError(f"Formas Student incorrectas: {model}")
        if any(not np.isfinite(A).all() for A in (local,angles,diag)):
            raise ValueError(f"Parametros no finitos: {model}")
        difference=[]; norms=[]; zstudent=np.empty((len(va),2),float)
        for j in range(2):
            U=independent_unitary(local[j],angles[j]); O=U.conj().T @ (diag[j][:,None]*U)
            Delta = (O - B[j]); normF=float(np.linalg.norm(Delta)); normB=float(np.linalg.norm(B[j])); normop=float(np.max(np.abs(np.linalg.eigvalsh((Delta+Delta.conj().T)/2))))
            relF=normF/normB
            normherm=float(np.max(np.abs(Delta-Delta.conj().T)))
            if normherm > 1e-9:
                raise ValueError(f"Delta no hermitico: {model}, B{j+1}")
            norms.append(normop); difference.append(Delta)
            op_rows.append({"modelo":model,"observable":f"B{j+1}","dimension":64,"norma_frobenius_delta":normF,"norma_frobenius_relativa":relF,"norma_operador_delta":normop,"errores_hermiticidad":normherm})
            coeff=pauli_coefficients(O)
            for start in range(0,len(va),192):
                end=min(len(va),start+192)
                zstudent[start:end,j] = np.asarray(X6[va[start:end]],float) @ coeff
        signed_delta = zstudent - z
        absolute_delta = np.abs(signed_delta)
        score_direct = baseline[va]+np.einsum("ij,ij->i",L[va],T4+zstudent@C+d)
        score_shift = np.einsum("ij,ij->i",weights,signed_delta)
        score_identity_err = float(np.max(np.abs((score_direct-target_score)-score_shift)))
        if score_identity_err > 1e-8:
            raise ValueError(f"Descomposicion del score incorrecta para {model}: {score_identity_err}")
        bound = np.abs(weights) @ np.asarray(norms)
        bound_viol = float(np.max(np.abs(score_shift)-bound))
        if bound_viol > 4e-4:
            raise ValueError(f"Cota de error no respetada: {model}, exceso {bound_viol}")
        historical_max = max(abs(score_direct[i]-saved_scores[model][int(idx)]) for i,idx in enumerate(va))
        if historical_max > 2e-7:
            raise ValueError(f"Scores Student difieren de INTEGRACION-01: {model}, error max={historical_max}")
        for i,idx in enumerate(va):
            rows.append({
                "modelo":model,"split":"INNER_VAL_YA_EXAMINADO","global_index":int(idx),
                "expectativa_B1_objetivo":float(z[i,0]),"expectativa_B2_objetivo":float(z[i,1]),
                "expectativa_O1_student":float(zstudent[i,0]),"expectativa_O2_student":float(zstudent[i,1]),
                "delta_expectativa_B1":float(signed_delta[i,0]),"delta_expectativa_B2":float(signed_delta[i,1]),
                "error_abs_expectativa_B1":float(absolute_delta[i,0]),"error_abs_expectativa_B2":float(absolute_delta[i,1]),
                "peso_score_B1":float(weights[i,0]),"peso_score_B2":float(weights[i,1]),
                "score_objetivo_B":float(target_score[i]),"score_student_recalculado":float(score_direct[i]),
                "delta_score":float(score_shift[i]),"cota_delta_score_operador":float(bound[i]),
            })
        summary[model]={
            "n_inner_val":len(va),"error_expectativa_B1":quantiles(absolute_delta[:,0]),"error_expectativa_B2":quantiles(absolute_delta[:,1]),
            "error_absoluto_score":quantiles(abs(score_shift)),"cota_absoluta_score":quantiles(bound),
            "error_max_score_vs_integracion01":float(historical_max),
            "max_error_identidad_delta_score":score_identity_err,"exceso_max_sobre_cota_teorica":bound_viol,
        }
        print(f"{model}: error absoluto medio expectativa B1={np.mean(absolute_delta[:,0]):.6g} B2={np.mean(absolute_delta[:,1]):.6g}; error medio score={np.mean(abs(score_shift)):.6g}; cotejo 01 max={historical_max:.2g}")

    parent = (worktree / "reports" / "H2B2A7_CONSOLIDACION").resolve()
    if not parent.is_relative_to(worktree) or parent.is_relative_to(root):
        raise ValueError("Salida fuera del worktree")
    tag = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
    dest = parent / ("H2B2A7_3C_OBSERVABLES_"+tag)
    if dest.exists():
        raise ValueError("El directorio de salida ya existe")
    dest.mkdir(parents=True,exist_ok=False)
    save_csv(dest / "3C_NORMAS_OPERADORES.csv",op_rows)
    save_csv(dest / "3C_ERRORES_POR_MATERIAL.csv", rows)
    summary_data={
        "etapa":"H2B2A7-FASE-3C1-3C2","estado":"DESCRIPTIVO_INNER_VAL_YA_EXAMINADO",
        "n_materiales":len(va),"n_filas":len(rows),"x6_shape":list(X6.shape),"max_error_x6_vs_z_objetivo":delta_cache,
        "resultado_por_modelo":summary,
        "alcance":"error operator vs expectativa sobre INNER_VAL, descomposicion de score congelado",
        "limites":["Sin nueva evaluacion independiente", "No se calcularon AUC ni ranking; no se ajustaron parametros", "No se calcularon recursos fisicos ni shots", "SHA de 1F y OPS solo observados previamente, no hashes historicos originales", "Requiere acceso a checkpoints fuera de Git"],
    }
    (dest / "3C_RESUMEN.json").write_text(json.dumps(summary_data,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    md=["# H2B2A7 — 3C.1/3C.2: operadores y errores de expectativa","",
        "## Alcance","Solo INNER VAL previamente examinado. Sin entrenamiento, OUTER, QPU, AUC nueva ni seleccion de modelos.","",
        "Se reconstruye U con la topologia congelada de Student 1E/1F, O=U† D U y se cotejan los scores con INTEGRACION-01.",
        "Las expectativas se calculan mediante X6 y los coeficientes Pauli; no se necesitan estados rho6 densos para los 1198 materiales.",
        "", "## Normas matriciales"]
    for row in op_rows:
        md.append(f"- {row['modelo']} {row['observable']}: ||O-B*||_F / ||B*||_F = {row['norma_frobenius_relativa']:.9f}; ||O-B*||_op = {row['norma_operador_delta']:.9f}")
    md.extend(["","## Errores en estados efectivamente codificados"])
    for model, data in summary.items():
        md.append(f"- {model}: media |Δexp B1|={data['error_expectativa_B1']['media']:.9g}; media |Δexp B2|={data['error_expectativa_B2']['media']:.9g}; media |Δscore|={data['error_absoluto_score']['media']:.9g}; max diferencia score vs 01={data['error_max_score_vs_integracion01']:.3g}")
    md.extend(["","## Identidad de score y cota", "Δs(x)=Σ_j [lambda(x) C^T]_j × Tr[rho(x)(O_j-B*_j)].",
        "|Δs(x)| ≤ Σ_j |[lambda(x) C^T]_j| × ||O_j-B*_j||_op.",
        "La cota es una garantia general; los errores reales pueden ser menores para los estados materiales.",
        "", "## Limitaciones", "Esta fase cuantifica error de expectativas y scores; NO demuestra causalidad en rankings ni ventaja de recursos.",
        "INNER VAL ya habia sido examinado. 1F/OPS carecen de hashes historicos originales previos."])
    (dest / "3C_INFORME.md").write_text("\n".join(md)+"\n",encoding="utf-8")
    manifest={"etapa":"H2B2A7-FASE-3C", "productos_sha256":{p.name:sha256_file(p) for p in sorted(dest.iterdir()) if p.is_file()},"nota":"El manifiesto no se incluye en su propia lista."}
    (dest / "3C_MANIFIESTO_SHA256.json").write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print("RESULTADOS EN:",dest)
    print("Nuevos archivos: 5 | Sin modificacion de informes 00/01 o Tesis4")

if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"ERROR: {type(exc).__name__}: {exc}",file=sys.stderr)
        raise SystemExit(1)
