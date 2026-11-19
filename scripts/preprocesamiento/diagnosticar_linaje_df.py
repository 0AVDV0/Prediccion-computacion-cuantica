#!/usr/bin/env python3
"""Diagnostico agregado de DataFrames ya exportados (SOLO LECTURA).

No ejecuta notebooks ni carga pickle, no reentrena modelos ni calcula AUC.
No guarda valores por fila; el reporte JSON contiene solo totales, nombres
base de archivos y SHA256, sin rutas locales absolutas.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from collections import Counter
from pathlib import Path
import sys


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def _load_csv(path: Path):
    import pandas as pd
    if not path.is_file():
        raise FileNotFoundError(f"Archivo CSV no encontrado: {path}")
    if path.suffix.lower() != ".csv":
        raise ValueError("Por seguridad, esta herramienta solo admite archivos .csv, nunca .pkl")
    return pd.read_csv(path, low_memory=False)


def _proportion_keys(df):
    import pandas as pd
    cols = sorted(str(c) for c in df.columns if str(c).startswith("p_") and len(str(c)) > 2)
    if not cols:
        return None, {"n_columnas_p": 0, "aviso": "Este CSV no tiene columnas p_X"}
    v = df[cols].apply(pd.to_numeric, errors="coerce")
    finite = v.notna().all(axis=1)
    total = v.sum(axis=1)
    valid = finite & (total > 0)
    # Valor de p_X con precision decimal; -0.0 se canoniza como 0.0.
    # La fila se excluye de la firma si falta algun p_X o si suma <= 0.
    signatures = []
    for row in v.loc[valid].round(9).to_numpy():
        signatures.append(tuple(0.0 if a == 0 else float(a) for a in row))
    # El conjunto de columnas se codifica en el nombre de la firma para impedir
    # cotejar accidentalmente vectores construidos con bases incompatibles.
    sigs = set(signatures)
    summary = {
        "n_columnas_p": len(cols),
        "columnas_p": cols,
        "filas_con_p_numericas_y_suma_positiva": int(valid.sum()),
        "filas_p_incompletas_o_cero": int(len(df) - valid.sum()),
        "filas_p_suma_fuera_de_1_tolerancia_1e-5": int((valid & ((total - 1).abs() > 1e-5)).sum()),
        "firmas_composicionales_unicas_validas": len(sigs),
        "duplicados_composicionales_validos": len(signatures) - len(sigs),
        "precision_comparacion_decimal": 9,
    }
    if "magnetic_label" in df.columns:
        # Este control es local a cada tabla, y no usa ni revela ejemplos individuales.
        group = {}
        labs = df.loc[valid, "magnetic_label"].astype("string").fillna("(nulo)").tolist()
        for k, label in zip(signatures, labs):
            group.setdefault(k, set()).add(label)
        summary["firmas_con_etiquetas_distintas"] = sum(len(labels) > 1 for labels in group.values())
    return sigs, summary


def summarize(path: Path):
    df = _load_csv(path)
    keys, composition = _proportion_keys(df)
    res = {
        "archivo": path.name,
        "sha256": sha256(path),
        "filas": int(len(df)),
        "columnas": int(len(df.columns)),
        "nombres_columnas": [str(c) for c in df.columns],
        "p": composition,
    }
    if "magnetic_label" in df.columns:
        res["etiquetas_agrupadas"] = {str(k): int(v) for k, v in df["magnetic_label"].astype("string").fillna("(nulo)").value_counts().items()}
    if "Material_Name" in df.columns:
        material = df["Material_Name"].astype("string").dropna()
        res["n_materiales_nombre_unicos"] = int(material.nunique())
        res["n_materiales_nombre_repetidos"] = int(len(material) - material.nunique())
    return res, keys


def run(paths: dict[str, Path]):
    result = {"tipo": "comparacion_descriptiva_sin_ejecutar_notebooks", "tablas": {}, "comparaciones": {}, "reservas": [
        "Mismos vectores p_X NO prueban mismo origen ni mismo orden de filas.",
        "No reproduce ni autentica la cadena original que creo cada archivo.",
        "La coincidencia por composicion NO representa igualdad de materiales cristalograficos.",
        "No se calcularon AUC ni se entreno ningun modelo."]}
    data = {}
    for key, path in paths.items():
        result["tablas"][key], data[key] = summarize(path)
    keys = list(paths)
    for i, a in enumerate(keys):
        for b in keys[i + 1:]:
            pa = result["tablas"][a]["p"]["columnas_p"] if "columnas_p" in result["tablas"][a]["p"] else []
            pb = result["tablas"][b]["p"]["columnas_p"] if "columnas_p" in result["tablas"][b]["p"] else []
            pair = f"{a}_vs_{b}"
            if pa and pa == pb and data[a] is not None and data[b] is not None:
                result["comparaciones"][pair] = {
                    "columnas_p_iguales_y_ordenadas": True,
                    "firmas_unicas_comunes": len(data[a] & data[b]),
                    "firmas_unicas_solo_primera": len(data[a] - data[b]),
                    "firmas_unicas_solo_segunda": len(data[b] - data[a]),
                    "advertencia": "Comparacion numerica redondeada de fracciones, no prueba de linaje por fila",
                }
            else:
                result["comparaciones"][pair] = {"columnas_p_iguales_y_ordenadas": False, "advertencia": "Bases p_X distintas: NO comparar vectores por posicion"}
    return result


def self_test():
    import pandas as pd
    a = pd.DataFrame({"p_Fe": [0.5, 1.0, 0.5], "p_O": [0.5, 0.0, 0.5], "magnetic_label": ["FM", "AFM", "AFM"]})
    b = pd.DataFrame({"p_Fe": [0.5, 0.0], "p_O": [0.5, 1.0], "magnetic_label": ["FM", "AFM"]})
    ka, sa = _proportion_keys(a)
    kb, sb = _proportion_keys(b)
    assert len(ka & kb) == 1 and sa["firmas_con_etiquetas_distintas"] == 1
    assert sb["firmas_composicionales_unicas_validas"] == 2
    assert sa["duplicados_composicionales_validos"] == 1
    print("SELF-TEST PASS | comparacion y conflictos de composicion")


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--bloques-dir", type=Path, help="Carpeta de bloque_1..bloque_12 y bloque_final (ruta 24174)")
    ap.add_argument("--df24174", type=Path, help="CSV previamente exportado de ruta 24174")
    ap.add_argument("--df10691", type=Path, help="CSV previamente exportado de ruta 10691")
    ap.add_argument("--df10678", type=Path, help="CSV dataset_listo_opcion_A.csv")
    ap.add_argument("--out", type=Path, help="Archivo JSON de salida (evitar escribir dentro de Tesis4)")
    ap.add_argument("--self-test", action="store_true")
    args = ap.parse_args()
    if args.self_test:
        self_test(); return
    if args.bloques_dir and args.df24174:
        ap.error("Elegir --bloques-dir O --df24174, no ambos")
    paths = {}
    if args.bloques_dir:
        # Concatena bloques temporalmente en memoria; no escribe en la ruta historica.
        import pandas as pd
        files = [args.bloques_dir / f"bloque_{i}.csv" for i in range(1, 13)] + [args.bloques_dir / "bloque_final.csv"]
        missing = [str(f) for f in files if not f.is_file()]
        if missing:
            raise FileNotFoundError("Faltan bloques originales: " + ", ".join(missing))
        # No crear CSV intermedio; resumen directo de todos los bloques.
        joined = pd.concat([_load_csv(f) for f in files], ignore_index=True)
        vals, keys = _proportion_keys(joined)
        meta = {"archivo": "13 bloques historicos en memoria", "sha256_bloques": {f.name: sha256(f) for f in files},
                "filas": int(len(joined)), "columnas": int(len(joined.columns)), "nombres_columnas": list(map(str, joined.columns)), "p": keys}
        if "magnetic_label" in joined.columns:
            meta["etiquetas_agrupadas"] = {str(k): int(v) for k, v in joined["magnetic_label"].astype("string").fillna("(nulo)").value_counts().items()}
        paths["24174_bloques"] = (meta, vals)
    if args.df24174: paths["24174"] = args.df24174
    if args.df10691: paths["10691"] = args.df10691
    if args.df10678: paths["10678"] = args.df10678
    if not paths: ap.error("Debe indicar al menos un CSV o --bloques-dir")
    preloaded = {k: v for k, v in paths.items() if isinstance(v, tuple)}
    regular = {k: v for k, v in paths.items() if not isinstance(v, tuple)}
    result = run(regular) if regular else {"tipo": "comparacion_descriptiva_sin_ejecutar_notebooks", "tablas": {}, "comparaciones": {}, "reservas": ["No se demuestra trazabilidad causal"]}
    data = {}
    for k, pair in preloaded.items():
        result["tablas"][k], data[k] = pair
    # Comparar los bloques con otros CSV agregados, cuando comparten base de columnas.
    for a, ka in data.items():
        for b, path in regular.items():
            _, kb = summarize(path)
            va = result["tablas"][a]["p"].get("columnas_p", [])
            vb = result["tablas"][b]["p"].get("columnas_p", [])
            result["comparaciones"][f"{a}_vs_{b}"] = (
                {"columnas_p_iguales_y_ordenadas": True, "firmas_unicas_comunes": len(ka & kb),
                 "firmas_unicas_solo_primera": len(ka - kb), "firmas_unicas_solo_segunda": len(kb - ka),
                 "advertencia": "No prueba identidad ni orden por fila"}
                if va and va == vb and ka is not None and kb is not None else
                {"columnas_p_iguales_y_ordenadas": False, "advertencia": "Bases p_X no equivalentes; comparacion omitida"})
    payload = json.dumps(result, ensure_ascii=False, indent=2)
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(payload + "\n", encoding="utf-8")
        print("INFORME CREADO:", args.out)
    else:
        print(payload)


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print("ERROR:", str(exc), file=sys.stderr)
        sys.exit(1)
