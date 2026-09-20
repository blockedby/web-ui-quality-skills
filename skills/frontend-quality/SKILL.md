---
name: frontend-quality
description: Use when planning, implementing, or reviewing frontend code changes against an existing product stack, UI contract, and fresh verification evidence.
license: MIT
---

# Frontend Quality

Use this skill as an evidence-led implementation and review checklist for an existing frontend. It improves the changed surface without silently replacing its framework, data flow, visual system, or public behavior.

## Contract

**Inputs**

- The requirements, acceptance criteria, primary user task, and a verification plan.
- The current frontend stack: framework and version, runtime, rendering mode, routing, styling approach, design tokens, supported browsers, and build/test commands.
- The existing surface map: route entry point, adjacent components, layout wrappers, hooks, client services, state/query patterns, API contracts, styles, assets, and relevant tests.
- Required data and interaction states: loading, empty, partial, error, success, disabled, submitting, permission-denied, selected, and expanded states where relevant.
- Supported viewport range, input methods, locales, themes, accessibility needs, performance constraints, and explicit files, APIs, or behavior that must not change.

**Outputs**

- Verified implementation guidance or review findings tied to the supplied requirements and inspected code.
- A focused change boundary, reuse targets, component/state contracts, responsive behavior, accessibility obligations, and relevant performance or motion decisions.
- Fresh verification evidence: commands and results, rendered/browser checks when relevant, unresolved questions, and residual risks. Do not call an assertion verified from source inspection alone.

If an input is missing, label the unknown. Do not invent product behavior when it would change a component contract, data flow, navigation path, permission boundary, or user consequence.

## Inspect before changing

1. Read the acceptance criteria and identify the primary task and the changed surface.
2. Trace the route from entry point through layout, components, state, client calls, styles, and tests.
3. Find the existing source of truth for primitives, tokens, navigation, forms, validation, permissions, feature flags, loading boundaries, and data fetching.
4. Inspect nearby surfaces for behavior and composition, not only matching colors. Record contracts that must remain stable: props, events, URLs, data shapes, focus behavior, and persisted state.
5. Write down affected UI states, responsive boundaries, and content risks before extracting or adding code.

## Implementation and review lens

### 1. Contracts and reuse

- Reuse shared components, layout wrappers, tokens, hooks, route helpers, form helpers, and API clients when their semantics and behavior match.
- Keep route orchestration near the route and reusable presentation or interaction in the repository's established shared layer.
- Prefer small explicit variants and composition over a growing set of unrelated boolean props.
- Preserve public props, events, routes, data shapes, focus order, and persisted state unless a deliberate breaking change is in scope.
- Use direct imports when a convenience barrel would pull unrelated client code or hide ownership.

### 2. State and data flow

- Represent mutually exclusive states with one explicit status or discriminated state instead of contradictory booleans.
- Keep one source of truth for server data and one deliberate owner for local interaction state; derive display values during render when possible.
- Reuse established query, cache, mutation, invalidation, cancellation, retry, and error conventions.
- Start independent work together and handle stale responses, duplicate submission, optimistic failure, and unmount behavior where they affect the user.
- Keep the stable page shell visible while a nested region waits. Localize loading, empty, permission, and error feedback to the owning region.
- Preserve useful previous content during refresh when it keeps the user oriented, and show pending feedback beside the action that caused it.

### 3. Semantic interaction and accessibility

- Use headings for structure, lists for collections, links for navigation, buttons for actions, and native form controls when they provide the needed behavior.
- Give every control an accessible name, every visible field a persistent label, and every meaningful image useful alternative text. Keep decorative media silent.
- Provide visible `:focus-visible` treatment and preserve logical reading, tab, and focus order when layout changes.
- Support keyboard activation, dismissal, navigation, focus return, and correct expanded/selected/disabled/pending semantics for composite controls.
- Associate help and validation messages with their fields; do not communicate status by color alone.
- Respect reduced motion, zoom, larger text, high contrast, forced colors, touch targets, paste, native editing, and password-manager behavior where applicable.

### 4. Responsive and content resilience

