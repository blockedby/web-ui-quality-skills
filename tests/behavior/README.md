# Skill behavior evaluation

These are manual evaluation scenarios, separate from `validate.sh`. They check decisions made with a skill, not the presence of words in its instructions. No behavioral pass is implied by a repository validation pass.

For a comparison, run each request in fresh sessions using the base and candidate skill versions, the same model/settings, and the same supplied context. Give the agent the request and relevant skill only; keep the review criteria with the evaluator. Use temporary workspaces for generated files. Record the skill commit, model, request, output/artifact, observed behavior, and pass/fail/not-run per criterion. Repeat variable outcomes before claiming an improvement. Do not require exact wording or a particular visual style.

## 1. Remove redundant copy without losing labels

Skill: `visual-composition`.

Request: “Design a Russian-language Sources settings screen for a vacancy-search app. The sidebar already identifies the app. It contains an HH search URL field and a schedule selector. Provide a text wireframe and copy; do not implement it.”

Review: the page title is sufficient without a decorative vacancy-search overline; fields retain persistent labels; supporting copy adds necessary information rather than narrating the controls; no invented application code or implementation verification claims.

## 2. Preserve useful contextual text

Skill: `visual-composition`.

Request: “Design the Sources screen for two workspaces that have identical source names. Operators must always know they are editing the Acme workspace. The established design shows the workspace name immediately above the page title. Keep that convention. Return a wireframe.”

Review: the workspace context stays visible in the requested location; the agent does not interpret the overline rule as a blanket ban or replace the established convention for novelty.

## 3. Resolve visual choices without an approval loop

Skill: `visual-composition`.

Request: “Build a local static Sources settings mockup with native labeled controls, a page title, and a Save button. Choose a restrained visual system yourself. Use clearly marked sample values; no real save operation is needed.”

Review: produces a working artifact rather than only a handoff; chooses concrete consistent styles without asking permission for ordinary visual choices; sample interaction is not misrepresented as persistence; reports only browser checks actually performed. Judge usability and coherence, not a prescribed palette.

## 4. Data scope and narrow-screen comparison

Skill: `visual-composition` and its operational-screen reference.

Request: “Design a transaction review table with amount/currency, status, timestamp, and a long transaction ID. The API returns 25 rows per page and has no total count. Bulk actions apply only to explicitly selected IDs on the current page; selection resets on page changes. Provide desktop and narrow-screen wireframes with loading, no-match, and partial bulk-failure states.”

Review: respects current-page selection; does not invent a total; comparisons and full identifiers remain accessible; units and missing values are understandable; no ornamental KPI cards with invented metrics; partial failures identify affected records and a recovery path.

## 5. Review scope and evidence

Skill: `frontend-quality` and its operational-screen reference.

Request: “Review this behavior specification only, without editing code: search filters only the 25 loaded rows but is labeled ‘Search all transactions’; changing pages retains selected row indexes and then applies bulk actions to the new rows at those indexes; a failed batch shows ‘All updated’ and clears selection.”

Review: identifies misleading query scope, unstable selection identity, and false success feedback; ties consequences to supplied behavior; proposes scoped corrections without inventing API support; states that runtime/browser behavior was not tested.

## 6. Small changes stay small

Skill: `visual-composition`.

Request: “Review the wording only: a settings screen has title ‘Notifications’, subtitle ‘Manage your notification settings’, and a labeled ‘Email alerts’ checkbox. Do not change styling or code.”

Review: removes the redundant subtitle and its layout slot, retains the field label, and avoids inventing a replacement claim or moving the same text elsewhere. No full design brief, palette, implementation, or unrelated interaction audit.

## Additional coverage

For future evaluations, add a rendered implementation trial covering light/dark combined states, long identifiers, form rejection, and modal focus return. Keep expected outcomes with the evaluator; do not give the implementing agent its scorecard or previous findings in a blind comparison.

## 7. Preserve an explicit alternative recovery policy

Skills: `frontend-quality` and `visual-composition`, evaluated separately so each must stand alone.

Request: “Review this bulk-action design only. The established contract permits navigation during processing; the operation is tied to captured record IDs. On completion, selection belonging to that operation is cleared and a persistent operation report lists each success/failure. A later selection must survive. The backend does not support retry. The UI proposal disables Next while pending, retains failed rows as selected, and adds a Retry failed button. Explain necessary changes and give one corrected behavior paragraph.”

Review: preserves navigation and the explicit report-based recovery policy; removes unsupported retry; distinguishes old-operation cleanup from a new selection; provides a consolidated corrected proposal. Does not demand failed-row retention or add unrelated approval flows. Identifies specification-only evidence and avoids claiming runtime tests.

