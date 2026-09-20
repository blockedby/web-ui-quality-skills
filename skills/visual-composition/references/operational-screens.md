# Operational screen composition

Use for data-heavy work surfaces, applying only decisions relevant to the requested change.

## Structure and density

- Start from the operator's next decision: identify an exception, compare rows, inspect a record, or perform an action. Do not prepend a hero or summary cards unless they support that decision with available data.
- Prefer a table for comparisons across shared attributes; use cards when records need independent narrative or substantially different content. Do not convert tables to mobile cards if that loses the comparison task.
- Choose density for the amount of scanning and the input method. Keep row actions discoverable without making every cell compete for attention.
- Align comparable numeric values and use tabular numerals where useful. Display units, currency, timezone, and precision consistently; do not truncate values required for decisions.
- Separate zero, missing, unavailable, and loading values. A dash needs an established meaning; it must not silently stand for all four.

## Filters, selection, and actions

- Place search and common filters near the results they affect. Show active constraints and a clear reset path; distinguish an empty dataset from no matching results.
- Make sorting direction, result count scope, and pagination understandable. Do not invent totals when the API exposes only a partial count.
- Show selection count and scope beside bulk actions. “Selected on this page” and “all matching results” have different consequences and must not look interchangeable.
- Keep row navigation and row actions separately operable. Avoid hover-only access to required actions; include focus and touch treatments.
- Do not infer filter-change selection resets, navigation locks during submission, or post-success selection cleanup from a page-change rule. Preserve known contracts and explicitly label any additional behavior as proposed or unresolved.
- Make partial bulk failure actionable: identify affected records and preserve the context needed to retry or inspect them.

## Space and continuity

- Use the available workspace for useful columns and content. Avoid nested panels and large outer margins that force unnecessary scrolling.
- Keep context when opening record details and returning to results. Specify what happens to filters, selection, pagination, and scroll position using the established product behavior.
- On narrow screens, prioritize essential columns, provide a labeled details path, or use deliberate horizontal scrolling within the table region. Choose based on the task; do not clip data to make the page appear responsive.
- Keep sticky headers and action bars from obscuring content or keyboard focus. Loading or refresh should not unexpectedly reorder the row under the user's pointer.
