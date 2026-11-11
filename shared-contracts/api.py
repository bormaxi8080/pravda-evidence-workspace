"""DTO parsing and contract-level command envelope checks, not a route authorizer."""
from build_api import DTOS, CODES
from engine import urls, instant
from validate import parse, shape, fail


def validate(raw,name):
    if name not in DTOS: fail('unsupported_dto')
    if len(raw)>1048576: fail('input_too_large')
    value=parse(raw,require_canonical=False);shape(value,DTOS[name])
    if name=='CaptureSubmit':
        urls(value['url'])
        condition=value.get('condition_type','load')
        if (condition in ('css','text')) != ('condition' in value): fail('condition_value')
    if name=='CaptureFilters' and 'date_start' in value and 'date_end' in value:
        if instant(value['date_start'])>instant(value['date_end']): fail('date_interval')
    if name=='BatchConfirm' and len(value['selected_rows'])!=len(set(value['selected_rows'])):
        fail('duplicate_row')
    if name=='PreviewText' and len(value['csv_text'].encode('utf-8'))>1048576:
        fail('input_too_large')
    if name=='Publish' and 'source_url' in value: urls(value['source_url'])
    return value


def envelope(method,session,csrf,idempotency=None,required_key=False):
    # Tests document errors; these booleans are trusted middleware facts, never user DTO fields.
    if not session: return 401,'session_required'
    if method!='get' and not csrf: return 403,'csrf_failed'
    if required_key and (not isinstance(idempotency,str) or not 1<=len(idempotency)<=128 or
                         any(not 32<=ord(c)<=126 for c in idempotency)):
        return 422,'validation_failed'
    return None


def validate_error(raw,status):
    value=validate(raw,'Error')
    if value['error']['code'] not in CODES.get(status,[]): fail('error_status')
    return value
