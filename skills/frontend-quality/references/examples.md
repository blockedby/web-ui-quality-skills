# Interaction examples

Read for ambiguous implementation/review decisions or skill evaluation; adapt to existing contracts.

| Situation | Weak choice | Better choice and reason |
| --- | --- | --- |
| Invalid form submission | Clear the form and display “Something went wrong” briefly | Retain values, show response-grounded field errors, and focus the summary or first invalid field. Recovery needs context. |
| Network timeout after payment submission | Offer blind resubmission and claim the payment failed | Show the uncertain outcome and use the established status/reconciliation path. A missing response does not establish failure. |
| Modal deletes its source row | Return focus to a removed DOM node | Focus a logical surviving row or region so keyboard work can continue. |
| Counter refresh | Announce “3” on every polling tick | Announce a relevant change with context, without moving focus or repeating unchanged values. |
| Read-only account identifier | Disable the input and prevent copying | Use appropriate read-only presentation with accessible full value and copying if supported. Read-only is not unavailable. |
| Failed bulk update | Toast “All updated” and clear every selection | Report successful and failed records separately and preserve useful retry context. UI feedback must match the outcome. |

For each review finding, identify the trigger, observed or specified behavior, user consequence, and a scoped correction. Label source/specification-only conclusions rather than presenting them as browser observations.
