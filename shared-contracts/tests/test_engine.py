import copy
import hashlib
import json
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from build_engine import artifacts
from engine import ROOT, validate
from validate import Invalid, canonical


class EngineTests(unittest.TestCase):
    def setUp(self):
        self.request = validate((ROOT/'fixtures/engine/request.json').read_bytes(), 'request')
        self.complete = json.loads((ROOT/'fixtures/engine/complete.json').read_text())

    def test_generated_artifacts_and_fingerprints(self):
        for name, raw in artifacts().items():
            self.assertEqual((ROOT/name).read_bytes(), raw, name)
        identity = json.loads((ROOT/'fixtures/engine/identity.json').read_text())
        for name, digest in identity['sha256'].items():
            self.assertEqual(hashlib.sha256((ROOT/name).read_bytes()).hexdigest(), digest, name)

    def test_examples(self):
        identity = json.loads((ROOT/'fixtures/engine/identity.json').read_text())
        for name, case in identity['expected'].items():
            with self.subTest(name=name):
                if case['expected'] == 'accepted':
                    validate((ROOT/name).read_bytes(), case['kind'], self.request)
                else:
                    with self.assertRaisesRegex(Invalid, '^'+case['expected']+'$'):
                        validate((ROOT/name).read_bytes(), case['kind'], self.request)

    def test_request_rejections(self):
        cases = []
        def changed(key, value):
            r = copy.deepcopy(self.request); r[key] = value; cases.append(r)
        changed('contract', 'capture-engine/2')
        changed('url', 'https://synthetic:secret@example.org/')
        changed('url', 'https://example.org:8080/')
        changed('deadline', '2026-02-30T00:00:00Z')
        changed('generation', True)
        r = copy.deepcopy(self.request); r['database_token'] = 'synthetic'; cases.append(r)
        for condition in [{'type':'css', 'value':None}, {'type':'text', 'value':''}, {'type':'load', 'value':'unexpected'}]:
            r = copy.deepcopy(self.request); r['options']['condition'] = condition; cases.append(r)
        for r in cases:
            with self.subTest(request=r), self.assertRaises(Invalid):
                validate(canonical(r), 'request')
        with self.assertRaisesRegex(Invalid, 'message_limit'):
            validate(b' ' * 262145, 'request')

    def test_result_authority_and_time(self):
        for key, value in [('attempt_id', self.request['job_id']), ('requested_url', 'https://example.org/other'),
                           ('finished_at', '2026-11-09T12:02:01Z'), ('started_at', '2026-11-09T12:00:02Z'),
                           ('main_document_status', None), ('error_code', 'browser_failed')]:
            r = dict(self.complete, **{key:value})
            with self.subTest(key=key), self.assertRaises(Invalid):
                validate(canonical(r), 'result', self.request)
        with self.assertRaisesRegex(Invalid, 'request_required'):
            validate(canonical(self.complete), 'result')
        r = copy.deepcopy(self.complete); r['outputs'][0]['path'] = 'evidence/screenshot.png'
        with self.assertRaises(Invalid):
            validate(canonical(r), 'result', self.request)

    def test_hints_do_not_establish_integrity(self):
        r = copy.deepcopy(self.complete)
        r['outputs'][0]['sha256_hint'] = '0' * 64
        validate(canonical(r), 'result', self.request)
        # This parser deliberately has no captured bytes or trusted digest authority.


if __name__ == '__main__':
    unittest.main()
