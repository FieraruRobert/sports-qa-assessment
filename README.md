# QA Take-Home Submission — Single Bet Placement

## Overview

This repository contains a focused QA submission for the Single Bet Placement feature. The goal is not to test everything, but to cover the highest-risk parts of the flow: bet placement, stake validation, single-selection behavior, API validation, and user-facing feedback.

## Scope

In scope:
- Desktop web application
- Football / soccer only
- Upcoming / pre-match events only
- Single bet only
- UI and API validation around stake, selection, match ID, balance, and user context

Out of scope:
- Live betting
- Accumulators / multi-bets
- Other sports
- Mobile-specific UX

## Required stack

- Python 3
- Selenium WebDriver
- Pytest
- requests
- Latest desktop Chrome

## Project structure

```text
.
├── README.md
├── test-plan.md
├── execution-results-and-bugs.md
├── strategy-and-recommendations.md
└── automation
    ├── requirements.txt
    ├── pytest.ini
    ├── conftest.py
    ├── pages
    │   └── betting_page.py
    ├── tests
    │   ├── test_place_bet_ui.py
    │   └── test_place_bet_api.py
    └── utils
        └── api_client.py
```

## Setup

```bash
cd automation
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Run tests

Run all tests:

```bash
pytest
```

Run only UI tests:

```bash
pytest -m ui
```

Run only API tests:

```bash
pytest -m api
```

Run with a custom user id:

```bash
pytest --user-id=robert99df
```

## Notes

The UI locators are written in a defensive way because the assignment does not provide stable `data-testid` attributes. If this were a production project, I would strongly recommend adding stable automation IDs for the match cards, odds buttons, stake field, balance, bet slip, and receipt modal.

## Automation

The automation project is under `automation/` and uses the stack required by the assignment:

- Python 3
- Selenium WebDriver
- Pytest
- Python `requests` library
- Latest desktop Chrome

### Default test user

The tests use the following user id by default:

```bash
candidate-XeYACiwXZx
```

It can be overridden through an environment variable:

```bash
export TEST_USER_ID="candidate-XeYACiwXZx"
```

The application URL can also be overridden if needed:

```bash
export BASE_URL="https://qae-assignment-tau.vercel.app"
```

### Setup

```bash
cd automation
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\\Scripts\\activate
pip install -r requirements.txt
```

### Run all tests

```bash
pytest
```

### Run only the UI test

```bash
pytest -m ui
```

### Run only the API test

```bash
pytest -m api
```

### Run UI tests with a visible browser

```bash
HEADLESS=false pytest -m ui
```

### Notes

The UI test resets the balance through the API before execution to keep the test deterministic.
The Selenium page object uses visible text because the feature specification does not mention stable automation selectors. If this project scaled, I would recommend adding `data-testid` attributes for key controls such as odds buttons, stake input, Place Bet, bet slip totals, and receipt fields.
