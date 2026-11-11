"""Validate bounded engine messages. No network, archive or filesystem access."""
from datetime import datetime
import json
from pathlib import Path
from urllib.parse import urlsplit
from validate import Invalid, fail, parse, shape

ROOT = Path(__file__).resolve().parent
SCHEMAS = {kind: json.loads((ROOT/f'schemas/capture-engine-1-{kind}.schema.json').read_text())
           for kind in ('request', 'result')}


def instant(text):
    try:
        return datetime.fromisoformat(text.replace('Z', '+00:00'))
    except ValueError:
        fail('invalid_time')


def options(value):
    condition = value['condition']
    if (condition['type'] in ('css', 'text')) != (condition['value'] is not None):
        fail('condition_value')
    viewport = value['viewport']
    if viewport['width'] * viewport['height'] > 40000000:
        fail('pixel_limit')


def urls(value):
    """Syntax only; DNS, redirects and public-address policy require runtime checks."""
    if len(value.encode('utf-8')) > 8192:
        fail('url_limit')
    try:
        parsed = urlsplit(value)
        port = parsed.port
        if not parsed.hostname or parsed.username is not None or parsed.password is not None:
            fail('invalid_url')
        if port not in (None, 80 if parsed.scheme == 'http' else 443):
            fail('invalid_url')
    except ValueError:
        fail('invalid_url')


def validate(raw, kind, request=None):
    if kind not in SCHEMAS:
        fail('unknown_contract_kind')
    if len(raw) > 262144:
        fail('message_limit')
    value = parse(raw)
    shape(value, SCHEMAS[kind])
    if kind == 'request':
        instant(value['deadline'])
        urls(value['url'])
        options(value['options'])
        caps = value['resource_caps']
        if caps['navigation_seconds'] > caps['attempt_seconds'] or caps['artifact_bytes'] > caps['total_bytes']:
            fail('resource_caps')
        viewport = value['options']['viewport']
        if viewport['width'] * viewport['height'] > caps['screenshot_pixels']:
            fail('pixel_limit')
        return value
    # A result is meaningful only against the original validated request.
    if request is None:
        fail('request_required')
    for key in ('attempt_id', 'job_id', 'capture_id', 'generation'):
        if value[key] != request[key]:
            fail('request_mismatch')
    if value['requested_url'] != request['url'] or value['options_actual'] != request['options']:
        fail('request_mismatch')
    start, end = instant(value['started_at']), instant(value['finished_at'])
    if start > end or end > instant(request['deadline']):
        fail('result_deadline')
    if (end-start).total_seconds() > request['resource_caps']['attempt_seconds']:
        fail('result_deadline')
    urls(value['requested_url'])
    for url in value['redirects'] + ([value['final_url']] if value['final_url'] is not None else []):
        urls(url)
    options(value['options_actual'])
    outputs = value['outputs']
    if len({o['kind'] for o in outputs}) != len(outputs) or len({o['path'] for o in outputs}) != len(outputs):
        fail('duplicate_output')
    paths = {'mhtml':'evidence/page.mhtml', 'screenshot':'evidence/screenshot.png'}
    if any(o['path'] != paths[o['kind']] for o in outputs):
        fail('output_kind_path')
    caps = request['resource_caps']
    if any(o['size_bytes'] > caps['artifact_bytes'] for o in outputs) or sum(o['size_bytes'] for o in outputs) > caps['total_bytes']:
        fail('resource_caps')
    outcome = value['outcome']
    if outcome == 'complete':
        if len(outputs) != 2:
            fail('required_outputs')
        if value['condition_result'] != 'satisfied' or value['error_code'] is not None:
            fail('complete_condition')
        if value['main_document_status'] is None or value['final_url'] is None:
            fail('complete_provenance')
    else:
        if value['error_code'] is None:
            fail('required_error')
        if outcome == 'partial' and not outputs:
            fail('partial_output')
        if outcome == 'failed' and outputs:
            fail('failed_output')
        if (outcome == 'cancelled') != (value['error_code'] == 'cancelled'):
            fail('cancelled_error')
    return value
