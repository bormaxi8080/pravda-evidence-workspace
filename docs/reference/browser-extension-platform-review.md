# Browser companion platform review

Reviewed: 2026-11-09. Status: **primary-documentation research, no extension built
or browser behavior tested**. Owner: browser/security engineering. Sources describe
platform capabilities; chosen Workspace boundaries are our engineering decisions.

| Primary source | Relevant fact / design consequence |
| --- | --- |
| [activeTab](https://developer.chrome.com/docs/extensions/develop/concepts/activeTab) | User invocation grants temporary tab access; same-origin navigation can retain it, another origin revokes it. Do not promise unrestricted recording. |
| [Tabs API](https://developer.chrome.com/docs/extensions/reference/api/tabs) | captureVisibleTab captures the active tab of a window and needs activeTab or all_urls. The documented maximum is two calls/second. Validate active tab around capture; use much lower product cadence. |
| [PageCapture API](https://developer.chrome.com/docs/extensions/reference/api/pageCapture) | saveAsMHTML returns tab MHTML under pageCapture permission. It is not an atomic PNG/MHTML transaction or a network WARC. |
| [Permissions API](https://developer.chrome.com/docs/extensions/reference/api/permissions) | Optional capabilities/hosts can be requested through a user gesture. Declare possible HTTPS hosts but request only the configured Workspace host; declared patterns are not granted access. |
| [Service worker lifecycle](https://developer.chrome.com/docs/extensions/develop/concepts/service-workers/lifecycle) | Workers can terminate and lose globals; long operations/network waits face limits. Persist bounded state, use resumable requests and test termination rather than artificial keep-alive. |
| [Storage API](https://developer.chrome.com/docs/extensions/reference/api/storage) | Session storage is memory-backed and clears on restart/update/disable; local data can survive history clearing. Use trusted-context session storage for short-lived credentials and explicit bounded IndexedDB staging for evidence. |
| [Network requests](https://developer.chrome.com/docs/extensions/develop/concepts/network-requests) | Extension cross-origin access uses host permissions; paths do not constrain that permission. Broker exact-origin/path requests in trusted extension code, never a page-controlled arbitrary fetch proxy. |
| [Scripting API](https://developer.chrome.com/docs/extensions/reference/api/scripting) | Injection results/targets carry document identity on supported Chrome versions; use top-frame identity with event fencing, not URL equality alone. |
| [Content scripts](https://developer.chrome.com/docs/extensions/develop/concepts/content-scripts) | Isolated execution worlds share the page DOM. Isolation does not make page-supplied values trustworthy. |
| [Messaging](https://developer.chrome.com/docs/extensions/develop/concepts/messaging) | Extension contexts communicate through messages; validate senders and bounded typed messages at the privileged boundary. |
| [Side panel](https://developer.chrome.com/docs/extensions/reference/api/sidePanel) | Extension UI can sit alongside a page. Selected for the later assisted session so controls need not disappear with a popup. |
| [Extension CSP](https://developer.chrome.com/docs/extensions/reference/manifest/content-security-policy) and [remote hosted code](https://developer.chrome.com/docs/extensions/develop/migrate/remote-hosted-code) | Package executable logic and enforce restrictive extension-page CSP. Server capabilities are data, not downloaded scripts. |
| [Chrome Web Store user-data guidance](https://developer.chrome.com/docs/webstore/program-policies/user-data-faq) | Captured page content/browsing information needs accurate handling disclosures, including local handling. Store publication needs its own current-policy review and authorization. |
| [RFC 8628](https://www.rfc-editor.org/rfc/rfc8628) | Device authorization separates user approval from secret polling, with expiry and polling/error controls. Our bounded pairing adopts that pattern; it does not claim to implement a general OAuth authorization server. |

## Selection and limits

Select Chromium Manifest V3, TypeScript, bundled UI and Chrome 120 as an API floor;
this floor does not promise support for outdated browsers. Qualify current stable
and the preceding supported stable on Windows/macOS/Linux, record exact versions,
and reopen the floor if real API/security tests require it. Edge requires its own
package/identity/qualification; Firefox/Safari/mobile are deferred adapters.

Do not request all_urls, cookies, history, debugger, proxy, nativeMessaging,
webRequest, downloads or background access to arbitrary sites in B0–B2. An optional
HTTPS host declaration exists only for pairing with a user-selected self-hosted
Workspace. Source-page access relies on activeTab; B2 must pause when that grant
or foreground-tab identity no longer suffices. No permission-free automatic recorder
or full-fidelity guarantee follows from vendor documentation.

Authenticated page content may already contain sensitive values even without cookie
API access. Absence of cookie extraction is not a sanitization guarantee. Local
browser/profile compromise and a dishonest collector are outside attestation claims.

See [ADR-007](../decisions/0007-browser-companion-acquisition.md) and
[requirements 34–38](../requirements/34-browser-companion-architecture.md).
