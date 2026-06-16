from __future__ import annotations

import re
from decimal import Decimal
from urllib.parse import quote

from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class BettingPage:
    """Page object for the Single Bet Placement UI.

    The app used in this take-home does not expose selectors in the specification, so the
    locators intentionally prefer user-facing text. If the product were to scale, I would
    recommend adding stable data-testid attributes for the main controls.
    """

    def __init__(self, driver: WebDriver, base_url: str, user_id: str, timeout: int = 10) -> None:
        self.driver = driver
        self.base_url = base_url.rstrip("/")
        self.user_id = user_id
        self.wait = WebDriverWait(driver, timeout)

    def open(self) -> None:
        self.driver.get(f"{self.base_url}/?user-id={quote(self.user_id)}")
        self.wait.until(lambda d: "Balance" in d.find_element(By.TAG_NAME, "body").text)
        self.wait.until(lambda d: any(self._looks_like_odds_button(button.text.strip()) for button in d.find_elements(By.TAG_NAME, "button")))

    def current_balance(self) -> Decimal:
        body_text = self.driver.find_element(By.TAG_NAME, "body").text
        match = re.search(r"Balance:?\s*€\s*(\d+(?:\.\d{1,2})?)", body_text, re.IGNORECASE)
        if not match:
            raise AssertionError(f"Could not find balance in page text:\n{body_text}")
        return Decimal(match.group(1))

    def select_first_available_outcome(self) -> Decimal:
        """Select the first visible odds button and return the odds value."""
        self.wait.until(lambda d: len(d.find_elements(By.TAG_NAME, "button")) > 0)

        for button in self.driver.find_elements(By.TAG_NAME, "button"):
            text = button.text.strip()
            if self._looks_like_odds_button(text) and button.is_displayed() and button.is_enabled():
                odds = self._extract_last_decimal(text)
                button.click()
                self.wait.until(lambda d: self._bet_slip_contains_selection())
                return odds

        raise AssertionError("No enabled odds button was found on the match list.")

    def enter_stake(self, stake: str) -> None:
        stake_input = self._stake_input()
        stake_input.click()
        stake_input.send_keys(Keys.CONTROL, "a")
        stake_input.send_keys(stake)

    def potential_payout(self) -> Decimal:
        body_text = self.driver.find_element(By.TAG_NAME, "body").text
        match = re.search(
            r"Potential\s+Payout\s*€\s*(\d+(?:\.\d{1,2})?)",
            body_text,
            re.IGNORECASE,
        )
        if not match:
            raise AssertionError(f"Could not find potential payout in page text:\n{body_text}")
        return Decimal(match.group(1))

    def wait_until_place_bet_enabled(self) -> WebElement:
        return self.wait.until(lambda d: self._place_bet_button() if self._place_bet_button().is_enabled() else False)

    def click_place_bet(self) -> None:
        self.wait_until_place_bet_enabled().click()

    def wait_for_success_receipt(self) -> None:
        self.wait.until(
            EC.visibility_of_element_located(
                (
                    By.XPATH,
                    "//*[contains(normalize-space(.), 'Bet Placed Successfully') "
                    "or contains(normalize-space(.), 'Bet ID')]",
                )
            )
        )

    def success_receipt_text(self) -> str:
        self.wait_for_success_receipt()
        return self.driver.find_element(By.TAG_NAME, "body").text

    def close_success_receipt(self) -> None:
        buttons = self.driver.find_elements(By.TAG_NAME, "button")
        for button in buttons:
            if button.is_displayed() and re.search(r"^(close|done|ok)$", button.text.strip(), re.IGNORECASE):
                button.click()
                return
        # Fallback: close the modal through Escape if the close button text changes.
        self.driver.find_element(By.TAG_NAME, "body").send_keys(Keys.ESCAPE)

    def _stake_input(self) -> WebElement:
        locators = [
            (By.XPATH, "//input[contains(translate(@placeholder, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'stake')]"),
            (By.XPATH, "//input[contains(translate(@aria-label, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'stake')]"),
            (By.XPATH, "//input[contains(translate(@name, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'stake')]"),
            (By.XPATH, "//input[@placeholder='0.00']"),
            (By.XPATH, "//input[@type='number']"),
            (By.XPATH, "//input[not(@type='hidden') and not(@type='range')]"),
        ]

        def first_visible_enabled_input(driver: WebDriver) -> WebElement | bool:
            for locator in locators:
                for element in driver.find_elements(*locator):
                    if element.is_displayed() and element.is_enabled():
                        return element
            return False

        try:
            return self.wait.until(first_visible_enabled_input)
        except TimeoutException as exc:
            raise NoSuchElementException("Stake input was not found.") from exc

    def _place_bet_button(self) -> WebElement:
        return self.driver.find_element(
            By.XPATH,
            "//button[contains(translate(normalize-space(.), 'abcdefghijklmnopqrstuvwxyz', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'), 'PLACE BET')]",
        )

    def _bet_slip_contains_selection(self) -> bool:
        body_text = self.driver.find_element(By.TAG_NAME, "body").text
        return "Bet Slip" in body_text and ("Match Winner" in body_text or "Total Stake" in body_text)

    @staticmethod
    def _looks_like_odds_button(text: str) -> bool:
        if not text:
            return False
        upper_text = text.upper()
        excluded = ["PLACE BET", "REMOVE ALL", "FILTER", "CLEAR", "RESET", "REBET", "CLOSE"]
        if any(label in upper_text for label in excluded):
            return False
        has_outcome_label = re.search(r"(^|\s)(1|X|2)(\s|$)", text)
        has_decimal_odds = re.search(r"\d+\.\d{2}", text)
        return bool(has_outcome_label and has_decimal_odds)

    @staticmethod
    def _extract_last_decimal(text: str) -> Decimal:
        values = re.findall(r"\d+\.\d{2}", text)
        if not values:
            raise AssertionError(f"No odds value found in button text: {text}")
        return Decimal(values[-1])
