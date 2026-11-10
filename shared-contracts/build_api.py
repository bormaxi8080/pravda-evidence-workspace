"""Cookie API DTO and OpenAPI 3.1 authority for the first core command set."""
import argparse
from build_core import UUID, TIME, URL, REV, HASH, BOOL, EMPTY_TEXT, JOB, EVENT, string, integer, obj, array, nullable, write_generated
from validate import canonical


def optional(schema,*names):
    schema['required']=[k for k in schema['required'] if k not in names]
    return schema


CODES={401:['session_required','session_expired'],403:['permission_denied','csrf_failed'],404:['not_found'],
       409:['revision_conflict','invalid_state','idempotency_conflict','preview_expired'],413:['input_too_large'],
       422:['validation_failed','target_denied','unsupported_option'],429:['queue_capacity','rate_limited'],
       503:['dependency_unavailable','storage_reserve']}
DTOS={
'Error':obj(error=obj(code={'enum':[c for values in CODES.values() for c in values]},message=string(256),
                     request_id=string(128),fields=optional(obj(url=string(256),expected_revision=string(256)), 'url','expected_revision'))),
'CaptureSubmit':optional(obj(url=URL,condition_type={'enum':['load','networkidle','css','text']},condition=string(),
    title=string(256),note=EMPTY_TEXT,tags=array(string(64),50),collection_ids=array(UUID,100),rationale=string(2048)),
    'condition_type','condition','title','note','tags','collection_ids','rationale'),
'CaptureAccepted':obj(capture_id=UUID,job_id=UUID,state={'const':'queued'},profile={'const':'workspace-capture-v0/1'}),
'EditorialPatch':optional(obj(expected_revision=REV,title=string(256),note=EMPTY_TEXT,tag_ids=array(UUID,50),collection_ids=array(UUID,100)),
                         'title','note','tag_ids','collection_ids'),
'Editorial':obj(revision=REV,title=string(256),note=EMPTY_TEXT,tag_ids=array(UUID,50),collection_ids=array(UUID,100),
                review={'enum':['unreviewed','in_review','approved','rejected']}),
'TriagePatch':obj(expected_triage_revision=REV,importance={'enum':['normal','important']}),
'Triage':obj(triage_revision=REV,importance={'enum':['normal','important']}),
'Review':obj(expected_revision=REV,state={'enum':['in_review','approved','rejected']},reason={'type':'string','maxLength':2048}),
'Cancel':obj(expected_revision=REV),
'ExportRequest':obj(profile={'const':'workspace-export-v0/1'},include_pdf=BOOL,include_editorial=BOOL,include_actor=BOOL,
                    expected_revision=REV,manifest_sha256=HASH),
'ExportAccepted':obj(export_id=UUID,job_id=UUID,state={'const':'queued'}),
'Publish':optional(obj(expected_revision=REV,manifest_sha256=HASH,title=string(256),display_url=string(8192),source_url=URL),'source_url'),
'Publication':obj(id=UUID,slug=string(128,pattern='^[a-zA-Z0-9_-]+$'),revision=REV,state={'enum':['active','revoked']}),
'Revoke':obj(expected_revision=REV,reason=string(2048)),
'Job':JOB,'JobEvent':EVENT}
# Each route is explicitly described; this file does not implement HTTP handlers.
OPERATIONS=[
('post','/captures','CaptureSubmit','CaptureAccepted',202,True,False),
('patch','/captures/{id}/editorial','EditorialPatch','Editorial',200,False,False),
('patch','/captures/{id}/triage','TriagePatch','Triage',200,False,False),
('post','/captures/{id}/review','Review','Editorial',200,False,False),
('get','/jobs/{id}',None,'Job',200,False,False),
('post','/jobs/{id}/cancel','Cancel','Job',202,False,False),
('post','/captures/{id}/publications','Publish','Publication',201,True,True),
('post','/publications/{id}/revoke','Revoke','Publication',200,False,True),
('post','/captures/{id}/exports','ExportRequest','ExportAccepted',202,True,False)]

