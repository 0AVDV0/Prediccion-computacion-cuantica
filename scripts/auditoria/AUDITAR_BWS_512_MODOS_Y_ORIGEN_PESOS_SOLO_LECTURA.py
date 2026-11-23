#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""H2B2A7: auditoría numérica de 512 pares propios y origen algebraico de pesos.
Solo lectura de TRAIN; nunca reentrena, aplica eigsh, usa VAL/TEST ni altera artefactos.
La verificación de pesos contra difficulty NO demuestra cronología histórica.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import tempfile
import numpy as np
from scipy import sparse
from scipy.special import expit

SHA = {
    "phi": "6c2f514200cb806705663bfee928c438fa21ce83c57aadc949e17fcf0bde7af3",
    "basis": "1831b92ff336bb9aa86bc5850d48cab3f40bcabc42658ed58f9969a4a1e9c9b4",
    "cache": "4a2ebcd6f1fc19663c68ae202eb9caca4a3d607a17dc410e2efaf5f7898f27d3",
    # Huella de pesos registrada en la auditoría muestral 2026-11-22;
    # NO es una huella histórica independiente.
    "weights": "d4b79177d23db03270dd480a5d94bd41a52c2fcf2d24c1a87a16388f7179b4c6",
}
ROOT_DEFAULT = Path.cwd()
ETA = 0.5


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(4 * 1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def candidates(root: Path, filename: str):
    seen = set()
    direct = root / filename
    if direct.is_file():
        seen.add(str(direct.resolve()).lower())
        yield direct
    for path in root.rglob(filename):
        if path.is_file():
            key = str(path.resolve()).lower()
            if key not in seen:
                seen.add(key)
                yield path


def localizar_verificar(root: Path, name: str, sha: str) -> Path:
    seen = []
    for path in candidates(root, name):
        h = sha256_file(path)
        seen.append((str(path), h))
        if h == sha:
            print("SHA-256 OK:", name, "|", str(path), flush=True)
            return path
    raise FileNotFoundError(
        f"No se encuentra copia autenticada de {name}. Candidatos: {seen[:8]}"
    )


def stats(x):
    v = np.asarray(x, dtype=np.float64).reshape(-1)
    return dict(n=int(len(v)), minimo=float(v.min()), media=float(v.mean()),
                mediana=float(np.median(v)), maximo=float(v.max()))


def crear_csr_por_bloques(phi: np.ndarray, filas_bloque: int = 256):
    partes = []
    for a in range(0, phi.shape[0], filas_bloque):
        b = min(a + filas_bloque, phi.shape[0])
        partes.append(sparse.csr_matrix(np.asarray(phi[a:b]), dtype=np.complex64))
    return sparse.vstack(partes, format="csr")


def aplicar_delta(Xafm, Xfm, wafm, wfm, V, eta=0.5):
    afm = Xafm.conjugate() @ V
    fm = Xfm.conjugate() @ V
    rho_afm_v = Xafm.T @ (afm * (wafm / wafm.sum())[:, None])
    rho_fm_v = Xfm.T @ (fm * (wfm / wfm.sum())[:, None])
    return eta * rho_fm_v - (1.0-eta) * rho_afm_v


def comprobar_pesos(root: Path, y, pesos, ruta_explicita=None):
    names = ["EXT_WEIGHT_train_difficulty.npy", "FINE_ERROR_train_difficulty.npy"]
    registros = []
    if ruta_explicita is not None:
        if not ruta_explicita.is_file():
            raise FileNotFoundError(ruta_explicita)
        paths = [ruta_explicita]
    else:
        paths = []
        for name in names:
            paths.extend(candidates(root, name))
    seen = set()
    for path in paths:
        if str(path.resolve()).lower() in seen:
            continue
        seen.add(str(path.resolve()).lower())
        data = np.load(path, allow_pickle=False)
        if data.ndim != 1 or len(data) != len(y) or not np.isfinite(data).all():
            registros.append({"nombre": path.name, "ruta": str(path),
                              "sha256": sha256_file(path), "estado": "FORMA_O_FINITEZ_INVALIDA"})
            continue
        t = 2.0 * y.astype(np.float64) - 1.0
        reconstruidos = 1.0 + 2.0 * expit(-10.0 * (t * (data.astype(np.float64)-0.5)))
        errores = np.abs(reconstruidos - pesos)
        registros.append({"nombre": path.name, "ruta": str(path),
                          "sha256": sha256_file(path), "estado": "EVALUADO",
                          "error_maximo_peso": float(errores.max()),
                          "error_rms_peso": float(np.sqrt(np.mean(errores**2))),
                          "filas_coincidentes_tol_1e_8": int(np.count_nonzero(errores <= 1e-8)),
                          "todas_coinciden_tol_1e_8": bool(np.all(errores <= 1e-8)),
                          "resumen_difficulty": stats(data)})
    return {"formula": "w=1+2*expit(-10*(2*y-1)*(difficulty-0.5))",
            "archivos_comprobados": registros,
            "algun_archivo_reconstruye_pesos": bool(any(x.get("todas_coinciden_tol_1e_8") for x in registros)),
            "nota": "Coincidencia algebraica no autentica la fecha ni la generación OOF de difficulty."}


def espectro(X, y, pesos, V, lam, num_plus, block=16, progreso=True):
    Xafm = X[y == 0].tocsr()
    Xfm = X[y == 1].tocsr()
    wafm = pesos[y == 0].astype(np.float64)
    wfm = pesos[y == 1].astype(np.float64)
    error_abs, error_rel, rayleigh_err, rayleigh_imag = [], [], [], []
    for a in range(0, len(lam), block):
        b = min(a + block, len(lam))
        B = V[:, a:b]
        DV = aplicar_delta(Xafm, Xfm, wafm, wfm, B, ETA)
        denom = np.linalg.norm(B, axis=0)
        r = DV - B * lam[None, a:b]
        abs_e = np.linalg.norm(r, axis=0)
        rel_e = abs_e / np.maximum(np.abs(lam[a:b]) * denom, 1e-15)
        rayleigh = np.sum(np.conj(B) * DV, axis=0) / np.sum(np.abs(B)**2, axis=0)
        error_abs.extend(abs_e.tolist())
        error_rel.extend(rel_e.tolist())
        rayleigh_err.extend(np.abs(rayleigh.real-lam[a:b]).tolist())
        rayleigh_imag.extend(np.abs(rayleigh.imag).tolist())
        if progreso:
            print(f"MODOS: {b}/{len(lam)} | max_abs={max(error_abs):.3e} | max_rel={max(error_rel):.3e}", flush=True)
    errors = np.asarray(error_abs)
    relatives = np.asarray(error_rel)
    ray_err = np.asarray(rayleigh_err)
    imag_err = np.asarray(rayleigh_imag)
    subset = {}
    for label, vals in [("positivo", slice(0, num_plus)), ("negativo", slice(num_plus, len(lam)))]:
        sub = relatives[vals]
        subset[label] = {"n": int(len(sub)), "residuo_absoluto": stats(errors[vals]),
                         "residuo_relativo": stats(sub), "max_error_rayleigh": float(ray_err[vals].max()),
                         "modos_rel_le_1e_4": int(np.count_nonzero(sub <= 1e-4))}
    worst = np.argsort(relatives)[-12:][::-1]
    return {
        "n_modos": int(len(lam)), "max_residuo_absoluto": float(errors.max()),
        "max_residuo_relativo": float(relatives.max()),
        "max_error_autovalor_rayleigh": float(ray_err.max()),
        "max_parte_imaginaria_rayleigh": float(imag_err.max()),
        "modos_residuo_abs_le_1e_6": int(np.count_nonzero(errors <= 1e-6)),
        "modos_residuo_rel_le_1e_4": int(np.count_nonzero(relatives <= 1e-4)),
        "todos_cumplen_ambas": bool(np.all(errors <= 1e-6) and np.all(relatives <= 1e-4)),
        "sectores": subset,
        "peores_12_residuos_relativos": [
            {"sector": "positivo" if i < num_plus else "negativo",
             "indice_sector": int(i if i < num_plus else i-num_plus),
             "autovalor": float(lam[i]), "residuo_l2": float(errors[i]),
             "residuo_relativo": float(relatives[i])} for i in worst
        ],
        "residuos_por_modo": [
            {"indice_global": i, "autovalor": float(lam[i]),
             "residuo_l2": float(errors[i]), "residuo_relativo": float(relatives[i]),
             "error_rayleigh": float(ray_err[i])} for i in range(len(lam))
        ],
    }


def ortogonalidad_completa(V, block=512):
    n = V.shape[1]
    gram = np.zeros((n,n), dtype=np.complex128)
    for a in range(0, V.shape[0], block):
        B = V[a:a+block]
        gram += B.conj().T @ B
    diff = gram - np.eye(n)
    diag = float(np.max(np.abs(np.diag(diff))))
    np.fill_diagonal(diff, 0)
    off = float(np.max(np.abs(diff)))
    return {"modo": "todos_los_512", "max_error_diagonal": diag,
            "max_solapamiento_fuera_diagonal": off,
            "max_error_gram": max(diag, off), "cumple_tol_1e_4": max(diag,off) <= 1e-4}


def autoprueba():
    rng = np.random.default_rng(7412)
    n, d = 12, 8
    psi = rng.normal(size=(n,d)) + 1j*rng.normal(size=(n,d))
    psi = psi / np.linalg.norm(psi, axis=1, keepdims=True)
    X = sparse.csr_matrix(psi)
    y = np.array([0]*6+[1]*6, dtype=int)
    difficulty = rng.uniform(.05, .95, size=n)
    w = 1+2*expit(-10 * (2*y-1)*(difficulty-.5))
    assert len(w) == n and w.min() >= 1 and w.max() <=3
    # Delta real-simetrico hermitico construido de forma distinta a aplicar_delta.
    ra = (psi[:6].T * w[:6]) @ psi[:6].conj() / w[:6].sum()
    rf = (psi[6:].T * w[6:]) @ psi[6:].conj() / w[6:].sum()
    delta = .5*(rf-ra)
    vals, v = np.linalg.eigh(delta)
    got = aplicar_delta(X[:6], X[6:], w[:6], w[6:], v)
    assert np.max(np.abs(got - delta @ v)) < 1e-12
    assert np.max(np.abs(got - v * vals)) < 1e-12
    r = espectro(X, y, w, v, vals, int((vals>0).sum()), block=3, progreso=False)
    assert r["modos_residuo_abs_le_1e_6"] == d
    assert ortogonalidad_completa(v)["max_error_gram"] < 1e-12
    with tempfile.TemporaryDirectory() as tmp:
        src = Path(tmp)/"EXT_WEIGHT_train_difficulty.npy"
        np.save(src, difficulty)
        res = comprobar_pesos(Path(tmp), y, w)
        assert res["algun_archivo_reconstruye_pesos"]
        wrong = w.copy()
        wrong[3] += 0.05
        assert not comprobar_pesos(Path(tmp), y, wrong)["algun_archivo_reconstruye_pesos"]
        badlam = vals.copy()
        badlam[0] += .1
        assert not espectro(X,y,w,v,badlam,4,block=3,progreso=False)["todos_cumplen_ambas"]
    print("SELF-TEST PASS | operador complejo, 512-style residual, Rayleigh, Gram, pesos Smooth-L2-K10 y alteraciones detectadas")


def auditar(args):
    root = args.raiz.expanduser()
    if not root.is_dir():
        raise FileNotFoundError(f"No existe raiz: {root}")
    path_phi = localizar_verificar(root, "Phi3_train_exact.npy", SHA["phi"])
    path_bas = localizar_verificar(root, "HELSTROM512_EXT_BASIS_REBUILT.npz", SHA["basis"])
    path_cac = localizar_verificar(root, "HELSTROM512_COORDINATES_CACHE.npz", SHA["cache"])
    path_w = localizar_verificar(root, "EXT_WEIGHT_train_weights.npy", SHA["weights"])
    phi = np.load(path_phi, mmap_mode="r", allow_pickle=False)
    if phi.shape != (7483,8399) or not np.iscomplexobj(phi):
        raise ValueError(f"Phi3 TRAIN inesperado: {phi.shape} {phi.dtype}")
    with np.load(path_bas, allow_pickle=False) as bas:
        if not all(k in bas.files for k in ("Vplus", "Vminus", "values_plus", "values_minus")):
            raise ValueError("Faltan claves de la base")
        vp = np.asarray(bas["Vplus"], dtype=np.complex128)
        vm = np.asarray(bas["Vminus"], dtype=np.complex128)
        lp = np.asarray(bas["values_plus"], dtype=np.float64).reshape(-1)
        lm = np.asarray(bas["values_minus"], dtype=np.float64).reshape(-1)
    if vp.shape!=(8399,320) or vm.shape!=(8399,192) or lp.shape!=(320,) or lm.shape!=(192,):
        raise ValueError("Dimensiones espectrales inesperadas")
    if not (np.all(lp>0) and np.all(lm<0)):
        raise ValueError("Signos de autovalores inesperados")
    V = np.concatenate((vp,vm), axis=1)
    lam = np.concatenate((lp,lm))
    if not np.isfinite(V).all() or not np.isfinite(lam).all():
        raise ValueError("Base espectral no finita")
    with np.load(path_cac, allow_pickle=False) as cac:
        y = np.asarray(cac["y_train"]).reshape(-1)
        if "C_train" not in cac.files or np.shape(cac["C_train"]) != (7483,512):
            raise ValueError("Cache de coordenadas inesperado")
    if y.shape != (7483,) or not np.isin(y, [0,1]).all():
        raise ValueError("Etiquetas TRAIN invalidas")
    y = y.astype(np.int8)
    if (np.sum(y==0),np.sum(y==1))!=(3144,4339):
        raise ValueError("Conteos de TRAIN no coinciden con historial")
    pesos = np.asarray(np.load(path_w, allow_pickle=False), dtype=np.float64).reshape(-1)
    if pesos.shape!=(7483,) or not np.isfinite(pesos).all() or (pesos<=0).any():
        raise ValueError("Pesos invalidos")
    report = {"tipo":"H2B2A7_AUDITORIA_EXHAUSTIVA_512_MODOS_Y_PESOS_SOLO_LECTURA",
              "alcance":"TRAIN, sin VAL/TEST, sin eigsh, sin ajuste, sin modificar artefactos",
              "sha256_pinned": SHA,
              "n_train":7483,"n_afm":3144,"n_fm":4339,"eta":ETA,
              "reconstruccion_pesos": comprobar_pesos(root,y,pesos,args.difficulty),
              "resumen_pesos":stats(pesos)}
    print("Revisando ortogonalidad de 512 modos...",flush=True)
    report["ortogonalidad_512"] = ortogonalidad_completa(V)
    print("Gram max error:",f'{report["ortogonalidad_512"]["max_error_gram"]:.3e}',flush=True)
    print("Construyendo TRAIN CSR por bloques (sin modificar Phi3)...",flush=True)
    X = crear_csr_por_bloques(phi, args.bloque_filas)
    report["n_elementos_no_cero_phi_train"] = int(X.nnz)
    report["residuos_espectrales"] = espectro(X,y,pesos,V,lam,320,block=args.bloque_modos)
    report["veredicto_numerico"] = bool(report["ortogonalidad_512"]["cumple_tol_1e_4"] and
                                    report["residuos_espectrales"]["todos_cumplen_ambas"])
    report["limitaciones"] = [
        "Los modos archivados se contrastan contra Delta, sin recalcular el espectro con eigsh.",
        "La auditora no certifica que los 512 modos sean necesariamente todos los extremos globales.",
        "La huella del archivo de pesos es posterior (de la auditoria muestral), no certificacion cronologica original.",
        "Una coincidencia de pesos con difficulty verifica su regla algebraica, no que difficulty sea OOF autentico.",
        "No evalua VAL, TEST, resultados predictivos ni hardware QPU.",
    ]
    out = args.out.expanduser()
    out.parent.mkdir(parents=True,exist_ok=True)
    # Modo x evita sobrescribir informes previos.
    with out.open("x",encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False,indent=2)
    print("AUDITORIA FINALIZADA | veredicto_numerico=",report["veredicto_numerico"],flush=True)
    print("Reporte:",out,flush=True)
    return report


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--raiz",type=Path,default=ROOT_DEFAULT)
    ap.add_argument("--out",type=Path,default=Path.cwd()/"AUDITORIA_BWS_512_MODOS_Y_PESOS_RESULTADO.json")
    ap.add_argument("--difficulty",type=Path,help="Archivo concreto de dificultad (opcional)")
    ap.add_argument("--bloque-modos",type=int,default=16)
    ap.add_argument("--bloque-filas",type=int,default=256)
    ap.add_argument("--self-test",action="store_true")
    args=ap.parse_args()
    if args.bloque_modos < 1 or args.bloque_filas < 1:
        ap.error("Los tamaños de bloques deben ser positivos")
    if args.self_test:
        autoprueba()
    else:
        auditar(args)

if __name__=="__main__":
    main()
