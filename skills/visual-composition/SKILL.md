---
name: visual-composition
description: Turn a concise visual brief into a product-specific, accessible, responsive composition with coherent hierarchy, states, feedback, and implementation handoff.
license: MIT
---

# Visual Composition

Use this skill when a browser-visible surface needs a clear visual direction, not merely attractive decoration. Design for the audience and task first, then express that intent through hierarchy, grouping, typography, imagery, interaction, responsive transformation, and purposeful motion.

## Contract

**Inputs**

- A visual brief: audience and usage scenario, purpose, primary task, required content, interaction model, and factual product constraints.
- Reference surfaces, existing components, design tokens, typography, brand rules, imagery/icons, and adjacent product patterns.
- Required UI states: default, loading, empty, partial, error, success, disabled, pending, selected, expanded, submitting, and permission-denied as applicable.
- Supported viewport range, breakpoints, themes, locales, input methods, accessibility requirements, content density, and technical constraints.

**Outputs**

- A coherent composition strategy chosen for the content relationship and task.
- Concrete hierarchy, grouping, reading order, visual system roles, primary/secondary actions, content and typography decisions, and interaction feedback.
- A responsive transformation that recomposes the surface rather than only shrinking it, plus relevant state, motion, media, and implementation handoff decisions.
- Explicit unresolved design questions and constraints. Do not silently invent brand rules, information architecture, claims, or product behavior.

## Match the requested work

- **Design:** return an actionable composition and handoff; implement only when requested.
- **Implementation:** build and verify the requested surface, then report the result and remaining limits. A design handoff alone does not complete an implementation request.
- **Review:** inspect the supplied surface and report actionable findings with evidence; do not redesign or edit it unless requested.

In a handoff, distinguish supplied behavior, proposed visual choices, and unresolved consequential behavior. Do not present an unprovided selection, persistence, navigation-blocking, or mutation rule as established behavior; label it as a proposal or an implementation dependency.

Use only the steps relevant to that mode and the size of the change. Routine styling choices do not require another approval; ask only when a missing decision materially changes the product contract.

## Start with a design brief

For a new composition or substantial redesign, record the smallest useful brief before choosing a visual treatment. For a small edit, retain only the decisions affected by that edit:

```md
Audience and usage scenario:
Purpose:
Primary user task:
Required content and states:
Reference surfaces:
Design-system invariants:
Composition strategy:
Visual signature:
Responsive transformation:
Motion and feedback intent:
Forbidden or discouraged outcomes:
```

Make each line concrete enough that another implementer can explain why the composition serves this content and task. Reuse supplied context rather than asking the user to fill out a template. Resolve ordinary visual choices from the existing system; flag unknowns only where they affect the requested outcome.

## Choose structure by purpose

Choose a pattern because it expresses an information relationship, not because it is fashionable:

| Purpose | Useful starting point | Decision to make |
| --- | --- | --- |
| Explain or persuade | Message plus proof | Give one message and action prominence; follow with relevant evidence. |
| Compare alternatives | Aligned comparison | Keep shared attributes aligned and make meaningful differences scannable. |
| Monitor or operate | Status-led dashboard | Surface status and exceptions before controls and detail. |
| Complete a task | Grouped form flow | Group fields by decision, reveal complexity progressively, and keep recovery local. |
| Teach or tell | Editorial flow | Preserve reading measure, narrative order, and media relevance. |
| Explore detail | Master-detail | Keep selection and context connected; sequence them clearly on narrow screens. |
| Browse peers | List or card collection | Repeat containers only when items are genuinely comparable. |

A named pattern is a starting structure. Combine or reject patterns when the content relationship requires it; do not force narrative or hierarchy into interchangeable cards.

## Build hierarchy and flow

- Establish one clear visual starting point for each page or major region.
- Order content by the user's next decision: orientation, relevant information, action, then confirmation or consequence.
- Group related elements with proximity and shared alignment; use whitespace to separate distinct decisions.
- Use position, scale, contrast, spacing, and typography together to express importance. Color must not carry meaning alone.
- Make primary, supporting, and destructive actions distinct. Name actions for their consequence rather than using ambiguous labels such as `Continue` when a specific label is possible.
- Give every prominent element a role in meaning, orientation, emphasis, feedback, or flow. Remove decoration that has no such role.
- Keep headings scannable, body copy within a readable measure, and realistic content visible during design. Test short, typical, long, missing, malformed, and localized values.

## Purposeful interface copy

- Do not add eyebrow headings, overlines, or category labels just to decorate a title. Keep them only when they add necessary context, such as the selected workspace or a workflow step.
- Omit “ПОИСКИ ВАКАНСИЙ” above “Источники” when the surrounding product already establishes that context. Uppercase styling and accent color do not make redundant text useful.
- A subtitle should explain a non-obvious scope, consequence, or next action. Do not narrate visible controls or add instructions merely to fill space beneath a heading.
- Use the user's vocabulary and consistent action names. Preserve persistent field labels, accessible names, recovery instructions, and meaningful status text when simplifying copy.
- Before finishing, remove text, badges, repeated navigation, and decorative containers whose removal leaves orientation, decisions, actions, and feedback equally clear. Preserve explicit brand and content requirements.

## Preserve a design system

