"""Pure bounded core DTO/package verification; never opens supplied member names."""
import hashlib
import re
from pathlib import PurePosixPath
from build_core import SCHEMAS
from engine import instant, options, urls
from validate import canonical, parse, shape, fail, verify


def safe_paths(paths):
    if len(paths)!=len(set(p.casefold() for p in paths)): fail('duplicate_path')
    for path in paths:
        if (not re.fullmatch(r'[A-Za-z0-9_./-]+', path) or '\\' in path or path.startswith('/') or
            any(p in ('','.','..') for p in path.split('/')) or str(PurePosixPath(path))!=path):
            fail('unsafe_path')


def validate(raw,name):
    if name not in SCHEMAS: fail('unsupported_contract')
    if len(raw)>1048576: fail('message_limit')
    value=parse(raw);shape(value,SCHEMAS[name])
    if name=='capture-metadata-1':
        times=[instant(value[k]) for k in ['requested_at','started_at','navigated_at','finished_at','finalized_at']]
        if times!=sorted(times): fail('time_order')
        for url in [value['requested_url'],value['final_url']]+value['redirects']: urls(url)
        options(value['options_actual'])
    elif name=='legacy-import-1':
        instant(value['imported_at'])
        if value['claimed_capture_time'] is not None: instant(value['claimed_capture_time'])
        if not value['provenance_notes']: fail('legacy_provenance')
        safe_paths([a['path'] for a in value['artifacts']])
    elif name=='export-metadata-v0-1':
        instant(value['exported_at'])
        if value['include_editorial'] != (value['editorial'] is not None and value['editorial_revision'] is not None):
            fail('editorial_disclosure')
        if not value['include_editorial'] and (value['editorial'] is not None or value['editorial_revision'] is not None):
            fail('editorial_disclosure')
        if value['include_actor'] != (value['actor'] is not None): fail('actor_disclosure')
    elif name=='job-1':
        if value['attempt_count']>value['max_attempts']: fail('attempt_count')
        if (value['state']=='retry_wait') != (value['next_retry'] is not None): fail('retry_time')
        instant(value['available_at'])
        if value['next_retry'] is not None: instant(value['next_retry'])
    elif name=='attempt-1':
        start,deadline=instant(value['started_at']),instant(value['deadline'])
        if start>deadline: fail('time_order')
        if value['finished_at'] is not None and not start<=instant(value['finished_at'])<=deadline:
            fail('time_order')
    elif name=='job-event-1':
        instant(value['timestamp'])
        if value['kind']=='terminal' and value['state'] not in ('completed','failed','cancelled'): fail('terminal_state')
    return value


def checksums(members):
    safe_paths(list(members))
    return ''.join(hashlib.sha256(raw).hexdigest()+'  '+name+'\n' for name,raw in sorted(members.items())).encode('ascii')


def verify_export(members):
    # Caller supplies already bounded bytes, not a ZIP decoder/filesystem authority.
    if len(members)>12 or sum(len(v) for v in members.values())>512*1024*1024: fail('export_limit')
    safe_paths(list(members))
    required={'capture/evidence/page.mhtml','capture/evidence/screenshot.png','capture/metadata/capture.json',
              'capture/manifest.json','export.json','receipt.html','manifest.json','SHA256SUMS','README.txt'}
    if not required<=members.keys(): fail('required_inventory')
    meta=validate(members['export.json'],'export-metadata-v0-1')
    expected=required|({'receipt.pdf'} if meta['include_pdf'] else set())
    if set(members)!=expected: fail('required_inventory')
    manifest=validate(members['manifest.json'],'export-manifest-v0-1')
    entries=manifest['artifacts'];names=[a['path'] for a in entries]
    safe_paths(names)
    if names!=sorted(expected-{'manifest.json','SHA256SUMS'}): fail('manifest_inventory')
    for a in entries:
        raw=members[a['path']]
        if a['size_bytes']!=len(raw) or a['sha256']!=hashlib.sha256(raw).hexdigest(): fail('integrity_failed')
    if members['SHA256SUMS']!=checksums({k:v for k,v in members.items() if k!='SHA256SUMS'}): fail('checksum_coverage')
    capture={k.removeprefix('capture/'):v for k,v in members.items() if k.startswith('capture/')}
    reference=verify(capture.pop('manifest.json'),capture)
    if reference['sha256']!=meta['capture_manifest_sha256']: fail('capture_reference')
    capture_manifest=parse(members['capture/manifest.json'])
    if not meta['capture_id']==manifest['capture_id']==capture_manifest['capture_id']: fail('capture_reference')
    metadata=validate(members['capture/metadata/capture.json'],'capture-metadata-1')
    if metadata['capture_id']!=capture_manifest['capture_id'] or metadata['attempt_id']!=capture_manifest['attempt_id']:
        fail('capture_reference')
    return reference