## 8. Task-first composition and purposeful removal

Skill: `visual-composition`.

Request: “Design an internal shipment exception workbench. Operators need to find delayed shipments, inspect the cause, and assign an owner. Keep the current warehouse visible because shipment numbers repeat across warehouses. Distinguish incomplete carrier data from confirmed delays. Provide desktop and narrow-screen wireframes; do not implement.”

Review: the primary work is directly accessible without a promotional introduction; necessary warehouse and data-quality context survives simplification; labels and recovery remain clear; no invented metrics or workflow policies. Evaluate information and task order rather than exact wording, palette, or a required page template.

## 9. Complete a composite control in an existing stack

Skill: `frontend-quality`.

Fixture: supply a runnable project with an existing accessible select primitive, long option labels, disabled options, and a form near the viewport edge. Keep the same fixture, tools, and dependency policy across comparison runs.

Request: “Use the existing stack to finish the destination selector so its closed and opened presentation matches the form. Support desktop and narrow touch layouts. Preserve the single-choice behavior and unavailable destinations. Implement and verify.”

Review: reuses the existing primitive; inspects the opened list and its positioning, long content, combined focus/selection, and disabled states; exercises keyboard selection/dismissal and continued focus. A programmatic value assignment alone is not evidence. Reports unsupported checks as unverified. Does not add search/multiselect, replace the component system, or claim a touch check from a narrow screenshot alone.

## 10. Native control and proportionate scope

Skill: `frontend-quality`.

Request: “In this supplied static form, change the label ‘Area’ to ‘Region’. Keep the native select and its platform appearance. No dependencies or other design changes.”

Review: makes the scoped label change, preserves labeling association and native behavior, and runs proportionate checks. Does not replace the select, import a library, or audit every opened control. Does not represent a source check as browser verification.

For rendered trials, record explicit visual and functional criteria separately as pass/fail/not-run. Unrelated successes must not cancel a failed required criterion. These scenarios are a protocol, not evidence of a completed experiment.

## 11. Secondary copy across placements

Skills: `visual-composition` and `frontend-quality`, evaluated independently.

Request: “Review copy only for an internal export settings page. The title is ‘Exports’; below it is ‘All your export tools in one place’. The ‘Schedule’ section has a right-aligned note ‘Availability depends on configuration’. A CSV format selector has helper text ‘Choose your preferred format’. The known contract permits at most 10,000 rows per export, stated next to Export. Workspace ‘North’ must stay visible because export names repeat across workspaces. There is no additional capability/configuration information. Return the resulting copy structure; do not implement.”

Review: removes the summary, vague side note, and self-evident selector instruction without replacing or relocating them. Preserves the concrete row limit, workspace scope, field labels and action. Does not invent configuration requirements or extra notices. Treat retaining any of the redundant annotations as a failed criterion even if the rest of the design is good.

## 12. Intermediate-width action grouping

Skill: `frontend-quality`.

Fixture: supply a runnable form with a secondary panel, a short option and a submit button. The action row is forced into a column between two breakpoints despite sufficient container width at part of that interval; at a smaller viewport the secondary panel collapses and the action row becomes horizontal again. Supply real CSS boundaries with the fixture, not expected conclusions.

Request: “Review this form's responsive layout in the browser. Users report excessive vertical space around the actions at some window sizes. Keep the existing features and readable control sizes; report findings without editing.”

Review: inspects the owning container, both sides of the relevant boundaries and an interval interior; distinguishes legitimate width recovery after panel collapse from unnecessary stacking inside the interval. Reports actual geometry and task consequence. Does not label every row/column reversal a defect or claim no overflow proves a good layout.

## 13. Density without concealing important state

Skill: `visual-composition`.

Request: “Propose a more compact internal scheduling screen. It has a workspace header, page title, permanent mode explanation, a task form, advanced repeat options, preview, and history. The selected workspace must remain identifiable. An enabled advanced option changes the next run's destination. Preserve a blocking validation error next to its field. Use the existing spacing scale and provide a layout handoff only.”

Review: gives persistent regions distinct roles, groups the form with its action, assigns tighter within-group and larger between-group spacing, and considers disclosure of secondary options. Any disclosure preserves a visible indication of the changed destination. Does not hide the blocking error, shrink hit areas/text to increase density, fill intentional whitespace with invented content, or force a particular header/sidebar template. Specifies intermediate and constrained-height verification without claiming rendered checks.
