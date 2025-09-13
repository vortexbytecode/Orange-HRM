"""Base page module containing core web interaction functionality.

This module provides the BasePage class which serves as a foundation for all page objects
in the Orange HRM test automation framework. It includes common web element interaction
methods with built-in waits, logging, and performance monitoring.

The module implements page object pattern best practices and handles common Selenium
operations like waiting for elements, checking visibility, and entering text.
"""

import logging
import time

from selenium.common import WebDriverException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait

from orange_hrm.constants.json_env_config import (
    PerformanceFields,
    TopKey,
    WebDriverFields,
)

performance_base_logger = logging.getLogger(f"{__name__}.performance")
performance_logger = logging.LoggerAdapter(
    performance_base_logger,
    {"role": "PERFORMANCE"},
)

base_logger = logging.getLogger(__name__)
logger = logging.LoggerAdapter(base_logger, {"role": "BASE"})


class BasePage:
    """Base page class providing core web interaction functionality.

    This class serves as a foundation for all page objects in the test automation framework.
    It implements common web element interaction methods with built-in waits, logging,
    and performance monitoring capabilities.

    The class follows page object pattern best practices and provides methods for:
    - Waiting for elements to be visible or clickable
    - Checking element visibility
    - Entering text into input fields
    - Performance logging of web interactions

    Attributes
    ----------
    driver : WebDriver
        Selenium WebDriver instance for browser automation
    performance : float
        Performance threshold in seconds for action timing
    explicit_wait_timeout : float
        Maximum time to wait for element interactions
    wait : WebDriverWait
        WebDriverWait instance configured with timeout

    """

    def __init__(self, driver: WebDriver, env_config: dict) -> None:
        """Initialize BasePage with WebDriver instance and environment configuration.

        Parameters
        ----------
        driver : WebDriver
            Selenium WebDriver instance for browser automation
        env_config : dict
            Dictionary containing environment configuration settings including:
            - Performance thresholds
            - WebDriver timeout settings

        Notes
        -----
        The BasePage class serves as a foundation for all page objects,
        providing common web interaction methods and performance monitoring.

        """
        self.driver = driver
        self.performance = env_config[TopKey.PERFORMANCE.value][PerformanceFields.PERFORMANCE_THRESHOLD.value]
        self.explicit_wait_timeout = env_config[TopKey.WEBDRIVER.value][WebDriverFields.EXPLICIT_WAIT.value]
        self.wait = WebDriverWait(self.driver, self.explicit_wait_timeout)

    def _log_performance(self, action: str, duration: float) -> None:
        """Log performance metrics for actions with threshold checking.

        Parameters
        ----------
        action : str
            Description of the action performed
        duration : float
            Time taken to complete the action in seconds

        """
        if duration > self.performance:
            performance_logger.warning(
                "Action '%s' took %.2f seconds which exceeds the threshold of %s seconds.",
                action,
                duration,
                self.performance,
            )
        else:
            performance_logger.info("Action '%s' took %.2f seconds.", action, duration)

    def wait_for_element_visible(self, locator: tuple) -> WebElement:
        """Wait for element to be visible on the page.

        Parameters
        ----------
        locator : tuple
            Element locator in format (By.TYPE, "value")

        Returns
        -------
        WebElement
            The visible element

        Raises
        ------
        TimeoutException
            If element is not visible within timeout period

        """
        try:
            logger.debug(
                "Waiting for visibility of element located by %s for up to %s seconds.",
                locator,
                self.explicit_wait_timeout,
            )
            start_time = time.time()

            element = self.wait.until(ec.visibility_of_element_located(locator))

        except TimeoutException as err:
            logger.warning(
                "Timeout while waiting for visibility of element located by %s after %s seconds.",
                locator,
                self.explicit_wait_timeout,
                exc_info=True,
            )
            msg = "Timeout while waiting for visibility of element located by %s after %s seconds."
            raise TimeoutException(msg % (locator, self.explicit_wait_timeout)) from err
        except Exception:
            logger.exception(
                "An error occurred while waiting for visibility of element located by %s after %s seconds.",
                locator,
                self.explicit_wait_timeout,
            )
            raise
        else:
            duration = time.time() - start_time
            self._log_performance(f"wait_for_element_visible({locator})", duration)

            logger.debug("Element located by %s is visible.", locator)
            return element

    def wait_for_element_clickable(self, locator: tuple) -> WebElement:
        """Wait for element to be clickable (visible and enabled).

        Parameters
        ----------
        locator : tuple
            Element locator in format (By.TYPE, "value")

        Returns
        -------
        WebElement
            The clickable element

        Raises
        ------
        TimeoutException
            If element is not clickable within timeout period

        """
        try:
            logger.debug(
                "Waiting for element located by %s to be clickable for up to %s seconds.",
                locator,
                self.explicit_wait_timeout,
            )
            start_time = time.time()

            element = self.wait.until(ec.element_to_be_clickable(locator))

        except TimeoutException as err:
            logger.warning(
                "Timeout while waiting for element located by %s to be clickable after %s seconds.",
                locator,
                self.explicit_wait_timeout,
                exc_info=True,
            )
            msg = "Timeout while waiting for element located by %s to be clickable after %s seconds."
            raise TimeoutException(msg % (locator, self.explicit_wait_timeout)) from err
        except Exception:
            logger.exception(
                "An error occurred while waiting for element located by %s to be clickable after %s seconds.",
                locator,
                self.explicit_wait_timeout,
            )
            raise
        else:
            duration = time.time() - start_time
            self._log_performance(f"wait_for_element_clickable({locator})", duration)

            logger.debug("Element located by %s is clickable.", locator)
            return element

    def is_element_visible(self, locator: tuple) -> bool:
        """Check if an element is visible on the page.

        Parameters
        ----------
        locator : tuple
            Element locator in format (By.TYPE, "value")

        Returns
        -------
        bool
            True if element is visible, False if not visible or times out

        Raises
        ------
        Exception
            For unexpected errors not related to element visibility timeouts

        """
        try:
            logger.debug(
                "Initiating visibility check for element with locator=%s. Timeout configured for %s seconds.",
                locator,
                self.explicit_wait_timeout,
            )

            start_time = time.time()
            element = self.wait.until(ec.visibility_of_element_located(locator))
            duration = time.time() - start_time

            self._log_performance(f"visibility_of_element_located({locator})", duration)

            logger.debug("Element located by %s is visible.", locator)
            return element.is_displayed()

        except TimeoutException:
            logger.warning(
                "Timeout while waiting for visibility of element located by %s after %s seconds.",
                locator,
                self.explicit_wait_timeout,
                exc_info=True,
            )
            return False
        except Exception:
            logger.exception(
                "An error occurred while checking visibility of element located by %s after %s seconds.",
                locator,
                self.explicit_wait_timeout,
            )
            raise

    def enter_text(self, locator: tuple, text: str, *, is_secret: bool = False) -> None:
        """Enter text into an input element.

        Parameters
        ----------
        locator : tuple
            Element locator in format (By.TYPE, "value")
        text : str
            Text to enter into element
        is_secret : bool, optional
            If True, masks text in logs, by default False. Must be passed as keyword argument.

        Raises
        ------
        WebDriverException
            If text entry fails
        Exception
            For unexpected errors

        Notes
        -----
        - wait_for_clickable exceptions are already logged in the wait_for_clickable method

        Examples
        --------
        >>> username_field = (By.ID, "username")
        >>> password_field = (By.ID, "password")
        >>> page.enter_text(username_field, "admin@example.com")
        >>> page.enter_text(password_field, "secret123", is_secret=True)

        """
        element = self.wait_for_element_clickable(locator)

        try:
            logger.debug("Clearing element: %s", locator)
            element.clear()
            logger.debug("Sending keys to element: %s", locator)
            element.send_keys(text)
            display_text = "*" * len(text) if is_secret else text
            logger.debug("Entered text '%s' [locator='%s']", display_text, locator)
        except WebDriverException as err:
            logger.warning("Error entering text [locator='%s']", locator, exc_info=True)
            msg = f"Error entering text [locator='{locator}']"
            raise WebDriverException(msg) from err
        except Exception:
            logger.exception("Unexpected error entering text [locator='%s']", locator)
            raise
