import os

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from utils.api_client import BettingApiClient


DEFAULT_BASE_URL = "https://qae-assignment-tau.vercel.app"
DEFAULT_USER_ID = "candidate-XeYACiwXZx"


@pytest.fixture(scope="session")
def base_url() -> str:
    return os.getenv("BASE_URL", DEFAULT_BASE_URL).rstrip("/")


@pytest.fixture(scope="session")
def test_user_id() -> str:
    return os.getenv("TEST_USER_ID", DEFAULT_USER_ID)


@pytest.fixture(scope="session")
def api_client(base_url: str, test_user_id: str) -> BettingApiClient:
    return BettingApiClient(base_url=base_url, user_id=test_user_id)


@pytest.fixture()
def driver():
    chrome_options = Options()
    chrome_options.add_argument("--window-size=1440,1000")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")

    if os.getenv("HEADLESS", "true").lower() in {"1", "true", "yes"}:
        chrome_options.add_argument("--headless=new")

    browser = webdriver.Chrome(options=chrome_options)
    browser.implicitly_wait(0)
    yield browser
    browser.quit()
