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

Review: recommends removing or making the redundant subtitle useful, retains the field label, and avoids a full design brief, palette, implementation, or unrelated interaction audit.

## Additional coverage and recorded evaluation

The [2026-09-21 evaluation report](../../reports/2026-09-21-skill-evaluation.md) records actual subagent review/application trials, found failures, revisions, and evidence limits. It includes reproducible task descriptions for a multi-workspace transaction handoff, faulty form/focus behavior, and conflicting persisted design decisions. These were qualitative text tasks, not execution of every scenario above or a base/candidate benchmark.

For future evaluations, add a rendered implementation trial covering light/dark combined states, long identifiers, form rejection, and modal focus return. Keep expected outcomes with the evaluator; do not give the implementing agent its scorecard or previous findings in a blind comparison.
