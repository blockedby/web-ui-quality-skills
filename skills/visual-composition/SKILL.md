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

This is a design and implementation handoff, not a screenshot scoring report or an excuse to replace an established system.

## Start with a design brief

Record the smallest useful brief before choosing a visual treatment:

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

Make each line concrete enough that another implementer can explain why the composition serves this content and task. If a line is unknown, preserve it as a design question.

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

## Preserve a design system

- Inspect existing layout wrappers, primitives, tokens, interaction patterns, and nearby surfaces before adding visual rules.
- Reuse typography, spacing, color, radius, elevation, icon, and breakpoint roles when their semantics match. Adapt hierarchy and density to the task without breaking recognizable product identity.
- Keep token families intentional: primary action, supporting action, surface, boundary, emphasis, success, warning, and error should each have a stable role.
- Prefer a small number of type levels, spacing increments, accent colors, and surface treatments with clear meaning.
- Reuse a component when semantics and states match; do not maximize reuse by forcing different content into a universal configuration language.
- Keep factual product copy and claims supplied by the brief. Visual polish cannot make invented content trustworthy.

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
4. Implement with existing primitives and semantic controls; keep uncertain product decisions explicit.
5. Render representative widths and realistic content while the surface is easy to change.
6. Fix hierarchy, flow, content, state, accessibility, and overflow problems before finishing visual details.
7. Return only the design handoff: brief, pattern and rationale, hierarchy/flow, state behavior, responsive transformation, reuse targets, unresolved questions, and anti-patterns to avoid.

## Anti-patterns

Avoid starting from a generic hero, bento grid, card wall, gradient, glow, or oversized heading before understanding the task; giving every card equal weight; forcing sequential content into peer cards; introducing one-off tokens beside a design system; shrinking desktop onto mobile; masking overflow; using placeholder-only copy; omitting error, empty, pending, long-content, keyboard, or reduced-motion behavior; and treating subjective decoration or a single screenshot as proof of quality.
