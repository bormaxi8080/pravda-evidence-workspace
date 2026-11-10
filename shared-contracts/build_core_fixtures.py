"""Reproducible grammar fixtures; no browser or deployment claims."""
import argparse
import base64
import hashlib
import json
from pathlib import Path
from build_core import write_generated
from core import checksums
from validate import canonical

ROOT=Path(__file__).resolve().parent
ID='00000000-0000-4000-8000-000000000003'
TIME='2026-11-09T12:00:00Z'


def generated():
    engine=json.loads((ROOT/'fixtures/engine/complete.json').read_text())
    metadata=dict(contract='workspace-capture-metadata/1',capture_id=ID,attempt_id=engine['attempt_id'],
        channel='server',requested_url=engine['requested_url'],final_url=engine['final_url'],
        **{key:TIME for key in ['requested_at','started_at','navigated_at','finished_at','finalized_at']},
        main_document_status=200,redirects=[],response_headers=engine['response_headers'],
        omitted_by_policy=['non_allowlisted_response_headers'],engine_version=engine['engine_version'],
        browser_version=engine['browser_version'],options_actual=engine['options_actual'],condition_result='satisfied',
        warnings=[],artifact_outcomes=dict(screenshot='complete',mhtml='complete'))
    legacy=dict(profile='workspace-legacy-import/1',capture_id=ID,imported_at=TIME,original_id='synthetic-old-id',
        requested_url=None,claimed_capture_time=None,original_creator=None,requester_id=None,
        provenance_notes=['Synthetic unknown source clock and requester; no local witnessing.'],
        outcome='unknown',artifacts=[],original_claimed_sha256=None,publication_eligible=False)
    job=dict(contract='workspace-job/1',id=engine['job_id'],type='capture',entity_id=ID,requester_id=ID,
        state='queued',state_revision=1,attempt_count=0,max_attempts=3,phase=None,available_at=TIME,
        next_retry=None,last_error=None,terminal_capture_id=None)
    attempt=dict(contract='workspace-attempt/1',id=engine['attempt_id'],job_id=engine['job_id'],capture_id=ID,
        attempt_no=1,generation=1,started_at=TIME,finished_at=None,deadline='2026-11-09T12:02:00Z',
        engine_version=None,browser_version=None,error_code=None)
    event=dict(contract='workspace-job-event/1',job_id=engine['job_id'],sequence=1,kind='state',
        state='queued',code=None,message='Queued',timestamp=TIME)
    files={f'fixtures/core/{name}.json':canonical(v) for name,v in [
        ('capture-metadata-1',metadata),('legacy-import-1',legacy),('job-1',job),('attempt-1',attempt),('job-event-1',event)]}
    original={p:base64.b64decode(v) for p,v in json.loads((ROOT/'fixtures/members.json').read_text()).items()}
    original['metadata/capture.json']=canonical(metadata)
    capture=json.loads((ROOT/'fixtures/complete.manifest.json').read_text())
    capture['capture_id']=ID;capture['attempt_id']=engine['attempt_id']
    for a in capture['artifacts']:
        raw=original[a['path']];a.update(size_bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest())
    original['manifest.json']=canonical(capture)
    for pdf in [False,True]:
        members={'capture/'+p:raw for p,raw in original.items()}
        meta=dict(profile='workspace-export-v0/1',capture_id=ID,exported_at=TIME,
            capture_manifest_sha256=hashlib.sha256(original['manifest.json']).hexdigest(),
            receipt_version='workspace-receipt-v0/1',include_pdf=pdf,include_editorial=False,include_actor=False,
            editorial_revision=None,editorial=None,actor=None)
        members.update({'export.json':canonical(meta),'receipt.html':b'<!doctype html><p>Synthetic receipt; WARC deferred. Hashes do not prove source truth.</p>\n',
                        'README.txt':b'Synthetic grammar package. No live capture or PDF fidelity proof.\n'})
        if pdf: members['receipt.pdf']=b'%PDF-synthetic-grammar-only\n'
        def mime(path):
            return 'application/json' if path.endswith('.json') else 'application/octet-stream'
        manifest=dict(profile='workspace-export-v0/1',capture_id=ID,warnings=[],deferred_formats=['warc'],
            artifacts=[dict(path=p,kind='package_member',mime_type=mime(p),size_bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest())
                       for p,raw in sorted(members.items())])
        members['manifest.json']=canonical(manifest);members['SHA256SUMS']=checksums(members)
        files[f'fixtures/core/export-{"pdf" if pdf else "default"}.json']=canonical({p:base64.b64encode(raw).decode() for p,raw in members.items()})
    files['fixtures/core/identity.json']=canonical(dict(seed='loc4-core-1',fixture_version=1,origin='synthetic-grammar-only',
        sha256={p:hashlib.sha256(raw).hexdigest() for p,raw in files.items()}))
    return files


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--check',action='store_true');args=p.parse_args()
    write_generated(generated(),args.check)
