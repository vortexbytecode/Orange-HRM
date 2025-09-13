# Usage Guide

> **Comprehensive guide for using the Orange HRM Test Automation Framework**

## Table of Contents

- [Quick Start](#quick-start)
- [Running Tests](#running-tests)
- [Configuration Management](#configuration-management)
- [Writing Tests](#writing-tests)
- [Page Object Model](#page-object-model)
- [Best Practices](#best-practices)
- [Advanced Usage](#advanced-usage)
- [Performance Monitoring](#performance-monitoring)
- [Logging and Debugging](#logging-and-debugging)
- [CI/CD Integration](#cicd-integration)

## Quick Start

### Basic Test Execution

```bash
# Run all tests with default settings
uv run pytest

# Run tests with verbose output
uv run pytest -v

# Run specific test file
uv run pytest tests/test_login.py

# Run specific test method
uv run pytest tests/test_login.py::test_login_valid_credentials
```

### Environment Selection

```bash
# Run tests against development environment (default)
uv run pytest --env=dev

# Run tests against staging environment
uv run pytest --env=staging

# Run tests against production environment
uv run pytest --env=prod
```

### Browser Options

```bash
# Run tests in headless mode (no browser window)
uv run pytest --headless

# Run tests with browser window visible (default)
uv run pytest
```

## Running Tests

### Test Execution Patterns

#### 1. Development Testing

```bash
# Quick feedback during development
uv run pytest tests/test_login.py -v --tb=short

# Run with immediate failure stop
uv run pytest -x

# Run last failed tests only
uv run pytest --lf
```

#### 2. Comprehensive Testing

```bash
# Full test suite with coverage
uv run pytest --cov=src --cov-report=html:reports/coverage --cov-report=term

# Generate detailed reports
uv run pytest --cov=src --cov-report=html:reports/coverage --cov-branch

# Run with performance profiling
uv run pytest --durations=10
```



### Test Filtering



#### By Keywords

```bash
# Run tests containing 'login' in name
uv run pytest -k login

# Run tests containing 'login' but not 'invalid'
uv run pytest -k "login and not invalid"
```

## Configuration Management

### Environment Variables

The framework uses a dual configuration system:

#### 1. Secret Management (via .env file)

```bash
# .env file
ORANGEHRM_USERNAME=Admin
ORANGEHRM_PASSWORD=admin123
```

#### 2. Application Settings (via JSON files)

```json
// src/orange_hrm/config/dev.json
{
    "webdriver": {
        "explicit_wait": 20
    },
    "application": {
        "base_url": "https://opensource-demo.orangehrmlive.com/web/index.php"
    },
    "performance": {
        "performance_threshold": 5
    }
}
```

### Configuration Access in Tests

```python
def test_example(driver, json_env_config, env_settings):
    # Access JSON configuration
    base_url = json_env_config["application"]["base_url"]
    timeout = json_env_config["webdriver"]["explicit_wait"]
    
    # Access secret credentials
    username = env_settings.username.get_secret_value()
    password = env_settings.password.get_secret_value()
```

### Environment-Specific Testing

```python
# Test with different environments
def test_staging_specific_behavior(json_env_config):
    if json_env_config.get("environment") == "staging":
        # Staging-specific test logic
        pass
```

## Writing Tests

### Basic Test Structure

```python
import logging
import pytest
from selenium.webdriver.chrome.webdriver import WebDriver

from orange_hrm.config.dotenv_config import EnvConfig
from orange_hrm.pages.login import LoginPage
from orange_hrm.pages.dashboard import DashboardPage

# Setup logging
base_logger = logging.getLogger(__name__)
logger = logging.LoggerAdapter(base_logger, {"role": "TEST_EXAMPLE"})

def test_login_workflow(driver: WebDriver, json_env_config: dict, env_settings: EnvConfig):
    """Test complete login workflow."""
    # Initialize page objects
    login_page = LoginPage(driver, json_env_config)
    dashboard_page = DashboardPage(driver, json_env_config)
    
    # Test steps
    login_page.navigate_to_login_page()
    logger.info("Navigated to login page")
    
    login_page.enter_username(env_settings.username.get_secret_value())
    login_page.enter_password(env_settings.password.get_secret_value())
    login_page.click_login_button()
    logger.info("Submitted login credentials")
    
    # Assertions
    assert dashboard_page.is_dashboard_title_displayed()
    logger.info("Login successful - dashboard displayed")
```

### Parameterized Tests

```python
@pytest.mark.parametrize("username,password,expected_error", [
    ("invalid_user", "invalid_pass", "Invalid credentials"),
    ("", "password", "Username is required"),
    ("username", "", "Password is required"),
    ("", "", "Username is required"),
])
def test_login_validation(driver, json_env_config, username, password, expected_error):
    """Test login validation with various invalid inputs."""
    login_page = LoginPage(driver, json_env_config)
    
    login_page.navigate_to_login_page()
    login_page.enter_username(username)
    login_page.enter_password(password)
    login_page.click_login_button()
    
    # Assert appropriate error message is displayed
    assert login_page.get_error_message() == expected_error
```

### Test Fixtures

```python
@pytest.fixture
def logged_in_user(driver, json_env_config, env_settings):
    """Fixture that provides a logged-in user session."""
    login_page = LoginPage(driver, json_env_config)
    
    login_page.navigate_to_login_page()
    login_page.enter_username(env_settings.username.get_secret_value())
    login_page.enter_password(env_settings.password.get_secret_value())
    login_page.click_login_button()
    
    yield  # Test runs here
    
    # Cleanup (if needed)
    driver.delete_all_cookies()

def test_dashboard_features(driver, json_env_config, logged_in_user):
    """Test that uses the logged_in_user fixture."""
    dashboard_page = DashboardPage(driver, json_env_config)
    assert dashboard_page.is_dashboard_title_displayed()
```

## Page Object Model

### Creating Page Objects

```python
import logging
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from orange_hrm.pages.base import BasePage
from orange_hrm.constants.json_env_config import ApplicationFields, TopKey

base_logger = logging.getLogger(__name__)
logger = logging.LoggerAdapter(base_logger, {"role": "EXAMPLE_PAGE"})

class ExamplePage:
    # Locators
    SUBMIT_BUTTON = (By.ID, "submit-btn")
    INPUT_FIELD = (By.NAME, "input-field")
    ERROR_MESSAGE = (By.CLASS_NAME, "error-message")
    
    def __init__(self, driver: WebDriver, env_config: dict):
        """Initialize page object."""
        self.driver = driver
        self.base_page = BasePage(driver, env_config)
        self.url = env_config[TopKey.APPLICATION.value][ApplicationFields.BASE_URL.value] + "/example"
    
    def navigate_to_page(self):
        """Navigate to the example page."""
        logger.info("Navigating to example page")
        self.driver.get(self.url)
    
    def enter_text(self, text: str):
        """Enter text into input field."""
        logger.info("Entering text into input field")
        self.base_page.enter_text(self.INPUT_FIELD, text)
    
    def click_submit(self):
        """Click the submit button."""
        logger.info("Clicking submit button")
        self.base_page.wait_for_element_clickable(self.SUBMIT_BUTTON).click()
    
    def get_error_message(self) -> str:
        """Get error message text."""
        logger.info("Getting error message")
        element = self.base_page.wait_for_element_visible(self.ERROR_MESSAGE)
        return element.text
    
    def is_submit_button_enabled(self) -> bool:
        """Check if submit button is enabled."""
        element = self.base_page.wait_for_element_visible(self.SUBMIT_BUTTON)
        return element.is_enabled()
```

### Using Base Page Methods

```python
class MyPage:
    def __init__(self, driver, env_config):
        self.base_page = BasePage(driver, env_config)
    
    def interact_with_element(self):
        # Wait for element to be visible
        element = self.base_page.wait_for_element_visible(self.LOCATOR)
        
        # Wait for element to be clickable
        clickable_element = self.base_page.wait_for_element_clickable(self.LOCATOR)
        
        # Enter text (with secret masking if needed)
        self.base_page.enter_text(self.INPUT_LOCATOR, "text", is_secret=False)
        self.base_page.enter_text(self.PASSWORD_LOCATOR, "password", is_secret=True)
        
        # Check if element is visible
        is_visible = self.base_page.is_element_visible(self.LOCATOR)
```

## Best Practices

### 1. Test Organization

```python
# Group related tests in classes
class TestLoginFunctionality:
    """Test suite for login functionality."""
    
    def test_valid_login(self, driver, json_env_config, env_settings):
        """Test login with valid credentials."""
        pass
    
    def test_invalid_login(self, driver, json_env_config):
        """Test login with invalid credentials."""
        pass
    
    @pytest.mark.parametrize("scenario", ["empty_username", "empty_password"])
    def test_validation_errors(self, driver, json_env_config, scenario):
        """Test various validation scenarios."""
        pass
```

### 2. Error Handling

```python
def test_with_error_handling(driver, json_env_config):
    """Test with proper error handling."""
    try:
        login_page = LoginPage(driver, json_env_config)
        login_page.navigate_to_login_page()
        
        # Test logic here
        
    except TimeoutException as e:
        logger.error(f"Timeout occurred: {e}")
        pytest.fail(f"Test failed due to timeout: {e}")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        # Take screenshot for debugging
        driver.save_screenshot("error_screenshot.png")
        raise
```

### 3. Data-Driven Testing

```python
# test_data.py
LOGIN_TEST_DATA = [
    {"username": "admin", "password": "admin123", "expected": "success"},
    {"username": "invalid", "password": "invalid", "expected": "error"},
]

# test_login.py
@pytest.mark.parametrize("test_data", LOGIN_TEST_DATA)
def test_login_scenarios(driver, json_env_config, test_data):
    """Data-driven login tests."""
    login_page = LoginPage(driver, json_env_config)
    
    login_page.navigate_to_login_page()
    login_page.enter_username(test_data["username"])
    login_page.enter_password(test_data["password"])
    login_page.click_login_button()
    
    if test_data["expected"] == "success":
        dashboard_page = DashboardPage(driver, json_env_config)
        assert dashboard_page.is_dashboard_title_displayed()
    else:
        assert login_page.is_error_message_displayed()
```



## Advanced Usage

### Custom Fixtures

```python
# conftest.py
@pytest.fixture(scope="session")
def test_data_manager():
    """Fixture for managing test data."""
    class TestDataManager:
        def get_user_data(self, user_type):
            # Load user data based on type
            return {"username": "test_user", "password": "test_pass"}
    
    return TestDataManager()

@pytest.fixture
def cleanup_test_data():
    """Fixture for cleaning up test data."""
    created_items = []
    
    def _add_item(item):
        created_items.append(item)
    
    yield _add_item
    
    # Cleanup after test
    for item in created_items:
        # Delete item logic
        pass
```

### Custom Wait Conditions

```python
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

class CustomConditions:
    """Custom wait conditions."""
    
    @staticmethod
    def element_text_contains(locator, text):
        """Wait for element text to contain specific text."""
        def _predicate(driver):
            element = driver.find_element(*locator)
            return text in element.text
        return _predicate
    
    @staticmethod
    def page_title_contains(title):
        """Wait for page title to contain specific text."""
        def _predicate(driver):
            return title in driver.title
        return _predicate

# Usage in page objects
def wait_for_success_message(self):
    """Wait for success message to appear."""
    wait = WebDriverWait(self.driver, 10)
    wait.until(CustomConditions.element_text_contains(
        self.SUCCESS_MESSAGE, "Success"
    ))
```

### Performance Testing

```python
import time

def test_page_load_performance(driver, json_env_config):
    """Test page load performance."""
    start_time = time.time()
    
    login_page = LoginPage(driver, json_env_config)
    login_page.navigate_to_login_page()
    
    load_time = time.time() - start_time
    
    # Assert page loads within acceptable time
    assert load_time < 5.0, f"Page load took {load_time:.2f}s, expected < 5.0s"
```

## Performance Monitoring

The framework includes built-in performance monitoring:

### Configuration

```json
// Environment configuration
{
    "performance": {
        "performance_threshold": 5  // seconds
    }
}
```

### Automatic Monitoring

```python
# Performance is automatically logged for:
# - Element wait operations
# - Page navigation
# - Form interactions

# Example log output:
# [INFO] [PERFORMANCE] Action 'wait_for_element_visible' took 1.23 seconds.
# [WARNING] [PERFORMANCE] Action 'page_load' took 6.45 seconds which exceeds the threshold of 5 seconds.
```

### Custom Performance Tracking

```python
import time
from orange_hrm.pages.base import BasePage

class MyPage(BasePage):
    def custom_operation(self):
        """Custom operation with performance tracking."""
        start_time = time.time()
        
        # Your operation here
        self.complex_operation()
        
        duration = time.time() - start_time
        self._log_performance("custom_operation", duration)
```

## Logging and Debugging

### Log Levels and Configuration

```python
# Logging is configured in pytest.ini
# Available log levels: DEBUG, INFO, WARNING, ERROR

# In test files
import logging

base_logger = logging.getLogger(__name__)
logger = logging.LoggerAdapter(base_logger, {"role": "TEST_NAME"})

def test_with_logging(driver, json_env_config):
    logger.debug("Starting test execution")
    logger.info("Navigating to login page")
    logger.warning("Unexpected behavior detected")
    logger.error("Test failed with error")
```

### Secret Masking

```python
# Secrets are automatically masked in logs
logger.info(f"Username: {username}")  # Shows actual username
logger.info(f"Password: {password}")  # Shows ********** if password is SecretStr

# Manual secret masking
from orange_hrm.pages.base import BasePage

base_page.enter_text(locator, "sensitive_data", is_secret=True)
# Log output: "Entered text '***************' [locator='...']"
```

### Debug Mode

```bash
# Run tests with debug logging
uv run pytest --log-cli-level=DEBUG

# Run with full tracebacks
uv run pytest --tb=long

# Run with PDB debugger on failure
uv run pytest --pdb
```

## CI/CD Integration

The Orange HRM Test Automation Framework includes comprehensive CI/CD support with automated testing, security scanning, and multi-environment deployment.

**📋 For complete CI/CD setup instructions, pipeline configuration, and platform-specific examples, see the [CI/CD Guide](CI_CD_GUIDE.md).**

### Quick CI/CD Commands

```bash
# Run tests as they would run in CI
uv run pytest --env=dev --headless --cov=src --cov-report=xml

# Run security scan
uv run bandit -r src/ -f json

# Run code quality checks
uv run ruff check src/ tests/
uv run ruff format --check src/ tests/
```

### Supported Platforms

- **GitHub Actions** (GitFlow Pipeline) - Primary CI/CD platform
- **GitLab CI/CD** - Full pipeline support
- **Jenkins** - Groovy pipeline configuration
- **Azure DevOps** - YAML pipeline support
- **CircleCI** - Docker-based workflows

---

**Next Steps**: 
- See [Troubleshooting Guide](TROUBLESHOOTING.md) for common issues
- Check [Contributing Guide](CONTRIBUTING.md) for development guidelines
- Review [ADRs](ADR/) for architectural decisions