- Inspect existing layout wrappers, primitives, tokens, interaction patterns, and nearby surfaces before adding visual rules.
- Reuse typography, spacing, color, radius, elevation, icon, and breakpoint roles when their semantics match. Adapt hierarchy and density to the task without breaking recognizable product identity.
- Keep token families intentional: primary action, supporting action, surface, boundary, emphasis, success, warning, and error should each have a stable role.
- Prefer a small number of type levels, spacing increments, accent colors, and surface treatments with clear meaning.
- Reuse a component when semantics and states match; do not maximize reuse by forcing different content into a universal configuration language.
- For a new visual system, record concrete decisions: type roles and sizes, spacing scale, content widths, density, surface/border roles, and semantic colors. For an existing system, name the reused tokens and only the necessary exceptions. Avoid a new palette or a forced visual signature for a small edit.
- Keep factual product copy and claims supplied by the brief. Visual polish cannot make invented content trustworthy.

## Focused design references

Read only the reference relevant to the changed surface:

- [Typography, color, and states](references/visual-system.md): visual hierarchy, supported themes, or component presentation.
- [Charts and data](references/charts-and-data.md): analytical graphics and their accessible alternatives.
- [Durable design decisions](references/design-decisions.md): multi-page consistency or requested persistence of design choices.
- [Decision examples](references/examples.md): ambiguous choices and concrete weak/better comparisons.

For forms or overlays, specify validation, persistence, focus, and recovery behavior in the handoff rather than only drawing the ideal state. During implementation, verify those contracts using the existing component system.

## Tables and operational screens

When the changed surface includes tables, filtering, bulk actions, or monitoring, read [Operational screen composition](references/operational-screens.md). Apply only patterns supported by the task; do not add a dashboard, metrics, or controls to satisfy a checklist.

## Design complete states and feedback

Design relevant state changes before polishing the ideal frame:

- **Loading/pending:** keep the stable shell visible, reserve the final geometry, and show progress near the changing region or initiating action.
- **Empty/partial:** explain what is absent, why it matters, and the next useful action; preserve orientation when only part of the data is available.
- **Error/permission:** place the explanation beside its cause, preserve valid input, identify the recovery action, and distinguish unavailable permissions from transient failure.
- **Success/submitting:** confirm the consequence in context without hiding the user's next step; prevent duplicate submission while keeping the action's meaning stable.
- **Selected/expanded:** make selection, focus, expansion, progress, and state changes visible without requiring memory of a previous screen.
- **Interaction:** define hover, active, checked, focus-visible, disabled, dragged, validation, keyboard, and touch feedback where applicable.

Use semantic links and buttons, visible labels, named icon controls, logical DOM order, visible focus, correct disabled/expanded semantics, and adequate touch targets. Keep help and validation connected to fields. Include reduced-motion behavior that preserves state and spatial meaning.

## Responsive transformation

Recompose deliberately at the point where relationships fail:

1. Identify the primary task and content that must survive every width.
2. Choose the existing breakpoint system or add a content-driven boundary only when necessary.
3. Collapse columns, reorder supporting regions, simplify nonessential decoration, and change control grouping rather than uniformly shrinking desktop.
4. Preserve reading/task order in the DOM as visual regions become sequential.
5. Let text, cards, controls, and media wrap or shrink using grid/flex intrinsic sizing; fix the overflowing element rather than hiding page overflow.
6. Set purposeful content measures on wide screens and readable spacing on narrow screens. Respect safe areas for edge-to-edge or sticky actions.
7. Verify touch, pointer, keyboard, zoom, larger text, themes, locales, and long content at representative widths.

Describe the transformation in user-facing terms—for example, “the filter summary remains above the results while advanced controls move into a labeled disclosure”—rather than only naming a breakpoint.

## Motion, media, and perceived performance

- Use motion to explain appearance, disappearance, reordering, hierarchy, progress, or spatial relationship; do not use ambient motion beside reading or primary actions without a purpose.
- Prefer transform and opacity, keep motion interruptible, and avoid broad `transition: all` rules.
- Give images explicit dimensions/aspect ratios, choose intentional crops, provide meaningful alt text, silence decorative media, and defer noncritical media.
- Keep the first frame coherent, reserve asynchronous space, and keep typing, scrolling, selection, and navigation responsive.
- Do not hide latency with a distracting animation or use visual effects to compensate for unclear hierarchy or interaction.

## Creation and handoff loop

1. Read the brief, references, current system, and constraints.
2. Select a structure that matches the content relationship and write the hierarchy and reading order before decoration.
3. Define responsive transformations, relevant states, interaction feedback, media behavior, and reduced-motion behavior.
4. In implementation mode, build with existing primitives and semantic controls; in design mode, specify the handoff; in review mode, inspect the existing result.
5. For implementation or review, inspect the rendered surface at representative widths with realistic content. For a design-only task, specify the checks needed when implemented; do not claim they ran.
6. Fix or report hierarchy, flow, content, state, accessibility, and overflow problems. Make a final removal pass for redundant copy and containers before finishing visual details.
7. Return the requested deliverable: a concise design handoff, a verified implementation summary, or evidence-backed review findings. State material unknowns and distinguish rendered checks from proposed checks.

## Anti-patterns

Avoid starting from a generic hero, bento grid, card wall, gradient, glow, or oversized heading before understanding the task; giving every card equal weight; forcing sequential content into peer cards; introducing one-off tokens beside a design system; shrinking desktop onto mobile; masking overflow; using placeholder-only copy; omitting error, empty, pending, long-content, keyboard, or reduced-motion behavior; and treating subjective decoration or a single screenshot as proof of quality.
