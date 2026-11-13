#!/usr/bin/env python3
"""H2B2A7 3D: auditoria offline de manifiestos y sintesis retrospectiva.

No toca Tesis4, no entrena, no llama servicios. --write solo crea una carpeta
nueva bajo reports/H2B2A7_CONSOLIDACION. Sin argumentos: solo lectura.
"""
from __future__ import annotations
import argparse
import csv
import hashlib
import json
import math
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

STAGES = {
    "3A": ("H2B2A7_3A_INVENTARIO_20261112T175419755767Z", "3A_MANIFIESTO_SHA256.json", "3A_DIAGNOSTICO.json"),
    "3B": ("H2B2A7_3B_ANALISIS_20261112T180620743124Z", "3B_MANIFIESTO_SHA256.json", "3B_DIAGNOSTICO.json"),
    "3C": ("H2B2A7_3C_OBSERVABLES_20261113T005505646168Z", "3C_MANIFIESTO_SHA256.json", "3C_RESUMEN.json"),
    "3C3": ("H2B2A7_3C3_RANKING_20261113T010127276174Z", "3C3_MANIFIESTO_SHA256.json", "3C3_RESUMEN.json"),
    "3C4": ("H2B2A7_3C4_RECURSOS_20261113T010927869588Z", "3C4_MANIFIESTO_SHA256.json", "3C4_RESUMEN.json"),
}

BASE = Path("reports/H2B2A7_CONSOLIDACION")

class AuditError(RuntimeError):
    pass


def read_json(path: Path):
    try:
        return json.loads(path.read_text(encoding="utf-8-sig"))
    except (ValueError, OSError) as ex:
        raise AuditError(f"No se pudo leer {path}: {ex}") from ex


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def committed_bytes(root: Path, relative: Path):
    try:
        return subprocess.run(
            ["git", "-C", str(root), "show", "HEAD:" + relative.as_posix()],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True
        ).stdout
    except (OSError, subprocess.CalledProcessError):
        return None


def check_sha(root: Path, file_path: Path, expected: str):
    # Check exact bytes on disk first. Git is only consulted to distinguish
    # harmless Windows CRLF checkout conversion from committed evidence.
    disk = file_path.read_bytes()
    if sha(disk) == expected:
        return "ARCHIVO_LOCAL"
    rel = file_path.relative_to(root)
    git_data = committed_bytes(root, rel)
    if git_data is not None and sha(git_data) == expected:
        return "BLOB_GIT_COINCIDE_LOCAL_DIFIERE"  # requires reporting distinction
    raise AuditError(f"SHA NO COINCIDE: {rel} (manifiesto={expected}, local={sha(disk)})")


def require(condition, message):
    if not condition:
        raise AuditError(message)


def as_int(v, title):
    require(type(v) is int, f"{title}: se esperaba entero")
    return v


def as_num(v, title):
    require(type(v) in (int, float) and math.isfinite(v), f"{title}: numero no valido")
    return float(v)


