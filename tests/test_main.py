'''
  Playwright Test Suite
  =====================
  This script includes test cases for login, navigation, and form validation using Playwright with pytest.
'''

import pytest



from playwright.sync_api import sync_playwright, Page, expect
import os
import pytest

# Configuration
BASE_URL = os.getenv("BASE_URL", "https://www.saucedemo.com/")

# Helper Function for Login
def login(page: Page, username: str, password: str):
    page.goto(BASE_URL)
    page.fill("#user-name", username)
    page.fill("#password", password)
    page.click("#login-button")

# Pytest Fixtures
@pytest.fixture(params=["chromium", "firefox", "webkit"])
def browser():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        yield browser
        browser.close()

@pytest.fixture(scope="function")
def page(browser):
    context = browser.new_context()
    page = context.new_page()
    yield page
    page.close()
    #fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff
    #eeeeee



# Test Login Functionality
def test_successful_login(page: Page):
    login(page, "standard_user", "secret_sauce")
    page.wait_for_url("**/inventory.html")  # Ensure the URL changes before assertion
    assert page.url.split('/')[-1] == "inventory.html"


    #expect(page).to_have_url("**/inventory.html")

def test_invalid_login(page: Page):
    login(page, "invalid_user", "wrong_password")
    pp= (page.locator('[data-test="error"]')).text_content()
    assert (page.locator('[data-test="error"]')).text_content()=='Epic sadface: Username and password do not match any user in this service'


def test_empty_fields(page: Page):
    page.goto(BASE_URL)
    page.click("#login-button")
    #assert page.locator('[data-test="error"]').text_content()=='Username is required'

    expect(page.locator('[data-test="error"]')).text_content().to_have_text("Username is required")

# Test Navigation


def test_navigation_bar_accessibility(page: Page):
    login(page, "standard_user", "secret_sauce")
    page.click(".bm-burger-button")
    expect(page.locator(".bm-menu-wrap")).to_be_visible()

# Test Form Validation
def test_invalid_email(page: Page):
    login(page, "standard_user", "secret_sauce")
    #page.pause()

    page.goto("https://www.saucedemo.com/checkout-step-one.html")
    #page.pause()

    page.fill("#first-name", "John")
    page.fill("#last-name", "Doe")
    page.fill("#postal-code", "12345")
#    page.fill("#email", "invalid-email")
    page.locator("[data-test=\"continue\"]").click()
    expect(page.locator("[data-test=\"total-label\"]")).to_have_text("Total: $0.00")



# Run Tests
if __name__ == "__main__":
    pytest.main(["-v", "--disable-warnings"])
