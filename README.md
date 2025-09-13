# Orange HRM Test Automation Framework

[![GitFlow CI/CD](https://github.com/Next-Wave-Code/OrangeHRM_Test_Automation_web/actions/workflows/gitflow-ci.yml/badge.svg)](https://github.com/Next-Wave-Code/OrangeHRM_Test_Automation_web/actions/workflows/gitflow-ci.yml) [![codecov](https://codecov.io/github/Next-Wave-Code/OrangeHRM_Test_Automation_web/graph/badge.svg?token=T20N42NZLF)](https://codecov.io/github/Next-Wave-Code/OrangeHRM_Test_Automation_web) [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT) [![Python 3.13+](https://img.shields.io/badge/python-3.13+-blue.svg)](https://www.python.org/downloads/) [![Selenium](https://img.shields.io/badge/selenium-4.35.0+-green.svg)](https://selenium-python.readthedocs.io/) [![Pydantic](https://img.shields.io/badge/pydantic-2.11.7+-red.svg)](https://pydantic-docs.helpmanual.io/) [![uv](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json)](https://github.com/astral-sh/uv)

> **Enterprise-grade test automation framework for Orange HRM web application testing, built with Python, Selenium, and modern configuration management practices.**

## 🚀 Overview

This comprehensive test automation framework provides robust, scalable, and maintainable testing solutions for the Orange HRM web application. Built following enterprise best practices, it features advanced configuration management, comprehensive logging, performance monitoring, and a clean Page Object Model architecture.

### Key Features

- **🏗️ Page Object Model Architecture** - Clean separation of concerns with reusable page components
- **🔐 Secure Configuration Management** - Pydantic-based settings with SecretStr for credential handling
- **📊 Comprehensive Logging System** - Multi-level logging with role-based adapters and secret masking
- **⚡ Performance Monitoring** - Built-in performance tracking with configurable thresholds
- **🛡️ Robust Error Handling** - Comprehensive exception handling with detailed diagnostics
- **🌍 Multi-Environment Support** - Environment-specific configurations (dev/staging/prod)
- **🔄 GitFlow CI/CD Pipeline** - Automated testing with code quality, security scans, and E2E tests
- **📈 Test Coverage & Reporting** - Integrated coverage reporting and test analytics
- **🚀 Modern Tooling** - Built with `uv` for fast dependency management and `ruff` for code quality

## 📋 Prerequisites

- **Python**: 3.13 or higher
- **Operating System**: Windows 11 (tested), Linux, macOS
- **Browser**: Chrome (ChromeDriver managed automatically)
- **Package Manager**: [uv](https://github.com/astral-sh/uv) (recommended) or pip

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/Next-Wave-Code/OrangeHRM_Test_Automation_web.git
cd orange-hrm
```

### 2. Environment Setup

#### Using uv (Recommended)

```bash
# Install uv if not already installed (Windows)
winget install --id=astral-sh.uv  -e

# Or using PowerShell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"

# Install dependencies
uv sync
```

#### Using pip (Alternative)

```bash
# Create virtual environment
python -m venv .venv

# Activate virtual environment
# Windows
.venv\Scripts\activate
# Linux/macOS
source .venv/bin/activate

# Install dependencies
pip install -e .
```

### 3. Configuration

```bash
# Copy environment template
cp .env.example .env

# Edit .env file with your credentials
# ORANGEHRM_USERNAME=your-username
# ORANGEHRM_PASSWORD=your-password
```

### 4. Run Tests

```bash
# Run all tests
uv run pytest

# Run with specific environment
uv run pytest --env=staging

# Run with coverage
uv run pytest --cov=src --cov-report=html

# Run specific test file
uv run pytest tests/test_login.py
```

## 📁 Project Structure

```
orange-hrm/
├── .github/                                    # GitHub configuration
│   └── workflows/
│       └── gitflow-ci.yml                      # GitFlow CI/CD pipeline
├── docs/                                       # Documentation
│   ├── ADR/                                    # Architecture Decision Records
│   │   ├── 0001-use-pydantic-for-secrets.md
│   │   └── 0002-json-configs-for-non-secrets.md
│   ├── CI_CD_GUIDE.md                          # CI/CD setup and configuration
│   ├── SETUP.md                                # Detailed setup instructions
│   ├── USAGE.md                                # Usage examples and guides
│   ├── TROUBLESHOOTING.md                      # Common issues and solutions
│   └── CONTRIBUTING.md                         # Contribution guidelines
├── src/orange_hrm/                             # Source code
│   ├── config/                                 # Configuration management
│   │   ├── dev.json                            # Development environment config
│   │   ├── staging.json                        # Staging environment config
│   │   ├── prod.json                           # Production environment config
│   │   └── dotenv_config.py                    # Pydantic settings for secrets
│   ├── constants/                              # Application constants
│   │   └── json_env_config.py                  # Configuration enums
│   └── pages/                                  # Page Object Model
│       ├── base.py                             # Base page class
│       ├── login.py                            # Login page implementation
│       └── dashboard.py                        # Dashboard page implementation
├── tests/                                      # Test suite
│   ├── conftest.py                             # Pytest configuration and fixtures
│   └── test_login.py                           # Login functionality tests
├── .env.example                                # Environment variables template
├── pytest.ini                                  # Pytest configuration
├── pyproject.toml                              # Project dependencies and metadata
└── README.md                                   # This file
```

## 🔧 Configuration Management

The framework uses a dual configuration system designed for enterprise environments:

### Secret Management [(ADR 0001)](docs/ADR/0001-use-pydantic-for-secrets.md)
- **Pydantic Settings** with `SecretStr` for credential handling
- **Environment Variables** or `.env` file support
- **Automatic Validation** with fail-fast behavior
- **Secret Masking** in logs and error messages
- **Priority Order**: Direct instantiation > Environment variable > .env file > Secrets dir > Default in model > Error

### Application Settings [(ADR 0002)](docs/ADR/0002-json-configs-for-non-secrets.md)
- **Environment-specific JSON files** (dev/staging/prod)
- **Type-safe configuration** using Python Enums
- **Session-scoped caching** for optimal performance with pytest fixtures
- **CLI-based environment selection** (`--env` flag)

## 🧪 Testing

### Running Tests

```bash
# Basic test execution
uv run pytest

# Environment-specific testing
uv run pytest --env=dev          # Development (default)
uv run pytest --env=staging      # Staging environment
uv run pytest --env=prod         # Production environment

# Headless mode
uv run pytest --headless

# Verbose output
uv run pytest -v

# Coverage reporting
uv run pytest --cov=src --cov-report=html:reports/coverage
```

## 📊 Reporting & Monitoring

### Test Reports
- **HTML Coverage Reports**: `reports/coverage/index.html`
- **Test Logs**: `reports/logs/test.log`
- **Performance Metrics**: Integrated threshold monitoring

### Logging Configuration
- **Multi-level Logging**: DEBUG, INFO, WARNING, ERROR, CRITICAL
- **Role-based Adapters**: Component-specific log formatting
- **Secret Masking**: Automatic credential protection
- **File & Console Output**: Configurable log destinations

## 🏗️ Architecture

### Architectural Principles
- **Separation of Concerns**: Clear boundaries between configuration, page objects, and test logic
- **Dependency Injection**: Configuration and WebDriver instances injected via pytest fixtures
- **Composition over Inheritance**: Page objects compose BasePage functionality rather than inheriting
- **Fail-Fast Design**: Early validation and error detection with comprehensive logging

### Design Patterns
- **Page Object Model**: Encapsulated page interactions with locator management and business logic separation
- **Template Method Pattern**: BasePage defines common interaction templates, pages implement specific behaviors
- **Adapter Pattern**: LoggerAdapter provides role-based logging context
- **Configuration Strategy**: Environment-specific JSON configurations with runtime selection
- **Caching Pattern**: LRU cache for configuration objects (`@lru_cache(maxsize=1)`)

### Key Components
- **BasePage**: Foundation class providing common web interaction methods, performance monitoring, and error handling
- **EnvConfig**: Pydantic-based secret management with SecretStr and field validation
- **Configuration Layer**: Dual configuration system (secrets via Pydantic, settings via JSON)
- **Fixture System**: Pytest-based dependency injection for WebDriver, configuration, and test data
- **Logging Infrastructure**: Role-based logging with automatic secret masking and performance tracking

### Configuration Architecture
- **Secrets Management**: Environment variables → .env file → Pydantic validation → SecretStr masking
- **Application Settings**: CLI selection → JSON file loading → Enum-based type safety → Session caching
- **Environment Isolation**: Separate configuration files per environment (dev/staging/prod)
- **Priority Chain**: Direct instantiation > Environment variable > .env file > Default values > Validation error

## 🔒 Security

- **Secret Management**: Pydantic SecretStr with automatic masking
- **Environment Isolation**: Separate configurations per environment
- **Credential Validation**: Fail-fast validation for missing secrets
- **Log Security**: Automatic secret redaction in all outputs

## 🚀 CI/CD Integration

The project includes a comprehensive **GitFlow CI/CD Pipeline** with automated testing, code quality checks, security scanning, and multi-environment deployment.

**📋 For complete CI/CD setup instructions, configuration details, and troubleshooting, see the [CI/CD Guide](docs/CI_CD_GUIDE.md).**

### Quick Overview

- **🔄 GitFlow Integration**: Automated workflows for all GitFlow branches
- **⚡ Fast Execution**: Parallel jobs with intelligent caching
- **🛡️ Security First**: Integrated vulnerability scanning
- **📊 Comprehensive Reporting**: Coverage, test results, and artifacts
- **🌍 Multi-Platform**: GitHub Actions, GitLab CI, Jenkins support

## 📚 Documentation

- **[Setup Guide](docs/SETUP.md)**: Detailed installation and configuration
- **[Usage Guide](docs/USAGE.md)**: Examples and best practices
- **[Troubleshooting](docs/TROUBLESHOOTING.md)**: Common issues and solutions
- **[Contributing](docs/CONTRIBUTING.md)**: Development guidelines
- **[ADRs](docs/ADR/)**: Architecture decision records

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](docs/CONTRIBUTING.md) for details on:

- Code style and standards
- Testing requirements
- Pull request process
- Development setup

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

- **Issues**: [GitHub Issues](https://github.com/Next-Wave-Code/OrangeHRM_Test_Automation_web/issues)
- **Documentation**: [Project Wiki](https://github.com/Next-Wave-Code/OrangeHRM_Test_Automation_web/wiki)
- **Email**: next.wavecode@gmail.com

## 🏆 Acknowledgments

- **Orange HRM**: For providing the demo application
- **Selenium**: For web automation capabilities
- **Pydantic**: For configuration management
- **Pytest**: For testing framework
- **uv**: For modern Python package management

---

**Built with ❤️ by [Next Wave Code](https://github.com/Next-Wave-Code)**