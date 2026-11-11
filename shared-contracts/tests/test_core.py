import base64
import copy
import json
from pathlib import Path
import sys
import unittest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from build_core import generated as core_generated
from build_api import generated as api_generated, OPERATIONS
from build_core_fixtures import generated as fixture_generated
from core import validate, verify_export, checksums
from validate import Invalid, canonical
from api import validate as dto, envelope, validate_error
ROOT=Path(__file__).resolve().parents[1]


class CoreTests(unittest.TestCase):
    def fixture(self,name):
        return json.loads((ROOT/f'fixtures/core/{name}.json').read_text())

    def package(self,name='export-default'):
        return {p:base64.b64decode(raw) for p,raw in self.fixture(name).items()}

    def test_generated_files(self):
        for generate in [core_generated,api_generated,fixture_generated]:
            for path,raw in generate().items():
                self.assertEqual((ROOT/path).read_bytes(),raw,path)

    def test_positive_core_examples(self):
        for name in ['capture-metadata-1','legacy-import-1','job-1','attempt-1','job-event-1']:
            validate(canonical(self.fixture(name)),name)
        for name in ['export-default','export-pdf']:
            verify_export(self.package(name))

    def test_export_required_inventory_and_digests(self):
        members=self.package()
        for path in members:
            changed=members.copy();del changed[path]
            with self.subTest(path=path),self.assertRaises(Invalid): verify_export(changed)
            changed=members.copy();changed[path]+=b'x'
            with self.subTest(tampered=path),self.assertRaises(Invalid): verify_export(changed)
        members=self.package('export-pdf');del members['receipt.pdf']
        with self.assertRaisesRegex(Invalid,'required_inventory'): verify_export(members)
        members=self.package();members['../extra']=b'x'
        with self.assertRaisesRegex(Invalid,'unsafe_path'): verify_export(members)
        members=self.package();members['README.TXT']=members['README.txt']
        with self.assertRaisesRegex(Invalid,'duplicate_path'): verify_export(members)

    def test_export_self_hash_and_checksum_coverage(self):
        members=self.package()
        manifest=json.loads(members['manifest.json'])
        self.assertNotIn('manifest.json',[a['path'] for a in manifest['artifacts']])
        self.assertNotIn('SHA256SUMS',[a['path'] for a in manifest['artifacts']])
        self.assertIn(b'  manifest.json\n',members['SHA256SUMS'])
        self.assertIn(b'  capture/manifest.json\n',members['SHA256SUMS'])
        self.assertNotIn(b'  SHA256SUMS\n',members['SHA256SUMS'])
        members['SHA256SUMS']=checksums({'README.txt':members['README.txt']})
        with self.assertRaisesRegex(Invalid,'checksum_coverage'): verify_export(members)

    def test_legacy_unknown_is_not_local_success(self):
        value=self.fixture('legacy-import-1')
        self.assertIsNone(value['claimed_capture_time'])
        for changes in [{'profile':'workspace-capture-v0/1'},{'publication_eligible':True},
                        {'provenance_notes':[]},{'outcome':'complete'}]:
            with self.subTest(changes=changes),self.assertRaises(Invalid):
                validate(canonical(dict(value,**changes)),'legacy-import-1')

    def test_disclosure_and_event_state(self):
        package=self.package();meta=json.loads(package['export.json'])
        for key,value in [('actor',{'id':'00000000-0000-4000-8000-000000000003','label':'Synthetic'}),
                          ('editorial_revision',1),('include_actor',True),('include_editorial',True)]:
            with self.subTest(key=key),self.assertRaises(Invalid):
                validate(canonical(dict(meta,**{key:value})),'export-metadata-v0-1')
        event=self.fixture('job-event-1');event['kind']='terminal'
        with self.assertRaisesRegex(Invalid,'terminal_state'): validate(canonical(event),'job-event-1')
        job=self.fixture('job-1');job['state']='retry_wait'
        with self.assertRaisesRegex(Invalid,'retry_time'): validate(canonical(job),'job-1')

    def test_checked_in_api_examples(self):
        for name,value in json.loads((ROOT/'fixtures/api-positive.json').read_text()).items():
            with self.subTest(name=name): dto(canonical(value),name)
        for case in json.loads((ROOT/'fixtures/api-negative.json').read_text()):
            with self.subTest(case=case),self.assertRaisesRegex(Invalid,'^'+case['expected']+'$'):
                dto(canonical(case['value']),case['dto'])

    def test_api_examples_and_envelope(self):
        dto(b'{ \"url\": \"https://example.org/article\" }','CaptureSubmit')
        dto(canonical({'url':'https://example.org/article','tags':['synthetic']}),'CaptureSubmit')
        for value in [{'url':'https://example.org','unknown':1},{'url':'https://example.org','condition_type':'css'},
                      {'url':'https://example.org','rationale':'x'*2049}]:
            with self.assertRaises(Invalid): dto(canonical(value),'CaptureSubmit')
        self.assertEqual(envelope('post',False,True), (401,'session_required'))
        self.assertEqual(envelope('post',True,False), (403,'csrf_failed'))
        self.assertEqual(envelope('post',True,True,required_key=True), (422,'validation_failed'))
        self.assertIsNone(envelope('post',True,True,'synthetic-key',True))
        error={'error':{'code':'revision_conflict','message':'Reload current revision.','request_id':'synthetic','fields':{}}}
        validate_error(canonical(error),409)
        with self.assertRaisesRegex(Invalid,'error_status'): validate_error(canonical(error),404)

    def test_openapi_security_and_generated_refs(self):
        doc=json.loads(api_generated()['openapi/core-commands.openapi.json'])
        for method,path,request,response,status,key,admin in OPERATIONS:
            operation=doc['paths'][path][method]
            self.assertEqual(operation['security'],[{'sessionCookie':[]}])
            params={p['name']:p for p in operation['parameters']}
            if method!='get': self.assertTrue(params['X-CSRF-Token']['required'])
            if key: self.assertTrue(params['Idempotency-Key']['required'])
            self.assertEqual(operation['x-required-role'],'admin' if admin else 'editor')
            if response: self.assertIn(response,doc['components']['schemas'])


if __name__=='__main__': unittest.main()
