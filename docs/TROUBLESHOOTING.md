# Troubleshooting Guide

> **Common issues and solutions for the Orange HRM Test Automation Framework**

## Table of Contents

- [Installation Issues](#installation-issues)
- [Configuration Problems](#configuration-problems)
- [Browser and WebDriver Issues](#browser-and-webdriver-issues)
- [Test Execution Problems](#test-execution-problems)
- [Environment and Dependencies](#environment-and-dependencies)
- [Performance Issues](#performance-issues)
- [CI/CD Pipeline Problems](#cicd-pipeline-problems)
- [Logging and Debugging](#logging-and-debugging)
- [Platform-Specific Issues](#platform-specific-issues)
- [Getting Help](#getting-help)

## Installation Issues

### Python Version Compatibility

**Problem**: `python: command not found` or version mismatch

**Solutions**:

```bash
# Check Python version
python --version
python3 --version

# If Python 3.13+ is not available:
# Windows: Download from python.org
# macOS: 
brew install python@3.13

# Linux (Ubuntu):
sudo apt update
sudo apt install python3.13 python3.13-venv

# Create alias if needed
alias python=python3.13
```

### uv Installation Problems

**Problem**: `uv: command not found`

**Solutions**:

```bash
# Windows PowerShell
irm https://astral.sh/uv/install.ps1 | iex

# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Alternative: Install via pip
pip install uv

# Verify installation
uv --version
```

**Problem**: Permission denied during uv installation

**Solutions**:

```bash
# Linux/macOS: Use user installation
curl -LsSf https://astral.sh/uv/install.sh | sh

# Add to PATH if needed
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc

# Windows: Run PowerShell as Administrator
```

### Dependency Installation Failures

**Problem**: `Failed to build` or `No module named 'xyz'`

**Solutions**:

```bash
# Clear cache and reinstall
uv cache clean
rm -rf .venv
uv sync

# For specific package issues
uv add package-name --force

# Check for system dependencies (Linux)
sudo apt install build-essential python3-dev

# macOS: Install Xcode command line tools
xcode-select --install
```

## Configuration Problems

### Environment Variables Not Loading

**Problem**: `ValidationError` for missing credentials

**Solutions**:

```bash
# 1. Check .env file exists and has correct format
cat .env
# Should contain:
# ORANGEHRM_USERNAME=Admin
# ORANGEHRM_PASSWORD=admin123

# 2. Verify file permissions
ls -la .env
chmod 600 .env  # Linux/macOS

# 3. Check for hidden characters
file .env
# Should show: ASCII text

# 4. Test configuration loading
uv run python -c "from orange_hrm.config.dotenv_config import get_dot_env_secrets; print(get_dot_env_secrets())"
```

**Problem**: Configuration validation errors

**Solutions**:

```python
# Debug configuration issues
from orange_hrm.config.dotenv_config import EnvConfig
from pydantic import ValidationError

try:
    config = EnvConfig()
    print("Configuration loaded successfully")
except ValidationError as e:
    print(f"Validation error: {e}")
    # Check specific field errors
    for error in e.errors():
        print(f"Field: {error['loc']}, Error: {error['msg']}")
```

### JSON Configuration Issues

**Problem**: `FileNotFoundError` for JSON config files

**Solutions**:

```bash
# 1. Verify JSON files exist
ls -la src/orange_hrm/config/
# Should show: dev.json, staging.json, prod.json

# 2. Check JSON syntax
python -m json.tool src/orange_hrm/config/dev.json

# 3. Verify package structure
uv run python -c "import orange_hrm.config; print(orange_hrm.config.__file__)"
```

**Problem**: Invalid JSON format

**Solutions**:

```bash
# Validate JSON files
for file in src/orange_hrm/config/*.json; do
    echo "Checking $file"
    python -m json.tool "$file" > /dev/null && echo "✓ Valid" || echo "✗ Invalid"
done

# Fix common JSON issues:
# - Remove trailing commas
# - Use double quotes for strings
# - Ensure proper nesting
```

## Browser and WebDriver Issues

### ChromeDriver Problems

**Problem**: `WebDriverException: 'chromedriver' executable needs to be in PATH`

**Solutions**:

```bash
# 1. Clear driver cache
rm -rf ./drivers
rm -rf ~/.cache/selenium

# 2. Set custom cache path
export SE_CACHE_PATH="$(pwd)/drivers"
mkdir -p drivers

# 3. Verify Chrome installation
# Windows: Check Program Files
# macOS: /Applications/Google Chrome.app
# Linux:
which google-chrome
google-chrome --version

# 4. Force driver download
uv run python -c "from selenium import webdriver; webdriver.Chrome()"
```

**Problem**: Chrome version mismatch

**Solutions**:

```bash
# 1. Update Chrome browser
# Windows: Chrome menu > Help > About Google Chrome
# macOS: Chrome menu > About Google Chrome
# Linux:
sudo apt update && sudo apt upgrade google-chrome-stable

# 2. Clear Selenium cache
rm -rf ~/.cache/selenium

# 3. Use specific Chrome options
```

```python
from selenium.webdriver.chrome.options import Options

options = Options()
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-gpu")
driver = webdriver.Chrome(options=options)
```

### Headless Mode Issues

**Problem**: Tests fail only in headless mode

**Solutions**:

```python
# Add headless-specific options
options = Options()
options.add_argument("--headless")
options.add_argument("--window-size=1920,1080")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
```

```bash
# Test with visible browser first
uv run pytest tests/test_login.py -v

# Then test headless
uv run pytest tests/test_login.py --headless -v
```

### Browser Crashes

**Problem**: Browser crashes during test execution

**Solutions**:

```python
# Add stability options
options = Options()
options.add_argument("--disable-extensions")
options.add_argument("--disable-plugins")
options.add_argument("--disable-images")
options.add_argument("--disable-javascript")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
```

```bash
# Increase system resources
# Linux: Increase shared memory
sudo mount -o remount,size=2G /dev/shm

# Monitor system resources during tests
top -p $(pgrep chrome)
```

## Test Execution Problems

### Timeout Errors

**Problem**: `TimeoutException` during element waits

**Solutions**:

```python
# 1. Increase timeout in configuration
# Edit src/orange_hrm/config/dev.json
{
    "webdriver": {
        "explicit_wait": 30  // Increase from 20
    }
}

# 2. Add custom waits
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

wait = WebDriverWait(driver, 30)
element = wait.until(EC.element_to_be_clickable(locator))

# 3. Debug element visibility
driver.save_screenshot("debug.png")
print(f"Page title: {driver.title}")
print(f"Current URL: {driver.current_url}")
```

**Problem**: Intermittent timeout failures

**Solutions**:

```python
# Add retry mechanism
import time
from selenium.common.exceptions import TimeoutException

def retry_operation(operation, max_attempts=3, delay=1):
    for attempt in range(max_attempts):
        try:
            return operation()
        except TimeoutException:
            if attempt == max_attempts - 1:
                raise
            time.sleep(delay)
            delay *= 2  # Exponential backoff

# Usage
retry_operation(lambda: login_page.click_login_button())
```

### Element Not Found Errors

**Problem**: `NoSuchElementException`

**Solutions**:

```python
# 1. Verify locator strategy
from selenium.webdriver.common.by import By

# Try different locator strategies
locators_to_try = [
    (By.ID, "element-id"),
    (By.NAME, "element-name"),
    (By.CLASS_NAME, "element-class"),
    (By.CSS_SELECTOR, ".element-class"),
    (By.XPATH, "//input[@placeholder='Username']"),
]

for locator in locators_to_try:
    try:
        element = driver.find_element(*locator)
        print(f"Found element with: {locator}")
        break
    except NoSuchElementException:
        continue

# 2. Wait for page to load completely
driver.implicitly_wait(10)
WebDriverWait(driver, 10).until(
    lambda d: d.execute_script("return document.readyState") == "complete"
)
```

### Test Data Issues

**Problem**: Tests fail due to invalid test data

**Solutions**:

```python
# 1. Validate test data before use
def validate_test_data(data):
    required_fields = ['username', 'password']
    for field in required_fields:
        if not data.get(field):
            raise ValueError(f"Missing required field: {field}")
    return data

# 2. Use data factories
class TestDataFactory:
    @staticmethod
    def create_valid_user():
        return {
            "username": "Admin",
            "password": "admin123"
        }
    
    @staticmethod
    def create_invalid_user():
        return {
            "username": "invalid_user",
            "password": "invalid_pass"
        }
```

## Environment and Dependencies

### Virtual Environment Issues

**Problem**: Wrong Python interpreter or packages not found

**Solutions**:

```bash
# 1. Verify virtual environment
which python
# Should point to .venv/bin/python or .venv\Scripts\python.exe

# 2. Recreate virtual environment
rm -rf .venv
uv sync

# 3. Activate manually if needed
source .venv/bin/activate  # Linux/macOS
.venv\Scripts\activate     # Windows

# 4. Verify packages
uv pip list
python -c "import selenium, pydantic, pytest; print('All imports successful')"
```

### Package Version Conflicts

**Problem**: Incompatible package versions

**Solutions**:

```bash
# 1. Check for conflicts
uv pip check

# 2. Update dependencies
uv sync --upgrade

# 3. Lock specific versions
# Edit pyproject.toml
[project]
dependencies = [
    "selenium==4.35.0",
    "pydantic==2.11.7",
    "pytest==8.4.1",
]

# 4. Clean install
uv cache clean
rm -rf .venv
uv sync
```

### Import Errors

**Problem**: `ModuleNotFoundError` for project modules

**Solutions**:

```bash
# 1. Verify PYTHONPATH
echo $PYTHONPATH
export PYTHONPATH="$(pwd):$PYTHONPATH"

# 2. Install in development mode
uv pip install -e .

# 3. Check package structure
find src -name "__init__.py"
# Should show __init__.py files in all package directories

# 4. Test imports
uv run python -c "from orange_hrm.config.dotenv_config import get_dot_env_secrets"
```

## Performance Issues

### Slow Test Execution

**Problem**: Tests running slower than expected

**Solutions**:

```bash
# 1. Profile test execution
uv run pytest --durations=10 -v

# 2. Use headless mode for faster execution
uv run pytest --headless

# 3. Optimize waits
# Reduce explicit_wait in config for faster environments
{
    "webdriver": {
        "explicit_wait": 10  // Reduce from 20
    }
}

# 4. Use headless mode
uv run pytest --headless
```

### Memory Issues

**Problem**: High memory usage or out-of-memory errors

**Solutions**:

```bash
# 1. Monitor memory usage
top -p $(pgrep python)

# 2. Limit parallel execution
uv run pytest -n 2  # Instead of -n auto

# 3. Add cleanup in tests
```

```python
@pytest.fixture
def driver(request):
    driver = webdriver.Chrome()
    yield driver
    try:
        driver.quit()
    except Exception:
        pass
    
    # Force cleanup
    import gc
    gc.collect()
```

### Network-Related Delays

**Problem**: Slow network causing test failures

**Solutions**:

```python
# 1. Add network wait conditions
from selenium.webdriver.support.ui import WebDriverWait

def wait_for_network_idle(driver, timeout=10):
    """Wait for network requests to complete."""
    WebDriverWait(driver, timeout).until(
        lambda d: d.execute_script(
            "return window.performance.timing.loadEventEnd > 0"
        )
    )

# 2. Increase timeouts for slow networks
# In config files, increase all timeout values

# 3. Add retry for network-dependent operations
```

## CI/CD Pipeline Problems

### GitHub Actions Failures

**Problem**: Tests pass locally but fail in GitHub Actions

**Solutions**:

```yaml
# 1. Add debugging steps
- name: Debug environment
  run: |
    echo "Python version: $(python --version)"
    echo "Chrome version: $(google-chrome --version)"
    echo "Working directory: $(pwd)"
    ls -la

# 2. Use specific Ubuntu version
runs-on: ubuntu-22.04  # Instead of ubuntu-latest

# 3. Add display for GUI tests
- name: Setup display
  run: |
    export DISPLAY=:99
    Xvfb :99 -screen 0 1024x768x24 > /dev/null 2>&1 &

# 4. Increase timeout
- name: Run tests
  timeout-minutes: 30
  run: uv run pytest --headless
```

### Docker Issues

**Problem**: Tests fail in Docker containers

**Solutions**:

```dockerfile
# Add necessary packages
RUN apt-get update && apt-get install -y \
    xvfb \
    x11vnc \
    fluxbox \
    wget \
    wmctrl

# Set display
ENV DISPLAY=:99

# Start Xvfb
RUN Xvfb :99 -screen 0 1024x768x24 > /dev/null 2>&1 &

# Add Chrome options for Docker
ENV CHROME_OPTIONS="--no-sandbox --disable-dev-shm-usage --headless"
```

### Permission Issues in CI

**Problem**: Permission denied errors in CI/CD

**Solutions**:

```bash
# 1. Fix file permissions
chmod +x scripts/*.sh
chmod 755 drivers/

# 2. Use non-root user in Docker
USER 1001:1001

# 3. Set proper ownership
chown -R $USER:$USER /app
```

## Logging and Debugging

### Log File Issues

**Problem**: Logs not being generated or incomplete

**Solutions**:

```bash
# 1. Check log directory permissions
mkdir -p reports/logs
chmod 755 reports/logs

# 2. Verify pytest.ini configuration
[pytest]
log_file = reports/logs/test.log
log_file_level = DEBUG
log_file_mode = w

# 3. Test logging manually
uv run python -c "
import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('test')
logger.info('Test log message')
"
```

### Debug Information

**Problem**: Need more debugging information

**Solutions**:

```python
# 1. Add debug fixtures
@pytest.fixture
def debug_on_failure(request):
    yield
    if request.node.rep_call.failed:
        # Take screenshot
        driver = request.getfixturevalue('driver')
        driver.save_screenshot(f"failure_{request.node.name}.png")
        
        # Save page source
        with open(f"failure_{request.node.name}.html", "w") as f:
            f.write(driver.page_source)
        
        # Log browser logs
        logs = driver.get_log('browser')
        print(f"Browser logs: {logs}")

# 2. Add verbose assertions
assert element.is_displayed(), f"""
Element not displayed:
- Locator: {locator}
- Page title: {driver.title}
- Current URL: {driver.current_url}
- Element text: {element.text if element else 'N/A'}
"""
```

## Platform-Specific Issues

### Windows Issues

**Problem**: Path separator issues

**Solutions**:

```python
# Use pathlib for cross-platform paths
from pathlib import Path

config_path = Path("src") / "orange_hrm" / "config" / "dev.json"
driver_path = Path.cwd() / "drivers"
```

**Problem**: PowerShell execution policy

**Solutions**:

```powershell
# Set execution policy
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Or run specific command
PowerShell -ExecutionPolicy Bypass -File script.ps1
```

### macOS Issues

**Problem**: Permission issues with ChromeDriver

**Solutions**:

```bash
# Allow ChromeDriver to run
xattr -d com.apple.quarantine /path/to/chromedriver

# Or use Homebrew Chrome
brew install --cask google-chrome
```

### Linux Issues

**Problem**: Display issues in headless environments

**Solutions**:

```bash
# Install virtual display
sudo apt-get install xvfb

# Start virtual display
export DISPLAY=:99
Xvfb :99 -screen 0 1024x768x24 > /dev/null 2>&1 &

# Or use in tests
from pyvirtualdisplay import Display
display = Display(visible=0, size=(1024, 768))
display.start()
```

## Getting Help

### Diagnostic Information

When reporting issues, include:

```bash
# System information
uname -a
python --version
uv --version
google-chrome --version

# Project information
uv pip list
ls -la src/orange_hrm/config/

# Test execution with verbose output
uv run pytest tests/test_login.py -v --tb=long
```

### Creating Bug Reports

**Include the following information**:

1. **Environment Details**:
   - Operating system and version
   - Python version
   - Browser version
   - Package versions (`uv pip list`)

2. **Steps to Reproduce**:
   - Exact commands run
   - Configuration files used
   - Test files involved

3. **Error Information**:
   - Complete error messages
   - Stack traces
   - Log files
   - Screenshots (if applicable)

4. **Expected vs Actual Behavior**:
   - What you expected to happen
   - What actually happened

### Support Channels

1. **GitHub Issues**: [Create an issue](https://github.com/Next-Wave-Code/OrangeHRM_Test_Automation_web/issues)
2. **Documentation**: Check [project documentation](../README.md)
3. **Email Support**: next.wavecode@gmail.com

### Self-Help Checklist

Before seeking help, try:

- [ ] Check this troubleshooting guide
- [ ] Search existing GitHub issues
- [ ] Verify your environment setup
- [ ] Test with a minimal example
- [ ] Check for recent changes in your code
- [ ] Try running tests in isolation
- [ ] Clear caches and reinstall dependencies

---

**Remember**: Most issues are environment-related. When in doubt, try recreating your virtual environment and reinstalling dependencies.