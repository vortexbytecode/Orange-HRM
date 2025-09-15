"""Test module for login functionality of Orange HRM application.

This module contains test cases to verify various login scenarios including:
- Valid login credentials
- Invalid login credentials
- Empty credentials
- Empty username
- Empty password
"""

import logging

import pytest
from selenium.webdriver.chrome.webdriver import WebDriver

from orange_hrm.config.dotenv_config import EnvConfig
from orange_hrm.pages.dashboard import DashboardPage
from orange_hrm.pages.login import LoginPage

base_logger = logging.getLogger(__name__)
logger = logging.LoggerAdapter(base_logger, {"role": "TEST LOGIN"})


@pytest.mark.smoke
@pytest.mark.login
@pytest.mark.positive
def test_login_valid_credentials(
    driver: WebDriver,
    json_env_config: dict,
    env_settings: EnvConfig,
) -> None:
    """Test successful login with valid credentials.

    This test verifies that a user can successfully log in to the Orange HRM
    application using valid credentials and access the dashboard page.

    Args:
        driver (WebDriver): Selenium WebDriver instance
        json_env_config (dict): Environment configuration dictionary
        env_settings (EnvConfig): Environment settings containing credentials

    Returns:
        None

    """
    login_page = LoginPage(driver, json_env_config)

    login_page.navigate_to_login_page()
    logger.info("Successfully navigated to and loaded the login page")

    login_page.enter_username(env_settings.username.get_secret_value())
    logger.info("Successfully entered the username")

    login_page.enter_password(env_settings.password.get_secret_value())
    logger.info("Successfully entered the password")

    login_page.click_login_button()
    logger.info("Successfully clicked the login button")

    dashboard_page = DashboardPage(driver, json_env_config)
    assert dashboard_page.is_dashboard_title_displayed(), "Dashboard title is not displayed after login"
    logger.info(
        "Successfully verified dashboard title visibility on the dashboard page",
    )


@pytest.mark.smoke
@pytest.mark.login
@pytest.mark.negative
@pytest.mark.parametrize(
    ("username", "password"),
    [
        ("invalid", "invalid123"),
        ("Admin", "invalid123"),
        ("invalid", "admin123"),
    ],
)
def test_login_invalid_credentials(
    driver: WebDriver,
    json_env_config: dict,
    username: str,
    password: str,
) -> None:
    """Test unsuccessful login with invalid credentials.

    This test verifies that appropriate error messages are displayed when attempting
    to log in with invalid credentials. It tests multiple combinations of invalid
    usernames and passwords.

    Args:
        driver (WebDriver): Selenium WebDriver instance
        json_env_config (dict): Environment configuration dictionary
        username (str): Username to test
        password (str): Password to test

    Returns:
        None

    """
    login_page = LoginPage(driver, json_env_config)

    login_page.navigate_to_login_page()
    logger.info("Successfully navigated to and loaded the login page")

    login_page.enter_username(username)
    logger.info("Successfully entered the username")

    login_page.enter_password(password)
    logger.info("Successfully entered the password")

    login_page.click_login_button()
    logger.info("Successfully clicked the login button")

    assert login_page.is_invalid_credentials_message_displayed(), "Invalid credentials message is not displayed after login with invalid credentials"
    logger.info("Successfully verified invalid credentials message visibility")


@pytest.mark.smoke
@pytest.mark.login
@pytest.mark.negative
def test_login_empty_credentials(driver: WebDriver, json_env_config: dict) -> None:
    """Test unsuccessful login with empty credentials.

    This test verifies that appropriate error messages are displayed when attempting
    to log in with empty credentials. It tests the scenario where both username and
    password fields are left empty.

    Args:
        driver (WebDriver): Selenium WebDriver instance
        json_env_config (dict): Environment configuration dictionary

    Returns:
        None

    """
    login_page = LoginPage(driver, json_env_config)

    login_page.navigate_to_login_page()
    logger.info("Successfully navigated to and loaded the login page")

    login_page.enter_username("")
    logger.info("Successfully entered the blank username")

    login_page.enter_password("")
    logger.info("Successfully entered the blank password")

    login_page.click_login_button()
    logger.info("Successfully clicked the login button")

    assert login_page.is_username_validation_error_displayed(), "Username validation error is not displayed after login with empty username"
    logger.info("Successfully verified username validation error visibility")

    assert login_page.is_password_validation_error_displayed(), "Password validation error is not displayed after login with empty password"
    logger.info("Successfully verified password validation error visibility")


@pytest.mark.smoke
@pytest.mark.login
@pytest.mark.negative
def test_login_empty_username(driver: WebDriver, json_env_config: dict) -> None:
    """Test unsuccessful login with empty username.

    This test verifies that appropriate error messages are displayed when attempting
    to log in with an empty username. It tests the scenario where the username field
    is left empty.

    Args:
        driver (WebDriver): Selenium WebDriver instance
        json_env_config (dict): Environment configuration dictionary

    Returns:
        None

    """
    login_page = LoginPage(driver, json_env_config)

    login_page.navigate_to_login_page()
    logger.info("Successfully navigated to and loaded the login page")

    login_page.enter_username("")
    logger.info("Successfully entered the blank username")

    login_page.enter_password("admin123")
    logger.info("Successfully entered the password")

    login_page.click_login_button()
    logger.info("Successfully clicked the login button")

    assert login_page.is_username_validation_error_displayed(), "Username validation error is not displayed after login with empty username"
    logger.info("Successfully verified username validation error visibility")


@pytest.mark.smoke
@pytest.mark.login
@pytest.mark.negative
def test_login_empty_password(driver: WebDriver, json_env_config: dict) -> None:
    """Test unsuccessful login with empty password.

    This test verifies that appropriate error messages are displayed when attempting
    to log in with an empty password. It tests the scenario where the password field
    is left empty.

    Args:
        driver (WebDriver): Selenium WebDriver instance
        json_env_config (dict): Environment configuration dictionary

    Returns:
        None

    """
    login_page = LoginPage(driver, json_env_config)

    login_page.navigate_to_login_page()
    logger.info("Successfully navigated to and loaded the login page")

    login_page.enter_username("Admin")
    logger.info("Successfully entered the username")

    login_page.enter_password("")
    logger.info("Successfully entered the blank password")

    login_page.click_login_button()
    logger.info("Successfully clicked the login button")

    assert login_page.is_password_validation_error_displayed(), "Password validation error is not displayed after login with empty password"
    logger.info("Successfully verified password validation error visibility")