def audit(root: Path):
    results = {}
    hashes = []
    for tag, (subdir, manifest, summary) in STAGES.items():
        folder = root / BASE / subdir
        require(folder.is_dir(), f"Falta carpeta {tag}: {folder}")
        manifest_path = folder / manifest
        m = read_json(manifest_path)
        products = m.get("productos_sha256")
        require(isinstance(products, dict) and products, f"{tag}: manifiesto vacio/invalido")
        require(manifest not in products, f"{tag}: manifiesto autoreferenciado")
        for filename, expected in products.items():
            require(isinstance(filename, str) and Path(filename).name == filename,
                    f"{tag}: nombre inseguro en manifiesto")
            require(isinstance(expected, str) and len(expected) == 64 and all(c in '0123456789abcdef' for c in expected),
                    f"{tag}: hash invalido {filename}")
            fp = folder / filename
            require(fp.is_file(), f"{tag}: archivo ausente {fp}")
            mode = check_sha(root, fp, expected)
            hashes.append(dict(etapa=tag, archivo=str(fp.relative_to(root)).replace('\\', '/'),
                               modo_verificacion=mode, sha256_esperado=expected))
        require(summary in products, f"{tag}: resumen no incluido en manifiesto")
        results[tag] = read_json(folder / summary)
    require(len(hashes) == 22, f"Esperabamos 22 productos verificados, hay {len(hashes)}")

    a, b, c, d, e = (results[k] for k in ("3A", "3B", "3C", "3C3", "3C4"))
    require(as_int(a["filas_scores_outer"], '3A outer') == 1497, "3A: conteo OUTER inesperado")
    require(as_int(a["interseccion_indices_inner_y_outer"], '3A overlap') == 0,
            "INNER/OUTER aparecen mezclados")
    require(as_int(a["inner_por_modelo"]["STUDENT_1E"], '3A inner E') == 1198, "INNER 1E no coincide")
    require(as_int(a["inner_por_modelo"]["STUDENT_1F"], '3A inner F') == 1198, "INNER 1F no coincide")
    require(a["etiquetas_en_csv_student"] is False, "Se declaran etiquetas Student no certificadas")
    require(as_int(b["n_pares"], '3B pares') == 7, "3B: pares inesperados")
    require(as_int(b["n_outer"], '3B OUTER') == 1497, "3B: OUTER inesperado")
    require(b["estado"] == "DESCRIPTIVO_POST_APERTURA", "3B: cambia estado de evidencia")
    require(as_int(c["n_materiales"], '3C muestras') == 1198, "3C: muestras inesperadas")
    require(as_int(c["n_filas"], '3C filas') == 2396, "3C: filas inesperadas")
    require(as_int(d["n_materiales"], '3C3 muestras') == 1198, "3C3: muestras inesperadas")
    require(as_int(d["n_pares"], '3C3 pares') == 717003, "3C3: pares inesperados")
    require(as_int(e["n_heads_student"], '3C4 cabezales') == 2, "3C4: cabezales inesperados")
    require(as_int(e["puertas_U_en_dos_decoders"], '3C4 puertas') == 504, "3C4: puertas inesperadas")
    require(e["costos_end_to_end_equivalentes"] is False, "3C4: falsa comparabilidad integral")
    require(as_int(e["QPU_shots_ejecutados"], '3C4 shots') == 0, "3C4: shots no nulos")

    # Purely retrospective summary: do not compute AUC from different splits.
    summary = dict(
        esquema="H2B2A7_3D_SINTESIS_v1",
        alcance="OFFLINE_DESCRIPTIVO_SIN_EVALUACION_NUEVA",
        n_etapas=len(STAGES),
        n_productos_sha_esperados=22,
        n_productos_sha_verificados=len(hashes),
        n_locales_exactos=sum(h['modo_verificacion'] == "ARCHIVO_LOCAL" for h in hashes),
        n_blob_git_por_conversion_checkout=sum(h['modo_verificacion'] != "ARCHIVO_LOCAL" for h in hashes),
        outer_hold_previamente_abierto=True,
        auc_retrospectivas=b["auc_out"],
        ranking_inner_val=[{k: row[k] for k in ("comparacion", "spearman", "kendall_tau_b", "fraccion_inversiones_total")}
                           for row in d["comparaciones"]],
        score_error_abs_medio_inner={model: as_num(c["resultado_por_modelo"][model]["error_absoluto_score"]["media"], model)
                                    for model in ("STUDENT_1E", "STUDENT_1F")},
        recursos=dict(student_puertas_dos_U=e["puertas_U_en_dos_decoders"],
                      student_RXX_dos_U=e["RXX_en_dos_decoders"],
                      qwc24_bases=e["bases_qwc24"],qwc64_bases=e["bases_qwc64"],
                      qwc_shots_incrementales=e["shot_incremental_qwc24_qwc64"],
                      qwc_referencia_shots_logicos=e["shots_logicos_plan_referencia_total"]),
        limites=[
            "Los resultados OUTER son retrospectivos y el conjunto ya habia sido abierto.",
            "Las AUC OUTER no se comparan directamente con AUC INNER VAL de Student.",
            "Las 22 huellas verifican productos archivados, no una reevaluacion independiente.",
            "El ranking del score objetivo B no es una etiqueta FM/AFM.",
            "Los shots parciales de QWC y las puertas de dos U Student no son costos end-to-end equivalentes.",
            "No hubo ejecucion QPU ni entrenamiento nuevo.",
        ],
    )
    return summary, hashes


