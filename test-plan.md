# Test Plan — Single Bet Placement

## Overview

The Single Bet Placement feature is the core journey of the application. A user browses available football matches, selects one outcome, enters a stake, and places a single bet against their available balance.

Because this flow directly affects user funds, balance calculations, and payout expectations, I focused this test plan on the areas where a defect would have the highest user or business impact:

- placing a valid bet successfully
- keeping the bet slip state predictable
- calculating payout correctly
- preventing invalid stakes
- handling failed placement safely
- enforcing the same rules at API level

The set below is intentionally focused rather than exhaustive. It covers the happy path, important negative cases, boundary conditions, UI state changes, and backend validation.

---

## SBP-001 — Place a valid single bet successfully

**Priority:** Critical

### Risk rationale

This is the main user journey and the feature that creates business value. If a valid user cannot place a bet, the product fails its primary purpose.

This scenario also checks several connected parts of the system at once: match selection, bet slip population, stake handling, payout calculation, loading state, balance deduction, and receipt generation. A defect in any of these areas could create user confusion or financial disputes.

### Preconditions

- The application is opened with a valid `user-id`.
- The user has sufficient balance available.
- At least one upcoming football match is displayed.

### Steps

1. Open the application with a valid `user-id`.
2. Confirm that upcoming football matches are displayed.
3. Select one available odds button, for example `1`, `X`, or `2`.
4. Verify the selected odds button is visually highlighted.
5. Verify the selected match appears in the Bet Slip.
6. Enter a valid stake, for example `10.00`.
7. Verify the Place Bet button becomes enabled.
8. Verify the potential payout is calculated before placement.
9. Click `Place Bet`.
10. Observe the loading state.
11. Wait for the bet placement to complete.
12. Review the success receipt.
13. Close the receipt.

### Expected result

- The selected outcome appears in the Bet Slip.
- The selected odds button and selected match are visually highlighted.
- Stake, available balance, total stake, and potential payout are displayed.
- Potential payout is calculated using `stake × odds`.
- `Place Bet` changes to `PLACING...` while the request is processing.
- Betting controls are not available while placement is in progress.
- A success receipt is displayed.
- The receipt contains:
  - Bet ID
  - Match details
  - Selection
  - Stake
  - Odds at placement
  - Potential payout
  - Placement timestamp
- The user balance is reduced by exactly the placed stake.
- Balance remains consistent wherever it is displayed.
- Closing the receipt returns the user to the main flow.
- The Bet Slip is cleared and no active selection remains.

---

## SBP-002 — Prevent invalid stake values

**Priority:** Critical

### Risk rationale

Stake validation protects both users and the business from invalid financial transactions.

If invalid values are accepted, the application could place bets outside the allowed limits, calculate payouts incorrectly, deduct the wrong balance, or allow a user to bet more than their available funds.

Because this flow involves money, validation defects are high risk even when they appear small from a UI perspective.

### Test data

| Case | Stake value |
| --- | --- |
| Empty stake | blank |
| Non-numeric value | `abc` |
| Zero value | `0` |
| Below minimum | `0.99` |
| Valid minimum boundary | `1.00` |
| Valid maximum boundary | `100.00` |
| Above maximum | `100.01` or `101` |
| Too many decimals | `10.999` |
| Negative value | `-10` |
| Exceeds available balance | balance + `1.00` |

### Steps

1. Open the application with a valid `user-id`.
2. Select a valid odds button.
3. Enter each stake value one by one.
4. Observe whether the value is accepted by the input.
5. Try to place the bet when possible.
6. Observe the validation message, Place Bet button state, and balance.

### Expected result

- Invalid stake values are rejected or blocked from submission.
- The bet is not placed when the stake is invalid.
- The Place Bet button remains disabled for invalid values.
- The balance is not changed after rejected attempts.
- No receipt is generated for invalid stakes.
- The stake input allows numeric values with a single decimal separator and up to two decimal places.
- Clear feedback is shown where relevant:
  - `Minimum stake is €1.00`
  - `Maximum stake is €100.00`
  - `Insufficient balance`

---

## SBP-003 — Replacing a selection does not create multiple bets

**Priority:** High

### Risk rationale

The product supports single bets only. A user should never end up with multiple active selections in the Bet Slip.

If multiple selections remain active, the UI could behave like an accumulator or multi-bet flow, which is explicitly outside the supported scope. This would be misleading for users and could result in bets being placed on unintended outcomes.

### Preconditions

- The application is opened with a valid `user-id`.
- At least two matches or at least two selectable outcomes are available.

### Steps

1. Select an outcome from Match A.
2. Verify the selection appears in the Bet Slip.
3. Select a different outcome from the same match.
4. Verify the Bet Slip updates to the latest selection.
5. Select an outcome from Match B.
6. Verify the Bet Slip again.
7. Click the per-selection remove `X`.
8. Select another outcome and click `Remove All`.

### Expected result

- The Bet Slip always shows only one active selection.
- Each new odds selection replaces the previous one.
- No accumulator or multi-bet behaviour is created.
- The latest selected match and outcome are the only ones available for placement.
- Removing the selection clears the selected match from the Bet Slip.
- `Remove All` clears:
  - selection
  - stake
  - total stake
  - potential payout
- Place Bet becomes unavailable after the selection is removed.

---

## SBP-004 — Verify Bet Slip calculations update dynamically

