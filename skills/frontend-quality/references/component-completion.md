# Component choice and completion

Read when adding or substantially changing pickers, menus, popovers, or dialogs. Apply to the affected components rather than auditing every control for an unrelated edit.

## Choose a complete primitive

1. Inspect the project's component system and use the established component when its semantics and states fit. Do not mix primitive libraries within a surface simply to obtain a different appearance.
2. A suitable native control is a valid choice. Check its actual rendered behavior in supported browsers; styling the closed element does not guarantee consistent styling of its browser-owned popup.
3. When the requirements need presentation or behavior the native control cannot reliably provide, prefer a maintained accessible primitive compatible with the stack. For React, Base UI, React Aria, or Radix are possible foundations, not mandatory dependencies. Respect dependency constraints and avoid migrating a working component system.
4. Treat keyboard navigation, focus management, accessible naming, selection, dismissal, and disabled semantics as part of the component. Do not recreate these with generic elements merely to style a popup. If constraints rule out a suitable primitive, keep the best supported implementation and state any unresolved requirement honestly.

Use a select for choosing a value, a combobox when text entry/filtering is needed, and a menu for actions. Do not change semantics to fit convenient styling. Add search, multiselect, or asynchronous options only when the task calls for them.

## Verify the opened surface

For each changed component type, inspect representative instances and any materially different configuration. Use the target browser and realistic content:

- Closed, opened, selected, focused, and disabled states as applicable; check selected + focused items remain distinguishable.
- Long labels, a long list if supported, internal scrolling, narrow layouts, and positioning near viewport edges or inside a scrolling container. Verify no clipping or obscured focused item.
- Open from the keyboard, move between options/actions, activate or select, dismiss, and continue from the expected focus. Use keys appropriate to the chosen pattern, including arrows, Enter, and Escape where supported. Do not impose a modal focus trap on a nonmodal list or menu.
- Check pointer operation, outside dismissal according to the product contract, and touch on supported touch layouts. Reopen to confirm the current value; verify any related async update preserves relevant focus and selection.
- Exercise empty, loading, error, or unavailable-option behavior when those states exist in the product. Do not add new product features to complete this list.

Functional assertions and visual inspection provide different evidence. Programmatically assigning a value does not test the opened popup. Capture or inspect the open state with tooling that can observe it; some screenshot tools omit browser-owned popups. If the available tooling cannot observe the surface, report that limit and leave its visual acceptance unverified. Do not replace the control solely to make a screenshot tool pass.

For overlay focus and dismissal details, read [Focus and overlays](focus-and-overlays.md).
