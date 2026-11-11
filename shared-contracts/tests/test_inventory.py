import base64
import copy
import hashlib
import json
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from validate import Invalid, ROOT, SCHEMA, canonical, parse, shape, verify


class InventoryTests(unittest.TestCase):
    def setUp(self):
        self.raw = (ROOT / 'fixtures/complete.manifest.json').read_bytes()
        self.manifest = parse(self.raw)
        self.members = {p: base64.b64decode(v, validate=True) for p, v in
                        json.loads((ROOT / 'fixtures/members.json').read_text()).items()}

    def test_checked_in_examples_and_fingerprints(self):
        identity = json.loads((ROOT / 'fixtures/identity.json').read_text())
        self.assertEqual(identity['schema_sha256'], hashlib.sha256(
            (ROOT / 'schemas/workspace-capture-v0-1.schema.json').read_bytes()).hexdigest())
        self.assertEqual(verify(self.raw, self.members), identity['manifest_reference'])
        for name, expected in identity['expected'].items():
            with self.subTest(name=name):
                raw = (ROOT / 'fixtures' / name).read_bytes()
                if expected == 'accepted':
                    verify(raw, self.members)
                else:
                    with self.assertRaisesRegex(Invalid, '^' + expected + '$'):
                        verify(raw, self.members)

    def test_required_files_and_tampering(self):
        for path in self.members:
            with self.subTest(path=path):
                members = self.members.copy()
                del members[path]
                with self.assertRaisesRegex(Invalid, 'required_inventory'):
                    verify(self.raw, members)
                members = self.members.copy()
                members[path] += b'x'
                with self.assertRaisesRegex(Invalid, 'integrity_failed'):
                    verify(self.raw, members)
                members[path] = bytes([self.members[path][0] ^ 1]) + self.members[path][1:]
                with self.assertRaisesRegex(Invalid, 'integrity_failed'):
                    verify(self.raw, members)

    def test_self_hash_is_external(self):
        self.assertNotIn('manifest.json', self.members)
        with self.assertRaisesRegex(Invalid, 'required_inventory'):
            verify(self.raw, dict(self.members, **{'manifest.json': self.raw}))
        changed = copy.deepcopy(self.manifest)
        changed['warnings'] = ['Synthetic warning']
        self.assertNotEqual(verify(canonical(changed), self.members)['sha256'],
                            verify(self.raw, self.members)['sha256'])
        self.assertEqual(changed['artifacts'], self.manifest['artifacts'])

    def test_paths_inventory_order_duplicates_and_bounds(self):
        for path in ['../page.mhtml', '/page.mhtml', 'evidence\\page.mhtml',
                     'evidence/./page.mhtml', 'Evidence/page.mhtml', 'manifest.json']:
            m = copy.deepcopy(self.manifest)
            m['artifacts'][0]['path'] = path
            with self.subTest(path=path), self.assertRaises(Invalid):
                verify(canonical(m), self.members)
        variants = []
        m = copy.deepcopy(self.manifest); m['artifacts'].reverse(); variants.append(m)
        m = copy.deepcopy(self.manifest); m['artifacts'][1] = m['artifacts'][0]; variants.append(m)
        m = copy.deepcopy(self.manifest); m['extra'] = 1; variants.append(m)
        m = copy.deepcopy(self.manifest); m['artifacts'][0]['size_bytes'] = True; variants.append(m)
        m = copy.deepcopy(self.manifest); m['artifacts'][0]['size_bytes'] = 0; variants.append(m)
        m = copy.deepcopy(self.manifest); m['artifacts'][0]['size_bytes'] = 104857601; variants.append(m)
        m = copy.deepcopy(self.manifest); m['warnings'] = ['x' * 1025]; variants.append(m)
        m = copy.deepcopy(self.manifest); m['deferred_formats'] = []; variants.append(m)
        m = copy.deepcopy(self.manifest); m['artifacts'][0]['sha256'] += '\n'; variants.append(m)
        m = copy.deepcopy(self.manifest); m['capture_id'] += '\n'; variants.append(m)
        m = copy.deepcopy(self.manifest); m['capture_id'] = None; variants.append(m)
        for m in variants:
            with self.subTest(m=m), self.assertRaises(Invalid):
                verify(canonical(m), self.members)
        with self.assertRaisesRegex(Invalid, 'manifest_limit'):
            verify(b' ' * 65537, {})

    def test_json_bytes_and_null_semantics(self):
        for raw in [b'{"a":1,"a":2}\n', b'{"a":1.0}\n', b'{"a":NaN}\n',
                    b'{"a":Infinity}\n', b'\xef\xbb\xbf{}\n', b'{}', b'{}\r\n',
                    b'{ "a":1}\n', b'{"b":1,"a":2}\n', b'{"a":"\\ud800"}\n']:
            with self.subTest(raw=raw), self.assertRaises(Invalid):
                parse(raw)
        raw = canonical({'z': None, 'é': 'unchanged e\u0301', 'a': True})
        self.assertEqual(raw, b'{"a":true,"z":null,"\xc3\xa9":"unchanged e\xcc\x81"}\n')
        self.assertIsNone(parse(raw)['z'])
        self.assertNotIn('unknown', parse(raw))
        for value in [1.0, float('nan'), {1: 'bad'}]:
            with self.assertRaises(Invalid):
                canonical(value)

    def test_schema_vocabulary_fails_closed(self):
        with self.assertRaisesRegex(Invalid, 'unsupported_schema'):
            shape({}, {'not': {}})
        shape(self.manifest, SCHEMA)


if __name__ == '__main__':
    unittest.main()
