"""Emit CycloneDX inventory from the installed image, without package installers."""
import hashlib
from importlib.metadata import distributions
import json
from pathlib import Path
import platform
import subprocess
from urllib.parse import quote

components = []
for dist in distributions():
    name, version = dist.metadata['Name'], dist.version
    components.append({"type": "library", "name": name, "version": version,
                       "purl": f"pkg:pypi/{quote(name.lower())}@{quote(version)}"})
browser = Path('/opt/browsers/chromium-1194/chrome-linux/chrome')
if browser.is_file():
    components.append({"type": "application", "name": "Chromium", "version": "141.0.7390.37",
                       "hashes": [{"alg": "SHA-256", "content": hashlib.sha256(browser.read_bytes()).hexdigest()}]})
rows = subprocess.check_output(['dpkg-query', '-W', '-f=${Package}\t${Version}\t${Architecture}\n'], text=True)
for row in rows.splitlines():
    name, version, arch = row.split('\t')
    components.append({"type": "library", "name": name, "version": version,
                       "purl": f"pkg:deb/debian/{quote(name)}@{quote(version)}?arch={arch}&distro=bookworm"})
print(json.dumps({"bomFormat": "CycloneDX", "specVersion": "1.6", "version": 1,
    "metadata": {"component": {"type": "application", "name": "provereno-role-image", "version": "1.1.1"},
                 "properties": [{"name": "python", "value": platform.python_version()},
                                {"name": "wheel-sha256", "value": Path('/usr/share/provereno/wheel.sha256').read_text().split()[0]}]},
    "components": sorted(components, key=lambda c: c.get('purl', c['name']))}, sort_keys=True, indent=2))
