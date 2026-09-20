# Forms and feedback

Read for form design implementation or review. Preserve the product's submission and persistence model; autosave is a feature decision, not a default enhancement.

## Input and validation

- Give each field a persistent label and use fieldset/legend for related groups. Put format or consequence guidance where it is needed; do not attach generic helper text to every input.
- Choose semantic type, inputmode, autocomplete, and name for the data. Numeric identifiers are not necessarily numbers: preserve leading zeros and do not add spinner semantics to account IDs.
- Support paste, native editing, password managers, and browser autofill. Do not disable autocomplete globally to work around one field.
- Avoid showing an error while the user is still entering a valid partial value. Choose validation timing by field and established convention; after a failed submit, revalidate corrected fields without repeatedly interrupting typing.
- Keep client validation helpful while treating the server as authoritative. Separate field errors, business-rule conflicts, authorization failures, and network errors; never invent a cause absent from the response.
- Associate inline errors with the affected control and mark invalid state semantically. After a failed submit with multiple errors, focus a linked error summary when present, otherwise the first invalid field. Do not move focus on every keystroke or announce the same error through multiple competing regions.

## Submission and persistence

- Retain valid input after failure. Keep the initiating action identifiable during pending work, prevent duplicate requests, and report success only after the relevant operation actually succeeds.
- Distinguish Save, autosaved, saving, and unsaved changes. A debounce timer or optimistic local value does not prove persistence. Preserve the existing draft and navigation-guard rules.
- For a timeout with unknown mutation outcome, use established reconciliation or idempotency behavior before proposing an unconditional retry of a consequential action.
- Keep recoverable errors near the task. A transient toast alone is insufficient when the user needs details to correct a field or resolve a failed operation.
- Respect the existing confirmation/undo convention. Do not invent an undo affordance when the backend operation cannot be reversed.

## Verification

Exercise keyboard submission, correction after server rejection, duplicate clicks, pending navigation, and network failure when changed. Confirm field values survive and the resulting status matches the server response. Test supported autofill behavior in a browser when relevant; source attributes alone do not prove it works.