# Additional V0 operations from document 16, with explicit bounded DTOs.
DTOS.update({
'CaptureSummary':obj(id=UUID,source_id=UUID,requested_at=nullable(TIME),
    outcome={'enum':['pending','complete','partial','failed','cancelled','unknown']},
    profile={'enum':['workspace-capture-v0/1','workspace-legacy-import/1']},
    editorial_revision=REV,importance={'enum':['normal','important']}),
'ArtifactSummary':obj(id=UUID,kind=string(64),mime_type=string(128),size_bytes=integer(1,104857600),sha256=HASH),
'Retry':optional(obj(condition_type={'enum':['load','networkidle','css','text']},condition=string()),'condition_type','condition'),
'PreviewText':obj(csv_text=string(1048576),collection_ids=array(UUID,100),rationale={'type':'string','maxLength':2048}),
'BatchConfirm':obj(preview_id=UUID,expected_revision=REV,selected_rows=dict(array(integer(1,500),500),minItems=1),keep_duplicates=BOOL),
'BatchRow':obj(row_no=integer(1,500),job_id=nullable(UUID),state={'enum':['invalid','duplicate','selected','queued','running','completed','failed','cancelled']},error_code=nullable(string(64))),
'Batch':obj(id=UUID,total=integer(0,500),completed=integer(0,500),failed=integer(0,500),rows=array(obj(row_no=integer(1,500),job_id=nullable(UUID),state=string(64)),100),next_cursor=nullable(string(2048))),
'GroupCreate':optional(obj(name=string(128),description={'type':'string','maxLength':2048}),'description'),
'GroupPatch':optional(obj(expected_revision=REV,name=string(128),description={'type':'string','maxLength':2048}),'name','description'),
'Group':obj(id=UUID,revision=REV,name=string(128),description={'type':'string','maxLength':2048}),
'TagCreate':obj(name=string(64)),
'TagPatch':obj(expected_revision=REV,name=string(64)),
'Tag':obj(id=UUID,revision=REV,name=string(64)),
'Archive':obj(expected_revision=REV,reason=string(2048)),
'Archived':obj(id=UUID,revision=REV,archived={'const':True}),
'ExportState':obj(id=UUID,state={'enum':['queued','running','ready','failed','expired']},expires_at=nullable(TIME),error_code=nullable(string(64))),
'UserPatch':optional(obj(expected_permission_revision=REV,enabled=BOOL,role={'enum':['admin','editor']}),'enabled','role'),
'User':obj(id=UUID,permission_revision=REV,enabled=BOOL,role={'enum':['admin','editor']},login=string(256)),
'AuditEvent':obj(id=UUID,actor_id=nullable(UUID),resource_id=nullable(UUID),action=string(128),timestamp=TIME,request_id=string(128),legacy=BOOL),
'Status':obj(capture_available=BOOL,export_available=BOOL,component_versions=array(obj(name=string(128),version=string(64)),16),
    limits=obj(max_pending=integer(1,1000),max_csv_rows=integer(1,500),max_artifact_bytes=integer(1,104857600)))})
DTOS['Preview']=obj(id=UUID,revision=REV,expires_at=TIME,digest=HASH,rows=array(DTOS['BatchRow'],500))
DTOS['CaptureDetail']=obj(capture=DTOS['CaptureSummary'],artifacts=array(DTOS['ArtifactSummary'],3),
    editorial=DTOS['Editorial'],triage=DTOS['Triage'],publication=nullable(DTOS['Publication']),
    submitted_context=obj(collection_ids=array(UUID,100),rationale=nullable(string(2048)),origin={'enum':['local','legacy_unknown']}),
    provenance=obj(requested_url=nullable(URL),final_url=nullable(URL),manifest_sha256=nullable(HASH),
        integrity={'enum':['unknown','valid','failed']},channel={'enum':['server','legacy']}))
for label,item in [('Captures','CaptureSummary'),('Groups','Group'),('Tags','Tag'),('Users','User'),('Audit','AuditEvent')]:
    DTOS[label]=obj(items=array(DTOS[item],100),next_cursor=nullable(string(2048)))
