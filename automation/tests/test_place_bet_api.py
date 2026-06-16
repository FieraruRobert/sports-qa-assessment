from decimal import Decimal

import pytest


@pytest.mark.api
def test_place_bet_rejects_stake_above_maximum(api_client):
    """API business-rule coverage: the backend must reject stakes above €100.

    I chose this test because UI validation can be bypassed. The API is the final protection
    layer for financial rules, so it must reject an over-limit stake and keep the balance
    unchanged.
    """
    reset_response = api_client.reset_balance()
    assert reset_response.status_code == 200, reset_response.text

    balance_before_response = api_client.get_balance()
    assert balance_before_response.status_code == 200, balance_before_response.text
    balance_before = Decimal(str(balance_before_response.json()["balance"]))

    matches_response = api_client.get_matches()
    assert matches_response.status_code == 200, matches_response.text
    matches = matches_response.json()
    assert matches, "Expected at least one available match from GET /api/matches"

    payload = {
        "matchId": matches[0]["id"],
        "selection": "HOME",
        "stake": 101,
    }

    response = api_client.place_bet(payload)

    assert response.status_code == 422, response.text

    balance_after_response = api_client.get_balance()
    assert balance_after_response.status_code == 200, balance_after_response.text
    balance_after = Decimal(str(balance_after_response.json()["balance"]))

    assert balance_after == balance_before
