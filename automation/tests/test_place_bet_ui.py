from decimal import Decimal, ROUND_HALF_UP

import pytest

from pages.betting_page import BettingPage


@pytest.mark.ui
def test_user_can_place_a_valid_single_bet(driver, base_url, test_user_id, api_client):
    """Critical E2E coverage: proves the main money flow works from selection to receipt.

    I chose this test because it covers the highest-value user journey: selecting a football
    outcome, entering a valid stake, seeing the payout, placing the bet, and confirming that
    the balance is deducted correctly.
    """
    reset_response = api_client.reset_balance()
    assert reset_response.status_code == 200, reset_response.text

    page = BettingPage(driver=driver, base_url=base_url, user_id=test_user_id)
    page.open()

    starting_balance = page.current_balance()
    odds = page.select_first_available_outcome()

    stake = Decimal("10.00")
    page.enter_stake(str(stake))

    expected_payout = (stake * odds).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    assert page.potential_payout() == expected_payout

    page.click_place_bet()
    page.wait_for_success_receipt()

    receipt_text = page.success_receipt_text()
    receipt_text_lower = receipt_text.lower()
    assert "bet id" in receipt_text_lower
    assert "stake" in receipt_text_lower
    assert "odds" in receipt_text_lower
    assert "potential payout" in receipt_text_lower

    page.close_success_receipt()
    assert page.current_balance() == starting_balance - stake