- Recompose with grid, flexbox, intrinsic sizing, wrapping, and content-driven breakpoints before reaching for JavaScript measurement.
- Let flexible children shrink (`min-width: 0` where needed); wrap or intentionally truncate long values while preserving access to the full value.
- Fix the element that overflows. Do not hide page-level overflow to conceal clipping or broken geometry.
- Check narrow, tablet, and wide layouts with short, typical, long, missing, malformed, localized, and zoomed content.
- Preserve task order and DOM reading order as columns collapse; keep controls usable with touch, mouse, and keyboard.
- Reserve space for images, charts, embeds, asynchronous labels, and deferred panels to avoid layout shifts.

### 5. Purposeful headings and labels

- Do not add unnecessary eyebrow headings, overlines, or decorative labels above titles. Remove them when they merely repeat the title, name an obvious category, or fill visual space.
- Keep an overline only when it supplies distinct, task-relevant context that the title does not convey, such as the current project or a step in a workflow. Uppercase styling or an accent color is not a reason to add text.
- For example, omit “ПОИСКИ ВАКАНСИЙ” above “Источники” on a vacancy-source screen: it consumes space without helping the user understand or operate the screen. Prefer the title alone and useful supporting instructions where needed.
- Apply the same test to subtitles, helper copy, badges, and repeated navigation: retain text that changes a decision, clarifies scope, or explains recovery; remove narration of obvious controls. Preserve field labels and accessible names.

### 6. Operational screen contracts

For changes involving tables, filters, pagination, selection, or bulk actions, read [Operational screen contracts](references/operational-screens.md). Preserve existing semantics and clarify missing consequential behavior before implementing it; the reference is not a requirement to add features.

### 7. Performance, motion, and media

- Measure a user-visible bottleneck before adding memoization, virtualization, layout reads, or other complexity.
- Keep the initial route bundle limited to the first useful interaction; defer heavy editors, charts, media, optional panels, and third-party scripts when justified.
- Use explicit image dimensions/aspect ratios, prioritize critical media, and keep server-only work out of client bundles where the architecture supports it.
- Animate only to explain hierarchy, progress, appearance, disappearance, or spatial relationship. Prefer transform/opacity, keep transitions interruptible, and define a reduced-motion treatment.
- Avoid waterfalls, broad `transition: all`, repeated layout reads, blocked typing/scrolling, and speculative optimization without visible benefit.

## State and content matrix

Before implementation or sign-off, mark each relevant row as implemented, reviewed, not applicable, or unknown:

| Dimension | Questions |
| --- | --- |
| Loading/pending | Does the stable shell remain usable? Is progress feedback near its cause? |
| Empty/partial | Does the user know what is absent and what to do next? |
| Error/permission | Is the cause and recovery action local, understandable, and safe? |
| Success/disabled | Is the consequence confirmed without obscuring the next step? Are unavailable actions truthful? |
| Long/malformed/localized | Do labels, values, user content, and validation survive realistic expansion? |
| Responsive/input | Is the primary task usable at supported widths with keyboard, touch, and pointer input? |
| Focus/semantics | Can a keyboard or assistive-technology user identify, operate, and recover from each control? |
| Performance/motion | Does the changed interaction stay responsive and respect reduced motion? |

Do not replace the whole surface with a spinner for a local request. Do not remove useful user input after a failed action. Warn before discarding unsaved work and confirm or undo destructive actions according to local conventions.

## Verification loop

1. Run the narrowest applicable type, lint, unit, component, integration, and build checks after the latest change.
2. Render the changed surface at representative narrow, medium, and wide viewports and inspect the actual result; implementation checks alone do not prove visual acceptance.
3. Exercise the affected default, loading, empty, error, pending, permission, long-content, keyboard, and reduced-motion states.
4. Review the diff for duplicated logic, incidental contract changes, hidden overflow, missing labels/focus, layout shifts, and accidental dependencies.
5. Report the conclusion first, then changed files or findings, verification evidence, and remaining risks. Separate passed checks from not-run checks and open questions.

## Non-goals and red flags

Do not replace the framework, rewrite unrelated routes, add one-off fetch logic beside an existing client pattern, make a generic container impersonate a control, mask overflow, remove focus indications, or claim quality from a screenshot or a zero exit code alone. Subjective decoration is not evidence of a correct implementation.
