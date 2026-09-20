# Typography, color, and component states

Read when creating a visual system or changing typography, themes, or component presentation. Existing tokens and explicit brand choices take precedence over these starting points.

## Typography and hierarchy

- Assign roles before choosing sizes: page title, section heading, field label, body, supporting text, and numeric data. Semantic heading levels follow document structure, not font size.
- Establish emphasis with placement, weight, and grouping before enlarging everything. A compact operator screen need not use a marketing-sized heading or a decorative display font.
- For sustained prose, start around 60–75 characters per line and a comfortable line height, then inspect the actual font and language. These are starting points, not limits for labels, tables, or code.
- Balance short headings when useful, but keep natural wrapping readable. Do not glue entire phrases together with nonbreaking spaces. Keep units with their values where appropriate.
- Let URLs and long identifiers wrap in shrinkable containers; do not break ordinary words arbitrarily. If truncation is necessary, expose the full value to keyboard, touch, and pointer users, not only through a hover tooltip.
- Use tabular numerals for changing or aligned numeric comparisons. Preserve units and meaningful precision. Check the actual font's glyph coverage for the product's languages.
- A new expressive surface may have one dominant visual accent; an established work screen may need none. Do not sacrifice legibility or the user's requested style to appear original.

## Color and themes

- Define foreground/background pairs by role: body, muted text, surface, boundary, action, selected, success, warning, and error. A muted role must remain readable.
- Measure contrast for the rendered pair, including opacity and the background beneath it. For WCAG AA text, use 4.5:1 for ordinary text and 3:1 for large text; required non-text control/state cues generally need 3:1 against adjacent colors. Distinguish applicable exceptions from a claim that all UI passes accessibility.
- Design supported light and dark themes as separate role mappings, not mechanical inversion. Check native inputs, selects, autofill, scrollbars, and focus indicators; set an appropriate CSS `color-scheme`.
- Define hover, pressed, focus-visible, selected, disabled, read-only, pending, and invalid states where relevant. Hover is transient; selection persists; focus identifies keyboard position. They must remain distinguishable when combined.
- Do not make disabled content so faint that the reason it is unavailable becomes unreadable. Read-only values should remain selectable/copyable when useful, rather than inheriting disabled behavior.
- Use one coherent icon language with consistent stroke weight and optical sizing. Decorative icons stay silent to assistive technology; icon actions need an accessible name. Do not replace a recognizable label with an ambiguous icon merely to save space.

## Inspection

Compare the same representative component in both supported themes and in combined states such as selected + focused and invalid + focused. Inspect long localized copy, enlarged text, and narrow layouts. Record measured pairs and observed states; do not infer contrast or readability from a palette name.
