[execution-results-and-bugs.md](https://github.com/user-attachments/files/29008517/execution-results-and-bugs.md)
# Execution Results and Bug Reports

## Execution note

These are the top three scenarios I executed first because they cover the main money flow and the most important guardrails.

Manual execution was performed against the live application using the assigned user context. During execution and exploratory testing, I also checked nearby areas around the bet placement flow, such as receipt consistency, balance updates, date filtering, odds filtering, and past match availability.

---

## Execution results

| Scenario ID | Title | Priority | Status | Notes |
|---|---|---|---|---|
| SBP-001 | Successful single bet placement | Critical | Failed | The bet can be placed successfully, but the receipt contains incorrect/incomplete details and the balance does not update immediately after purchase. |
| SBP-002 | Stake validation and balance protection | Critical | Passed | Tested invalid and boundary stake values. Stake above the maximum is rejected and Place Bet remains disabled. |
| SBP-003 | Single-selection replacement in bet slip | High | Passed | Selecting a new outcome replaces the previous selection, and the bet slip does not keep multiple active selections. |

---

# Bug Reports

## BUG-001 — Users Can Access and Place Bets on Past Matches

**Severity:** Critical  
**Related scenario:** Exploratory testing around match availability and date filtering

### Reproduction steps

1. Open the application using a valid user ID:  
   `https://qae-assignment-tau.vercel.app/?user-id=<your-user-id>`
2. Open the **Date** filter.
3. Select a past date or past date range.
4. Apply the filter.
5. Observe that matches marked as `PAST` are displayed.
6. Select odds for one of the past matches.
7. Enter a valid stake, for example `10.00`.
8. Click **Place Bet**.
9. Observe the result.

### Expected result

The application should only allow betting on upcoming / pre-match football events.

Past matches should not be available in the active betting flow. They should either not be displayed at all, or they should be shown as historical information only, with disabled odds and no betting actions.

### Actual result

Past matches are displayed in the **Upcoming Football Matches** list.

The Date filter allows users to select past dates and returns past matches. The user can also select odds and place a bet on a match marked as `PAST`.

### Business impact

This is a serious betting integrity issue.

Users should not be able to place pre-match bets on events that have already happened. Allowing this can create invalid betting transactions, user disputes, and major trust issues with the platform.

### Evidence

Past matches are displayed under the **Upcoming Football Matches** section:

![Past matches visible in upcoming matches list](screenshots/bug-001-past-ma![Uploading bug-001-date-filter-past-range.png…]()
tches-visible.png)

The date filter allows selecting a past date range and still returns betting events:

![Date filter allows past date range](screenshots/bug-001-date-filter-past-range.png)

---

## BUG-002 — Bet Receipt Shows Incorrect Match Order and Payout After Placement

**Severity:** High  
**Related scenario:** SBP-001 Successful single bet placement

### Reproduction steps

1. Open the application using a valid user ID:  
   `https://qae-assignment-tau.vercel.app/?user-id=<your-user-id>`
2. Select the match `AC Milan vs Napoli`.
3. Select the **Away** outcome.
4. Enter a stake of `10.00`.
5. Observe the Bet Slip before placing the bet.
6. Click **Place Bet**.
7. Wait for the success receipt to be displayed.
8. Compare the receipt values with the Bet Slip values shown before placement.

### Expected result

The success receipt should show the same bet details that were displayed before placement.

For this example, the receipt should show:

- Match: `AC Milan vs Napoli`
- Selection: `Away` / `Napoli`
- Stake: `€10.00`
- Odds: `3.20`
- Potential payout: `€32.00`

The match order should remain consistent with the match list, where the home team is displayed first and the away team second.

### Actual result

The success receipt displays inconsistent bet details.

Before placement, the Bet Slip shows:

- Match: `AC Milan vs Napoli`
- Selection: `Away`
- Odds: `3.20`
- Stake: `€10.00`
- Potential payout: `€32.00`

After placement, the receipt shows:

- Match: `Napoli vs AC Milan`
- Stake: `€10.00`
- Odds: `3.20`
- Potential payout: `€20.00`

The receipt also does not clearly display the selected outcome.

### Business impact

The receipt is the user's confirmation of the placed bet.

If it shows the teams in the wrong order, omits the selected outcome, or displays an incorrect payout, the user cannot reliably confirm what they actually placed.

This can lead to user confusion, loss of trust, and possible disputes around bet confirmation and payout expectations.

### Evidence

Before placement, the Bet Slip shows `AC Milan vs Napoli`, `Away`, odds `3.20`, stake `€10.00`, and potential payout `€32.00`:

![Bet Slip before placement](screenshots/bug-002-bet-slip-before-placement.png)

After placement, the receipt shows reversed match order and incorrect potential payout:

![Receipt after placement](screenshots/bug-002-receipt-after-placement.png)

---

## BUG-003 — Balance Is Not Updated Immediately After Successful Bet Placement

**Severity:** High  
**Related scenario:** SBP-001 Successful single bet placement

### Reproduction steps

1. Open the application using a valid user ID:  
   `https://qae-assignment-tau.vercel.app/?user-id=<your-user-id>`
2. Note the current balance displayed in the header and/or Bet Slip.
3. Select any available match outcome.
4. Enter a valid stake, for example `10.00`.
5. Click **Place Bet**.
6. Wait for the success receipt to be displayed.
7. Close the success receipt.
8. Observe the displayed balance.
9. Refresh the page.
10. Observe the balance again.

### Expected result

After successful bet placement, the displayed balance should update immediately without requiring a page refresh.

For example, if the initial balance is `€120.00` and the user places a `€10.00` bet, the balance should update to `€110.00` as soon as the bet is successfully placed.

### Actual result

After successful bet placement, the balance remains unchanged in the UI.

The updated balance is only displayed after refreshing the page.

### Business impact

This can confuse users because the UI suggests that their balance was not deducted even though the bet was successfully processed.

For a betting flow, delayed or stale balance updates can reduce user trust and may lead users to believe the transaction failed or that they still have more funds available than they actually do.

### Evidence

Manual observation during the bet placement flow. No screenshot pair was captured for this issue yet.

Recommended evidence to add if time allows:

- Screenshot before placing the bet showing the initial balance.
- Screenshot after closing the success receipt showing the unchanged balance.
- Screenshot after refresh showing the updated balance.

---

## BUG-004 — Odds Filter Does Not Update the Match List

**Severity:** Medium  
**Related scenario:** Exploratory testing around filters

### Reproduction steps

1. Open the application using a valid user ID:  
   `https://qae-assignment-tau.vercel.app/?user-id=<your-user-id>`
2. Observe the initial list of matches.
3. Open the **Odds** filter.
4. Select an odds range, for example:
   - Minimum odds: `1.00`
   - Maximum odds: `5.09`
5. Apply the filter.
6. Observe the match list.

### Expected result

The match list should update based on the selected odds range.

Only matches containing odds within the selected range should be displayed. The odds filter should be inclusive, meaning odds equal to the minimum or maximum values should also be included.

### Actual result

The match list remains unchanged after applying the odds filter.

Matches outside the selected odds range remain visible / the same match list is still displayed.

### Business impact

Users cannot narrow down matches based on odds, even though the feature is available in the UI.

This reduces usability and makes it harder for users to find betting options that match their risk or payout preference.

### Evidence

The Odds filter shows a selected range, but the list still contains matches outside that range and the match count remains unchanged:

![Odds filter does not update match list](screenshots/bug-004-odds-filter-not-updating-list.png)

---

## Exploratory checks performed

These are quick checks I ran around the main bet placement flow:

- Refreshed the page after placing a bet to compare balance behaviour before and after refresh.
- Removed a selection using the per-selection `X`.
- Used `Remove All` after entering a stake.
- Compared balance behaviour after successful bet placement.
- Confirmed payout calculation before placement using `stake × odds`.
- Tried stake values above the maximum allowed amount.
- Checked that receipt values match the pre-submit values.
- Checked whether the receipt includes the selected outcome.
- Checked date filtering with past dates.
- Checked whether past matches are selectable for betting.
- Checked whether the odds filter updates the match list.
- Reviewed the failed placement modal and its available actions.