def make_report(s):
    rows = [
        "# H2B2A7 — Síntesis científica 3D (retrospectiva)", "",
        "## Alcance y trazabilidad", "",
        f"- Etapas auditadas: {s['n_etapas']} (3A, 3B, 3C, 3C.3, 3C.4).",
        f"- Productos verificados: {s['n_productos_sha_verificados']}/{s['n_productos_sha_esperados']} SHA-256.",
        f"- Coincidencia exacta local: {s['n_locales_exactos']}; coincidencia con blob Git por diferencia de checkout: {s['n_blob_git_por_conversion_checkout']}.",
        "- No se consultaron checkpoints locales de Tesis4 ni se ejecutaron circuitos.", "",
        "## Predicción descriptiva: OUTER HOLD archivado", "",
        "| Modelo | AUC retrospectiva |", "|---|---:|",
    ]
    for model, auc in s["auc_retrospectivas"].items():
        rows.append(f"| {model} | {auc:.8f} |")
    rows += ["", "Estas AUC pertenecen al OUTER HOLD ya examinado: no son validación independiente nueva.",
             "No comparar estas AUC con las AUC Student de INNER VAL como prueba pareada.", "",
             "## Ranking y observables: INNER VAL previamente examinado", "",
             "| Comparación | Spearman | Kendall τ-b | Pares invertidos |",
             "|---|---:|---:|---:|"]
    for r in s["ranking_inner_val"]:
        rows.append(f"| {r['comparacion']} | {r['spearman']:.6f} | {r['kendall_tau_b']:.6f} | {100*r['fraccion_inversiones_total']:.3f}% |")
    rows += ["", "| Student | Error absoluto medio de score |", "|---|---:|"]
    for name, value in s["score_error_abs_medio_inner"].items():
        rows.append(f"| {name} | {value:.8f} |")
    rows += ["", "En 3C se reconstruyó O=U†DU; la discrepancia matricial no equivale a discrepancia de expectativa.",
             "La condición de margen de 3C.3 es suficiente para preservar el orden de un par, pero se aplicó a posteriori.",
             "", "## Recursos conocidos, sin costos físicos completos", ""]
    r=s["recursos"]
    rows += [f"- Student: {r['student_puertas_dos_U']} puertas en dos decodificadores U, de las cuales {r['student_RXX_dos_U']} son RXX.",
             f"- QWC24/QWC64: {r['qwc24_bases']}/{r['qwc64_bases']} bases; {r['qwc_shots_incrementales']} shots incrementales rho6.",
             f"- QWC de referencia: {r['qwc_referencia_shots_logicos']} shots lógicos planificados, no shots físicos ejecutados.",
             "- No está certificado costo end-to-end comparable entre Student y QWC.", "",
             "## Reservas metodológicas", ""]
    rows += ["- " + x for x in s["limites"]]
    rows += ["", "## Próximas validaciones (no realizadas aquí)", "",
             "Documentar procedencia histórica pendiente de 1F/OPS; diseñar costo end-to-end bajo mismo hardware; preparar protocolo de evaluación externa nueva sin reutilizar OUTER.", ""]
    return '\n'.join(rows)


def atomic_write_unique(folder: Path, files: dict[str, bytes]):
    folder.mkdir(parents=True, exist_ok=False)
    for name, data in files.items():
        (folder / name).write_bytes(data)


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1], help="Raiz del Worktree")
    p.add_argument("--write", action="store_true", help="Crear reporte nuevo de sintesis")
    args = p.parse_args(argv)
    root = args.root.resolve()
    try:
        summary, hashes = audit(root)
        print("H2B2A7 | 3D | AUDITORIA OFFLINE")
        print(f"Integridad: {len(hashes)}/22 productos verificados en 5 etapas")
        print(f"Hashes de archivo local: {summary['n_locales_exactos']} | Coincidencia de blob Git: {summary['n_blob_git_por_conversion_checkout']}")
        print("Separacion INNER/OUTER: OK | Costos parciales: OK | Sin entrenamiento ni QPU")
        if not args.write:
            print("PREFLIGHT OK. Sin escrituras. Para generar sintesis, usa --write")
            return 0
        stamp = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
        dest = root / BASE / ('H2B2A7_3D_SINTESIS_'+stamp)
        summary['fecha_creacion_utc'] = datetime.now(timezone.utc).isoformat()
        payload = {
            '3D_RESUMEN.json':(json.dumps(summary,ensure_ascii=False,indent=2)+'\n').encode('utf-8'),
            '3D_INFORME.md':make_report(summary).encode('utf-8'),
            '3D_INTEGRIDAD_PRODUCTOS.csv':None,
        }
        import io
        buf = io.StringIO(newline='')
        w=csv.DictWriter(buf,fieldnames=['etapa','archivo','modo_verificacion','sha256_esperado']);w.writeheader();w.writerows(hashes)
        payload['3D_INTEGRIDAD_PRODUCTOS.csv']=buf.getvalue().encode('utf-8-sig')
        manifest={'etapa':'H2B2A7-FASE-3D','productos_sha256':{n:sha(v) for n,v in payload.items()},
                  'nota':'Manifiesto no autoreferenciado; informes anteriores permanecen intactos.'}
        payload['3D_MANIFIESTO_SHA256.json']=(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n').encode('utf-8')
        atomic_write_unique(dest, payload)
        print('SINTESIS GENERADA:',dest)
        print('Archivos nuevos: 4 | Evidencia anterior intacta')
        return 0
    except (AuditError, OSError, KeyError, TypeError, ValueError) as ex:
        print('BLOQUEADO:',str(ex),file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
