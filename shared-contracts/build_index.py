"""Fingerprint the current contract corpus, excluding this index's own digest."""
import argparse
import hashlib
from pathlib import Path
from build_core import write_generated
from validate import canonical
ROOT=Path(__file__).resolve().parent


def generated():
    paths=sorted(p for folder in ['schemas','fixtures','openapi'] for p in (ROOT/folder).rglob('*.json'))
    return {'contract-index.json':canonical({'version':1,'component':'evidence-contracts','component_version':'0.1.0',
        'catalogue':['CTR-01','CTR-02','CTR-03'],
        'authorities':{'inventory':'schemas/workspace-capture-v0-1.schema.json','engine':'build_engine.py',
                       'profiles_jobs_events':'build_core.py','api':'build_api.py'},
        'sha256':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}})}


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--check',action='store_true');args=p.parse_args()
    write_generated(generated(),args.check)
