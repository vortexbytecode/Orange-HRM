"""Pytest configuration and fixtures for Orange HRM test automation.

This module contains shared pytest fixtures and configuration used across
the test suite, including environment setup, WebDriver configuration,
and logging settings.
"""

import contextlib
import json
import logging
import os
import tempfile
from collections.abc import Generator
from importlib import resources
from pathlib import Path
from typing import Any

import pytest
from selenium import webdriver
from selenium.common import WebDriverException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.webdriver import WebDriver

from orange_hrm.config.dotenv_config import EnvConfig, get_dot_env_secrets
from orange_hrm.constants.json_env_config import Environment

base_logger = logging.getLogger(__name__)
logger = logging.LoggerAdapter(base_logger, {"role": "TEST CONFTEST"})


@pytest.fixture
def refresh_env_config() -> Generator[None, Any]:
    """Use this fixture in tests that mutate environment variables.

    It clears the cache before test, and clears again after test to avoid leaks.

    Example:
    -------
    >>> def test_override_using_cache_clear(monkeypatch, refresh_env_config):
    >>>     monkeypatch.setenv("ORANGEHRM_USERNAME", "temp_user2")
    >>>     fresh = get_dot_env_secrets()   # now reads patched env and caches it
    >>>     assert fresh.username.get_secret_value() == "temp_user2"
    >>> # fixture automatically clears cache at teardown

    """
    get_dot_env_secrets.cache_clear()  # ensure no stale cached object
    yield
    get_dot_env_secrets.cache_clear()  # cleanup after test


@pytest.fixture(scope="session")
def env_settings() -> EnvConfig:
    """Get cached pydantic settings from .env or real env vars.

    Returns:
        EnvConfig: Pydantic settings object containing environment configuration

    Notes:
        Do not use with monkeypatch since this fixture is session-scoped.
        It will not refresh after environment variable overrides.
        For monkeypatch tests, call get_dot_env_secrets() directly instead.

    """
    return get_dot_env_secrets()


@pytest.fixture(scope="session")
def json_env_config(request: pytest.FixtureRequest) -> dict:
    """Load environment configuration from JSON file.

    Parameters
    ----------
    request : pytest.FixtureRequest
        Pytest fixture request object containing configuration

    Returns
    -------
    dict
        Dictionary containing environment configuration

    Notes
    -----
    Reads environment configuration from a JSON file based on the
    --env command line option. Defaults to 'dev' if not specified.

    """
    env = request.config.getoption("--env")  # get CLI value
    raw = resources.read_text(
        "orange_hrm.config",
        f"{env}.json",
    )
    return json.loads(raw)


def pytest_addoption(parser: pytest.Parser) -> None:
    """Add command line options for pytest.

    Parameters
    ----------
    parser : pytest.Parser
        Pytest parser object for adding options

    """
    parser.addoption(
        "--env",
        action="store",
        default=Environment.DEV.value,  # fallback
        choices=[e.value for e in Environment],
        help="Environment to run tests against: dev/staging/prod",
    )
    parser.addoption(
        "--headless",
        action="store_true",
        default=False,
        help="Run browser in headless mode",
    )


@pytest.fixture(scope="function")  # noqa: PT003
def driver(request: pytest.FixtureRequest) -> Generator[WebDriver, Any]:
    """Create and configure Chrome WebDriver instance for testing.

    Parameters
    ----------
    request : pytest.FixtureRequest
        Pytest fixture request object containing configuration

    Returns
    -------
    WebDriver
        Configured Chrome WebDriver instance with logging disabled
        and window maximized

    Notes
    -----
    Configures Chrome WebDriver with options to disable logging
    and set log level to FATAL only.

    """
    # canonical absolute cache path for drivers
    cache_root = Path(os.environ.get("SE_CACHE_PATH", "./drivers")).resolve()
    cache_root.mkdir(parents=True, exist_ok=True)
    os.environ["SE_CACHE_PATH"] = str(cache_root)  # Cache drivers in the root directory

    # ignore failures (e.g., on Windows or restricted CI runners)
    with contextlib.suppress(OSError, PermissionError, NotImplementedError):
        cache_root.chmod(0o700)  # Use the existing Path object

    chrome_options = Options()
    chrome_options.add_argument("--disable-logging")
    chrome_options.add_argument("--log-level=3")  # FATAL only
    chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])

    # Add headless mode and CI-specific options if requested
    if request.config.getoption("--headless"):
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")

    # Use a unique user data directory to avoid conflicts
    user_data_dir = tempfile.TemporaryDirectory(prefix="chrome_user_data_")
    chrome_options.add_argument(f"--user-data-dir={user_data_dir.name}")

    driver = webdriver.Chrome(options=chrome_options)

    # If not headless, maximize for better visual debugging
    if not request.config.getoption("--headless"):
        try:
            driver.maximize_window()
        except (OSError, WebDriverException):
            # some drivers may raise; safe fallback to a fixed size
            driver.set_window_size(1920, 1080)

    yield driver

    with contextlib.suppress(WebDriverException):
        driver.quit()

    # TemporaryDirectory automatically cleans up when context exits
    with contextlib.suppress(Exception):
        user_data_dir.cleanup()


def pytest_configure() -> None:
    """Configure pytest logging settings to reduce noise from external libraries.

    Parameters
    ----------
    config : pytest.Config
        Pytest configuration object

    """
    logging.getLogger("selenium").setLevel(logging.WARNING)
    logging.getLogger("urllib3").setLevel(logging.WARNING)