**Priority:** High

### Risk rationale

Users rely on the displayed payout before deciding whether to place a bet. If the calculation is wrong or does not update when the stake changes, users may place a bet based on incorrect expectations.

This is a high-risk area because payout values are directly tied to user trust and financial accuracy.

### Preconditions

- The application is opened with a valid `user-id`.
- At least one match outcome is available.

### Steps

1. Select a match outcome.
2. Note the selected odds value.
3. Enter a stake of `10.00`.
4. Verify the displayed potential payout.
5. Change the stake to `20.00`.
6. Verify the payout updates again.
7. Change the stake to `50.50`.
8. Verify the payout updates again.

### Expected result

- Potential payout updates immediately after the stake changes.
- No page refresh or extra action is needed.
- The calculation follows this formula:

```text
Potential payout = stake × odds
```

Example using odds `3.10`:

| Stake | Expected payout |
| --- | --- |
| `10.00` | `31.00` |
| `20.00` | `62.00` |
| `50.50` | `156.55` |

---

## SBP-005 — Recover gracefully from failed bet placement

**Priority:** High

### Risk rationale

Bet placement can fail because of backend errors, network issues, or temporary service interruptions. When that happens, the user needs a clear recovery path and an unambiguous state.

The main risk is that the user may not know whether the bet was placed or whether their balance was affected. Poor error handling in this flow can quickly damage trust.

### Preconditions

- The application is opened with a valid `user-id`.
- A valid match outcome is selected.
- A valid stake is entered.
- A placement failure can be triggered or simulated.

### Steps

1. Select a valid outcome.
2. Enter a valid stake.
3. Trigger a bet placement failure.
4. Review the error modal.
5. Click `Rebet`.
6. Observe whether the placement is retried.
7. Trigger another placement failure.
8. Click `Close`.
9. Trigger another placement failure.
10. Click the top-right `X`.

### Expected result

- Error modal title is `Something went wrong`.
- The modal explains that the bet could not be processed and suggests trying again.
- `Rebet` closes the modal and retries the placement.
- `Close` closes the modal and clears the current selection and stake.
- The top-right `X` behaves the same as `Close`.
- No duplicate bets are created.
- Balance is not deducted after a failed placement.
- The user is not left in an unclear or inconsistent state.

---

## SBP-006 — Validate place-bet API rules and authorization

**Priority:** High

### Risk rationale

Client-side validation can be bypassed by sending requests directly to the backend. Because this is a betting flow, the API must enforce the same core rules as the UI.

The API is the final protection layer for user context, match validity, selection validity, stake limits, and request format. If the API accepts invalid requests, the platform could allow bets that the UI correctly blocks.

### Endpoint under test

```http
POST /api/place-bet
```

### Required header

```http
x-user-id: <valid-user-id>
```

### Valid request example

```json
{
  "matchId": "valid-match-id",
  "selection": "HOME",
  "stake": 10
}
```

### Validation checks

| Check | Request change | Expected result |
| --- | --- | --- |
| Valid request | Send valid header and valid body | `200 OK` |
| Missing user context | Remove `x-user-id` header | `401 Unauthorized` |
| Invalid user context | Send invalid or blank `x-user-id` | `401 Unauthorized` |
| Malformed payload | Send invalid JSON or non-object payload | `400 Bad Request` |
| Missing match ID | Remove or blank `matchId` | `422 Validation Error` |
| Unknown match ID | Send a match ID that does not exist | `422 Validation Error` |
| Invalid selection | Send value outside `HOME`, `DRAW`, `AWAY` | `422 Validation Error` |
| Missing stake | Remove `stake` | `422 Validation Error` |
| Stake below minimum | Send `0.99` | `422 Validation Error` |
| Stake above maximum | Send `100.01` or `101` | `422 Validation Error` |
| Invalid stake precision | Send `10.999` | `422 Validation Error` |
| Unsupported HTTP method | Send unsupported method to `/api/place-bet` | `405 Method Not Allowed` |
| Bet already in progress | Send concurrent placement for the same user | `409 Conflict` |

### Expected result

- Only valid requests place a bet.
- Invalid requests return the expected status code.
- Validation errors clearly explain what failed.
- Rejected requests do not change the user balance.
- UI and API validation remain consistent for the same business rules.

---

## Coverage note — Filters

Date and odds filters were considered during test planning, but I did not include them as one of the top six prioritized scenarios.

I treated filters as lower risk compared with balance handling, payout calculation, bet placement, error recovery, selection state, and API validation. If time allows during exploratory testing, I would still check the following:

- single-day date filtering
- inclusive date range filtering
- minimum and maximum odds filtering
- invalid odds range validation where minimum odds is greater than maximum odds
- whether clearing filters restores the full match list

This keeps the main test plan focused on the highest-risk betting flows while still acknowledging filter coverage from the specification.

---

## Scenario selection rationale

I selected these scenarios because they cover the parts of the feature where defects would have the highest impact.

Successful placement and stake validation are Critical because they directly affect whether users can place bets safely and whether their balance is protected.

Selection replacement, payout recalculation, failure recovery, and API validation are High priority because they protect the integrity of the betting flow and reduce the risk of unclear or incorrect user transactions.

I intentionally kept lower-risk usability areas, such as filters, outside the top six so the plan remains focused and aligned with risk-based testing.
