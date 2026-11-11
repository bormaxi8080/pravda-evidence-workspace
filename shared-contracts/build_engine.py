"""Authoritative capture-engine/1 definitions; generate JSON schemas and fixtures."""
import argparse
import base64
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DRAFT = 'https://json-schema.org/draft/2020-12/schema'


def string(limit=1024, **extra):
    return dict(type='string', minLength=1, maxLength=limit, **extra)


def integer(low, high):
    return dict(type='integer', minimum=low, maximum=high)


def obj(**fields):
    return dict(type='object', additionalProperties=False, required=list(fields), properties=fields)


def array(item, limit):
    return dict(type='array', items=item, maxItems=limit)


def nullable(schema):
    return {'anyOf': [schema, {'type': 'null'}]}


UUID = dict(
    type='string', minLength=36, maxLength=36,
    pattern='^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$')
TIME = string(30, pattern=r'^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d{1,6})?Z$')
URL = string(8192, pattern=r'^https?://[^\s]+$')
VERSION = string(128)
WARNINGS = array(string(), 64)
ERRORS = ['target_denied', 'invalid_options', 'navigation_timeout', 'condition_timeout',
          'browser_failed', 'resource_limit', 'output_incomplete', 'cancelled']
CONDITION = obj(type={'enum': ['load', 'networkidle', 'css', 'text']}, value=nullable(string()))
OPTIONS = obj(condition=CONDITION, viewport=obj(width=integer(1, 40000), height=integer(1, 40000)),
              locale=string(64), timezone=string(128))
CAPS = obj(navigation_seconds=integer(1, 60), attempt_seconds=integer(1, 120),
           artifact_bytes=integer(1, 104857600), total_bytes=integer(1, 262144000),
           screenshot_pixels=integer(1, 40000000))
IDS = dict(attempt_id=UUID, job_id=UUID, capture_id=UUID, generation=integer(1, 2147483647))
HEADERS = obj(**{k: nullable(string(4096)) for k in ['content-type', 'cache-control', 'last-modified', 'etag']})
OUTPUT = obj(kind={'enum': ['screenshot', 'mhtml']},
             path={'enum': ['evidence/screenshot.png', 'evidence/page.mhtml']},
             size_bytes=integer(1, 104857600),
             sha256_hint=string(64, pattern='^[0-9a-f]{64}$'))
REQUEST = obj(contract={'const': 'capture-engine/1'}, **IDS,
              authorization=string(512, pattern='^[!-~]+$'), deadline=TIME,
              url=URL, options=OPTIONS, resource_caps=CAPS,
              output_namespace=string(128, pattern='^[a-z0-9][a-z0-9_-]*$'), network_policy_id=string(128))
RESULT = obj(contract={'const': 'capture-engine/1'}, **IDS,
             engine_version=VERSION, browser_version=VERSION,
             started_at=TIME, finished_at=TIME, requested_url=URL, final_url=nullable(URL),
             redirects=array(URL, 32), main_document_status=nullable(integer(100, 599)),
             response_headers=HEADERS, options_actual=OPTIONS,
             condition_result={'enum': ['satisfied', 'failed', 'not_evaluated']},
             outcome={'enum': ['complete', 'partial', 'failed', 'cancelled']},
             warnings=WARNINGS, error_code=nullable({'enum': ERRORS}), outputs=array(OUTPUT, 2))


def canonical(value):
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':'))+'\n').encode()


def artifacts():
    files = {}
    for name, schema in [('request', REQUEST), ('result', RESULT)]:
        files[f'schemas/capture-engine-1-{name}.schema.json'] = canonical(
            dict(schema, **{'$schema': DRAFT, 'title': f'capture-engine/1 {name}'}))
    ids = dict(attempt_id='00000000-0000-4000-8000-000000000001',
               job_id='00000000-0000-4000-8000-000000000002',
               capture_id='00000000-0000-4000-8000-000000000003', generation=1)
    options = dict(condition=dict(type='load', value=None), viewport=dict(width=1280, height=900),
                   locale='en-US', timezone='UTC')
    request = dict(contract='capture-engine/1', **ids, authorization='synthetic-job-scope-only',
                   deadline='2026-11-09T12:02:00Z', url='https://example.org/article', options=options,
                   resource_caps=dict(navigation_seconds=60, attempt_seconds=120, artifact_bytes=104857600,
                                      total_bytes=262144000, screenshot_pixels=40000000),
                   output_namespace='synthetic-attempt-1', network_policy_id='public-http-v0')
    members = json.loads((ROOT/'fixtures/members.json').read_text())
    outputs = []
    for path, kind in [('evidence/page.mhtml', 'mhtml'), ('evidence/screenshot.png', 'screenshot')]:
        raw = base64.b64decode(members[path])
        outputs.append(dict(path=path, kind=kind, size_bytes=len(raw), sha256_hint=hashlib.sha256(raw).hexdigest()))
    result = dict(contract='capture-engine/1', **ids, engine_version='synthetic-engine-1',
                  browser_version='synthetic-browser-1', started_at='2026-11-09T12:00:00Z',
                  finished_at='2026-11-09T12:00:01Z', requested_url=request['url'], final_url=request['url'],
                  redirects=[], main_document_status=200, response_headers={k:None for k in HEADERS['properties']},
                  options_actual=options, condition_result='satisfied', outcome='complete', warnings=[],
                  error_code=None, outputs=outputs)
    cases = [('request', request, 'accepted'), ('complete', result, 'accepted')]
    def variant(name, changes, expected):
        cases.append((name, dict(result, **changes), expected))
    variant('http-404', {'main_document_status':404}, 'accepted')
    variant('partial', {'outcome':'partial', 'condition_result':'failed', 'error_code':'condition_timeout',
                        'outputs':outputs[:1]}, 'accepted')
    variant('failed', {'outcome':'failed', 'condition_result':'not_evaluated', 'error_code':'target_denied',
                       'outputs':[], 'final_url':None, 'main_document_status':None}, 'accepted')
    variant('cancelled', {'outcome':'cancelled', 'condition_result':'not_evaluated', 'error_code':'cancelled',
                          'outputs':[]}, 'accepted')
    variant('unknown-version', {'contract':'capture-engine/2'}, 'schema_const')
    variant('missing-output', {'outputs':outputs[:1]}, 'required_outputs')
    variant('stale-generation', {'generation':2}, 'request_mismatch')
    variant('false-complete', {'condition_result':'failed'}, 'complete_condition')
    variant('duplicate-output', {'outputs':[outputs[0], outputs[0]]}, 'duplicate_output')
    variant('secret-header', {'response_headers':dict(result['response_headers'], **{'set-cookie':'synthetic'})}, 'schema_unknown_field')
    expected = {}
    for name, value, outcome in cases:
        path = f'fixtures/engine/{name}.json'
        files[path] = canonical(value)
        expected[path] = dict(kind='request' if name=='request' else 'result', expected=outcome)
    files['fixtures/engine/identity.json'] = canonical(dict(fixture_version=1, seed='loc4-engine-1',
        origin='synthetic-grammar-only', authority='build_engine.py', expected=expected,
        sha256={p:hashlib.sha256(raw).hexdigest() for p,raw in files.items()}))
    return files


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    stale = []
    for name, raw in artifacts().items():
        path = ROOT/name
        if args.check:
            if not path.exists() or path.read_bytes() != raw:
                stale.append(name)
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(raw)
    if stale:
        parser.exit(1, 'Generated engine artifacts differ: '+', '.join(stale)+'\n')
