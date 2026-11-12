#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Ejecutor portable y verificable de H2B2A7-INTEGRACION-00.

Por defecto realiza SOLO comprobaciones (no ejecuta la celda).
Con --run reproduce los scores usando checkpoints historicos congelados.
Con --verify-report verifica SHA-256 de una carpeta de informes existente.

No modifica el notebook ni los archivos del directorio historico.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

SOURCE_SHA256 = "350bc3d092f1c2098a28fdf7c05f5f92b1e6004f6a9b692afe9a149ecdff7ca9"
REPO = Path(__file__).resolve().parent.parent
SOURCE_NB = REPO / "experiments" / "INTEGRACION_00.ipynb"
DEFAULT_OUTPUT = REPO / "reports" / "H2B2A7_INTEGRACION_00"

# Estos 7 archivos se contrastan con hashes del manifiesto historico H2B2A7-13.
MANIFEST_PATH = Path("H2B2A7_PAULI_AUDIT/H2B2A7_13_FINAL_OUTER_HOLD/MANIFEST_PREVIO.json")
MANIFEST_RELATIVE = {
    "ARCH4FH2B2A0_FREEZE_R3_TEACHER.npz": "ARCH4FH2B2A0_FREEZE_R3_TEACHER.npz",
    "ARCH4FH2B2A4_1D2_SAFE_LOCAL_MODEL.npz": "ARCH4FH2B2A4_1D2_SAFE_LOCAL_MODEL.npz",
    "ARCH4FH2B2A2_BEST_JOINT_FOUR_HEAD_MODEL.npz": "ARCH4FH2B2A2_BEST_JOINT_FOUR_HEAD_MODEL.npz",
    "MODELO_FINAL_CONGELADO.npz": "H2B2A7_PAULI_AUDIT/H2B2A7_12_LOCAL_QWC_SWAPS/MODELO_FINAL_CONGELADO.npz",
    "congelado_K24_Ridge_var.npz": "H2B2A7_PAULI_AUDIT/H2B2A7_10_QWC_FULL_PAULI/congelado_K24_Ridge_var.npz",
    "elegido_N10000.npz": "H2B2A7_PAULI_AUDIT/H2B2A7_7_SHOT_BUDGET_SELECTION/elegido_N10000.npz",
    "modelo_QWC_G64.npz": "H2B2A7_PAULI_AUDIT/H2B2A7_3_GROUP_QWC/modelo_QWC_G64.npz",
}


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for block in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def read_source() -> str:
    if not SOURCE_NB.is_file():
        raise FileNotFoundError(f"Notebook no encontrado: {SOURCE_NB}")
    notebook = json.loads(SOURCE_NB.read_text(encoding="utf-8"))
    cells = notebook.get("cells", [])
    if len(cells) != 1 or cells[0].get("cell_type") != "code":
        raise ValueError("Se esperaba exactamente una celda de codigo")
    source = "".join(cells[0]["source"])
    actual = hashlib.sha256(source.encode("utf-8")).hexdigest()
    if actual != SOURCE_SHA256:
        raise ValueError(f"SHA-256 de la celda diferente al certificado: {actual}")
    return source


def replace_exact(source: str, regex: str, replacement: str, label: str) -> str:
    updated, count = re.subn(regex, lambda _: replacement, source, flags=re.MULTILINE)
    if count != 1:
        raise ValueError(f"No se puede parchear {label}: coincidencias={count} (se requiere 1)")
    return updated


def preflight_history(root: Path) -> None:
    if not root.is_dir():
        raise FileNotFoundError(f"Carpeta historica no existe: {root}")
    manifest_file = root / MANIFEST_PATH
    if not manifest_file.is_file():
        raise FileNotFoundError(f"Manifiesto de H2B2A7-13 no encontrado: {manifest_file}")
    manifest = json.loads(manifest_file.read_text(encoding="utf-8"))
    expected = manifest.get("hashes", {})
    if not isinstance(expected, dict):
        raise ValueError("El manifiesto historico no tiene un campo 'hashes' valido")
    for filename, relative in MANIFEST_RELATIVE.items():
        p = root / relative
        if not p.is_file():
            raise FileNotFoundError(f"Checkpoint faltante: {p}")
        if filename not in expected or digest(p).lower() != str(expected[filename]).lower():
            raise ValueError(f"SHA-256 no coincide con H2B2A7-13: {p}")
    scores = root / "H2B2A7_PAULI_AUDIT" / "H2B2A7_13_FINAL_OUTER_HOLD" / "predicciones_OUTER_HOLD.csv"
    if not scores.is_file():
        raise FileNotFoundError(f"Predicciones historicas del OUTER HOLD ausentes: {scores}")
    print("7/7 hashes de checkpoints H2B2A7-13: OK")
    print("Scores archivados del OUTER HOLD: ENCONTRADOS")


