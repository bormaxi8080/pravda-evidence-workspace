"""Core contract authority. Generated JSON is reproducible, not hand-maintained."""
import argparse
import hashlib
import json
from pathlib import Path
from build_engine import UUID, TIME, URL, WARNINGS, OPTIONS, HEADERS, ERRORS, DRAFT
from build_engine import obj, array, string, integer, nullable
from validate import canonical

ROOT = Path(__file__).resolve().parent
REV = integer(1, 2147483647)
HASH = string(64, pattern='^[0-9a-f]{64}$')
BOOL = {'type':'boolean'}
EMPTY_TEXT = {'type':'string','maxLength':16384}
STATES = ['queued','retry_wait','leased','running','finalizing','completed','failed','cancelled']
TERMINAL = ['completed','failed','cancelled']
SAFE_CODES = ERRORS + ['integrity_failed','permission_revoked','migration_cancelled']
ARTIFACT = obj(path=string(256,pattern=r'^[a-zA-Z0-9_./-]+$'),kind=string(64),mime_type=string(128),
               size_bytes=integer(1,104857600),sha256=HASH)
METADATA = obj(contract={'const':'workspace-capture-metadata/1'},capture_id=UUID,attempt_id=UUID,
               channel={'const':'server'},requested_url=URL,final_url=URL,
               requested_at=TIME,started_at=TIME,navigated_at=TIME,finished_at=TIME,finalized_at=TIME,
               main_document_status=integer(100,599),redirects=array(URL,32),response_headers=HEADERS,
               omitted_by_policy={'const':['non_allowlisted_response_headers']},
               engine_version=string(128),browser_version=string(128),options_actual=OPTIONS,
               condition_result={'const':'satisfied'},warnings=WARNINGS,
               artifact_outcomes=obj(screenshot={'const':'complete'},mhtml={'const':'complete'}))
LEGACY = obj(profile={'const':'workspace-legacy-import/1'},capture_id=UUID,
             imported_at=TIME,original_id=string(256),requested_url=nullable(URL),
             claimed_capture_time=nullable(TIME),original_creator=nullable(string(256)),
             requester_id=nullable(UUID),provenance_notes=array(string(2048),64),
             outcome={'enum':['incomplete','unknown']},artifacts=array(ARTIFACT,3),
             original_claimed_sha256=nullable(HASH),publication_eligible={'const':False})
EXPORT_META = obj(profile={'const':'workspace-export-v0/1'},capture_id=UUID,exported_at=TIME,
                  capture_manifest_sha256=HASH,receipt_version={'const':'workspace-receipt-v0/1'},
                  include_pdf=BOOL,include_editorial=BOOL,include_actor=BOOL,
                  editorial_revision=nullable(REV),editorial=nullable(obj(title=string(256),note=EMPTY_TEXT,
                    tags=array(string(64),50),collection_ids=array(UUID,100))),
                  actor=nullable(obj(id=UUID,label=string(256))))
EXPORT_MANIFEST = obj(profile={'const':'workspace-export-v0/1'},capture_id=UUID,
                      artifacts=array(ARTIFACT,12),warnings=WARNINGS,deferred_formats={'const':['warc']})
JOB = obj(contract={'const':'workspace-job/1'},id=UUID,type={'enum':['capture','export']},
          entity_id=UUID,requester_id=UUID,state={'enum':STATES},state_revision=REV,
          attempt_count=integer(0,3),max_attempts=integer(1,3),phase=nullable(string(64)),
          available_at=TIME,next_retry=nullable(TIME),last_error=nullable({'enum':SAFE_CODES}),
          terminal_capture_id=nullable(UUID))
ATTEMPT = obj(contract={'const':'workspace-attempt/1'},id=UUID,job_id=UUID,capture_id=UUID,
              attempt_no=integer(1,3),generation=REV,started_at=TIME,finished_at=nullable(TIME),
              deadline=TIME,engine_version=nullable(string(128)),browser_version=nullable(string(128)),
              error_code=nullable({'enum':SAFE_CODES}))
EVENT = obj(contract={'const':'workspace-job-event/1'},job_id=UUID,sequence=integer(1,9223372036854775807),
            kind={'enum':['state','phase','terminal','reset']},state={'enum':STATES},
            code=nullable({'enum':SAFE_CODES}),message=string(256),timestamp=TIME)
SCHEMAS = {'capture-metadata-1':METADATA,'legacy-import-1':LEGACY,'export-metadata-v0-1':EXPORT_META,
           'export-manifest-v0-1':EXPORT_MANIFEST,'job-1':JOB,'attempt-1':ATTEMPT,'job-event-1':EVENT}


def generated():
    return {f'schemas/{name}.schema.json':canonical(dict(value,**{'$schema':DRAFT,'title':name}))
            for name,value in SCHEMAS.items()}


def write_generated(files,check=False):
    stale=[]
    for name,raw in files.items():
        path=ROOT/name
        if check:
            if not path.exists() or path.read_bytes()!=raw: stale.append(name)
        else:
            path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes(raw)
    if stale: raise SystemExit('Generated files differ: '+', '.join(stale))


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--check',action='store_true');args=p.parse_args()
    write_generated(generated(),args.check)
