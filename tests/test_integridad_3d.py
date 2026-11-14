"""Pruebas sin dependencias externas de la auditoria de consolidacion."""
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location('h2b2a7_3d', ROOT/'scripts'/'auditar_sintesis_3d.py')
mod = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(mod)

class Auditoria3DTests(unittest.TestCase):
    def test_sha_hexadecimal(self):
        self.assertEqual(mod.sha(b'abc'),
                         'ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad')

    def test_manifesto_autoreferencia_rechazada(self):
        with tempfile.TemporaryDirectory() as base:
            root=Path(base)
            # A fake first stage is enough to enforce the self-reference rule.
            sub, manifest, _ = mod.STAGES['3A']
            folder = root/mod.BASE/sub
            folder.mkdir(parents=True)
            (folder/manifest).write_text(json.dumps({'productos_sha256':{manifest:'0'*64}}),encoding='utf-8')
            with self.assertRaises(mod.AuditError):
                mod.audit(root)

    def test_rechaza_manifiesto_nombre_con_directorio(self):
        with tempfile.TemporaryDirectory() as base:
            root=Path(base)
            sub, manifest, _ = mod.STAGES['3A']
            folder = root/mod.BASE/sub
            folder.mkdir(parents=True)
            (folder/manifest).write_text(json.dumps({'productos_sha256':{'../extra':'0'*64}}),encoding='utf-8')
            with self.assertRaises(mod.AuditError):
                mod.audit(root)

    def test_rechaza_hash_incorrecto(self):
        with tempfile.TemporaryDirectory() as base:
            root=Path(base)
            path=root/'evidencia.csv';path.write_bytes(b'contenido')
            with self.assertRaises(mod.AuditError):
                mod.check_sha(root,path,'0'*64)

    def test_git_lf_reconstruye_sha_crlf_original(self):
        with tempfile.TemporaryDirectory() as base:
            root = Path(base)
            path = root / 'evidencia.csv'
            git_blob = b'columna\nvalor\n'
            path.write_bytes(git_blob)
            original = b'columna\r\nvalor\r\n'
            with mock.patch.object(mod, 'committed_bytes', return_value=git_blob):
                self.assertEqual(mod.check_sha(root, path, mod.sha(original)),
                                 'BLOB_GIT_CRLF_RECONSTRUIDO_SHA_ORIGINAL')

    def test_git_lf_rechaza_contenido_alterado(self):
        with tempfile.TemporaryDirectory() as base:
            root = Path(base)
            path = root / 'evidencia.csv'
            altered = b'columna\nvalor_alterado\n'
            path.write_bytes(altered)
            with mock.patch.object(mod, 'committed_bytes', return_value=altered):
                with self.assertRaises(mod.AuditError):
                    mod.check_sha(root, path, mod.sha(b'columna\r\nvalor\r\n'))

    def test_integracion_sintetica_22_productos(self):
        with tempfile.TemporaryDirectory() as base:
            root = Path(base)
            specs = {
                '3A': (4, {'filas_scores_outer':1497,'interseccion_indices_inner_y_outer':0,
                            'inner_por_modelo':{'STUDENT_1E':1198,'STUDENT_1F':1198},
                            'etiquetas_en_csv_student':False}),
                '3B': (4, {'n_pares':7,'n_outer':1497,'estado':'DESCRIPTIVO_POST_APERTURA',
                            'auc_out':{'SAFE_ideal':0.925}}),
                '3C': (4, {'n_materiales':1198,'n_filas':2396,
                            'resultado_por_modelo':{'STUDENT_1E':{'error_absoluto_score':{'media':0.0149}},
                                                     'STUDENT_1F':{'error_absoluto_score':{'media':0.0156}}}}),
                '3C3':(5, {'n_materiales':1198,'n_pares':717003,
                             'comparaciones':[{'comparacion':'OBJETIVO_B vs STUDENT_1E',
                                               'spearman':0.91,'kendall_tau_b':0.74,
                                               'fraccion_inversiones_total':0.13}]}),
                '3C4':(5, {'n_heads_student':2,'puertas_U_en_dos_decoders':504,
                             'costos_end_to_end_equivalentes':False,'QPU_shots_ejecutados':0,
                             'RXX_en_dos_decoders':96,'bases_qwc24':24,'bases_qwc64':64,
                             'shot_incremental_qwc24_qwc64':10000,
                             'shots_logicos_plan_referencia_total':110000}),
            }
            for tag,(n, obj) in specs.items():
                sub, manifest, summary = mod.STAGES[tag]
                folder = root / mod.BASE / sub
                folder.mkdir(parents=True)
                product = {summary: (json.dumps(obj)+'\n').encode('utf-8')}
                for i in range(n-1):
                    product[f'extra_{i}.csv'] = f'{tag},{i}\n'.encode('utf-8')
                for name, data in product.items():
                    (folder/name).write_bytes(data)
                (folder/manifest).write_text(json.dumps({'productos_sha256':{name:mod.sha(data)
                        for name,data in product.items()}}),encoding='utf-8')
            result, hashes = mod.audit(root)
            self.assertEqual(len(hashes),22)
            self.assertTrue(all(row['modo_verificacion']=='ARCHIVO_LOCAL' for row in hashes))
            self.assertEqual(result['n_productos_sha_verificados'],22)
            self.assertEqual(result['recursos']['student_puertas_dos_U'],504)

    def test_sintesis_contiene_reservas(self):
        s={'n_etapas':5,'n_productos_sha_verificados':22,'n_productos_sha_esperados':22,
           'n_locales_exactos':22,'n_blob_git_por_conversion_checkout':0,
           'auc_retrospectivas':{'SAFE':0.92},'ranking_inner_val':[],
           'score_error_abs_medio_inner':{},
           'recursos':{'student_puertas_dos_U':504,'student_RXX_dos_U':96,
                       'qwc24_bases':24,'qwc64_bases':64,'qwc_shots_incrementales':10000,
                       'qwc_referencia_shots_logicos':110000},
           'limites':['No hay costo end-to-end equivalente.']}
        rendered=mod.make_report(s)
        self.assertIn('INNER VAL',rendered)
        self.assertIn('OUTER HOLD',rendered)
        self.assertIn('No hay costo end-to-end equivalente',rendered)

if __name__=='__main__':
    unittest.main()
