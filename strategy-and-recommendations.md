# Strategy and Recommendations

## Why I selected these two automated tests

I selected one E2E UI test and one API test because together they cover the two most important layers of the feature.

The E2E UI test validates the critical user journey: a user selects an outcome, enters a valid stake, places the bet, and receives a confirmation. This is the flow most directly connected to user trust and business value.

The API test validates a business rule directly at the backend layer. This is important because UI validation can be bypassed. The API still needs to reject invalid requests, especially missing user context or invalid betting data.

## What I intentionally left manual

I would keep the following areas manual at this stage:

- Detailed visual checks around the bet slip, receipt modal, and error modal.
- Exploratory testing around loading states and interrupted flows.
- Filter usability checks, because these are easier to assess manually while the UI is still small.
- Cross-browser checks, unless the product starts supporting a broader browser matrix.
- Copy review, especially error messages and receipt details.

## Recommendations if the project scales

1. Add stable selectors such as `data-testid` for match cards, odds buttons, stake input, balance, bet slip, place bet button, and receipt modal. This would make UI automation less fragile.

2. Add CI execution for smoke tests on every pull request. I would run the API validation tests first because they are faster, then a small E2E smoke suite in Chrome.

3. Improve test data control. A reliable reset endpoint already exists, so I would use it before tests to keep balance predictable. For a larger suite, I would also recommend deterministic match data or a seeded test environment.

4. Clarify a few specification details before expanding coverage: whether the minimum stake is `€1.00` or `€1.01`, how odds filtering is exposed in the UI, and how placement failures can be deterministically triggered for testing.
