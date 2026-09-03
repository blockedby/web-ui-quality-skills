# Web UI Quality Skills

A small, selective skill set for building and reviewing browser interfaces. Each skill is independent: install only the workflow you need instead of loading a framework-specific bundle.

## Selective skills.sh installs

Run one command per skill:

```sh
npx skills add blockedby/web-ui-quality-skills --skill frontend-quality
npx skills add blockedby/web-ui-quality-skills --skill visual-composition
npx skills add blockedby/web-ui-quality-skills --skill static-html-browser-audit
```

The install source is `blockedby/web-ui-quality-skills`; the skill names map directly to the directories under [`skills/`](skills/).

## Included skills

| Skill | Use it for | Contract |
| --- | --- | --- |
| [`frontend-quality`](skills/frontend-quality/SKILL.md) | Implementation and review of an existing frontend | Takes requirements and the current frontend stack; returns evidence-backed implementation or review guidance. |
| [`visual-composition`](skills/visual-composition/SKILL.md) | Turning a visual brief into a product-specific surface | Takes a visual brief; returns coherent hierarchy, composition, states, and responsive decisions. |
| [`static-html-browser-audit`](skills/static-html-browser-audit/SKILL.md) | Fast, local checks for static HTML pages | Takes local HTML paths and an optional viewport; checks parsing, dependencies, local links, and horizontal overflow. |

These are generic workflows. They do not replace a framework, invent product requirements, treat decoration as proof of quality, mutate a network, or deploy an application.

## Local audit quick start

The audit helper uses only the Python standard library for its static checks:

```sh
python3 skills/static-html-browser-audit/scripts/audit.py ./site/index.html --viewport 390x844
python3 skills/static-html-browser-audit/scripts/audit.py ./site --viewport 1280x800 --json
```

External URLs are reported but never fetched. Static overflow analysis is always available; add `--browser` when a local Chromium/Chrome binary is available for a computed `scrollWidth`/viewport measurement. Browser mode runs in a disposable profile with page JavaScript disabled by default.

Exit status is `0` when no error findings are present, `1` when an audit finding fails (or `--strict` escalates warnings), and `2` for invalid command input. A static “pass” means no obvious source-level risk was found; it is not a substitute for rendered browser evidence.

## Validation

From the repository root:

```sh
./validate.sh
# equivalent: python3 scripts/validate_repository.py
```

Validation checks all three skill contracts and frontmatter, compiles the dependency-light helpers, runs a passing fixture through the static audit, and confirms that a deliberately broken fixture is detected. Browser-mode validation is run when Chromium is available.

## License

MIT © 2026 Alexandr Kondakov. See [`LICENSE`](LICENSE).
