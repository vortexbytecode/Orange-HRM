# CI/CD Guide

> **Comprehensive CI/CD setup and configuration guide for the Orange HRM Test Automation Framework**

## Table of Contents

- [Overview](#overview)
- [GitFlow CI/CD Pipeline](#gitflow-cicd-pipeline)
- [Pipeline Configuration](#pipeline-configuration)
- [Environment Setup](#environment-setup)
- [Security Configuration](#security-configuration)
- [Alternative CI/CD Platforms](#alternative-cicd-platforms)
- [Monitoring and Reporting](#monitoring-and-reporting)
- [Troubleshooting](#troubleshooting)
- [Best Practices](#best-practices)

## Overview

The Orange HRM Test Automation Framework includes a comprehensive CI/CD pipeline built with GitHub Actions, following GitFlow branching strategy and enterprise best practices.

### Pipeline Features

- **GitFlow Integration**: Automated testing on feature, develop, release, and hotfix branches
- **Multi-Environment Testing**: Parallel execution across development, staging, and production environments
- **Security Scanning**: Integrated security vulnerability detection
- **Code Quality**: Automated linting, formatting, and quality checks
- **Performance Monitoring**: Test execution time tracking and optimization
- **Comprehensive Reporting**: Coverage reports, test results, and artifacts

### Supported Platforms

- ✅ **GitHub Actions** (Primary - GitFlow Pipeline)
- ✅ **GitLab CI/CD**
- ✅ **Jenkins**
- ✅ **Azure DevOps**
- ✅ **CircleCI**

## GitFlow CI/CD Pipeline

### Pipeline Triggers

The GitFlow CI/CD pipeline automatically triggers on:

```yaml
# Trigger Configuration
on:
  push:
    branches:
      - main           # Production releases
      - develop        # Development integration
      - 'release/**'   # Release preparation
      - 'hotfix/**'    # Critical fixes
      - 'feature/**'   # Feature development
  pull_request:
    branches:
      - main
      - develop
  workflow_dispatch:   # Manual execution
```

### Pipeline Jobs

The pipeline consists of four parallel jobs:

#### 1. Code Quality and Linting
- **Purpose**: Ensures code quality and consistency
- **Tools**: `ruff` for linting and formatting
- **Scope**: All Python files in `src/` and `tests/`
- **Failure Impact**: Blocks pipeline progression

#### 2. UI Smoke Tests
- **Purpose**: Quick validation of core UI functionality
- **Environment**: Development
- **Browser**: Chrome (headless)
- **Duration**: ~2-3 minutes

#### 3. Security Scan
- **Purpose**: Identifies security vulnerabilities
- **Tools**: `bandit` for Python security analysis
- **Scope**: Source code and dependencies
- **Reports**: Security findings and recommendations

#### 4. E2E Tests
- **Purpose**: Comprehensive end-to-end testing
- **Environments**: Development, Staging, Production
- **Strategy**: Matrix execution for parallel testing
- **Coverage**: Full test suite with coverage reporting

### Workflow Features

- **Parallel Execution**: Jobs run simultaneously for faster feedback
- **Environment Matrix**: Tests across multiple environments
- **Artifact Management**: Test reports, coverage, and logs
- **Cache Optimization**: Dependencies and browser drivers
- **Failure Handling**: Graceful degradation and retry logic

## Pipeline Configuration

### Complete GitHub Actions Configuration

```yaml
# .github/workflows/gitflow-ci.yml
name: GitFlow CI/CD Pipeline

on:
  push:
    branches:
      - main
      - develop
      - 'release/**'
      - 'hotfix/**'
      - 'feature/**'
  pull_request:
    branches:
      - main
      - develop
  workflow_dispatch:

env:
  PYTHON_VERSION: '3.13'
  UV_VERSION: 'v0.5.11'

jobs:
  code-quality:
    name: Code Quality and Linting
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: ${{ env.PYTHON_VERSION }}

      - name: Install uv
        uses: astral-sh/setup-uv@v4
        with:
          version: ${{ env.UV_VERSION }}
          enable-cache: true
        continue-on-error: true

      - name: Install dependencies
        run: uv sync --dev

      - name: Run ruff linting
        run: uv run ruff check src/ tests/

      - name: Run ruff formatting check
        run: uv run ruff format --check src/ tests/

  ui-smoke-tests:
    name: UI Smoke Tests
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: ${{ env.PYTHON_VERSION }}

      - name: Install uv
        uses: astral-sh/setup-uv@v4
        with:
          version: ${{ env.UV_VERSION }}
          enable-cache: true
        continue-on-error: true

      - name: Install dependencies
        run: uv sync

      - name: Run smoke tests
        env:
          ORANGEHRM_USERNAME: ${{ secrets.ORANGEHRM_USERNAME }}
          ORANGEHRM_PASSWORD: ${{ secrets.ORANGEHRM_PASSWORD }}
        run: |
          uv run pytest tests/test_login.py \
            --env=dev \
            --headless \
            -v

  security-scan:
    name: Security Scan
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: ${{ env.PYTHON_VERSION }}

      - name: Install uv
        uses: astral-sh/setup-uv@v4
        with:
          version: ${{ env.UV_VERSION }}
          enable-cache: true
        continue-on-error: true

      - name: Install dependencies
        run: uv sync --dev

      - name: Run security scan
        run: uv run bandit -r src/ -f json -o security-report.json
        continue-on-error: true

      - name: Upload security report
        uses: actions/upload-artifact@v4
        if: always()
        with:
          name: security-report
          path: security-report.json

  e2e-tests:
    name: E2E Tests
    runs-on: ubuntu-latest
    strategy:
      matrix:
        environment: [dev, staging, prod]
      fail-fast: false
    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: ${{ env.PYTHON_VERSION }}

      - name: Install uv
        uses: astral-sh/setup-uv@v4
        with:
          version: ${{ env.UV_VERSION }}
          enable-cache: true
        continue-on-error: true

      - name: Install dependencies
        run: uv sync

      - name: Run E2E tests
        env:
          ORANGEHRM_USERNAME: ${{ secrets.ORANGEHRM_USERNAME }}
          ORANGEHRM_PASSWORD: ${{ secrets.ORANGEHRM_PASSWORD }}
        run: |
          uv run pytest \
            --env=${{ matrix.environment }} \
            --headless \
            --cov=src \
            --cov-report=xml:coverage-${{ matrix.environment }}.xml \
            --cov-report=html:reports/coverage-${{ matrix.environment }} \
            --junit-xml=reports/junit-${{ matrix.environment }}.xml \
            -v

      - name: Upload coverage reports
        uses: codecov/codecov-action@v4
        if: always()
        with:
          file: ./coverage-${{ matrix.environment }}.xml
          flags: ${{ matrix.environment }}
          name: coverage-${{ matrix.environment }}
        env:
          CODECOV_TOKEN: ${{ secrets.CODECOV_TOKEN }}

      - name: Upload test artifacts
        uses: actions/upload-artifact@v4
        if: always()
        with:
          name: test-results-${{ matrix.environment }}
          path: |
            reports/
            coverage-${{ matrix.environment }}.xml

  workflow-status:
    name: Workflow Status Notification
    runs-on: ubuntu-latest
    needs: [code-quality, ui-smoke-tests, security-scan, e2e-tests]
    if: always()
    steps:
      - name: Notify workflow completion
        run: |
          echo "GitFlow CI/CD Pipeline completed"
          echo "Code Quality: ${{ needs.code-quality.result }}"
          echo "UI Smoke Tests: ${{ needs.ui-smoke-tests.result }}"
          echo "Security Scan: ${{ needs.security-scan.result }}"
          echo "E2E Tests: ${{ needs.e2e-tests.result }}"
```

## Environment Setup

### Repository Secrets

Configure the following secrets in your GitHub repository:

| Secret Name | Description | Example Value |
|-------------|-------------|---------------|
| `ORANGEHRM_USERNAME` | Orange HRM login username | `Admin` |
| `ORANGEHRM_PASSWORD` | Orange HRM login password | `admin123` |
| `CODECOV_TOKEN` | Codecov integration token | `abc123...` |

### Environment Variables

The pipeline uses these environment variables:

```yaml
env:
  PYTHON_VERSION: '3.13'        # Python version
  UV_VERSION: 'v0.5.11'         # uv package manager version
  SE_CACHE_PATH: './drivers'     # Selenium driver cache
  PYTEST_CURRENT_TEST: '1'       # Enable pytest current test tracking
```

### Branch Protection Rules

Recommended branch protection settings:

#### Main Branch
- ✅ Require pull request reviews
- ✅ Require status checks to pass
- ✅ Require branches to be up to date
- ✅ Include administrators
- ✅ Required status checks:
  - `Code Quality and Linting`
  - `UI Smoke Tests`
  - `Security Scan`
  - `E2E Tests (dev)`
  - `E2E Tests (staging)`

#### Develop Branch
- ✅ Require pull request reviews
- ✅ Require status checks to pass
- ✅ Required status checks:
  - `Code Quality and Linting`
  - `UI Smoke Tests`
  - `E2E Tests (dev)`

## Security Configuration

### Secret Management

```yaml
# Secure secret handling
env:
  ORANGEHRM_USERNAME: ${{ secrets.ORANGEHRM_USERNAME }}
  ORANGEHRM_PASSWORD: ${{ secrets.ORANGEHRM_PASSWORD }}
```

### Security Scanning

The pipeline includes automated security scanning:

```bash
# Security tools used
uv run bandit -r src/ -f json -o security-report.json
```

### Access Control

- **Repository Access**: Limit to authorized team members
- **Secret Access**: Restrict to necessary workflows only
- **Branch Protection**: Enforce review requirements
- **Audit Logging**: Enable GitHub audit logs

## Alternative CI/CD Platforms

### GitLab CI/CD

```yaml
# .gitlab-ci.yml
stages:
  - quality
  - test
  - security
  - report

variables:
  PYTHON_VERSION: "3.13"
  PIP_CACHE_DIR: "$CI_PROJECT_DIR/.cache/pip"

cache:
  paths:
    - .cache/pip
    - .venv/

code-quality:
  stage: quality
  image: python:$PYTHON_VERSION
  before_script:
    - pip install uv
    - uv sync --dev
  script:
    - uv run ruff check src/ tests/
    - uv run ruff format --check src/ tests/

ui-smoke-tests:
  stage: test
  image: python:$PYTHON_VERSION
  variables:
    ORANGEHRM_USERNAME: $ORANGEHRM_USERNAME
    ORANGEHRM_PASSWORD: $ORANGEHRM_PASSWORD
  before_script:
    - apt-get update && apt-get install -y wget gnupg
    - wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add -
    - echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list
    - apt-get update && apt-get install -y google-chrome-stable
    - pip install uv
    - uv sync
  script:
    - uv run pytest tests/test_login.py --env=dev --headless -v

security-scan:
  stage: security
  image: python:$PYTHON_VERSION
  before_script:
    - pip install uv
    - uv sync --dev
  script:
    - uv run bandit -r src/ -f json -o security-report.json
  artifacts:
    reports:
      junit: security-report.json
    paths:
      - security-report.json
    expire_in: 1 week
  allow_failure: true

e2e-tests:
  stage: test
  image: python:$PYTHON_VERSION
  parallel:
    matrix:
      - ENVIRONMENT: [dev, staging, prod]
  variables:
    ORANGEHRM_USERNAME: $ORANGEHRM_USERNAME
    ORANGEHRM_PASSWORD: $ORANGEHRM_PASSWORD
  before_script:
    - apt-get update && apt-get install -y wget gnupg
    - wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add -
    - echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list
    - apt-get update && apt-get install -y google-chrome-stable
    - pip install uv
    - uv sync
  script:
    - uv run pytest --env=$ENVIRONMENT --headless --cov=src --cov-report=xml --junit-xml=reports/junit-$ENVIRONMENT.xml
  artifacts:
    reports:
      coverage_report:
        coverage_format: cobertura
        path: coverage.xml
      junit: reports/junit-$ENVIRONMENT.xml
    paths:
      - reports/
      - coverage.xml
    expire_in: 1 week
```

### Jenkins Pipeline

```groovy
// Jenkinsfile
pipeline {
    agent any
    
    environment {
        PYTHON_VERSION = '3.13'
        ORANGEHRM_USERNAME = credentials('orangehrm-username')
        ORANGEHRM_PASSWORD = credentials('orangehrm-password')
    }
    
    stages {
        stage('Setup') {
            steps {
                sh '''
                    python -m pip install --upgrade pip
                    pip install uv
                    uv sync --dev
                '''
            }
        }
        
        stage('Code Quality') {
            parallel {
                stage('Linting') {
                    steps {
                        sh 'uv run ruff check src/ tests/'
                    }
                }
                stage('Formatting') {
                    steps {
                        sh 'uv run ruff format --check src/ tests/'
                    }
                }
            }
        }
        
        stage('Security Scan') {
            steps {
                sh 'uv run bandit -r src/ -f json -o security-report.json'
            }
            post {
                always {
                    archiveArtifacts artifacts: 'security-report.json', fingerprint: true
                }
            }
        }
        
        stage('UI Smoke Tests') {
            steps {
                sh 'uv run pytest tests/test_login.py --env=dev --headless --junit-xml=reports/junit-smoke.xml'
            }
            post {
                always {
                    junit 'reports/junit-smoke.xml'
                }
            }
        }
        
        stage('E2E Tests') {
            parallel {
                stage('Development') {
                    steps {
                        sh 'uv run pytest --env=dev --headless --cov=src --cov-report=xml:coverage-dev.xml --junit-xml=reports/junit-dev.xml'
                    }
                    post {
                        always {
                            junit 'reports/junit-dev.xml'
                        }
                    }
                }
                stage('Staging') {
                    steps {
                        sh 'uv run pytest --env=staging --headless --cov=src --cov-report=xml:coverage-staging.xml --junit-xml=reports/junit-staging.xml'
                    }
                    post {
                        always {
                            junit 'reports/junit-staging.xml'
                        }
                    }
                }
                stage('Production') {
                    when {
                        anyOf {
                            branch 'main'
                            branch 'release/*'
                        }
                    }
                    steps {
                        sh 'uv run pytest --env=prod --headless --cov=src --cov-report=xml:coverage-prod.xml --junit-xml=reports/junit-prod.xml'
                    }
                    post {
                        always {
                            junit 'reports/junit-prod.xml'
                        }
                    }
                }
            }
        }
        
        stage('Coverage Report') {
            steps {
                sh 'uv run pytest --cov=src --cov-report=html:reports/coverage --cov-report=xml'
                publishHTML([
                    allowMissing: false,
                    alwaysLinkToLastBuild: true,
                    keepAll: true,
                    reportDir: 'reports/coverage',
                    reportFiles: 'index.html',
                    reportName: 'Coverage Report'
                ])
            }
        }
    }
    
    post {
        always {
            archiveArtifacts artifacts: 'reports/**/*', fingerprint: true
            cleanWs()
        }
        success {
            echo 'Pipeline completed successfully!'
        }
        failure {
            echo 'Pipeline failed. Check logs for details.'
        }
    }
}
```

## Monitoring and Reporting

### Test Reports

The pipeline generates comprehensive reports:

- **JUnit XML**: Test execution results
- **Coverage Reports**: Code coverage analysis (HTML + XML)
- **Security Reports**: Vulnerability assessments
- **Performance Reports**: Test execution metrics

### Artifacts

Generated artifacts include:

```yaml
artifacts:
  - reports/junit-*.xml          # Test results
  - reports/coverage-*/          # Coverage reports
  - coverage-*.xml               # Coverage data
  - security-report.json         # Security findings
  - logs/                        # Execution logs
```

### Integration with External Services

#### Codecov Integration

```yaml
- name: Upload coverage reports
  uses: codecov/codecov-action@v4
  with:
    file: ./coverage-${{ matrix.environment }}.xml
    flags: ${{ matrix.environment }}
    name: coverage-${{ matrix.environment }}
  env:
    CODECOV_TOKEN: ${{ secrets.CODECOV_TOKEN }}
```

#### Slack Notifications

```yaml
- name: Slack Notification
  uses: 8398a7/action-slack@v3
  with:
    status: ${{ job.status }}
    channel: '#ci-cd'
    webhook_url: ${{ secrets.SLACK_WEBHOOK }}
  if: always()
```

## Troubleshooting

### Common Issues

#### Cache Service Failures

**Problem**: "Failed to save" or "Failed to restore" cache errors

**Solution**:
```yaml
- name: Install uv
  uses: astral-sh/setup-uv@v4
  with:
    enable-cache: true
  continue-on-error: true  # Make cache failures non-critical
```

#### ChromeDriver Issues

**Problem**: Browser driver compatibility issues

**Solution**:
```yaml
- name: Setup Chrome
  uses: browser-actions/setup-chrome@latest
  with:
    chrome-version: stable
```

#### Test Timeouts

**Problem**: Tests timing out in CI environment

**Solution**:
```python
# Increase timeouts for CI
@pytest.fixture
def driver_options():
    options = ChromeOptions()
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    return options
```

#### Environment Variable Issues

**Problem**: Missing or incorrect environment variables

**Solution**:
```yaml
- name: Debug Environment
  run: |
    echo "Python version: $(python --version)"
    echo "Environment: ${{ matrix.environment }}"
    echo "Secrets available: ${{ secrets.ORANGEHRM_USERNAME != '' }}"
```

### Debug Mode

Enable debug logging:

```yaml
- name: Run tests with debug
  env:
    PYTEST_CURRENT_TEST: 1
    LOG_LEVEL: DEBUG
  run: |
    uv run pytest --env=${{ matrix.environment }} \
      --headless \
      --log-cli-level=DEBUG \
      -v -s
```

## Best Practices

### Pipeline Optimization

1. **Parallel Execution**: Run independent jobs simultaneously
2. **Cache Management**: Cache dependencies and browser drivers
3. **Fail-Fast Strategy**: Stop on critical failures
4. **Resource Limits**: Set appropriate timeouts and resource constraints

### Security Best Practices

1. **Secret Management**: Use repository secrets, never hardcode
2. **Least Privilege**: Grant minimum necessary permissions
3. **Audit Logging**: Enable comprehensive logging
4. **Regular Updates**: Keep actions and dependencies updated

### Testing Strategy

1. **Smoke Tests**: Quick validation on every commit
2. **Progressive Testing**: More comprehensive tests on important branches
3. **Environment Parity**: Test across all target environments
4. **Coverage Goals**: Maintain minimum coverage thresholds

### Maintenance

1. **Regular Reviews**: Periodically review and update pipeline configuration
2. **Performance Monitoring**: Track pipeline execution times
3. **Dependency Updates**: Keep tools and actions up to date
4. **Documentation**: Maintain up-to-date documentation

---

**Related Documentation**:
- [Setup Guide](SETUP.md) - Initial project setup
- [Usage Guide](USAGE.md) - Running tests locally
- [Troubleshooting Guide](TROUBLESHOOTING.md) - Common issues and solutions
- [Contributing Guide](CONTRIBUTING.md) - Development guidelines