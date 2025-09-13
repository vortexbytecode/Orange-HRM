# Contributing Guide

> **Guidelines for contributing to the Orange HRM Test Automation Framework**

## Table of Contents

- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Code Standards](#code-standards)
- [Testing Guidelines](#testing-guidelines)
- [Documentation Standards](#documentation-standards)
- [Pull Request Process](#pull-request-process)
- [Issue Reporting](#issue-reporting)
- [Architecture Decisions](#architecture-decisions)
- [Release Process](#release-process)
- [Community Guidelines](#community-guidelines)

## Getting Started

### Prerequisites

Before contributing, ensure you have:

- **Python 3.13+** installed
- **Git** configured with your GitHub account
- **uv** package manager installed
- **Chrome browser** for testing
- **IDE** with Python support (VS Code, PyCharm recommended)

### First-Time Setup

```bash
# 1. Fork the repository on GitHub
# 2. Clone your fork
git clone https://github.com/YOUR_USERNAME/OrangeHRM_Test_Automation_web.git
cd orange-hrm

# 3. Add upstream remote
git remote add upstream https://github.com/Next-Wave-Code/OrangeHRM_Test_Automation_web.git

# 4. Install dependencies
uv sync



# 6. Create environment file
cp .env.example .env
# Edit .env with your credentials
```

### Development Workflow

```bash
# 1. Create a feature branch
git checkout -b feature/your-feature-name

# 2. Make your changes
# ... code, test, document ...

# 3. Run tests
uv run pytest

# 4. Commit your changes
git add .
git commit -m "feat: add new feature description"

# 5. Push to your fork
git push origin feature/your-feature-name

# 6. Create a Pull Request on GitHub
```

## Development Setup

### IDE Configuration

#### Visual Studio Code

Recommended extensions and settings:

```json
// .vscode/extensions.json
{
    "recommendations": [
        "ms-python.python",
        "ms-python.black-formatter",
        "ms-python.isort",
        "ms-python.pylint",
        "charliermarsh.ruff",
        "ms-python.pytest",
        "ms-python.mypy-type-checker"
    ]
}
```

```json
// .vscode/settings.json
{
    "python.defaultInterpreterPath": "./.venv/bin/python",
    "python.testing.pytestEnabled": true,
    "python.testing.pytestArgs": ["tests"],
    "python.linting.enabled": true,
    "python.linting.pylintEnabled": true,
    "python.formatting.provider": "black",
    "python.sortImports.args": ["--profile", "black"],
    "editor.formatOnSave": true,
    "editor.codeActionsOnSave": {
        "source.organizeImports": true
    },
    "files.exclude": {
        "**/__pycache__": true,
        "**/.pytest_cache": true,
        "**/reports": true,
        "**/.coverage": true
    }
}
```

#### PyCharm

1. **Configure Interpreter**: File → Settings → Project → Python Interpreter
2. **Enable pytest**: File → Settings → Tools → Python Integrated Tools
3. **Code Style**: File → Settings → Editor → Code Style → Python
   - Set line length to 88 (Black standard)
   - Enable "Optimize imports on the fly"

### Development Dependencies

```bash
# Install development dependencies
uv sync --group dev

# Or add individual tools as needed
# uv add --group dev black isort pylint mypy
```

## Code Standards

### Python Style Guide

We follow **PEP 8** with these specific guidelines:

#### Formatting

- **Line Length**: 88 characters (Black standard)
- **Indentation**: 4 spaces (no tabs)
- **Quotes**: Double quotes for strings, single quotes for string literals in code
- **Imports**: Organized using isort with Black profile

#### Code Formatting Tools (Optional)

```bash
# These tools can be added to your project as needed:
# uv add --group dev black isort pylint mypy

# Format code with Black (if installed)
# uv run black src/ tests/

# Sort imports with isort (if installed)
# uv run isort src/ tests/ --profile black

# Lint with pylint (if installed)
# uv run pylint src/ tests/

# Type checking with mypy (if installed)
# uv run mypy src/
```

#### Naming Conventions

```python
# Classes: PascalCase
class LoginPage:
    pass

# Functions and variables: snake_case
def get_user_credentials():
    user_name = "admin"
    return user_name

# Constants: UPPER_SNAKE_CASE
DEFAULT_TIMEOUT = 30
MAX_RETRY_ATTEMPTS = 3

# Private methods: leading underscore
def _internal_helper_method(self):
    pass

# Test methods: descriptive names
def test_login_with_valid_credentials_should_redirect_to_dashboard():
    pass
```

### Documentation Standards

#### Docstrings

Use **NumPy style** docstrings:

```python
def wait_for_element_visible(self, locator: tuple, timeout: int = 10) -> WebElement:
    """
    Wait for element to be visible on the page.

    Parameters
    ----------
    locator : tuple
        Element locator in format (By.TYPE, "value")
    timeout : int, optional
        Maximum time to wait in seconds, by default 10

    Returns
    -------
    WebElement
        The visible element

    Raises
    ------
    TimeoutException
        If element is not visible within timeout period

    Examples
    --------
    >>> login_button = (By.ID, "login-btn")
    >>> element = page.wait_for_element_visible(login_button, timeout=15)
    """
    # Implementation here
```

#### Type Hints

Always use type hints:

```python
from typing import Dict, List, Optional, Union
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement

def process_test_results(
    results: List[Dict[str, Union[str, int]]], 
    driver: WebDriver
) -> Optional[WebElement]:
    """Process test results and return element if found."""
    pass
```

### Error Handling

#### Exception Handling Patterns

```python
# Good: Specific exception handling with logging
def click_element(self, locator: tuple) -> None:
    """Click element with proper error handling."""
    try:
        element = self.wait_for_element_clickable(locator)
        element.click()
        logger.info(f"Successfully clicked element: {locator}")
    except TimeoutException as e:
        logger.error(f"Timeout waiting for element {locator}: {e}")
        self.driver.save_screenshot("timeout_error.png")
        raise
    except WebDriverException as e:
        logger.error(f"WebDriver error clicking element {locator}: {e}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error clicking element {locator}: {e}")
        raise

# Bad: Generic exception handling
def click_element_bad(self, locator: tuple) -> None:
    try:
        element = self.driver.find_element(*locator)
        element.click()
    except Exception:
        pass  # Silent failure - never do this!
```

#### Custom Exceptions

```python
# Define custom exceptions for domain-specific errors
class PageLoadError(Exception):
    """Raised when a page fails to load properly."""
    pass

class ElementNotInteractableError(Exception):
    """Raised when an element cannot be interacted with."""
    pass

class ConfigurationError(Exception):
    """Raised when configuration is invalid or missing."""
    pass
```

## Testing Guidelines

### Test Structure

#### Test Organization

```
tests/
├── conftest.py              # Shared fixtures
├── test_login.py           # Login functionality tests
├── integration/            # Integration tests (future)
│   └── test_full_workflow.py
├── unit/                   # Unit tests (future)
│   └── test_config.py
└── data/                   # Test data files (future)
    └── test_users.json
```

#### Test Naming

```python
# Pattern: test_[action]_[condition]_[expected_result]
def test_login_with_valid_credentials_should_redirect_to_dashboard():
    """Test that valid login redirects to dashboard."""
    pass

def test_login_with_invalid_password_should_show_error_message():
    """Test that invalid password shows appropriate error."""
    pass

def test_form_submission_with_empty_required_field_should_prevent_submission():
    """Test that empty required fields prevent form submission."""
    pass
```

#### Test Categories and Parameterization

```python
# Use parameterized tests for multiple scenarios
@pytest.mark.parametrize("username,password,expected", [
    ("valid_user", "valid_pass", "success"),
    ("invalid_user", "invalid_pass", "error"),
])
def test_login_scenarios(username, password, expected):
    """Parameterized test for multiple login scenarios."""
    pass
```

### Test Quality Standards

#### Test Independence

```python
# Good: Independent test with proper setup/teardown
def test_user_can_update_profile(driver, json_env_config, logged_in_user):
    """Test user profile update functionality."""
    profile_page = ProfilePage(driver, json_env_config)
    
    # Test-specific setup
    original_name = profile_page.get_current_name()
    new_name = "Updated Name"
    
    # Test action
    profile_page.update_name(new_name)
    
    # Assertion
    assert profile_page.get_current_name() == new_name
    
    # Cleanup (if needed)
    profile_page.update_name(original_name)

# Bad: Test depends on previous test state
def test_dependent_on_previous_test():
    # Assumes previous test left user logged in
    dashboard_page = DashboardPage(driver, config)
    assert dashboard_page.is_user_logged_in()  # May fail if run in isolation
```

#### Assertions

```python
# Good: Descriptive assertions with custom messages
assert login_page.is_error_message_displayed(), \
    f"Expected error message to be displayed after invalid login attempt"

assert dashboard_page.get_welcome_message() == f"Welcome, {username}!", \
    f"Welcome message should contain username '{username}'"

# Good: Multiple specific assertions
def test_form_validation():
    form_page.submit_empty_form()
    
    assert form_page.is_username_error_displayed(), "Username error should be shown"
    assert form_page.is_password_error_displayed(), "Password error should be shown"
    assert not form_page.is_form_submitted(), "Form should not be submitted with errors"

# Bad: Generic assertions without context
assert element.is_displayed()  # What element? Why should it be displayed?
assert result == True  # What result? What does True mean here?
```

### Test Data Management

```python
# test_data.py - Centralized test data
class TestData:
    VALID_USERS = {
        "admin": {"username": "Admin", "password": "admin123"},
        "hr_user": {"username": "hr_user", "password": "hr_pass"}
    }
    
    INVALID_CREDENTIALS = [
        {"username": "invalid", "password": "invalid", "error": "Invalid credentials"},
        {"username": "", "password": "password", "error": "Username is required"},
        {"username": "username", "password": "", "error": "Password is required"}
    ]

# Usage in tests
@pytest.mark.parametrize("user_data", TestData.INVALID_CREDENTIALS)
def test_login_validation(driver, json_env_config, user_data):
    login_page = LoginPage(driver, json_env_config)
    
    login_page.login(user_data["username"], user_data["password"])
    
    assert login_page.get_error_message() == user_data["error"]
```

## Documentation Standards

### Code Documentation

#### Module Documentation

```python
"""
Login Page Module.

This module contains the LoginPage class which provides methods for interacting
with the Orange HRM login page. It follows the Page Object Model pattern and
includes comprehensive error handling and logging.

Example:
    >>> from orange_hrm.pages.login import LoginPage
    >>> login_page = LoginPage(driver, config)
    >>> login_page.login("username", "password")

Author: Your Name
Date: 2024-01-01
"""
```

#### Class Documentation

```python
class LoginPage:
    """
    Page Object Model for Orange HRM login page.
    
    This class encapsulates all interactions with the login page,
    providing a clean interface for test methods.
    
    Attributes
    ----------
    driver : WebDriver
        Selenium WebDriver instance
    base_page : BasePage
        Base page functionality
    url : str
        Login page URL
    
    Examples
    --------
    >>> login_page = LoginPage(driver, config)
    >>> login_page.navigate_to_login_page()
    >>> login_page.login("admin", "password")
    """
```

### README and Documentation Files

#### Structure Requirements

1. **Clear Purpose**: What the component/feature does
2. **Prerequisites**: What's needed to use it
3. **Installation/Setup**: Step-by-step instructions
4. **Usage Examples**: Practical examples
5. **API Reference**: Detailed parameter descriptions
6. **Troubleshooting**: Common issues and solutions

#### Markdown Standards

```markdown
# Use H1 for main title only
## Use H2 for major sections
### Use H3 for subsections

<!-- Use code blocks with language specification -->
```python
def example_function():
    return "Hello, World!"
```

<!-- Use tables for structured information -->
| Parameter | Type | Description | Default |
|-----------|------|-------------|----------|
| timeout   | int  | Wait time   | 10      |

<!-- Use callouts for important information -->
> **Note**: This is an important note

> **Warning**: This is a warning

<!-- Use proper linking -->
See the [Setup Guide](SETUP.md) for installation instructions.
```

## Pull Request Process

### Before Creating a PR

1. **Sync with upstream**:
   ```bash
   git fetch upstream
   git checkout main
   git merge upstream/main
   git push origin main
   ```

2. **Run full test suite**:
   ```bash
   uv run pytest --cov=src --cov-report=html
   ```

3. **Check code quality** (if tools are installed):
   ```bash
   # Only run if you have these tools installed:
   # uv run black src/ tests/
   # uv run isort src/ tests/ --profile black
   # uv run pylint src/ tests/
   # uv run mypy src/
   ```

4. **Update documentation** if needed

### PR Requirements

#### PR Title Format

Use [Conventional Commits](https://www.conventionalcommits.org/) format:

```
type(scope): description

Examples:
feat(login): add remember me functionality
fix(config): resolve environment variable loading issue
docs(readme): update installation instructions
test(login): add edge case tests for password validation
refactor(base): improve error handling in BasePage
```

#### PR Description Template

```markdown
## Description
Brief description of changes made.

## Type of Change
- [ ] Bug fix (non-breaking change which fixes an issue)
- [ ] New feature (non-breaking change which adds functionality)
- [ ] Breaking change (fix or feature that would cause existing functionality to not work as expected)
- [ ] Documentation update
- [ ] Refactoring (no functional changes)
- [ ] Performance improvement

## Testing
- [ ] All existing tests pass
- [ ] New tests added for new functionality
- [ ] Manual testing completed
- [ ] Cross-browser testing (if applicable)

## Screenshots (if applicable)
[Add screenshots here]

## Checklist
- [ ] Code follows project style guidelines
- [ ] Self-review completed
- [ ] Code is commented where necessary
- [ ] Documentation updated
- [ ] No new warnings introduced
- [ ] Tests added/updated as needed

## Related Issues
Closes #[issue_number]
Related to #[issue_number]
```

### Review Process

1. **Automated Checks**: All CI checks must pass
2. **Code Review**: At least one maintainer approval required
3. **Testing**: Reviewer should test the changes locally
4. **Documentation**: Ensure documentation is updated

### Merge Requirements

- ✅ All CI checks passing
- ✅ At least 1 approving review from maintainer
- ✅ No merge conflicts
- ✅ Branch is up-to-date with main
- ✅ All conversations resolved

## Issue Reporting

### Bug Reports

Use the bug report template:

```markdown
**Bug Description**
A clear description of what the bug is.

**Steps to Reproduce**
1. Go to '...'
2. Click on '....'
3. Scroll down to '....'
4. See error

**Expected Behavior**
What you expected to happen.

**Actual Behavior**
What actually happened.

**Environment**
- OS: [e.g. Windows 11, macOS 12, Ubuntu 22.04]
- Python Version: [e.g. 3.13.0]
- Browser: [e.g. Chrome 120.0]
- Framework Version: [e.g. 1.0.0]

**Additional Context**
- Error messages
- Screenshots
- Log files
- Configuration files (remove sensitive data)
```

### Feature Requests

```markdown
**Feature Description**
A clear description of the feature you'd like to see.

**Problem Statement**
What problem does this feature solve?

**Proposed Solution**
Describe your preferred solution.

**Alternative Solutions**
Describe alternatives you've considered.

**Additional Context**
Any other context, mockups, or examples.
```

## Architecture Decisions

### ADR Process

For significant architectural changes:

1. **Create ADR**: Use the template in `docs/ADR/`
2. **Discuss**: Open issue for discussion
3. **Review**: Get feedback from maintainers
4. **Implement**: Create PR with implementation
5. **Update**: Update ADR status to "Accepted"

### ADR Template

```markdown
# ADR XXXX — Title

- Date: YYYY-MM-DD
- Status: [Proposed|Accepted|Rejected|Superseded]
- Deciders: [List of people involved]
- Related: [Links to related files/ADRs]

## Context
What is the issue that we're seeing that is motivating this decision or change?

## Decision
What is the change that we're proposing or have agreed to implement?

## Rationale
Why are we making this decision? What are the benefits?

## Alternatives Considered
What other options did we consider?

## Consequences
What becomes easier or more difficult to do and any risks introduced by this change?
```

## Release Process

### Version Numbering

We use [Semantic Versioning](https://semver.org/):

- **MAJOR**: Breaking changes
- **MINOR**: New features (backward compatible)
- **PATCH**: Bug fixes (backward compatible)

Examples:
- `1.0.0` → `1.0.1` (bug fix)
- `1.0.1` → `1.1.0` (new feature)
- `1.1.0` → `2.0.0` (breaking change)

### Release Checklist

- [ ] All tests passing
- [ ] Documentation updated
- [ ] CHANGELOG.md updated
- [ ] Version bumped in `pyproject.toml`
- [ ] Git tag created
- [ ] Release notes prepared

## Community Guidelines

### Code of Conduct

We are committed to providing a welcoming and inclusive environment. Please:

- **Be respectful** in all interactions
- **Be constructive** in feedback and criticism
- **Be collaborative** and help others learn
- **Be patient** with newcomers and questions

### Communication

- **GitHub Issues**: For bug reports and feature requests
- **Pull Requests**: For code discussions
- **Email**: next.wavecode@gmail.com for private matters

### Recognition

Contributors are recognized in:
- `CONTRIBUTORS.md` file
- Release notes
- Project documentation

---

## Quick Reference

### Common Commands

```bash
# Setup
uv sync
cp .env.example .env

# Development
uv run pytest                    # Run tests
uv run pytest --cov=src        # Run with coverage
# uv run black src/ tests/      # Format code (if installed)
# uv run pylint src/            # Lint code (if installed)

# Git workflow
git checkout -b feature/name    # Create feature branch
git add .
git commit -m "feat: description"
git push origin feature/name    # Push to fork
```

### Getting Help

- 📖 **Documentation**: [README.md](../README.md)
- 🐛 **Issues**: [GitHub Issues](https://github.com/Next-Wave-Code/OrangeHRM_Test_Automation_web/issues)
- 💬 **Discussions**: [GitHub Discussions](https://github.com/Next-Wave-Code/OrangeHRM_Test_Automation_web/discussions)
- 📧 **Email**: next.wavecode@gmail.com

---

**Thank you for contributing to the Orange HRM Test Automation Framework!** 🎉