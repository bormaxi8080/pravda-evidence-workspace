"""Real disposable PG16/web and role-image checks; synthetic data only."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import time
import urllib.request
import uuid


def run(*args, **kw):
    return subprocess.check_output(['docker', *args], text=True, **kw).strip()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--identities', type=Path, required=True,
                        help='Build record produced by build_images.py')
    args = parser.parse_args()
    record = json.loads(args.identities.read_text())
    root = Path(__file__).resolve().parents[1]
    paths = [root/'Dockerfile', root/'.dockerignore', root/'pyproject.toml']
    paths += sorted((root/'locks').glob('*.txt'))
    paths += sorted(p for p in (root/'provereno').rglob('*')
                    if p.is_file() and '__pycache__' not in p.parts and p.suffix != '.pyc')
    current = {str(p.relative_to(root)): hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}
    if current != record['context_files']:
        raise RuntimeError('Source differs from build record; rebuild before verification')
    for role in ('web', 'capture', 'offline'):
        image = json.loads(run('image', 'inspect', 'provereno-loc5/'+role+':1.1.1'))[0]
        if image['Id'] != record['images'][role]['id']:
            raise RuntimeError('Image differs from build record: '+role)
        assert image['Config']['User'] == '10001:10001'
        assert not image['Config'].get('Volumes'), 'Unexpected implicit runtime volume'
        assert not any(value.split('=', 1)[0] in
                       ('DATABASE_URL', 'SESSION_SECRET_KEY', 'GITHUB_CLIENT_SECRET')
                       for value in image['Config']['Env']), 'Baked runtime configuration'
        sbom = args.identities.parent/(role+'.cdx.json')
        if hashlib.sha256(sbom.read_bytes()).hexdigest() != record['images'][role]['sbom_sha256']:
            raise RuntimeError('SBOM differs from build record: '+role)
    name = 'provereno-loc5-' + uuid.uuid4().hex[:10]
    label = ['--label', 'org.provereno.task=LOC-5']
    owned = []
    network = False
    try:
        run('network', 'create', *label, name)
        network = True
        db = run('run', '-d', '--name', name+'-db', *label, '--network', name,
                 '--network-alias', 'db', '--tmpfs', '/var/lib/postgresql/data',
                 '-e', 'POSTGRES_PASSWORD=synthetic-fixture-only',
                 'postgres:16.10-bookworm')
        owned.append(db)
        for _ in range(60):
            if subprocess.run(['docker', 'exec', db, 'pg_isready', '-U', 'postgres'],
                              stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).returncode == 0:
                break
            time.sleep(1)
        else:
            raise RuntimeError('PG16 readiness timeout')
        flags = ['--read-only', '--cap-drop=ALL', '--security-opt=no-new-privileges',
                 '--tmpfs', '/tmp:rw,nosuid,nodev,size=64m', '--pids-limit', '128',
                 '--memory', '512m', '--cpus', '1']
        web = run('run', '-d', *label, '--network', name, *flags,
                  '-p', '127.0.0.1::8080', '-e',
                  'DATABASE_URL=postgresql+asyncpg://postgres:synthetic-fixture-only@db/postgres',
                  '-e', 'SESSION_SECRET_KEY=synthetic-fixture-session-key-32-characters',
                  'provereno-loc5/web:1.1.1')
        owned.append(web)
        port = run('port', web, '8080/tcp').split(':')[-1]
        for _ in range(60):
            try:
                with urllib.request.urlopen('http://127.0.0.1:'+port+'/auth/login', timeout=2) as response:
                    assert response.status == 200
                    assert b'<html' in response.read().lower()
                break
            except Exception:
                time.sleep(1)
        else:
            raise RuntimeError('Web login readiness timeout: '+run('logs', web))
        with urllib.request.urlopen('http://127.0.0.1:'+port+'/static/style.css', timeout=2) as response:
            assert response.status == 200 and len(response.read()) > 0
        check = '''
import asyncio, importlib.util, os, pathlib, shutil
from provereno.jobs import enqueue
from provereno.config import Settings
from fastapi import HTTPException
from pydantic import ValidationError
assert os.getuid() == 10001
try:
    Settings(_env_file=None, session_secret_key='')
except ValidationError:
    pass
else:
    raise AssertionError('Empty session key accepted')
for module in ('playwright', 'weasyprint', 'pip', 'setuptools'):
    assert importlib.util.find_spec(module) is None, module
for binary in ('gcc','g++','cc','make','chromium','google-chrome'):
    assert shutil.which(binary) is None, binary
assert not pathlib.Path('/var/run/docker.sock').exists()
assert not pathlib.Path('/app/provereno').exists()
assert not pathlib.Path('/runtime/.env').exists()
assert not pathlib.Path('/opt/browsers').exists()
try:
    pathlib.Path('/runtime/write-probe').write_text('synthetic')
except OSError:
    pass
else:
    raise AssertionError('Runtime root is writable')
async def check():
    try:
        await enqueue('https://example.invalid')
    except HTTPException as e:
        assert e.status_code == 503
    else:
        raise AssertionError('Capture admitted')
asyncio.run(check())
print('web UID/package/compiler/socket/capture-denial checks passed')
'''
        print(run('exec', web, 'python', '-c', check))
        tables = run('exec', db, 'psql', '-U', 'postgres', '-Atc',
                     "SELECT count(*) FROM pg_tables WHERE schemaname='public'")
        assert tables == '0', 'Startup created schema'
        for role in ('capture','offline'):
            result = run('run', '--rm', *label, '--network=none', *flags,
                         'provereno-loc5/'+role+':1.1.1')
            info = json.loads(result)
            assert info['uid'] == 10001
            print(result)
        browser = '/opt/browsers/chromium-1194/chrome-linux/chrome'
        linked = run('run', '--rm', *label, '--network=none', *flags,
                     'provereno-loc5/capture:1.1.1', 'ldd', browser)
        assert 'not found' not in linked, linked
        print(run('run', '--rm', *label, '--network=none', *flags,
                  'provereno-loc5/capture:1.1.1', browser, '--version'))
        print(json.dumps({'result':'PASS', 'web_login':200, 'schema_tables':0,
                          'db_image':json.loads(run('inspect', db))[0]['Image'],
                          'web_image':json.loads(run('inspect', web))[0]['Image'],
                          'loopback_port':port, 'fixture':'synthetic PG16, no host mounts'}))
    finally:
        for container in reversed(owned):
            run('rm', '-f', container)
        if network:
            run('network', 'rm', name)


if __name__ == '__main__':
    main()
