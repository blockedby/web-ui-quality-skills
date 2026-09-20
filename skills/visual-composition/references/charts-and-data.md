# Charts and data communication

Read when a requested interface contains charts or analytical summaries. Use actual available data and the user's question; do not invent metrics or add charts as decoration.

- Choose an encoding for the comparison: line for change over ordered time, bars for category comparison, and distribution plots for spread. A part-to-whole chart requires a meaningful whole and few distinguishable parts; bars are often clearer for precise comparisons.
- State units, aggregation, period, timezone where relevant, and the population or filters represented. Do not sum incompatible currencies or imply a conversion rate that was not supplied.
- Make scales truthful. Bars normally start at zero because length encodes magnitude; justify and visibly communicate unusual scales or breaks. Do not connect missing observations as though they were measured zeros.
- Distinguish no observations, zero values, loading, stale data, and load failure. Refresh may preserve prior data with clear freshness context; it must not label old values as current.
- Show exact values through labels or an accessible interaction that works with keyboard and touch. Do not make hover the only path to the data.
- Identify series through direct labels or a nearby legend as appropriate. Supplement color with shape, pattern, or text where needed; a separate legend is unnecessary when direct labels already disambiguate every series.
- Provide a concise textual explanation and access to underlying values, often through a table. Do not imply every point must be a tab stop in a dense time series; choose a usable navigation or table alternative.
- On narrow screens, reduce tick density or change orientation while preserving the comparison. Keep units and meaningful labels available. Respect reduced motion and make data readable without waiting for an entrance animation.
- For large datasets, disclose aggregation or sampling and preserve access to needed detail when the product supports it. Do not silently alter the meaning to improve rendering speed.

Review with a keyboard, narrow viewport, missing interval, all-zero data, and failed refresh when relevant. A chart's visual polish is not evidence that its underlying calculations are correct.
