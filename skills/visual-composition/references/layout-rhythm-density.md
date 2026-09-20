# Layout, rhythm, and density

Read for new compositions or changes to grouping, spacing, page chrome, density, and responsive structure. Apply to the affected surface; preserve existing tokens, product contracts, and explicit style choices. These decisions do not require a new approval or a user-facing design report.

## Give space a job

- Identify the primary task, its necessary context, its controls, and its outcome. Group these before assigning columns or drawing containers. Keep the action visually connected to the input or selection it acts on.
- Give each persistent header, toolbar, notice, and side panel a distinct responsibility. Merge redundant layers when the design scope permits. Do not reserve a tall row for branding or a short title merely because a page template includes it.
- Judge empty space by its effect on task flow. Space can separate decisions, support reading, or reserve geometry for changing content. Unused width beside a short heading is not automatically a defect. Remove unnecessary vertical bands that push useful work away; never fill them with copy, icons, or cards just to occupy space.
- Avoid large fixed/minimum heights on empty panels and short inputs unless they serve the expected content, stable state transitions, or an explicit product requirement. Choose an initial input height for typical content and a usable growth/scroll policy for longer input.

## Use relationship-based spacing

- Reuse the project's spacing tokens. Assign roles for label-to-control, related controls, field groups, sections, and page edges instead of choosing a new margin for each element.
- Keep related elements closer than unrelated groups. A heading should sit closer to the content it introduces than to the preceding section; a helper or error belongs with its field, not halfway between fields.
- If no scale exists, a compact working UI can start with 4–8 CSS px for tightly coupled elements, 12–16 for related controls, and 24–32 between sections. These are starting ranges, not universal acceptance thresholds; adjust to typography, content, input targets, and the intended density.
- Check the effective rendered gap, including parent padding, child margin, line-height, and layout gap. Avoid accidental double spacing from wrappers and inconsistent gaps caused by margin collapse. Prefer one clear owner for spacing between siblings.
- Align repeated labels, controls, row actions, and content edges to shared tracks. Equal CSS boxes do not guarantee visual alignment: inspect icon viewboxes, glyph baselines, stroke weight, and optical centering before making small corrections. Do not change recognizable symbols merely to hide alignment defects.

## Match density to the work

- Choose density for the frequency of use, scanning/comparison task, content complexity, and input method. Compactness must not rely on unreadably small text, reduced hit areas, or clipping.
- Reduce repeated chrome, nested padding, decorative wrappers, and unnecessary always-visible content before shrinking text and controls. Make the primary action easy to find; maximizing the number of items above the fold is not the goal.
- Keep essential decisions and current state visible. Secondary setup, infrequent options, and diagnostic controls may use a clearly labeled disclosure when doing so fits the workflow. Do not hide common actions or introduce an obscure icon-only menu merely to save space.
- If a collapsed option changes the next action's outcome, show its active state near that action. Disclosure must work with keyboard and touch; a hover tooltip alone is insufficient.
- Distinguish persistent mode/scope from a new event or blocking problem. Stable metadata need not occupy a permanent alert banner; preserve a visible truthful summary and an accessible explanation where needed. Keep actionable errors at their cause and do not hide required warnings or change acknowledgement contracts.

## Recompose when relationships stop fitting

- Base a transformation on the available component/container width, content length, and usable control sizes. A viewport label such as “tablet” does not itself justify stacking every action.
- When a sidebar or secondary region squeezes the task area, consider reducing or disclosing that region before fragmenting the primary input/action group. Preserve access and reading/focus order.
- Let related controls remain in a row while their content and targets fit; wrap or stack deliberately when they no longer fit. More viewport width can still yield less component width when columns appear, so assess the container rather than assuming every transition must be monotonic.
- Define what moves, wraps, collapses, scrolls, or stays visible at each affected transition. Do not introduce a sticky toolbar automatically; if used, ensure it does not cover content or focus at short heights and zoom.

## Verify the composition

For implementation/review, inspect the rendered affected surface. For a design-only task, specify these checks as a handoff without claiming execution.

- Inspect narrow, intermediate, and wide layouts plus a short or near-square viewport where relevant. At each changed layout threshold, inspect just below, at, and just above the boundary, and an interior width in the affected interval. A pair of endpoint screenshots cannot validate that interval.
- Compare the primary task's position, group spacing, text/control fit, and action reachability. Check for awkward orphaned controls, unexplained blank bands, abrupt height jumps, overlap, clipping, and focus obscured by chrome. No horizontal overflow alone is not a composition pass.
- Repeat affected transitions with realistic long labels, errors or expanded controls, and enlarged text/zoom. Preserve grouping and task order; do not repair the layout by concealing content or reducing usability.
- Remove or fix unsupported space and broken relationships within scope; retain intentional breathing room. Record the problematic size/state and observed result rather than asserting that a spacing scale or framework makes the layout good.
