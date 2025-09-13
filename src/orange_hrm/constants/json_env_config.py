"""Constants module for JSON environment configuration."""

from enum import Enum


class Environment(Enum):
    """Enum class for environment types."""

    DEV = "dev"
    PROD = "prod"
    STAGING = "staging"


class TopKey(Enum):
    """Enum class for top-level configuration keys."""

    WEBDRIVER = "webdriver"
    APPLICATION = "application"
    PERFORMANCE = "performance"


class WebDriverFields(Enum):
    """Enum class for WebDriver configuration fields."""

    EXPLICIT_WAIT = "explicit_wait"


class ApplicationFields(Enum):
    """Enum class for Application configuration fields."""

    BASE_URL = "base_url"


class PerformanceFields(Enum):
    """Enum class for Performance configuration fields."""

    PERFORMANCE_THRESHOLD = "performance_threshold"
