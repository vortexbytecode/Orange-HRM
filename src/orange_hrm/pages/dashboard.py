"""Module containing the DashboardPage class for interacting with the OrangeHRM dashboard page.

This module provides functionality to verify and interact with elements on the dashboard
page of the OrangeHRM application.
"""

import logging

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from orange_hrm.pages.base import BasePage

base_logger = logging.getLogger(__name__)
logger = logging.LoggerAdapter(base_logger, {"role": "DASHBOARD PAGE"})


class DashboardPage:
    """Class representing the dashboard page of the OrangeHRM application.

    This class provides methods to interact with and verify elements on the
    dashboard page, including checking visibility of dashboard components.
    """

    DASHBOARD_TITLE = (By.XPATH, "//h6[normalize-space()='Dashboard']")

    def __init__(self, driver: WebDriver, env_config: dict) -> None:
        """Initialize DashboardPage with WebDriver instance.

        Parameters
        ----------
        driver : WebDriver
            Selenium WebDriver instance for browser automation
        env_config : dict
            Environment configuration dictionary

        """
        self.base_page = BasePage(driver, env_config)

    def is_dashboard_title_displayed(self) -> bool:
        """Check if the dashboard title is displayed on the page.

        Returns
        -------
        bool
            True if dashboard title is visible, False otherwise

        """
        return self.base_page.is_element_visible(self.DASHBOARD_TITLE)
