# Focus, overlays, and live feedback

Read when changing dialogs, menus, popovers, navigation, dynamic status, or gesture-based controls.

- Prefer the established accessible primitive or a suitable native element. A modal dialog, nonmodal popover, tooltip, and menu have different keyboard contracts; do not apply a modal focus trap to all overlays.
- A modal needs an accessible name, meaningful initial focus, contained keyboard navigation, and an operable dismissal path. Make background content non-interactive while modal. Follow the product's Escape and unsaved-change behavior.
- On close, return focus to the trigger if it still exists; otherwise use a logical nearby target. If the action deletes the triggering row, choose a sensible surviving row or region.
- Keep focused controls visible despite sticky headers, footers, and nested scrolling. Resolve layering through the established layer scale rather than escalating arbitrary z-index values.
- At a route transition, deliberately manage the new page's title and focus according to the router convention. Background refresh must not reset focus or scroll.
- Announce relevant async status with a suitable status/live region and contextual text such as “3 records selected.” Do not steal focus for toasts, announce every polling tick, or duplicate announcements. Reserve urgent interruption for genuinely urgent feedback.
- Required information and actions must work without hover. Dismissible hover/focus content should be reachable and remain available while being used; do not hide the full value as focus moves into its disclosure.
- Provide an operable single-pointer and keyboard alternative to dragging when the movement itself is not essential. Preserve browser/system shortcuts and zoom.

Verify with a concrete sequence: open, traverse, perform or cancel, close, and continue from the returned focus. Include a removed trigger, long content, and sticky UI if those cases are in scope. Distinguish keyboard testing from assistive-technology testing; one does not prove the other.