DTOS['CaptureFilters']=optional(obj(q=string(1024),host=string(253),creator=UUID,tag_ids=array(UUID,50),
    collection_id=UUID,states=array({'enum':['pending','complete','partial','failed','cancelled','unknown']},6),
    date_start=TIME,date_end=TIME,importance={'enum':['normal','important']},cursor=string(2048),limit=integer(1,100)),
    'q','host','creator','tag_ids','collection_id','states','date_start','date_end','importance','cursor','limit')
DTOS['PreviewUpload']=obj(file={'type':'string'},collection_ids=array(UUID,100),rationale={'type':'string','maxLength':2048})
# Error fields use known DTO field names; arbitrary server/provider diagnostics are not accepted.
error_fields={key:string(256) for schema in DTOS.values() for key in schema.get('properties',{})}
DTOS['Error']['properties']['error']['properties']['fields']=optional(obj(**error_fields),*error_fields)
OPERATIONS += [
('get','/captures',None,'Captures',200,False,False),
('get','/captures/{id}',None,'CaptureDetail',200,False,False),
('get','/sources/{id}/captures',None,'Captures',200,False,False),
('post','/captures/{id}/retry','Retry','CaptureAccepted',202,True,False),
('post','/batch-previews','PreviewText','Preview',201,False,False),
('post','/batches','BatchConfirm','Batch',202,True,False),
('get','/batches/{id}',None,'Batch',200,False,False),
('get','/collections',None,'Groups',200,False,False),
('post','/collections','GroupCreate','Group',201,False,False),
('patch','/collections/{id}','GroupPatch','Group',200,False,False),
('delete','/collections/{id}','Cancel',None,204,False,False),
('put','/collections/{id}/captures/{capture_id}','Cancel','Editorial',200,False,False),
('delete','/collections/{id}/captures/{capture_id}','Cancel','Editorial',200,False,False),
('get','/tags',None,'Tags',200,False,False),
('post','/tags','TagCreate','Tag',201,False,False),
('patch','/tags/{id}','TagPatch','Tag',200,False,False),
('delete','/tags/{id}','Cancel',None,204,False,False),
('get','/exports/{id}',None,'ExportState',200,False,False),
('post','/captures/{id}/archive','Archive','Archived',200,False,True),
('get','/audit',None,'Audit',200,False,True),
('get','/settings/status',None,'Status',200,False,False),
('get','/users',None,'Users',200,False,True),
('patch','/users/{id}','UserPatch','User',200,False,True)]


