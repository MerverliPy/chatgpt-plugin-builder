# Contributing

Contributions should improve the guided creation of a user-selected ChatGPT plugin.

## Scope requirements

- Preserve guided creation as the primary purpose.
- Keep MCP, OAuth, UI, benchmarks, tests, and patches attached to the selected plugin.
- Treat MCP, OAuth, and UI as evidence-based options rather than mandatory infrastructure.
- Keep patch application behind explicit user approval.
- Do not introduce standalone benchmark products for unspecified plugins.

## Pull requests

1. Describe the selected-plugin problem and expected user-visible improvement.
2. Add or update a regression test before changing behavior.
3. Keep changes small and reviewable.
4. Run `python -m unittest discover -s tests -v`.
5. Report measured results separately from assumptions or planned checks.

Do not include credentials, private data, proprietary fixtures, or benchmark claims that cannot be reproduced.
