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

## Choosing and combining skills

- Use `visual-composition` for design decisions, implementation with visual direction, or visual review. The requested mode determines the deliverable; small edits do not need a full design brief.
- Use `frontend-quality` for implementation contracts, state/data behavior, and evidence-backed review. Both skills include optional references for operational screens; read only the relevant reference.
- Use `static-html-browser-audit` for its bounded local HTML checks. Dynamic application behavior requires a suitable browser workflow and is not proven by this helper.

Install only the relevant skills, then check that your agent discovers them. Keeping this repository on disk does not itself load its instructions. If necessary, explicitly invoke an installed skill by name.

Optional external companions: [Anthropic frontend-design](https://github.com/anthropics/skills/tree/main/skills/frontend-design) for expressive visual direction, [UI/UX Pro Max](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill) for searchable design references, and [Vercel agent-skills](https://github.com/vercel-labs/agent-skills) for an additional interface review or React-specific implementation guidance. These are not dependencies or bundled copies. Choose them for a concrete gap; preserve the project's existing design and behavior contracts when recommendations differ.

## Focused guidance

`visual-composition` includes references for typography and visual hierarchy, color/theme/state design, analytical charts, durable design decisions, operational screens, and weak/better examples. `frontend-quality` includes references for form validation and persistence, overlay focus and announcements, operational contracts, and interaction examples. Each skill routes to its own bundled references and can be installed independently.

The guidance adapts ideas from the optional external companions linked above: intentional visual decisions and critique (Anthropic), topic-specific UX guidance and shared/page design decisions (UI/UX Pro Max), and actionable review rules and weak/better examples (Vercel). It is written for this repository rather than copied as an external rule bundle. Universal row-count thresholds, forced typography casing, mandatory animation, and blanket bans on local horizontal scrolling are deliberately not adopted.

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

For behavioral evaluation, use the [manual scenarios](tests/behavior/README.md) to compare base and candidate instructions in fresh sessions. These cover redundant copy, necessary context, implementation vs. handoff, table semantics, review evidence, and small-task scope. The automated validator does not run these scenarios or prove that an agent follows the guidance.

## License

MIT © 2026 Alexandr Kondakov. See [`LICENSE`](LICENSE).
