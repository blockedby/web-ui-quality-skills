# Responsive layout checks

Read when changing layout, spacing, density, responsive controls, or breakpoint/container rules. Check the affected regions and transitions; a wording-only edit does not require a full breakpoint audit.

## Establish the actual layout constraints

- Inspect the owning container, column tracks, wrapper padding, child margins, gap, minimum sizes, and control content. Measure available inline space after sidebars and padding; viewport width alone does not establish whether a control group fits.
- Reuse spacing roles and tokens. Give sibling spacing a clear owner; inspect computed gaps to catch stacked padding/margins and unexpected margin collapse. Preserve existing density and typography unless changing them is in scope.
- Keep input/selection and its primary action visibly related. Prefer intrinsic sizing and deliberate wrapping before a viewport-wide rule that stacks every action. Preserve reading and keyboard order when rearranging regions.
- If reducing density or decluttering is requested, inspect repeated chrome, nested padding, oversized empty/min-height regions, and infrequent controls before shrinking readable text or hit areas. Preserve required context and access to any disclosed controls.

## Build a scoped transition matrix

1. Identify the media/container thresholds whose rules affect the changed surface, including overlapping rules and parent layout switches.
2. For each affected threshold B, inspect B−1, B, and B+1 CSS px (or equivalently close values for non-pixel thresholds), plus a representative width inside the affected interval. Resize the relevant container for container queries. Record the effective CSS dimensions; do not infer them from screenshot pixel dimensions.
3. Include a short or near-square viewport when the work involves stacked chrome, side panels, or action bars. Verify the affected layout at enlarged text or browser zoom, such as 200%, and with representative long labels or validation content. Do not combine every possible state unless needed to reproduce a failure.
4. Check rendered geometry AND task relationships: overlap, clipping, hidden controls, avoidable vertical gaps, primary-action displacement, awkward wraps, unnecessary stacking, and abrupt height changes. Compare effective space with control widths, text wrapping, and usable targets.
5. Explain surprising transitions using actual container changes. A narrower viewport may legitimately expose a wider main area after a sidebar collapses; do not enforce monotonic rows/columns blindly. Fix accidental overrides or unsupported stacking rather than adding another arbitrary breakpoint.

## Acceptance and evidence

- A clean scrollWidth check and two endpoint screenshots do not establish responsive quality. Keep intentional whitespace; fail only concrete fit, grouping, hierarchy, or task-access requirements.
- Open affected menus/pickers and inspect focus visibility when surrounding layout changes. Check sticky/fixed regions at reduced heights, and keep action targets reachable without obscuring content.
- Fix scoped failures in implementation mode and recheck the affected threshold/state. In review mode report the trigger, consequence, and evidence. If rendering is unavailable, distinguish source-derived risks from observed defects.
- Report actual sizes/states tested and unresolved gaps. No mandatory external library, new navigation, hidden warning, or universal first-screen quota follows from this checklist.
