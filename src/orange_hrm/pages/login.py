"""Login page module for Orange HRM application.

This module provides the LoginPage class which handles all interactions with
the login page of the Orange HRM application, including entering credentials,
clicking the login button, and validating error messages.
"""

import logging

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from orange_hrm.constants.json_env_config import ApplicationFields, TopKey
from orange_hrm.pages.base import BasePage

base_logger = logging.getLogger(__name__)
logger = logging.LoggerAdapter(base_logger, {"role": "LOGIN PAGE"})


class LoginPage:
    """Page object representing the Orange HRM login page.

    This class provides methods to interact with elements on the login page,
    including entering credentials, submitting the login form, and validating
    error messages.

    Attributes
    ----------
    INVALID_CREDENTIALS_MESSAGE : tuple
        Locator for invalid credentials error message
    USERNAME_FIELD : tuple
        Locator for username input field
    USERNAME_VALIDATION_ERROR : tuple
        Locator for username validation error message
    PASSWORD_FIELD : tuple
        Locator for password input field
    PASSWORD_VALIDATION_ERROR : tuple
        Locator for password validation error message
    LOGIN_BUTTON : tuple
        Locator for login submit button

    """

    INVALID_CREDENTIALS_MESSAGE = (By.XPATH, "//p[@class='oxd-text oxd-text--p oxd-alert-content-text']")

    USERNAME_FIELD = (By.XPATH, "//input[@placeholder='Username']")
    USERNAME_VALIDATION_ERROR = (By.XPATH, "//div[@class='orangehrm-login-slot-wrapper']//div[1]//div[1]//span[1]")

    PASSWORD_FIELD = (By.XPATH, "//input[@placeholder='Password']")
    PASSWORD_VALIDATION_ERROR = (By.XPATH, "//div[@class='orangehrm-login-form']//div[2]//div[1]//span[1]")

    LOGIN_BUTTON = (By.XPATH, "//button[normalize-space()='Login']")

    def __init__(self, driver: WebDriver, env_config: dict) -> None:
        """Initialize LoginPage with WebDriver instance.

        Parameters
        ----------
        driver : WebDriver
            Selenium WebDriver instance for browser automation
        env_config : dict
            Environment configuration dictionary

        """
        self.driver = driver
        self.base_page = BasePage(driver, env_config)
        self.base_url = env_config[TopKey.APPLICATION.value][ApplicationFields.BASE_URL.value]
        self.url = self.base_url + "/auth/login"

    def navigate_to_login_page(self) -> None:
        """Navigate to the Orange HRM login page."""
        logger.info("Navigating to login page")
        self.driver.get(self.url)

    def enter_username(self, username: str) -> None:
        """Enter username into the username field.

        Parameters
        ----------
        username : str
            Username to enter

        """
        logger.info("Entering username")
        self.base_page.enter_text(self.USERNAME_FIELD, username)

    def enter_password(self, password: str) -> None:
        """Enter password into the password field.

        Parameters
        ----------
        password : str
            Password to enter (will be masked in logs)

        """
        logger.info("Entering password")
        self.base_page.enter_text(self.PASSWORD_FIELD, password, is_secret=True)

    def click_login_button(self) -> None:
        """Click the login button to submit credentials."""
        logger.info("Clicking login button")
        self.base_page.wait_for_element_clickable(self.LOGIN_BUTTON).click()

    def is_invalid_credentials_message_displayed(self) -> bool:
        """Check if invalid credentials error message is displayed.

        Returns
        -------
        bool
            True if invalid credentials message is visible, False otherwise

        """
        logger.info("Checking if invalid credentials message is displayed")
        element = self.base_page.wait_for_element_visible(self.INVALID_CREDENTIALS_MESSAGE)
        return element.is_displayed()

    def is_username_validation_error_displayed(self) -> bool:
        """Check if username validation error message is displayed.

        Returns
        -------
        bool
            True if username validation error is visible, False otherwise

        """
        logger.info("Checking if username validation error is displayed")
        element = self.base_page.wait_for_element_visible(self.USERNAME_VALIDATION_ERROR)
        return element.is_displayed()

    def is_password_validation_error_displayed(self) -> bool:
        """Check if password validation error message is displayed.

        Returns
        -------
        bool
            True if password validation error is visible, False otherwise

        """
        logger.info("Checking if password validation error is displayed")
        element = self.base_page.wait_for_element_visible(self.PASSWORD_VALIDATION_ERROR)
        return element.is_displayed()
