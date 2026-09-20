# Durable design decisions

Read for a multi-page visual system or when asked to preserve design decisions across tasks. A small styling edit does not require a new design document.

- Inspect the existing token source, component documentation, brand guide, and design decisions first. Extend their established home rather than introducing a competing standard.
- If no convention exists and persistence is in scope, use a short project-level design document plus page-specific exceptions only where needed. Record token names and source paths rather than copying mutable values into a second specification.
- Capture the audience/task, density rationale, type roles, semantic color roles, layout constraints, component reuse, and required interaction behavior. Record why a decision exists, not merely what the screenshot looks like.
- A page exception must identify the inherited rule, the local deviation, its reason, and scope. Do not let one page's exception silently become the global default.
- Read the shared decisions and applicable exceptions before designing the next page. If documentation and implemented tokens disagree, inspect ownership/history and report the conflict; do not silently regenerate either one.
- Update relevant decisions when an authorized change supersedes them. Preserve unrelated decisions and factual constraints. Never persist private data from a search query or invent approval history.

Example: the shared system uses compact rows for desktop comparison. A touch-operated review page may use taller rows while retaining the same text roles and status semantics. Document that exception and point to its implementation; do not fork the entire palette and spacing system.