def verify_report(folder: Path) -> None:
    index_file = folder / "INTEGRACION00_HUELLAS_SHA256.json"
    if not index_file.is_file():
        raise FileNotFoundError(f"Indice de SHA-256 no encontrado: {index_file}")
    index = json.loads(index_file.read_text(encoding="utf-8"))
    expected = index.get("productos_sha256", {})
    if not isinstance(expected, dict) or not expected:
        raise ValueError("Indice sin productos_sha256 validos")
    for name, target in expected.items():
        if Path(name).name != name:
            raise ValueError(f"Nombre no seguro en manifiesto: {name!r}")
        file = folder / name
        if not file.is_file() or digest(file).lower() != str(target).lower():
            raise ValueError(f"Falta el archivo o difiere SHA-256: {file}")
        print(f"OK {name}")
    summary_file = folder / "INTEGRACION00_RESUMEN.json"
    summary = json.loads(summary_file.read_text(encoding="utf-8"))
    print(f"Verificados: {len(expected)}/{len(expected)} archivos de evidencia")
    print(f"Estado cientifico archivado: {summary.get('estado', 'SIN ESTADO')}")
    print("Nota: esto certifica integridad de archivos, no reemplaza el replay numerico")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--historical-root", type=Path, help="Directorio Tesis4 (requerido para --run y preflight)")
    parser.add_argument("--output-root", type=Path, default=DEFAULT_OUTPUT,
                        help="Carpeta base de informes, por defecto dentro del repositorio")
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--run", action="store_true", help="Ejecuta el replay; sin este parametro solo verifica")
    mode.add_argument("--verify-report", type=Path, metavar="CARPETA",
                      help="Verifica el hash de los reportes existentes sin ejecutar el notebook")
    args = parser.parse_args()

    if args.verify_report is not None:
        verify_report(args.verify_report.expanduser().resolve())
        return

    if args.historical_root is None:
        parser.error("Indica --historical-root RUTA para comprobacion o --run")
    root = args.historical_root.expanduser().resolve()
    out = args.output_root.expanduser().resolve()

    # Nunca escribir reportes dentro de los historicos ni sobre el propio directorio Tesis4.
    if out == root or root in out.parents:
        raise ValueError("La salida debe quedar fuera de la carpeta historica")
    if out == SOURCE_NB.parent.resolve() or out == SOURCE_NB.resolve():
        raise ValueError("La salida no puede ser el archivo notebook")

    source = read_source()
    preflight_history(root)

    # Se modifica SOLO el codigo en memoria, nunca el archivo .ipynb.
    # Se fija ROOT directamente: asi el autodetector historico no puede elegir otra ruta.
    patched = replace_exact(source, r"^ROOT=choose_root\(\)[ \t]*$",
                            f"ROOT=Path({str(root)!r}).resolve()", "ROOT")
    patched = replace_exact(patched, r"^AUDIT=ROOT/'H2B2A7_PAULI_AUDIT'[ \t]*$",
                            f"AUDIT=Path({str(out)!r}).resolve()", "AUDIT")
    code = compile(patched, str(SOURCE_NB), "exec")
    print("Notebook:", SOURCE_NB)
    print("SHA-256 del codigo original: OK", SOURCE_SHA256)
    print("Entradas historicas (solo lectura):", root)
    print("Salida exclusiva:", out)

    if not args.run:
        print("PREFLIGHT OK. No se ejecuto ninguna celda ni se creo ningun informe.")
        print("Para ejecutar: agrega --run al mismo comando.")
        return

    print("INICIANDO REPLAY (sin entrenamiento ni acceso a QPU)", flush=True)
    namespace = {"__name__": "__main__", "__file__": str(SOURCE_NB)}
    exec(code, namespace)


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"ERROR: {type(exc).__name__}: {exc}", file=sys.stderr)
        raise SystemExit(1)
