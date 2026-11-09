# Interactive UI blueprints

Design revision 0.10. English, synthetic, offline design artifacts for Evidence
Workspace and its browser companion. These files are owned by UI Prototype;
they are not the deployed application or an installed browser extension.

## Open and review

Open [index.html](index.html) in a browser; no server, package installation or
credentials are needed. Open [extension.html](extension.html) for popup, side-panel
and options designs. All fonts/assets are local system/repository resources.
The [original root mockup](../index.html) remains a historical reference.

Workspace has 23 screen designs. Use navigation, target, role and state controls.
Core transitions are connected synthetic simulations; later report/search/transfer/
access screens provide layouts and explanatory previews, not complete applications.
Reload resets the in-memory model; no captures, cookies, API calls or secrets exist.

Examples (append to the local HTML filename):

- `index.html#capture`: evidence tabs, editable context, review and importance.
- `index.html?role=editor#publication`: administrator-only publication boundary.
- `index.html?theme=dark#compare`: future offline comparison in dark theme.
- `index.html?state=queue-full#new`: no accepted request at capacity.
- `index.html#pairing`: manual demonstration code/phrase and exact scopes.
- `extension.html?state=unpaired`: request/approve synthetic pairing.
- `extension.html?target=B1&state=local-review`: selected local bytes and upload consent.
- `extension.html?target=B2&surface=sidepanel&state=paused`: explicit session resume.
- `extension.html?target=B2&state=unregistered`: stopped unregistered descriptor → new manual B1 review.

Design tools are not product controls. Future screens visibly identify their stage.
Choosing one raises the design target; returning to V0 closes future product previews.
The sample source page and all people/records are fictional. Dates/counts/digests/
progress/backup status are illustrative; no fixture digest verifies a real capture.

## Previews

| Workspace | Companion |
| --- | --- |
| [Overview](previews/workspace-overview.png) | [Local upload review](previews/extension-local-review.png) |
| [Evidence and editorial layers](previews/workspace-evidence.png) | [Assisted session](previews/extension-assisted-session.png) |
| [Dark comparison](previews/workspace-comparison-dark.png) | [Narrow viewport](previews/extension-mobile.png) |
| [Narrow archive](previews/workspace-mobile.png) | Popup 360 px / side panel 384 px within responsive studio |

The narrow archive deliberately scrolls its table inside a labeled region; the page
itself does not overflow. Extension studio controls precede the mock extension on
small screens, so scroll to inspect the entire frame. Screenshots are design outputs,
not real captured evidence or proof of application access/security.

## Reproduce design checks

Requires Node 22 with built-in WebSocket and an installed Chrome that can run an
isolated headless profile. No npm dependencies. Example on this development machine:

```bash
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
  --headless=new --no-first-run --no-default-browser-check \
  --disable-background-networking --disable-component-update \
  --remote-debugging-port=9337 \
  --user-data-dir=/private/tmp/evidence-ui-design-check about:blank
```

In a separate shell from repository root:

```bash
node --check design/workspace.js
node --check design/extension.js
node --check design/verify-ui.mjs
node design/verify-ui.mjs
```

Use only an isolated disposable profile on a trusted local machine, never a personal
browser debugging port. The checker creates and closes its own target, loads local
files, exercises design flows, checks page overflow/JS exceptions/network requests,
and refreshes seven preview PNGs. `DESIGN_CDP_PORT` can select another local port.
Stop the isolated Chrome process after checking. No application service is started.

The design evidence run on 2026-11-09 used Node 22.22.3 and Chrome 157.0.8103.39,
1500×1050, 1024×768 and 390×844 CSS-pixel viewports. The final run passed 216
design checks across 23 Workspace screens and companion flows, with no JavaScript
exceptions or HTTP requests from the pages. Seven screenshots were visually inspected.
Keyboard evidence includes dialog focus containment and Escape dismissal; full
keyboard/assistive-technology qualification remains pending. This is not
a supported-browser commitment or an accessibility audit. Real OAuth/PG/Docker/
SSRF/queue/integrity/revocation/extension/restore proof remains unperformed.

See [UI contracts](../docs/requirements/54-ui-blueprints-and-interaction-map.md),
[versioned implementation plan](../docs/requirements/55-versioned-implementation-plan.md)
and [ADR-011](../docs/decisions/0011-ui-blueprints-and-versioned-delivery.md).
