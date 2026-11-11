"""Read-only role-image inventory; this is not a capture/decoder dispatcher."""
from importlib.metadata import distributions
import json
import os
import platform
import sys


def main():
    role = sys.argv[1]
    result = {
        "role": role, "uid": os.getuid(), "gid": os.getgid(),
        "python": platform.python_version(), "architecture": platform.machine(),
        "dependencies": sorted((d.metadata["Name"], d.version) for d in distributions()),
        "capture_admission": "disabled",
    }
    if role == "capture":
        from playwright.sync_api import sync_playwright
        with sync_playwright() as p:
            result["chromium_executable"] = p.chromium.executable_path
            if not os.path.isfile(result["chromium_executable"]):
                raise RuntimeError("Matched Chromium is missing")
    elif role == "offline":
        from weasyprint import HTML
        result["pdf_smoke_bytes"] = len(HTML(string="<p>Synthetic image fixture</p>").write_pdf())
    else:
        raise ValueError("Unknown role")
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
