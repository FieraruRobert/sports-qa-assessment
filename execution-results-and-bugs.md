# Execution Results and Bug Reports

## Execution note

These are the top three scenarios I would execute first because they cover the main money flow and the most important guardrails. Actual results should be updated after running against the live application and attaching screenshots where relevant.

---

## Execution results

| Scenario ID | Title | Priority | Status | Notes |
|---|---|---:|---|---|
| SBP-001 | Successful single bet placement | Critical | Not run yet | Execute first because it validates the main user journey. |
| SBP-002 | Stake validation and balance protection | Critical | Not run yet | Execute second because it protects balance and invalid financial input. |
| SBP-003 | Single-selection replacement in bet slip | High | Not run yet | Execute third because only single bets are supported. |

---

# Bug Reports

## BUG-001 — Placeholder: update after execution

**Severity:** TBD  
**Related scenario:** TBD

### Reproduction steps
1. TBD
2. TBD
3. TBD

### Expected result
TBD

### Actual result
TBD

### Business impact
TBD

### Evidence
TBD

---

## Exploratory checks to perform

These are quick checks I would run around the main bet placement flow:

- Refresh page after selecting an outcome and entering stake.
- Remove selection using per-selection `x`.
- Use `Remove All` after stake entry.
- Compare balance value in header and bet slip.
- Confirm payout calculation uses `stake × odds` and includes the original stake.
- Place a bet close to max stake, for example `100.00`.
- Try minimum stake `1.00`.
- Try decimal formats such as `1`, `1.0`, `1.00`, and `1.001`.
- Check that receipt values match the pre-submit values.
