#!/usr/bin/env python3
"""Preflight and controlled replay of the frozen H2B2A7-INTEGRACION-01 notebook.

The notebook's code is checked against a fixed SHA-256 and AST-patched only
in memory to redirect ROOT_OVERRIDE and DEST. No model training or QPU calls.
The historical archive is read-only by convention; outputs are confined to
an isolated timestamped directory under the student worktree.
"""
from __future__ import annotations

import argparse
import ast
import hashlib
import importlib.util
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

EXPECTED_CODE_SHA256 = "089415d27e535700d5de2d56e78d4f255edc2c718d57141be125bd30ef9556d8"
SOURCES = {
    "TEACHER": "ARCH4FH2B2A0_FREEZE_R3_TEACHER.npz",
    "SAFE": "ARCH4FH2B2A4_1D2_SAFE_LOCAL_MODEL.npz",
    "OPS_B1B2": "ARCH4FH2B2A5_0_OPERATORS_AND_EIGENBASES.npz",
    "X6": "ARCH4FH2B1D2_X6_PAULI_EXPECTATIONS.npy",
    "STUDENT_1E": "ARCH4FH2B2A5_1E_RANKING_SAFE_MODEL.npz",
    "QPY_1E": "ARCH4FH2B2A5_1E_RANKING_SAFE_CIRCUITS.qpy",
    "STUDENT_1F": "H2B2A5_1F_LABEL_AWARE/best_model_1f.npz",
    "A6_2B1": "H2B2A6_QAS/DIAGONALES_2B1/tabla_final.csv",
    "A6_2B2": "H2B2A6_QAS/JOINT_2B2/tabla_progresiva.csv",
}
# Five historical reference digests embedded in the signed original cell.
EXPECTED_HISTORICAL_SHA256 = {
    "TEACHER": "0d851421e8ad0e370c3cc365dc053e9ad53b8a5ac5c0d437c72e61df67aa9b89",
    "SAFE": "e203c6e3d36266b20b859bce8f2f4e157dd95e82dde41a656d580d1cdc39b256",
    "X6": "5c76826e8f2e64b3effb943beacbce8cb12f0e4f883afa14372a8f5fdbefaee4",
    "STUDENT_1E": "aa18a34dca6284dd8ad17b9c2565d1132fa58f612fc59356eb9df4aa34d41bfd",
    "QPY_1E": "e6ef44e89f63624f3f0049d5dee45f0ff32e160e7bfb8ddd7d0752dfdd62f9ec",
}

def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def load_original_code(notebook: Path) -> str:
    nb = json.loads(notebook.read_text(encoding="utf-8"))
    cells = nb.get("cells", [])
    if len(cells) != 1 or cells[0].get("cell_type") != "code":
        raise RuntimeError("Se esperaba un notebook exportado con exactamente una celda de código.")
    content = "".join(cells[0].get("source", []))
    actual = hashlib.sha256(content.encode("utf-8")).hexdigest()
    if actual != EXPECTED_CODE_SHA256:
        raise RuntimeError(f"SHA256 del código inesperado: {actual}")
    ast.parse(content)
    return content


