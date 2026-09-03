---
name: static-html-browser-audit
description: Audit local static HTML pages for parse errors, local and external dependencies, broken local links, and horizontal overflow at an optional viewport without fetching or mutating a network.
license: MIT
---

# Static HTML Browser Audit

Use this skill for a bounded, read-only audit of local `.html`/`.htm` pages. It is deliberately generic: it reports evidence from the files and, when requested, a disposable local Chromium measurement. It does not crawl a site, submit forms, call external URLs, deploy anything, or replace a frontend framework.

## Contract

**Inputs**

- One or more local HTML file paths, or directories containing local HTML files.
- An optional viewport such as `390x844` or `1440x900`; the default is `1280x800`.
- Optional `--root` for resolving site-root references such as `/assets/app.css`.
- Optional `--browser` and `--chromium PATH` for a computed layout measurement when a local Chromium/Chrome binary is available.

**Outputs**

For every discovered HTML file, report four named checks:

1. **Parse errors** — malformed parser input, mismatched non-void tags, and suspicious unclosed structural tags with file/line evidence.
2. **Dependencies** — local resources and whether they exist, plus external resources that were identified but deliberately not fetched. HTML resources and local CSS `url()`/`@import` references are included.
3. **Broken local links** — missing local `a`/`area` targets and missing same-document or local-document fragments when the target can be inspected.
4. **Horizontal overflow** — source-level width/nowrap risks for every run; with `--browser`, actual `scrollWidth` and outlying element bounds at each requested viewport.

The default human report is concise and the `--json` report is machine-readable. Exit `0` means no error findings, `1` means an error finding (or a warning escalated by `--strict`), and `2` means invalid CLI input. External dependencies are informational and are never a failure merely because they are external.

A static overflow pass means “no obvious source-level risk found,” not “the rendered page is proven safe.” Treat a browser measurement as the stronger evidence and record the browser, viewport, and whether page JavaScript was enabled.

## Run the bundled helper

From the repository root:

```sh
python3 skills/static-html-browser-audit/scripts/audit.py ./site/index.html --viewport 390x844
python3 skills/static-html-browser-audit/scripts/audit.py ./site --viewport 390x844 --viewport 1440x900 --json
python3 skills/static-html-browser-audit/scripts/audit.py ./site/index.html --browser --chromium chromium
```

The helper is Python 3 standard-library code; it has no package install step. Use `--help` for all options. It follows local references without issuing HTTP requests. Browser mode uses a disposable profile, blocks hostname resolution for page resources, and disables page JavaScript by default. Use `--allow-page-javascript` only for an explicitly authorized, read-only local page when script-rendered geometry is part of the question; do not click, submit, or mutate state.

## Audit procedure

### 1. Establish scope

- Expand only the supplied files and HTML files directly under supplied directories (recursively, in deterministic path order).
- Resolve relative resources from the referring file. Resolve leading `/` references from `--root`, or the common supplied site directory when no root is provided.
- Keep query strings and fragments out of filesystem existence checks. URL-decode local paths, but do not normalize a reference into a path outside the intended root without surfacing it.
- Treat `http:`, `https:`, protocol-relative URLs, and other non-file schemes as external or non-file references. Report them; never fetch them.
- Use the requested viewport(s) for overflow checks. If no viewport is supplied, state that the default `1280x800` was used.

### 2. Check parsing

Parse with a forgiving HTML parser but report structural evidence rather than pretending browsers reject all imperfect HTML. Flag mismatched closing tags and unclosed non-optional elements; do not flag valid void elements or common optional HTML end tags solely because their closing tag is omitted. A parser exception is an error. Include the source line when available.

Do not turn missing optional metadata, a fragment-only document, or framework-generated markup into a parse failure unless it is part of the supplied acceptance criteria.

### 3. Inventory dependencies

Inspect URL-bearing HTML attributes including `script[src]`, `link[href]`, `img[src/srcset]`, `source[src/srcset]`, `video[src/poster]`, `audio[src]`, `iframe[src]`, `object[data]`, `embed[src]`, `track[src]`, SVG `image`/`use` references, and CSS `url()`/`@import` values in linked or inline styles. Classify each as:

- **local present** — resolved path exists;
- **local missing** — resolved path does not exist, an error finding;
- **external unverified** — network URL or protocol-relative URL, informational only;
- **non-file/inline** — `data:`, `blob:`, `mailto:`, `tel:`, `javascript:`, fragment-only, or similar, reported only when useful.

Read local CSS as UTF-8 with a clear warning if it cannot be read. Follow local CSS dependencies with cycle protection. Do not treat an external stylesheet's internal assets as locally auditable.

### 4. Check local links

Inspect navigation links in `a[href]` and `area[href]`. For a local path, check the file or directory (including an `index.html`/`index.htm` entry point). For `#fragment`, check the current document's `id` values and named anchors. For a local HTML target with a fragment, inspect that target's IDs/named anchors. Report the raw reference, resolved target, and source line. Skip external and non-file schemes instead of attempting network validation.

A missing asset and a broken navigation link are separate findings even if they resolve to the same path. Report each check independently so one noisy page does not hide the rest.

### 5. Check horizontal overflow

Always run the source-level pass. Look for fixed or minimum widths larger than the requested viewport, oversized numeric width attributes, long unbreakable text/preformatted content, and likely nowrap combinations. Label these as risks because CSS cascade, intrinsic layout, font metrics, replaced-element behavior, and scripts can change the result.

When `--browser` is available, measure each page and viewport in an isolated local Chromium session:

- set the viewport before navigation;
- wait for the local document to settle without interacting with it;
- compare `document.documentElement.scrollWidth` and `document.body.scrollWidth` with `window.innerWidth`;
- inspect element bounds for content extending beyond the left or right viewport edge;
- report the measured widths, viewport, browser path, and a short list of offending elements.

A browser overflow finding is an error by default. Fix the responsible element or its intrinsic sizing; do not recommend page-level `overflow-x: hidden` as a concealment strategy. If browser mode cannot start, report it as not run rather than presenting source heuristics as rendered proof.

## Report shape

A JSON result has this shape (additional evidence fields are allowed):

```json
{
  "path": "site/index.html",
  "viewport": {"width": 390, "height": 844},
  "checks": {
    "parse": {"status": "pass", "findings": []},
    "dependencies": {
      "status": "pass",
      "local": [{"reference": "styles.css", "status": "present"}],
      "external": [{"reference": "https://example.test/font.css", "status": "unverified"}],
      "findings": []
    },
    "links": {"status": "pass", "checked": 1, "broken": [], "findings": []},
    "horizontal_overflow": {
      "status": "pass",
      "mode": "static",
      "verified": false,
      "risks": [],
      "measurements": [],
      "findings": []
    }
  },
  "summary": {"errors": 0, "warnings": 0}
}
```

For a handoff, state the aggregate conclusion first, then list paths, check statuses, exact findings, command/viewport evidence, and residual limitations. Do not silently convert “not run,” “external unverified,” or static-only evidence into a pass claim.

## Non-goals

This skill does not validate subjective visual taste, accessibility conformance, JavaScript application behavior, remote availability, SEO, security, network contracts, automatic deployment, or framework replacement. Pair it with `frontend-quality` for implementation/review guidance and `visual-composition` for design decisions; do not use this audit as proof of either.
