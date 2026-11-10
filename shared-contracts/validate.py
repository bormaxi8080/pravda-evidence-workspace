"""Bounded contract tooling; never opens artifact paths or executes archive content."""
import hashlib
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent
SCHEMA = json.loads((ROOT / 'schemas/workspace-capture-v0-1.schema.json').read_text())


class Invalid(ValueError):
    """Rejected contract data."""


def canonical(value):
    def check(v):
        if type(v) in (str, int, bool, type(None)):
            return
        if type(v) is list:
            for child in v:
                check(child)
            return
        if type(v) is dict and all(type(k) is str for k in v):
            for child in v.values():
                check(child)
            return
        raise Invalid('unsupported_json_type')
    check(value)
    try:
        return (json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':'), allow_nan=False) + '\n').encode('utf-8')
    except (ValueError, UnicodeError) as exc:
        raise Invalid('invalid_json') from exc


def parse(raw, require_canonical=True):
    def pairs(items):
        result = {}
        for key, value in items:
            if key in result:
                raise Invalid('duplicate_key')
            result[key] = value
        return result
    try:
        value = json.loads(raw.decode('utf-8'), object_pairs_hook=pairs,
                           parse_float=lambda _: fail('floating_point'),
                           parse_constant=lambda _: fail('nonfinite'))
        if canonical(value) != raw and require_canonical:
            raise Invalid('noncanonical_json')
        return value
    except (ValueError, UnicodeError, RecursionError) as exc:
        if isinstance(exc, Invalid):
            raise
        raise Invalid('invalid_json') from exc


def fail(code):
    raise Invalid(code)


def shape(value, schema):
    """Evaluate only the checked-in vocabulary; unknown keywords fail closed.

    This is deliberately not a general JSON Schema implementation. The published
    schema can also be consumed by a full Draft 2020-12 validator.
    """
    supported = {'$schema', 'title', 'description', 'type', 'const', 'required',
                 'properties', 'additionalProperties', 'minItems', 'maxItems',
                 'items', 'prefixItems', 'minLength', 'maxLength', 'pattern',
                 'minimum', 'maximum', 'enum', 'anyOf'}
    if not isinstance(schema, dict) or set(schema) - supported:
        fail('unsupported_schema')
    if 'anyOf' in schema:
        for branch in schema['anyOf']:
            try:
                shape(value, branch)
                break
            except Invalid:
                pass
        else:
            fail('schema_anyof')
    if 'enum' in schema and not any(type(value) is type(item) and value == item for item in schema['enum']):
        fail('schema_enum')
    types = {'object': dict, 'array': list, 'string': str, 'integer': int,
             'null': type(None), 'boolean': bool}
    if 'type' in schema and type(value) is not types[schema['type']]:
        fail('schema_type')
    if 'const' in schema and (type(value) is not type(schema['const']) or value != schema['const']):
        fail('schema_const')
    if type(value) is dict:
        if set(schema.get('required', [])) - value.keys():
            fail('schema_required')
        props = schema.get('properties', {})
        if schema.get('additionalProperties') is False and value.keys() - props.keys():
            fail('schema_unknown_field')
        for key, item in value.items():
            if key in props:
                shape(item, props[key])
    if type(value) is list:
        if not schema.get('minItems', 0) <= len(value) <= schema.get('maxItems', len(value)):
            fail('schema_array_bound')
        prefix = schema.get('prefixItems', [])
        for index, item in enumerate(value):
            if index < len(prefix):
                shape(item, prefix[index])
            elif schema.get('items') is False:
                fail('schema_extra_item')
            else:
                shape(item, schema.get('items', {}))
    if type(value) is str:
        if not schema.get('minLength', 0) <= len(value) <= schema.get('maxLength', len(value)):
            fail('schema_string_bound')
        if 'pattern' in schema and re.search(schema['pattern'], value) is None:
            fail('schema_pattern')
    if type(value) is int:
        if not schema.get('minimum', value) <= value <= schema.get('maximum', value):
            fail('schema_integer_bound')


def verify(manifest_bytes, members):
    """Check an already bounded in-memory mapping of relative names to bytes.

    Filesystem/link validation, PNG decoding and MHTML validation are producer/
    trusted-finalizer gates, outside this inventory-only slice.
    """
    if len(manifest_bytes) > 65536:
        fail('manifest_limit')
    manifest = parse(manifest_bytes)
    if not isinstance(manifest, dict) or manifest.get('profile') != SCHEMA['properties']['profile']['const']:
        fail('unsupported_profile')
    shape(manifest, SCHEMA)
    expected = {a['path'] for a in manifest['artifacts']}
    if set(members) != expected:
        fail('required_inventory')
    if sum(len(v) for v in members.values()) > 250 * 1024 * 1024:
        fail('attempt_limit')
    for artifact in manifest['artifacts']:
        raw = members[artifact['path']]
        if len(raw) != artifact['size_bytes'] or hashlib.sha256(raw).hexdigest() != artifact['sha256']:
            fail('integrity_failed')
        if artifact['kind'] == 'metadata':
            parse(raw)
    return {'size_bytes': len(manifest_bytes), 'sha256': hashlib.sha256(manifest_bytes).hexdigest()}
