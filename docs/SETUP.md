# Setup Guide

> **Comprehensive setup instructions for the Orange HRM Test Automation Framework**

## Table of Contents

- [System Requirements](#system-requirements)
- [Installation Methods](#installation-methods)
- [Environment Configuration](#environment-configuration)
- [Browser Setup](#browser-setup)
- [Verification](#verification)
- [IDE Configuration](#ide-configuration)
- [Docker Setup](#docker-setup)
- [Troubleshooting](#troubleshooting)

## System Requirements

### Minimum Requirements

| Component | Requirement | Recommended |
|-----------|-------------|-------------|
| **Python** | 3.13+ | 3.13+ |
| **RAM** | 4GB | 8GB+ |
| **Storage** | 2GB free space | 5GB+ |
| **OS** | Windows 10+, macOS 10.15+, Ubuntu 18.04+ | Windows 11, macOS 12+, Ubuntu 22.04+ |
| **Browser** | Chrome 120+ | Chrome Latest |

### Supported Platforms

- ✅ **Windows 11** (Primary development platform)
- ✅ **Windows 10** (Tested)
- ✅ **macOS** (Intel & Apple Silicon)
- ✅ **Linux** (Ubuntu, CentOS, RHEL)

## Installation Methods

### Method 1: Using uv (Recommended)

[uv](https://github.com/astral-sh/uv) is a fast Python package manager that provides better dependency resolution and faster installations.

#### Step 1: Install uv

**Windows (PowerShell):**
```powershell
# Using PowerShell
irm https://astral.sh/uv/install.ps1 | iex

# Or using Scoop
scoop install uv

# Or using Chocolatey
choco install uv
```

**macOS:**
```bash
# Using Homebrew
brew install uv

# Or using curl
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**Linux:**
```bash
# Using curl
curl -LsSf https://astral.sh/uv/install.sh | sh

# Or using pip
pip install uv
```

#### Step 2: Clone and Setup Project

```bash
# Clone the repository
git clone https://github.com/Next-Wave-Code/OrangeHRM_Test_Automation_web.git
cd orange-hrm

# Install dependencies and create virtual environment
uv sync

# Activate the virtual environment (if needed)
source .venv/bin/activate  # Linux/macOS
# or
.venv\Scripts\activate     # Windows
```

### Method 2: Using pip (Traditional)

#### Step 1: Verify Python Installation

```bash
# Check Python version
python --version
# Should output: Python 3.13.x or higher

# If python command doesn't work, try:
python3 --version
```

#### Step 2: Clone Repository

```bash
git clone https://github.com/Next-Wave-Code/OrangeHRM_Test_Automation_web.git
cd orange-hrm
```

#### Step 3: Create Virtual Environment

```bash
# Create virtual environment
python -m venv .venv

# Activate virtual environment
# Windows
.venv\Scripts\activate

# macOS/Linux
source .venv/bin/activate
```

#### Step 4: Install Dependencies

```bash
# Upgrade pip
pip install --upgrade pip

# Install project in development mode
pip install -e .

# Install development dependencies
pip install -e ".[dev]"
```

## Environment Configuration

### Step 1: Create Environment File

```bash
# Copy the example environment file
cp .env.example .env

# Windows (if cp doesn't work)
copy .env.example .env
```

### Step 2: Configure Credentials

Edit the `.env` file with your Orange HRM credentials:

```bash
# Orange HRM Demo Credentials
ORANGEHRM_USERNAME=Admin
ORANGEHRM_PASSWORD=admin123

# Optional: Custom configuration
# SE_CACHE_PATH=./drivers
# PYTEST_CURRENT_TEST=1
```

### Step 3: Environment-Specific Configuration

The framework supports multiple environments through JSON configuration files:

#### Development Environment (`src/orange_hrm/config/dev.json`)
```json
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

#### Staging Environment (`src/orange_hrm/config/staging.json`)
```json
{
    "webdriver": {
        "explicit_wait": 15
    },
    "application": {
        "base_url": "https://opensource-demo.orangehrmlive.com/web/index.php"
    },
    "performance": {
        "performance_threshold": 5
    }
}
```

#### Production Environment (`src/orange_hrm/config/prod.json`)
```json
{
    "webdriver": {
        "explicit_wait": 10
    },
    "application": {
        "base_url": "https://opensource-demo.orangehrmlive.com/web/index.php"
    },
    "performance": {
        "performance_threshold": 5
    }
}
```

## Browser Setup

### Chrome Browser

The framework uses Chrome as the primary browser with automatic ChromeDriver management.

#### Installation

**Windows:**
- Download from [Google Chrome](https://www.google.com/chrome/)
- Install using the downloaded installer

**macOS:**
```bash
# Using Homebrew
brew install --cask google-chrome
```

**Linux (Ubuntu/Debian):**
```bash
# Download and install Chrome
wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | sudo apt-key add -
echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" | sudo tee /etc/apt/sources.list.d/google-chrome.list
sudo apt update
sudo apt install google-chrome-stable
```

#### ChromeDriver Management

The framework automatically manages ChromeDriver through Selenium Manager. No manual installation required!

**Custom Driver Cache (Optional):**
```bash
# Set custom driver cache location
export SE_CACHE_PATH="./drivers"

# Windows
set SE_CACHE_PATH=.\drivers
```

## Verification

### Step 1: Verify Installation

```bash
# Check if all dependencies are installed
uv run python -c "import selenium, pydantic, pytest; print('All dependencies installed successfully!')"

# Or with pip
python -c "import selenium, pydantic, pytest; print('All dependencies installed successfully!')"
```

### Step 2: Run Configuration Test

```bash
# Test configuration loading
uv run python -c "from orange_hrm.config.dotenv_config import get_dot_env_secrets; print('Configuration loaded:', get_dot_env_secrets())"
```

### Step 3: Run Sample Test

```bash
# Run a single test to verify everything works
uv run pytest tests/test_login.py::test_login_valid_credentials -v

# Expected output should show test passing
```

### Step 4: Full Test Suite

```bash
# Run all tests
uv run pytest

# Run with coverage
uv run pytest --cov=src --cov-report=html
```

## IDE Configuration

### Visual Studio Code

#### Recommended Extensions

```json
{
    "recommendations": [
        "ms-python.python",
        // Optional formatting and linting extensions:
        // "ms-python.black-formatter",
        // "ms-python.isort",
        // "ms-python.pylint",
        "charliermarsh.ruff",
        "ms-python.pytest"
    ]
}
```

#### Settings Configuration (`.vscode/settings.json`)

```json
{
    "python.defaultInterpreterPath": "./.venv/bin/python",
    "python.testing.pytestEnabled": true,
    "python.testing.pytestArgs": [
        "tests"
    ],
    // Optional linting and formatting settings (if tools are installed):
     // "python.linting.enabled": true,
     // "python.linting.pylintEnabled": true,
     // "python.formatting.provider": "black",
     // "python.sortImports.args": ["--profile", "black"],
    "files.exclude": {
        "**/__pycache__": true,
        "**/.pytest_cache": true,
        "**/reports": true,
        "**/.coverage": true
    }
}
```

### PyCharm

1. **Open Project**: File → Open → Select project directory
2. **Configure Interpreter**: 
   - File → Settings → Project → Python Interpreter
   - Add Interpreter → Existing Environment
   - Select `.venv/bin/python` (or `.venv\Scripts\python.exe` on Windows)
3. **Configure Test Runner**:
   - File → Settings → Tools → Python Integrated Tools
   - Set Default test runner to "pytest"
4. **Code Style** (Optional): File → Settings → Editor → Code Style → Python
   - Set line length to 88 characters
   - Configure import optimization as needed
5. **Enable Coverage**:
   - Run → Edit Configurations → Templates → Python tests → pytest
   - Check "Run with coverage"

## Docker Setup

### Dockerfile

Create a `Dockerfile` for containerized testing:

```dockerfile
FROM python:3.13-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    unzip \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Chrome
RUN wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list \
    && apt-get update \
    && apt-get install -y google-chrome-stable \
    && rm -rf /var/lib/apt/lists/*

# Install uv
RUN pip install uv

# Set working directory
WORKDIR /app

# Copy project files
COPY . .

# Install dependencies
RUN uv sync

# Set environment variables
ENV PYTHONPATH=/app
ENV SE_CACHE_PATH=/app/drivers

# Run tests
CMD ["uv", "run", "pytest", "--headless"]
```

### Docker Compose

Create `docker-compose.yml`:

```yaml
version: '3.8'

services:
  test-runner:
    build: .
    environment:
      - ORANGEHRM_USERNAME=${ORANGEHRM_USERNAME}
      - ORANGEHRM_PASSWORD=${ORANGEHRM_PASSWORD}
    volumes:
      - ./reports:/app/reports
    command: uv run pytest --headless --env=staging
```

### Running with Docker

```bash
# Build and run tests
docker-compose up --build

# Run specific environment
docker-compose run test-runner uv run pytest --env=prod --headless
```

## Troubleshooting

### Common Issues

#### Python Version Issues

```bash
# Check Python version
python --version

# If version is < 3.13, install newer Python
# Windows: Download from python.org
# macOS: brew install python@3.13
# Linux: Use pyenv or package manager
```

#### ChromeDriver Issues

```bash
# Clear driver cache
rm -rf ./drivers
# Windows: rmdir /s drivers

# Set custom cache path
export SE_CACHE_PATH="$(pwd)/drivers"
```

#### Permission Issues (Linux/macOS)

```bash
# Fix permissions for driver cache
chmod 755 ./drivers

# If using system-wide installation
sudo chown -R $USER:$USER ~/.cache/selenium
```

#### Virtual Environment Issues

```bash
# Remove and recreate virtual environment
rm -rf .venv
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
# or
.venv\Scripts\activate     # Windows

# Reinstall dependencies
uv sync
# or
pip install -e .
```

### Getting Help

If you encounter issues not covered here:

1. Check the [Troubleshooting Guide](TROUBLESHOOTING.md)
2. Search [GitHub Issues](https://github.com/Next-Wave-Code/OrangeHRM_Test_Automation_web/issues)
3. Create a new issue with:
   - Operating system and version
   - Python version
   - Error messages
   - Steps to reproduce

---

**Next Steps**: After completing setup, see the [Usage Guide](USAGE.md) for examples and best practices.