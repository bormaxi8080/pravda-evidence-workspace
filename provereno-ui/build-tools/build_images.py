"""Build the three local ARM role images and record source/image/SBOM identities.

Outputs contain synthetic build inventories only. No registry publication occurs.
"""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[1]


def run(*args, **kwargs):
    return subprocess.check_output(args, text=True, **kwargs)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--no-cache', action='store_true')
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    paths = [ROOT/'Dockerfile', ROOT/'.dockerignore', ROOT/'pyproject.toml']
    paths += sorted((ROOT/'locks').glob('*.txt'))
    paths += sorted(p for p in (ROOT/'provereno').rglob('*')
                    if p.is_file() and '__pycache__' not in p.parts and p.suffix != '.pyc')
    source = {str(p.relative_to(ROOT)): digest(p.read_bytes()) for p in paths}
    record = {'lane': 'MAC-DEV', 'source_commit': run('git', 'rev-parse', 'HEAD').strip(),
              'context_files': source,
              'context_sha256': digest(json.dumps(source, sort_keys=True).encode()),
              'images': {}, 'docker_context': run('docker', 'context', 'show').strip()}
    for role in ('web', 'capture', 'offline'):
        tag = f'provereno-loc5/{role}:1.1.1'
        command = ['docker', 'build', '--platform', 'linux/arm64', '--target', role, '-t', tag]
        if args.no_cache:
            command.append('--no-cache')
        subprocess.run(command + [str(ROOT)], check=True)
        info = json.loads(run('docker', 'image', 'inspect', tag))[0]
        sbom = run('docker', 'run', '--rm', '-i', '--label', 'org.provereno.task=LOC-5',
                   '--network=none', '--read-only', '--cap-drop=ALL', '--security-opt=no-new-privileges',
                   tag, 'python', '-', input=(ROOT/'build-tools/inventory.py').read_text())
        sbom_path = args.output/f'{role}.cdx.json'
        sbom_path.write_text(sbom)
        record['images'][role] = {'tag': tag, 'id': info['Id'], 'architecture': info['Architecture'],
                                  'uid_gid': info['Config']['User'], 'sbom_sha256': digest(sbom.encode())}
        (args.output/'identities.json').write_text(json.dumps(record, indent=2)+'\n')


if __name__ == '__main__':
    main()
