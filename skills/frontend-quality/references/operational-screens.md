# Operational screen contracts

Inspect these contracts when the requested change affects them. Preserve existing behavior; do not add capabilities or silently change selection semantics.

## Query and navigation state

- Identify which layer owns search, filters, sorting, pagination, and result counts. Determine whether each operation applies to loaded rows or the full server dataset; labels must describe the actual scope.
- Reuse established URL/history conventions for shareable state. Preserve Back behavior and record-detail return context. Do not put sensitive search terms into URLs without considering the existing product contract.
- Resolve stale responses and define what happens to the current page when filters change. Keep refreshed data separate from initial loading and preserve useful content while waiting.

## Selection and mutations

- Establish stable record identity and selection scope: current page, explicit records across pages, or all matching records. Define what filter changes and refreshes do to selection before implementing bulk actions.
- Keep nested row controls independently keyboard-operable; avoid interactive elements inside another interactive element and accidental row navigation during actions.
- Use the existing permission and mutation contracts. Prevent duplicate submissions and handle per-record failures without claiming the entire batch succeeded or discarding failed selections.
- Follow the product's confirmation or undo convention for consequential actions; state the scope and consequence using truthful counts.

## Data and verification

- Preserve required precision and distinguish zero, missing, unavailable, and loading. Use established locale, unit, currency, and timezone formatters; keep full identifiers accessible when visually shortened.
- Check the changed behavior with active filters, no matches, long identifiers, page transitions, stale responses, selection changes, and partial failure as relevant. Include keyboard operation and narrow-screen access to required columns/actions.
- Choose pagination or virtualization based on measured responsiveness and data semantics, not a universal row-count threshold. Verify focus and selection continuity if virtualization changes mounted rows.