def redirect_in_memory(content: str, root: Path, destination: Path) -> ast.Module:
    tree = ast.parse(content, filename="INTEGRACION_01_CERT.ipynb")
    replacements = {"ROOT_OVERRIDE": 0, "DEST": 0}
    for statement in tree.body:
        if not isinstance(statement, ast.Assign) or len(statement.targets) != 1:
            continue
        target = statement.targets[0]
        if not isinstance(target, ast.Name):
            continue
        if target.id == "ROOT_OVERRIDE":
            statement.value = ast.Constant(str(root))
            replacements["ROOT_OVERRIDE"] += 1
        elif target.id == "DEST":
            statement.value = ast.Call(
                func=ast.Name(id="Path", ctx=ast.Load()),
                args=[ast.Constant(str(destination))], keywords=[]
            )
            replacements["DEST"] += 1
    if replacements != {"ROOT_OVERRIDE": 1, "DEST": 1}:
        raise RuntimeError(f"No se pudo identificar de manera única ROOT_OVERRIDE/DEST: {replacements}")
    ast.fix_missing_locations(tree)
    return tree


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--historical-root", type=Path, required=True,
                        help="Ruta histórica Tesis4, solo lectura")
    parser.add_argument("--worktree", type=Path, default=Path.cwd(),
                        help="Carpeta del worktree Tesis5_STUDENT (por defecto: cwd)")
    parser.add_argument("--run", action="store_true",
                        help="Ejecutar la celda después de completar todas las comprobaciones")
    args = parser.parse_args()

    try:
        root = args.historical_root.expanduser().resolve(strict=True)
        worktree = args.worktree.expanduser().resolve(strict=True)
        if not root.is_dir() or not worktree.is_dir():
            raise RuntimeError("Las rutas de origen y worktree deben ser directorios existentes.")
        if worktree == root or worktree.is_relative_to(root) or root.is_relative_to(worktree):
            raise RuntimeError("Origen y destino no pueden estar uno dentro del otro.")
        notebook = worktree / "experiments" / "INTEGRACION_01_CERT.ipynb"
        source = load_original_code(notebook)
        report_parent = (worktree / "reports" / "H2B2A7_INTEGRACION_01").resolve()
        if report_parent.is_relative_to(root) or not report_parent.is_relative_to(worktree):
            raise RuntimeError("El directorio de informes no está confinado al worktree Student.")
        tag = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
        destination = report_parent / ("H2B2A7_INTEGRACION_01_CERT_" + tag)
        if destination.exists():
            raise RuntimeError("La carpeta de salida ya existe. No se sobrescribirá.")
        patched_tree = redirect_in_memory(source, root, destination)

        print("INTEGRACION-01 | PREPARACION CONTROLADA")
        print("Notebook:", notebook)
        print("SHA256 del código: OK", EXPECTED_CODE_SHA256)
        print("Histórico (entradas solamente):", root)
        print("Salida exclusiva:", destination)
        print("Fuentes esperadas:", len(SOURCES))
        missing = []
        mismatched = []
        for key, relative in SOURCES.items():
            location = root / relative
            if not location.is_file():
                missing.append(key)
                print("FALTA", key, relative)
                continue
            if key in EXPECTED_HISTORICAL_SHA256:
                actual = file_sha256(location)
                if actual != EXPECTED_HISTORICAL_SHA256[key]:
                    mismatched.append(key)
                    print("SHA_NO_COINCIDE", key, actual)
                else:
                    print("SHA_OK", key)
            else:
                print("PRESENTE_SIN_SHA_PREVIO", key, file_sha256(location))
        print(f"Fuentes localizadas: {len(SOURCES) - len(missing)}/{len(SOURCES)}")
        print(f"SHA previos correctos: {len(EXPECTED_HISTORICAL_SHA256) - len(mismatched)}/{len(EXPECTED_HISTORICAL_SHA256)}")
        if missing or mismatched:
            raise RuntimeError(f"No se ejecutará: faltantes={missing}, hashes_diferentes={mismatched}")
        for module in ("numpy", "qiskit"):
            if importlib.util.find_spec(module) is None:
                raise RuntimeError(f"Dependencia no disponible: {module}")
        print("NumPy y Qiskit: localizables")
        if not args.run:
            print("PREFLIGHT OK. No se ejecutó ninguna celda ni se escribieron informes.")
            print("Para ejecutar: agrega --run al mismo comando.")
            return 0
        print("EJECUTANDO CERTIFICACION MATEMATICA CONGELADA 1E/1F; SIN REENTRENAR NI QPU")
        # The verified original code is compiled with only two in-memory AST
        # substitutions. All report writes in this specific signed source use DEST.
        scope = {"__name__": "__main__", "__file__": str(notebook)}
        exec(compile(patched_tree, str(notebook), "exec"), scope, scope)
        print("RESULTADO EN:", destination)
        return 0
    except Exception as error:
        print("ERROR:", error, file=sys.stderr)
        return 1

if __name__ == "__main__":
    raise SystemExit(main())
