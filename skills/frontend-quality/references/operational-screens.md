# Operational screen contracts

Inspect these contracts when the requested change affects them. Preserve existing behavior; do not add capabilities or silently change selection semantics.

## Query and navigation state

- Identify which layer owns search, filters, sorting, pagination, and result counts. Determine whether each operation applies to loaded rows or the full server dataset; labels must describe the actual scope.
- Reuse established URL/history conventions for shareable state. Preserve Back behavior and record-detail return context. Do not put sensitive search terms into URLs without considering the existing product contract.
- Resolve stale responses and define what happens to the current page when filters change. Keep refreshed data separate from initial loading and preserve useful content while waiting.

## Selection and mutations

- Establish stable record identity and selection scope: current page, explicit records across pages, or all matching records. Define what filter changes and refreshes do to selection before implementing bulk actions.
- Keep nested row controls independently keyboard-operable; avoid interactive elements inside another interactive element and accidental row navigation during actions.
- Use the existing permission and mutation contracts. Prevent duplicate submissions and report per-record outcomes truthfully. Preserve access to failed-record details, but follow the established selection policy: retaining failed selections is one recovery design, not a universal requirement. A product may instead clear selection and expose an operation report.
- Treat duplicate-submit prevention, pending navigation, cancellation, and selection cleanup as separate decisions. Do not block navigation merely because a request is pending, or add retry/undo controls without an operation contract supporting them.
- Keep an operation's original record IDs and query/workspace scope associated with its result. A late response must not apply selection cleanup to a different page or overwrite a new selection; use the existing operation/state ownership model.
- Follow the product's confirmation or undo convention for consequential actions; state the scope and consequence using truthful counts.

## Resolve behavior proportionally

Inspect existing components, state handlers, API contracts, and relevant tests before treating a behavior as unknown. Reuse established behavior for an existing surface. For a new flow, distinguish an explicitly delegated interaction decision from a missing consequential requirement: make ordinary layout choices directly; propose a specific policy when design is requested; clarify only an unresolved decision that changes the affected records, operation outcome, or permitted navigation before implementing that decision. Continue independent work instead of blocking the entire task.

## Data and verification

- Preserve required precision and distinguish zero, missing, unavailable, and loading. Use established locale, unit, currency, and timezone formatters; keep full identifiers accessible when visually shortened.
- Check the changed behavior with active filters, no matches, long identifiers, page transitions, stale responses, selection changes, and partial failure as relevant. Include keyboard operation and narrow-screen access to required columns/actions.
- Choose pagination or virtualization based on measured responsiveness and data semantics, not a universal row-count threshold. Verify focus and selection continuity if virtualization changes mounted rows.