def generated():
    paths={}
    for method,path,request,response,status,idempotent,admin in OPERATIONS:
        parameters=[]
        for field in ('id','capture_id'):
            if '{'+field+'}' in path:
                parameters.append(dict(name=field,**{'in':'path'},required=True,schema=UUID))
        if method=='get' and response in ('Captures','Groups','Tags','Users','Audit','Batch'):
            parameters += [dict(name='cursor',**{'in':'query'},schema=string(2048)),
                           dict(name='limit',**{'in':'query'},schema=dict(integer(1,100),default=25))]
        if method!='get': parameters.append(dict(name='X-CSRF-Token',**{'in':'header'},required=True,schema=string(512)))
        if idempotent: parameters.append(dict(name='Idempotency-Key',**{'in':'header'},required=True,schema=string(128,pattern='^[ -~]+$')))
        def ref(name): return {'$ref':'#/components/schemas/'+name}
        operation=dict(operationId=method+'_'+path.replace('/','_').replace('{id}','id'),parameters=parameters,
                       security=[{'sessionCookie':[]}],**{'x-required-role':'admin' if admin else 'editor',
                       'x-authorization':'Reauthorize resource membership, actor enablement, revisions and fences in service transaction.'},
                       responses={str(status):dict(description='Durable intent' if status==202 else 'Success',
                          **({'content':{'application/json':{'schema':ref(response)}}} if response else {}))})
        for code in CODES:
            operation['responses'][str(code)]={'description':', '.join(CODES[code]),
                'content':{'application/json':{'schema':ref('Error')}},
                **({'headers':{'Retry-After':{'schema':{'type':'integer','minimum':1},'description':'Bounded retry delay in seconds'}}} if code==429 else {})}
        if request: operation['requestBody']={'required':True,'content':{'application/json':{'schema':ref(request)}}}
        if path=='/captures' and method=='get':
            operation['parameters']=[dict(name=name,**{'in':'query'},schema=schema)
                for name,schema in DTOS['CaptureFilters']['properties'].items()]
            operation['x-reject-unknown-query-parameters']=True
        if path=='/batch-previews':
            operation['requestBody']['content']['multipart/form-data']={'schema':ref('PreviewUpload')}
            operation['description']='Select JSON text or multipart CSV, never both. Enforce CSV UTF-8 byte and row limits before preview.'
        paths.setdefault(path,{})[method]=operation
    doc={'openapi':'3.1.0','info':{'title':'Evidence Workspace core command contracts','version':'0.1.0',
        'description':'Proposed DTOs; no routes deployed. Byte and SSE responses are specified separately. Cookie name is a proposed contract detail.'},
        'servers':[{'url':'/api/v1'}],'paths':paths,
        'components':{'securitySchemes':{'sessionCookie':{'type':'apiKey','in':'cookie','name':'workspace_session'}},'schemas':DTOS}}
    for path,media in [('/captures/{id}/artifacts/{artifact_id}','application/octet-stream'),
                       ('/exports/{id}/download','application/zip'),('/audit/export','text/csv'),
                       ('/jobs/{id}/events','text/event-stream')]:
        params=[dict(name=field,**{'in':'path'},required=True,schema=UUID)
                for field in ('id','artifact_id') if '{'+field+'}' in path]
        if media=='text/event-stream':
            params.append(dict(name='Last-Event-ID',**{'in':'header'},schema=string(80)))
        doc['paths'][path]={'get':{'security':[{'sessionCookie':[]}],'parameters':params,
            'x-required-role':'admin' if path=='/audit/export' else 'editor',
            'responses':{'200':{'description':'Reauthorize and verify before success headers; raw archives attachment-only. SSE data uses JobEvent with id job_uuid:sequence.',
            'content':{media:{'schema':{'type':'string'}}}},'404':{'description':'Generic unavailable'},
            '503':{'description':'Dependency or integrity unavailable'}}}}
    files={'openapi/core-commands.openapi.json':canonical(doc)}
    for name,schema in DTOS.items():
        files[f'schemas/api-{name}.schema.json']=canonical(dict(schema,**{'$schema':'https://json-schema.org/draft/2020-12/schema','title':name}))
    def sample(schema):
        if 'const' in schema: return schema['const']
        if 'enum' in schema: return schema['enum'][0]
        if 'anyOf' in schema: return sample(schema['anyOf'][-1])
        kind=schema.get('type')
        if kind=='object': return {k:sample(schema['properties'][k]) for k in schema.get('required',[])}
        if kind=='array': return [sample(schema['items']) for _ in range(schema.get('minItems',0))]
        if kind=='integer': return schema.get('minimum',1)
        if kind=='boolean': return False
        if kind=='null': return None
        if schema==UUID: return '00000000-0000-4000-8000-000000000003'
        if schema==TIME: return '2026-11-09T12:00:00Z'
        if schema==URL: return 'https://example.org/article'
        if schema==HASH: return '0'*64
        return 'synthetic'
    examples={name:sample(schema) for name,schema in DTOS.items()}
    files['fixtures/api-positive.json']=canonical(examples)
    files['fixtures/api-negative.json']=canonical([
        {'dto':'CaptureSubmit','value':{'url':'https://example.org/','unexpected':True},'expected':'schema_unknown_field'},
        {'dto':'EditorialPatch','value':{'expected_revision':None},'expected':'schema_type'},
        {'dto':'ExportRequest','value':dict(examples['ExportRequest'],profile='workspace-export-v0/2'),'expected':'schema_const'}])
    return files


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--check',action='store_true');args=p.parse_args()
    write_generated(generated(),args.check)
